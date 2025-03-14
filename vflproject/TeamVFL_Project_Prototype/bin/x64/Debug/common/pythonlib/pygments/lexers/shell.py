"""
    pygments.lexers.shell
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for various shells.

    :copyright: Copyright 2006-2023 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, do_insertions, bygroups, \
    include, default, this, using, words, line_re
from pygments.token import Punctuation, Whitespace, \
    Text, Comment, Operator, Keyword, Name, String, Number, Generic
from pygments.util import shebang_matches

__all__ = ['BashLexer', 'BashSessionLexer', 'TcshLexer', 'BatchLexer',
           'SlurmBashLexer', 'MSDOSSessionLexer', 'PowerShellLexer',
           'PowerShellSessionLexer', 'TcshSessionLexer', 'FishShellLexer',
           'ExeclineLexer']


class BashLexer(RegexLexer):
    """
    Lexer for (ba|k|z|)sh shell scripts.

    .. versionadded:: 0.6
    """

    name = 'Bash'
    aliases = ['bash', 'sh', 'ksh', 'zsh', 'shell']
    filenames = ['*.sh', '*.ksh', '*.bash', '*.ebuild', '*.eclass',
                 '*.exheres-0', '*.exlib', '*.zsh',
                 '.bashrc', 'bashrc', '.bash_*', 'bash_*', 'zshrc', '.zshrc',
                 '.kshrc', 'kshrc',
                 'PKGBUILD']
    mimetypes = ['application/x-sh', 'application/x-shellscript', 'text/x-shellscript']

    tokens = {
        'root': [
            include('basic'),
            (r'`', String.Backtick, 'backticks'),
            include('data'),
            include('interp'),
        ],
        'interp': [
            (r'\$\(\(', Keyword, 'math'),
            (r'\$\(', Keyword, 'paren'),
            (r'\$\{#?', String.Interpol, 'curly'),
            (r'\$[a-zA-Z_]\w*', Name.Variable),  # user variable
            (r'\$(?:\d+|[#$?!_*@-])', Name.Variable),      # builtin
            (r'\$', Text),
        ],
        'basic': [
            (r'\b(if|fi|else|while|in|do|done|for|then|return|function|case|'
             r'select|break|continue|until|esac|elif)(\s*)\b',
             bygroups(Keyword, Whitespace)),
            (r'\b(alias|bg|bind|builtin|caller|cd|command|compgen|'
             r'complete|declare|dirs|disown|echo|enable|eval|exec|exit|'
             r'export|false|fc|fg|getopts|hash|help|history|jobs|kill|let|'
             r'local|logout|popd|printf|pushd|pwd|read|readonly|set|shift|'
             r'shopt|source|suspend|test|time|times|trap|true|type|typeset|'
             r'ulimit|umask|unalias|unset|wait)(?=[\s)`])',
             Name.Builtin),
            (r'\A#!.+\n', Comment.Hashbang),
            (r'#.*\n', Comment.Single),
            (r'\\[\w\W]', String.Escape),
            (r'(\b\w+)(\s*)(\+?=)', bygroups(Name.Variable, Whitespace, Operator)),
            (r'[\[\]{}()=]', Operator),
            (r'<<<', Operator),  # here-string
            (r'<<-?\s*(\'?)\\?(\w+)[\w\W]+?\2', String),
            (r'&&|\|\|', Operator),
        ],
        'data': [
            (r'(?s)\$?"(\\.|[^"\\$])*"', String.Double),
            (r'"', String.Double, 'string'),
            (r"(?s)\$'(\\\\|\\[0-7]+|\\.|[^'\\])*'", String.Single),
            (r"(?s)'.*?'", String.Single),
            (r';', Punctuation),
            (r'&', Punctuation),
            (r'\|', Punctuation),
            (r'\s+', Whitespace),
            (r'\d+\b', Number),
            (r'[^=\s\[\]{}()$"\'`\\<&|;]+', Text),
            (r'<', Text),
        ],
        'string': [
            (r'"', String.Double, '#pop'),
            (r'(?s)(\\\\|\\[0-7]+|\\.|[^"\\$])+', String.Double),
            include('interp'),
        ],
        'curly': [
            (r'\}', String.Interpol, '#pop'),
            (r':-', Keyword),
            (r'\w+', Name.Variable),
            (r'[^}:"\'`$\\]+', Punctuation),
            (r':', Punctuation),
            include('root'),
        ],
        'paren': [
            (r'\)', Keyword, '#pop'),
            include('root'),
        ],
        'math': [
            (r'\)\)', Keyword, '#pop'),
            (r'\*\*|\|\||<<|>>|[-+*/%^|&<>]', Operator),
            (r'\d+#[\da-zA-Z]+', Number),
            (r'\d+#(?! )', Number),
            (r'0[xX][\da-fA-F]+', Number),
            (r'\d+', Number),
            (r'[a-zA-Z_]\w*', Name.Variable),  # user variable
            include('root'),
        ],
        'backticks': [
            (r'`', String.Backtick, '#pop'),
            include('root'),
        ],
    }

    def analyse_text(text):
        if shebang_matches(text, r'(ba|z|)sh'):
            return 1
        if text.startswith('$ '):
            return 0.2


class SlurmBashLexer(BashLexer):
    """
    Lexer for (ba|k|z|)sh Slurm scripts.

    .. versionadded:: 2.4
    """

    name = 'Slurm'
    aliases = ['slurm', 'sbatch']
    filenames = ['*.sl']
    mimetypes = []
    EXTRA_KEYWORDS = {'srun'}

    def get_tokens_unprocessed(self, text):
        for index, token, value in BashLexer.get_tokens_unprocessed(self, text):
            if token is Text and value in self.EXTRA_KEYWORDS:
                yield index, Name.Builtin, value
            elif token is Comment.Single and 'SBATCH' in value:
                yield index, Keyword.Pseudo, value
            else:
                yield index, token, value


class ShellSessionBaseLexer(Lexer):
    """
    Base lexer for shell sessions.

    .. versionadded:: 2.1
    """

    _bare_continuation = False
    _venv = re.compile(r'^(\([^)]*\))(\s*)')

    def get_tokens_unprocessed(self, text):
        innerlexer = self._innerLexerCls(**self.options)

        pos = 0
        curcode = ''
        insertions = []
        backslash_continuation = False

        for match in line_re.finditer(text):
            line = match.group()

            venv_match = self._venv.match(line)
            if venv_match:
                venv = venv_match.group(1)
                venv_whitespace = venv_match.group(2)
                insertions.append((len(curcode),
                                   [(0, Generic.Prompt.VirtualEnv, venv)]))
                if venv_whitespace:
                    insertions.append((len(curcode),
                                       [(0, Text, venv_whitespace)]))
                line = line[venv_match.end():]

            m = self._ps1rgx.match(line)
            if m:
                # To support output lexers (say diff output), the output
                # needs to be broken by prompts whenever the output lexer
                # changes.
                if not insertions:
                    pos = match.start()

                insertions.append((len(curcode),
                                   [(0, Generic.Prompt, m.group(1))]))
                curcode += m.group(2)
                backslash_continuation = curcode.endswith('\\\n')
            elif backslash_continuation:
                if line.startswith(self._ps2):
                    insertions.append((len(curcode),
                                       [(0, Generic.Prompt,
                                         line[:len(self._ps2)])]))
                    curcode += line[len(self._ps2):]
                else:
                    curcode += line
                backslash_continuation = curcode.endswith('\\\n')
            elif self._bare_continuation and line.startswith(self._ps2):
                insertions.append((len(curcode),
                                   [(0, Generic.Prompt,
                                     line[:len(self._ps2)])]))
                curcode += line[len(self._ps2):]
            else:
                if insertions:
                    toks = innerlexer.get_tokens_unprocessed(curcode)
                    for i, t, v in do_insertions(insertions, toks):
                        yield pos+i, t, v
                yield match.start(), Generic.Output, line
                insertions = []
                curcode = ''
        if insertions:
            for i, t, v in do_insertions(insertions,
                                         innerlexer.get_tokens_unprocessed(curcode)):
                yield pos+i, t, v


class BashSessionLexer(ShellSessionBaseLexer):
    """
    Lexer for Bash shell sessions, i.e. command lines, including a
    prompt, interspersed with output.

    .. versionadded:: 1.1
    """

    name = 'Bash Session'
    aliases = ['console', 'shell-session']
    filenames = ['*.sh-session', '*.shell-session']
    mimetypes = ['application/x-shell-session', 'application/x-sh-session']

    _innerLexerCls = BashLexer
    _ps1rgx = re.compile(
        r'^((?:(?:\[.*?\])|(?:\(\S+\))?(?:| |sh\S*?|\w+\S+[@:]\S+(?:\s+\S+)' \
        r'?|\[\S+[@:][^\n]+\].+))\s*[$#%]\s*)(.*\n?)')
    _ps2 = '> '


class BatchLexer(RegexLexer):
    """
    Lexer for the DOS/Windows Batch file format.

    .. versionadded:: 0.7
    """
    name = 'Batchfile'
    aliases = ['batch', 'bat', 'dosbatch', 'winbatch']
    filenames = ['*.bat', '*.cmd']
    mimetypes = ['application/x-dos-batch']

    flags = re.MULTILINE | re.IGNORECASE

    _nl = r'\n\x1a'
    _punct = r'&<>|'
    _ws = r'\t\v\f\r ,;=\xa0'
    _nlws = r'\s\x1a\xa0,;='
    _space = r'(?:(?:(?:\^[%s])?[%s])+)' % (_nl, _ws)
    _keyword_terminator = (r'(?=(?:\^[%s]?)?[%s+./:[\\\]]|[%s%s(])' %
                           (_nl, _ws, _nl, _punct))
    _token_terminator = r'(?=\^?[%s]|[%s%s])' % (_ws, _punct, _nl)
    _start_label = r'((?:(?<=^[^:])|^[^:]?)[%s]*)(:)' % _ws
    _label = r'(?:(?:[^%s%s+:^]|\^[%s]?[\w\W])*)' % (_nlws, _punct, _nl)
    _label_compound = r'(?:(?:[^%s%s+:^)]|\^[%s]?[^)])*)' % (_nlws, _punct, _nl)
    _number = r'(?:-?(?:0[0-7]+|0x[\da-f]+|\d+)%s)' % _token_terminator
    _opword = r'(?:equ|geq|gtr|leq|lss|neq)'
    _string = r'(?:"[^%s"]*(?:"|(?=[%s])))' % (_nl, _nl)
    _variable = (r'(?:(?:%%(?:\*|(?:~[a-z]*(?:\$[^:]+:)?)?\d|'
                 r'[^%%:%s]+(?::(?:~(?:-?\d+)?(?:,(?:-?\d+)?)?|(?:[^%%%s^]|'
                 r'\^[^%%%s])[^=%s]*=(?:[^%%%s^]|\^[^%%%s])*)?)?%%))|'
                 r'(?:\^?![^!:%s]+(?::(?:~(?:-?\d+)?(?:,(?:-?\d+)?)?|(?:'
                 r'[^!%s^]|\^[^!%s])[^=%s]*=(?:[^!%s^]|\^[^!%s])*)?)?\^?!))' %
                 (_nl, _nl, _nl, _nl, _nl, _nl, _nl, _nl, _nl, _nl, _nl, _nl))
    _core_token = r'(?:(?:(?:\^[%s]?)?[^"%s%s])+)' % (_nl, _nlws, _punct)
    _core_token_compound = r'(?:(?:(?:\^[%s]?)?[^"%s%s)])+)' % (_nl, _nlws, _punct)
    _token = r'(?:[%s]+|%s)' % (_punct, _core_token)
    _token_compound = r'(?:[%s]+|%s)' % (_punct, _core_token_compound)
    _stoken = (r'(?:[%s]+|(?:%s|%s|%s)+)' %
               (_punct, _string, _variable, _core_token))

    def _make_begin_state(compound, _core_token=_core_token,
                          _core_token_compound=_core_token_compound,
                          _keyword_terminator=_keyword_terminator,
                          _nl=_nl, _punct=_punct, _string=_string,
                          _space=_space, _start_label=_start_label,
                          _stoken=_stoken, _token_terminator=_token_terminator,
                          _variable=_variable, _ws=_ws):
        rest = '(?:%s|%s|[^"%%%s%s%s])*' % (_string, _variable, _nl, _punct,
                                            ')' if compound else '')
        rest_of_line = r'(?:(?:[^%s^]|\^[%s]?[\w\W])*)' % (_nl, _nl)
        rest_of_line_compound = r'(?:(?:[^%s^)]|\^[%s]?[^)])*)' % (_nl, _nl)
        set_space = r'((?:(?:\^[%s]?)?[^\S\n])*)' % _nl
        suffix = ''
        if compound:
            _keyword_terminator = r'(?:(?=\))|%s)' % _keyword_terminator
            _token_terminator = r'(?:(?=\))|%s)' % _token_terminator
            suffix = '/compound'
        return [
            ((r'\)', Punctuation, '#pop') if compound else
             (r'\)((?=\()|%s)%s' % (_token_terminator, rest_of_line),
              Comment.Single)),
            (r'(?=%s)' % _start_label, Text, 'follow%s' % suffix),
            (_space, using(this, state='text')),
            include('redirect%s' % suffix),
            (r'[%s]+' % _nl, Text),
            (r'\(', Punctuation, 'root/compound'),
            (r'@+', Punctuation),
            (r'((?:for|if|rem)(?:(?=(?:\^[%s]?)?/)|(?:(?!\^)|'
             r'(?<=m))(?:(?=\()|%s)))(%s?%s?(?:\^[%s]?)?/(?:\^[%s]?)?\?)' %
             (_nl, _token_terminator, _space,
              _core_token_compound if compound else _core_token, _nl, _nl),
             bygroups(Keyword, using(this, state='text')),
             'follow%s' % suffix),
            (r'(goto%s)(%s(?:\^[%s]?)?/(?:\^[%s]?)?\?%s)' %
             (_keyword_terminator, rest, _nl, _nl, rest),
             bygroups(Keyword, using(this, state='text')),
             'follow%s' % suffix),
            (words(('assoc', 'break', 'cd', 'chdir', 'cls', 'color', 'copy',
                    'date', 'del', 'dir', 'dpath', 'echo', 'endlocal', 'erase',
                    'exit', 'ftype', 'keys', 'md', 'mkdir', 'mklink', 'move',
                    'path', 'pause', 'popd', 'prompt', 'pushd', 'rd', 'ren',
                    'rename', 'rmdir', 'setlocal', 'shift', 'start', 'time',
                    'title', 'type', 'ver', 'verify', 'vol'),
                   suffix=_keyword_terminator), Keyword, 'follow%s' % suffix),
            (r'(call)(%s?)(:)' % _space,
             bygroups(Keyword, using(this, state='text'), Punctuation),
             'call%s' % suffix),
            (r'call%s' % _keyword_terminator, Keyword),
            (r'(for%s(?!\^))(%s)(/f%s)' %
             (_token_terminator, _space, _token_terminator),
             bygroups(Keyword, using(this, state='text'), Keyword),
             ('for/f', 'for')),
            (r'(for%s(?!\^))(%s)(/l%s)' %
             (_token_terminator, _space, _token_terminator),
             bygroups(Keyword, using(this, state='text'), Keyword),
             ('for/l', 'for')),
            (r'for%s(?!\^)' % _token_terminator, Keyword, ('for2', 'for')),
            (r'(goto%s)(%s?)(:?)' % (_keyword_terminator, _space),
             bygroups(Keyword, using(this, state='text'), Punctuation),
             'label%s' % suffix),
            (r'(if(?:(?=\()|%s)(?!\^))(%s?)((?:/i%s)?)(%s?)((?:not%s)?)(%s?)' %
             (_token_terminator, _space, _token_terminator, _space,
              _token_terminator, _space),
             bygroups(Keyword, using(this, state='text'), Keyword,
                      using(this, state='text'), Keyword,
                      using(this, state='text')), ('(?', 'if')),
            (r'rem(((?=\()|%s)%s?%s?.*|%s%s)' %
             (_token_terminator, _space, _stoken, _keyword_terminator,
              rest_of_line_compound if compound else rest_of_line),
             Comment.Single, 'follow%s' % suffix),
            (r'(set%s)%s(/a)' % (_keyword_terminator, set_space),
             bygroups(Keyword, using(this, state='text'), Keyword),
             'arithmetic%s' % suffix),
            (r'(set%s)%s((?:/p)?)%s((?:(?:(?:\^[%s]?)?[^"%s%s^=%s]|'
             r'\^[%s]?[^"=])+)?)((?:(?:\^[%s]?)?=)?)' %
             (_keyword_terminator, set_space, set_space, _nl, _nl, _punct,
              ')' if compound else '', _nl, _nl),
             bygroups(Keyword, using(this, state='text'), Keyword,
                      using(this, state='text'), using(this, state='variable'),
                      Punctuation),
             'follow%s' % suffix),
            default('follow%s' % suffix)
        ]

    def _make_follow_state(compound, _label=_label,
                           _label_compound=_label_compound, _nl=_nl,
                           _space=_space, _start_label=_start_label,
                           _token=_token, _token_compound=_token_compound,
                           _ws=_ws):
        suffix = '/compound' if compound else ''
        state = []
        if compound:
            state.append((r'(?=\))', Text, '#pop'))
        state += [
            (r'%s([%s]*)(%s)(.*)' %
             (_start_label, _ws, _label_compound if compound else _label),
             bygroups(Text, Punctuation, Text, Name.Label, Comment.Single)),
            include('redirect%s' % suffix),
            (r'(?=[%s])' % _nl, Text, '#pop'),
            (r'\|\|?|&&?', Punctuation, '#pop'),
            include('text')
        ]
        return state

    def _make_arithmetic_state(compound, _nl=_nl, _punct=_punct,
                               _string=_string, _variable=_variable,
                               _ws=_ws, _nlws=_nlws):
        op = r'=+\-*/!~'
        state = []
        if compound:
            state.append((r'(?=\))', Text, '#pop'))
        state += [
            (r'0[0-7]+', Number.Oct),
            (r'0x[\da-f]+', Number.Hex),
            (r'\d+', Number.Integer),
            (r'[(),]+', Punctuation),
            (r'([%s]|%%|\^\^)+' % op, Operator),
            (r'(%s|%s|(\^[%s]?)?[^()%s%%\^"%s%s]|\^[%s]?%s)+' %
             (_string, _variable, _nl, op, _nlws, _punct, _nlws,
              r'[^)]' if compound else r'[\w\W]'),
             using(this, state='variable')),
            (r'(?=[\x00|&])', Text, '#pop'),
            include('follow')
        ]
        return state

    def _make_call_state(compound, _label=_label,
                         _label_compound=_label_compound):
        state = []
        if compound:
            state.append((r'(?=\))', Text, '#pop'))
        state.append((r'(:?)(%s)' % (_label_compound if compound else _label),
                      bygroups(Punctuation, Name.Label), '#pop'))
        return state

    def _make_label_state(compound, _label=_label,
                          _label_compound=_label_compound, _nl=_nl,
                          _punct=_punct, _string=_string, _variable=_variable):
        state = []
        if compound:
            state.append((r'(?=\))', Text, '#pop'))
        state.append((r'(%s?)((?:%s|%s|\^[%s]?%s|[^"%%^%s%s%s])*)' %
                      (_label_compound if compound else _label, _string,
                       _variable, _nl, r'[^)]' if compound else r'[\w\W]', _nl,
                       _punct, r')' if compound else ''),
                      bygroups(Name.Label, Comment.Single), '#pop'))
        return state

    def _make_redirect_state(compound,
                             _core_token_compound=_core_token_compound,
                             _nl=_nl, _punct=_punct, _stoken=_stoken,
                             _string=_string, _space=_space,
                             _variable=_variable, _nlws=_nlws):
        stoken_compound = (r'(?:[%s]+|(?:%s|%s|%s)+)' %
                           (_punct, _string, _variable, _core_token_compound))
        return [
            (r'((?:(?<=[%s])\d)?)(>>?&|<&)([%s]*)(\d)' %
             (_nlws, _nlws),
             bygroups(Number.Integer, Punctuation, Text, Number.Integer)),
            (r'((?:(?<=[%s])(?<!\^[%s])\d)?)(>>?|<)(%s?%s)' %
             (_nlws, _nl, _space, stoken_compound if compound else _stoken),
             bygroups(Number.Integer, Punctuation, using(this, state='text')))
        ]

    tokens = {
        'root': _make_begin_state(False),
        'follow': _make_follow_state(False),
        'arithmetic': _make_arithmetic_state(False),
        'call': _make_call_state(False),
        'label': _make_label_state(False),
        'redirect': _make_redirect_state(False),
        'root/compound': _make_begin_state(True),
        'follow/compound': _make_follow_state(True),
        'arithmetic/compound': _make_arithmetic_state(True),
        'call/compound': _make_call_state(True),
        'label/compound': _make_label_state(True),
        'redirect/compound': _make_redirect_state(True),
        'variable-or-escape': [
            (_variable, Name.Variable),
            (r'%%%%|\^[%s]?(\^!|[\w\W])' % _nl, String.Escape)
        ],
        'string': [
            (r'"', String.Double, '#pop'),
            (_variable, Name.Variable),
            (r'\^!|%%', String.Escape),
            (r'[^"%%^%s]+|[%%^]' % _nl, String.Double),
            default('#pop')
        ],
        'sqstring': [
            include('variable-or-escape'),
            (r'[^%]+|%', String.Single)
        ],
        'bqstring': [
            include('variable-or-escape'),
            (r'[^%]+|%', String.Backtick)
        ],
        'text': [
            (r'"', String.Double, 'string'),
            include('variable-or-escape'),
            (r'[^"%%^%s%s\d)]+|.' % (_nlws, _punct), Text)
        ],
        'variable': [
            (r'"', String.Double, 'string'),
            include('variable-or-escape'),
            (r'[^"%%^%s]+|.' % _nl, Name.Variable)
        ],
        'for': [
            (r'(%s)(in)(%s)(\()' % (_space, _space),
             bygroups(using(this, state='text'), Keyword,
                      using(this, state='text'), Punctuation), '#pop'),
            include('follow')
        ],
        'for2': [
            (r'\)', Punctuation),
            (r'(%s)(do%s)' % (_space, _token_terminator),
             bygroups(using(this, state='text'), Keyword), '#pop'),
            (r'[%s]+' % _nl, Text),
            include('follow')
        ],
        'for/f': [
            (r'(")((?:%s|[^"])*?")([%s]*)(\))' % (_variable, _nlws),
             bygroups(String.Double, using(this, state='string'), Text,
                      Punctuation)),
            (r'"', String.Double, ('#pop', 'for2', 'string')),
            (r"('(?:%%%%|%s|[\w\W])*?')([%s]*)(\))" % (_variable, _nlws),
             bygroups(using(this, state='sqstring'), Text, Punctuation)),
            (r'(`(?:%%%%|%s|[\w\W])*?`)([%s]*)(\))' % (_variable, _nlws),
             bygroups(using(this, state='bqstring'), Text, Punctuation)),
            include('for2')
        ],
        'for/l': [
            (r'-?\d+', Number.Integer),
            include('for2')
        ],
        'if': [
            (r'((?:cmdextversion|errorlevel)%s)(%s)(\d+)' %
             (_token_terminator, _space),
             bygroups(Keyword, using(this, state='text'),
                      Number.Integer), '#pop'),
            (r'(defined%s)(%s)(%s)' % (_token_terminator, _space, _stoken),
             bygroups(Keyword, using(this, state='text'),
                      using(this, state='variable')), '#pop'),
            (r'(exist%s)(%s%s)' % (_token_terminator, _space, _stoken),
             bygroups(Keyword, using(this, state='text')), '#pop'),
            (r'(%s%s)(%s)(%s%s)' % (_number, _space, _opword, _space, _number),
             bygroups(using(this, state='arithmetic'), Operator.Word,
                      using(this, state='arithmetic')), '#pop'),
            (_stoken, using(this, state='text'), ('#pop', 'if2')),
        ],
        'if2': [
            (r'(%s?)(==)(%s?%s)' % (_space, _space, _stoken),
             bygroups(using(this, state='text'), Operator,
                      using(this, state='text')), '#pop'),
            (r'(%s)(%s)(%s%s)' % (_space, _opword, _space, _stoken),
             bygroups(using(this, state='text'), Operator.Word,
                      using(this, state='text')), '#pop')
        ],
        '(?': [
            (_space, using(this, state='text')),
            (r'\(', Punctuation, ('#pop', 'else?', 'root/compound')),
            default('#pop')
        ],
        'else?': [
            (_space, using(this, state='text')),
            (r'else%s' % _token_terminator, Keyword, '#pop'),
            default('#pop')
        ]
    }


class MSDOSSessionLexer(ShellSessionBaseLexer):
    """
    Lexer for MS DOS shell sessions, i.e. command lines, including a
    prompt, interspersed with output.

    .. versionadded:: 2.1
    """

    name = 'MSDOS Session'
    aliases = ['doscon']
    filenames = []
    mimetypes = []

    _innerLexerCls = BatchLexer
    _ps1rgx = re.compile(r'^([^>]*>)(.*\n?)')
    _ps2 = 'More? '


class TcshLexer(RegexLexer):
    """
    Lexer for tcsh scripts.

    .. versionadded:: 0.10
    """

    name = 'Tcsh'
    aliases = ['tcsh', 'csh']
    filenames = ['*.tcsh', '*.csh']
    mimetypes = ['application/x-csh']

    tokens = {
        'root': [
            include('basic'),
            (r'\$\(', Keyword, 'paren'),
            (r'\$\{#?', Keyword, 'curly'),
            (r'`', String.Backtick, 'backticks'),
            include('data'),
        ],
        'basic': [
            (r'\b(if|endif|else|while|then|foreach|case|default|'
             r'break|continue|goto|breaksw|end|switch|endsw)\s*\b',
             Keyword),
            (r'\b(alias|alloc|bg|bindkey|builtins|bye|caller|cd|chdir|'
             r'complete|dirs|echo|echotc|eval|exec|exit|fg|filetest|getxvers|'
             r'glob|getspath|hashstat|history|hup|inlib|jobs|kill|'
             r'limit|log|login|logout|ls-F|migrate|newgrp|nice|nohup|notify|'
             r'onintr|popd|printenv|pushd|rehash|repeat|rootnode|popd|pushd|'
             r'set|shift|sched|setenv|setpath|settc|setty|setxvers|shift|'
             r'source|stop|suspend|source|suspend|telltc|time|'
             r'umask|unalias|uncomplete|unhash|universe|unlimit|unset|unsetenv|'
             r'ver|wait|warp|watchlog|where|which)\s*\b',
             Name.Builtin),
            (r'#.*', Comment),
            (r'\\[\w\W]', String.Escape),
            (r'(\b\w+)(\s*)(=)', bygroups(Name.Variable, Text, Operator)),
            (r'[\[\]{}()=]+', Operator),
            (r'<<\s*(\'?)\\?(\w+)[\w\W]+?\2', String),
            (r';', Punctuation),
        ],
        'data': [
            (r'(?s)"(\\\\|\\[0-7]+|\\.|[^"\\])*"', String.Double),
            (r"(?s)'(\\\\|\\[0-7]+|\\.|[^'\\])*'", String.Single),
            (r'\s+', Text),
            (r'[^=\s\[\]{}()$"\'`\\;#]+', Text),
            (r'\d+(?= |\Z)', Number),
            (r'\$#?(\w+|.)', Name.Variable),
        ],
        'curly': [
            (r'\}', Keyword, '#pop'),
            (r':-', Keyword),
            (r'\w+', Name.Variable),
            (r'[^}:"\'`$]+', Punctuation),
            (r':', Punctuation),
            include('root'),
        ],
        'paren': [
            (r'\)', Keyword, '#pop'),
            include('root'),
        ],
        'backticks': [
            (r'`', String.Backtick, '#pop'),
            include('root'),
        ],
    }


class TcshSessionLexer(ShellSessionBaseLexer):
    """
    Lexer for Tcsh sessions, i.e. command lines, including a
    prompt, interspersed with output.

    .. versionadded:: 2.1
    """

    name = 'Tcsh Session'
    aliases = ['tcshcon']
    filenames = []
    mimetypes = []

    _innerLexerCls = TcshLexer
    _ps1rgx = re.compile(r'^([^>]+>)(.*\n?)')
    _ps2 = '? '


class PowerShellLexer(RegexLexer):
    """
    For Windows PowerShell code.

    .. versionadded:: 1.5
    """
    name = 'PowerShell'
    aliases = ['powershell', 'pwsh', 'posh', 'ps1', 'psm1']
    filenames = ['*.ps1', '*.psm1']
    mimetypes = ['text/x-powershell']

    flags = re.DOTALL | re.IGNORECASE | re.MULTILINE

    keywords = (
        'while validateset validaterange validatepattern validatelength '
        'validatecount until trap switch return ref process param parameter in '
        'if global: local: function foreach for finally filter end elseif else '
        'dynamicparam do default continue cmdletbinding break begin alias \\? '
        '% #script #private #local #global mandatory parametersetname position '
        'valuefrompipeline valuefrompipelinebypropertyname '
        'valuefromremainingarguments helpmessage try catch throw').split()

    operators = (
        'and as band bnot bor bxor casesensitive ccontains ceq cge cgt cle '
        'clike clt cmatch cne cnotcontains cnotlike cnotmatch contains '
        'creplace eq exact f file ge gt icontains ieq ige igt ile ilike ilt '
        'imatch ine inotcontains inotlike inotmatch ireplace is isnot le like '
        'lt match ne not notcontains notlike notmatch or regex replace '
        'wildcard').split()

    verbs = (
        'write where watch wait use update unregister unpublish unprotect '
        'unlock uninstall undo unblock trace test tee take sync switch '
        'suspend submit stop step start split sort skip show set send select '
        'search scroll save revoke resume restore restart resolve resize '
        'reset request repair rename remove register redo receive read push '
        'publish protect pop ping out optimize open new move mount merge '
        'measure lock limit join invoke install initialize import hide group '
        'grant get format foreach find export expand exit enter enable edit '
        'dismount disconnect disable deny debug cxnew copy convertto '
        'convertfrom convert connect confirm compress complete compare close '
        'clear checkpoint block backup assert approve aggregate add').split()

    aliases_ = (
        'ac asnp cat cd cfs chdir clc clear clhy cli clp cls clv cnsn '
        'compare copy cp cpi cpp curl cvpa dbp del diff dir dnsn ebp echo epal '
        'epcsv epsn erase etsn exsn fc fhx fl foreach ft fw gal gbp gc gci gcm '
        'gcs gdr ghy gi gjb gl gm gmo gp gps gpv group gsn gsnp gsv gu gv gwmi '
        'h history icm iex ihy ii ipal ipcsv ipmo ipsn irm ise iwmi iwr kill lp '
        'ls man md measure mi mount move mp mv nal ndr ni nmo npssc nsn nv ogv '
        'oh popd ps pushd pwd r rbp rcjb rcsn rd rdr ren ri rjb rm rmdir rmo '
        'rni rnp rp rsn rsnp rujb rv rvpa rwmi sajb sal saps sasv sbp sc select '
        'set shcm si sl sleep sls sort sp spjb spps spsv start sujb sv swmi tee '
        'trcm type wget where wjb write').split()

    commenthelp = (
        'component description example externalhelp forwardhelpcategory '
        'forwardhelptargetname functionality inputs link '
        'notes outputs parameter remotehelprunspace role synopsis').split()

    tokens = {
        'root': [
            # we need to count pairs of parentheses for correct highlight
            # of '$(...)' blocks in strings
            (r'\(', Punctuation, 'child'),
            (r'\s+', Text),
            (r'^(\s*#[#\s]*)(\.(?:%s))([^\n]*$)' % '|'.join(commenthelp),
             bygroups(Comment, String.Doc, Comment)),
            (r'#[^\n]*?$', Comment),
            (r'(&lt;|<)#', Comment.Multiline, 'multline'),
            (r'@"\n', String.Heredoc, 'heredoc-double'),
            (r"@'\n.*?\n'@", String.Heredoc),
            # escaped syntax
            (r'`[\'"$@-]', Punctuation),
            (r'"', String.Double, 'string'),
            (r"'([^']|'')*'", String.Single),
            (r'(\$|@@|@)((global|script|private|env):)?\w+',
             Name.Variable),
            (r'(%s)\b' % '|'.join(keywords), Keyword),
            (r'-(%s)\b' % '|'.join(operators), Operator),
            (r'(%s)-[a-z_]\w*\b' % '|'.join(verbs), Name.Builtin),
            (r'(%s)\s' % '|'.join(aliases_), Name.Builtin),
            (r'\[[a-z_\[][\w. `,\[\]]*\]', Name.Constant),  # .net [type]s
            (r'-[a-z_]\w*', Name),
            (r'\w+', Name),
            (r'[.,;:@{}\[\]$()=+*/\\&%!~?^`|<>-]', Punctuation),
        ],
        'child': [
            (r'\)', Punctuation, '#pop'),
            include('root'),
        ],
        'multline': [
            (r'[^#&.]+', Comment.Multiline),
            (r'#(>|&gt;)', Comment.Multiline, '#pop'),
            (r'\.(%s)' % '|'.join(commenthelp), String.Doc),
            (r'[#&.]', Comment.Multiline),
        ],
        'string': [
            (r"`[0abfnrtv'\"$`]", String.Escape),
            (r'[^$`"]+', String.Double),
            (r'\$\(', Punctuation, 'child'),
            (r'""', String.Double),
            (r'[`$]', String.Double),
            (r'"', String.Double, '#pop'),
        ],
        'heredoc-double': [
            (r'\n"@', String.Heredoc, '#pop'),
            (r'\$\(', Punctuation, 'child'),
            (r'[^@\n]+"]', String.Heredoc),
            (r".", String.Heredoc),
        ]
    }


class PowerShellSessionLexer(ShellSessionBaseLexer):
    """
    Lexer for PowerShell sessions, i.e. command lines, including a
    prompt, interspersed with output.

    .. versionadded:: 2.1
    """

    name = 'PowerShell Session'
    aliases = ['pwsh-session', 'ps1con']
    filenames = []
    mimetypes = []

    _innerLexerCls = PowerShellLexer
    _bare_continuation = True
    _ps1rgx = re.compile(r'^((?:\[[^]]+\]: )?PS[^>]*> ?)(.*\n?)')
    _ps2 = '> '


class FishShellLexer(RegexLexer):
    """
    Lexer for Fish shell scripts.

    .. versionadded:: 2.1
    """

    name = 'Fish'
    aliases = ['fish', 'fishshell']
    filenames = ['*.fish', '*.load']
    mimetypes = ['application/x-fish']

    tokens = {
        'root': [
            include('basic'),
            include('data'),
            include('interp'),
        ],
        'interp': [
            (r'\$\(\(', Keyword, 'math'),
            (r'\(', Keyword, 'paren'),
            (r'\$#?(\w+|.)', Name.Variable),
        ],
        'basic': [
            (r'\b(begin|end|if|else|while|break|for|in|return|function|block|'
             r'case|continue|switch|not|and|or|set|echo|exit|pwd|true|false|'
             r'cd|count|test)(\s*)\b',
             bygroups(Keyword, Text)),
            (r'\b(alias|bg|bind|breakpoint|builtin|command|commandline|'
             r'complete|contains|dirh|dirs|emit|eval|exec|fg|fish|fish_config|'
             r'fish_indent|fish_pager|fish_prompt|fish_right_prompt|'
             r'fish_update_completions|fishd|funced|funcsave|functions|help|'
             r'history|isatty|jobs|math|mimedb|nextd|open|popd|prevd|psub|'
             r'pushd|random|read|set_color|source|status|trap|type|ulimit|'
             r'umask|vared|fc|getopts|hash|kill|printf|time|wait)\s*\b(?!\.)',
             Name.Builtin),
            (r'#.*\n', Comment),
            (r'\\[\w\W]', String.Escape),
            (r'(\b\w+)(\s*)(=)', bygroups(Name.Variable, Whitespace, Operator)),
            (r'[\[\]()=]', Operator),
            (r'<<-?\s*(\'?)\\?(\w+)[\w\W]+?\2', String),
        ],
        'data': [
            (r'(?s)\$?"(\\\\|\\[0-7]+|\\.|[^"\\$])*"', String.Double),
            (r'"', String.Double, 'string'),
            (r"(?s)\$'(\\\\|\\[0-7]+|\\.|[^'\\])*'", String.Single),
            (r"(?s)'.*?'", String.Single),
            (r';', Punctuation),
            (r'&|\||\^|<|>', Operator),
            (r'\s+', Text),
            (r'\d+(?= |\Z)', Number),
            (r'[^=\s\[\]{}()$"\'`\\<&|;]+', Text),
        ],
        'string': [
            (r'"', String.Double, '#pop'),
            (r'(?s)(\\\\|\\[0-7]+|\\.|[^"\\$])+', String.Double),
            include('interp'),
        ],
        'paren': [
            (r'\)', Keyword, '#pop'),
            include('root'),
        ],
        'math': [
            (r'\)\)', Keyword, '#pop'),
            (r'[-+*/%^|&]|\*\*|\|\|', Operator),
            (r'\d+#\d+', Number),
            (r'\d+#(?! )', Number),
            (r'\d+', Number),
            include('root'),
        ],
    }

class ExeclineLexer(RegexLexer):
    """
    Lexer for Laurent Bercot's execline language
    (https://skarnet.org/software/execline).

    .. versionadded:: 2.7
    """

    name = 'execline'
    aliases = ['execline']
    filenames = ['*.exec']

    tokens = {
        'root': [
            include('basic'),
            include('data'),
            include('interp')
        ],
        'interp': [
            (r'\$\{', String.Interpol, 'curly'),
            (r'\$[\w@#]+', Name.Variable),  # user variable
            (r'\$', Text),
        ],
        'basic': [
            (r'\b(background|backtick|cd|define|dollarat|elgetopt|'
             r'elgetpositionals|elglob|emptyenv|envfile|exec|execlineb|'
             r'exit|export|fdblock|fdclose|fdmove|fdreserve|fdswap|'
             r'forbacktickx|foreground|forstdin|forx|getcwd|getpid|heredoc|'
             r'homeof|if|ifelse|ifte|ifthenelse|importas|loopwhilex|'
             r'multidefine|multisubstitute|pipeline|piperw|posix-cd|'
             r'redirfd|runblock|shift|trap|tryexec|umask|unexport|wait|'
             r'withstdinas)\b', Name.Builtin),
            (r'\A#!.+\n', Comment.Hashbang),
            (r'#.*\n', Comment.Single),
            (r'[{}]', Operator)
        ],
        'data': [
            (r'(?s)"(\\.|[^"\\$])*"', String.Double),
            (r'"', String.Double, 'string'),
            (r'\s+', Text),
            (r'[^\s{}$"\\]+', Text)
        ],
        'string': [
            (r'"', String.Double, '#pop'),
            (r'(?s)(\\\\|\\.|[^"\\$])+', String.Double),
            include('interp'),
        ],
        'curly': [
            (r'\}', String.Interpol, '#pop'),
            (r'[\w#@]+', Name.Variable),
            include('root')
        ]

    }

    def analyse_text(text):
        if shebang_matches(text, r'execlineb'):
            return 1
