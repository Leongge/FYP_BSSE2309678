"""
    pygments.lexers.gcodelexer
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the G Code Language.

    :copyright: Copyright 2006-2023 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, Name, Text, Keyword, Number

__all__ = ['GcodeLexer']


class GcodeLexer(RegexLexer):
    """
    For gcode source code.

    .. versionadded:: 2.9
    """
    name = 'g-code'
    aliases = ['gcode']
    filenames = ['*.gcode']

    tokens = {
        'root': [
            (r';.*\n', Comment),
            (r'^[gmGM]\d{1,4}\s', Name.Builtin),  # M or G commands
            (r'([^gGmM])([+-]?\d*[.]?\d+)', bygroups(Keyword, Number)),
            (r'\s', Text.Whitespace),
            (r'.*\n', Text),
        ]
    }
