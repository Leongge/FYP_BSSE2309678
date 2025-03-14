"""
    pygments.lexers.thingsdb
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the ThingsDB language.

    :copyright: Copyright 2006-2023 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Comment, Keyword, Name, Number, String, Text, \
    Operator, Punctuation, Whitespace

__all__ = ['ThingsDBLexer']


class ThingsDBLexer(RegexLexer):
    """
    Lexer for the ThingsDB programming language.

    .. versionadded:: 2.9
    """
    name = 'ThingsDB'
    aliases = ['ti', 'thingsdb']
    filenames = ['*.ti']

    tokens = {
        'root': [
            include('expression'),
        ],
        'expression': [
            include('comments'),
            include('whitespace'),

            # numbers
            (r'[-+]?0b[01]+', Number.Bin),
            (r'[-+]?0o[0-8]+', Number.Oct),
            (r'([-+]?0x[0-9a-fA-F]+)', Number.Hex),
            (r'[-+]?[0-9]+', Number.Integer),
            (r'[-+]?((inf|nan)([^0-9A-Za-z_]|$)|[0-9]*\.[0-9]+(e[+-][0-9]+)?)',
            Number.Float),

            # strings
            (r'(?:"(?:[^"]*)")+', String.Double),
            (r"(?:'(?:[^']*)')+", String.Single),

            # literals
            (r'(true|false|nil)\b', Keyword.Constant),

            # regular expressions
            (r'(/[^/\\]*(?:\\.[^/\\]*)*/i?)', String.Regex),

            # thing id's
            (r'#[0-9]+', Comment.Preproc),

            # name, assignments and functions
            include('names'),

            (r'[(){}\[\],;]', Punctuation),
            (r'[+\-*/%&|<>^!~@=:?]', Operator),
        ],
        'names': [
            (r'(\.)'
             r'(add|call|contains|del|endswith|extend|filter|find|findindex|'
             r'get|has|id|indexof|keys|len|lower|map|pop|push|remove|set|sort|'
             r'splice|startswith|test|unwrap|upper|values|wrap)'
             r'(\()',
             bygroups(Name.Function, Name.Function, Punctuation), 'arguments'),
            (r'(array|assert|assert_err|auth_err|backup_info|backups_info|'
             r'bad_data_err|bool|closure|collection_info|collections_info|'
             r'counters|deep|del_backup|del_collection|del_expired|del_node|'
             r'del_procedure|del_token|del_type|del_user|err|float|'
             r'forbidden_err|grant|int|isarray|isascii|isbool|isbytes|iserr|'
             r'isfloat|isinf|isint|islist|isnan|isnil|israw|isset|isstr|'
             r'isthing|istuple|isutf8|lookup_err|max_quota_err|mod_type|new|'
             r'new_backup|new_collection|new_node|new_procedure|new_token|'
             r'new_type|new_user|node_err|node_info|nodes_info|now|'
             r'num_arguments_err|operation_err|overflow_err|procedure_doc|'
             r'procedure_info|procedures_info|raise|refs|rename_collection|'
             r'rename_user|reset_counters|return|revoke|run|set_log_level|set|'
             r'set_quota|set_type|shutdown|str|syntax_err|thing|try|type|'
             r'type_err|type_count|type_info|types_info|user_info|users_info|'
             r'value_err|wse|zero_div_err)'
             r'(\()',
             bygroups(Name.Function, Punctuation),
             'arguments'),
            (r'(\.[A-Za-z_][0-9A-Za-z_]*)'
             r'(\s*)(=)',
             bygroups(Name.Attribute, Text, Operator)),
            (r'\.[A-Za-z_][0-9A-Za-z_]*', Name.Attribute),
            (r'([A-Za-z_][0-9A-Za-z_]*)(\s*)(=)',
            bygroups(Name.Variable, Text, Operator)),
            (r'[A-Za-z_][0-9A-Za-z_]*', Name.Variable),
        ],
        'whitespace': [
            (r'\n', Whitespace),
            (r'\s+', Whitespace),
        ],
        'comments': [
            (r'//(.*?)\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'comment'),
        ],
        'comment': [
            (r'[^*/]+', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline),
        ],
        'arguments': [
            include('expression'),
            (',', Punctuation),
            (r'\(', Punctuation, '#push'),
            (r'\)', Punctuation, '#pop'),
        ],
    }
