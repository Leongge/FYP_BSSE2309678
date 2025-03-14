"""
    pygments.lexers.roboconf
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Roboconf DSL.

    :copyright: Copyright 2006-2023 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words, re
from pygments.token import Text, Operator, Keyword, Name, Comment

__all__ = ['RoboconfGraphLexer', 'RoboconfInstancesLexer']


class RoboconfGraphLexer(RegexLexer):
    """
    Lexer for Roboconf graph files.

    .. versionadded:: 2.1
    """
    name = 'Roboconf Graph'
    aliases = ['roboconf-graph']
    filenames = ['*.graph']

    flags = re.IGNORECASE | re.MULTILINE
    tokens = {
        'root': [
            # Skip white spaces
            (r'\s+', Text),

            # There is one operator
            (r'=', Operator),

            # Keywords
            (words(('facet', 'import'), suffix=r'\s*\b', prefix=r'\b'), Keyword),
            (words((
                'installer', 'extends', 'exports', 'imports', 'facets',
                'children'), suffix=r'\s*:?', prefix=r'\b'), Name),

            # Comments
            (r'#.*\n', Comment),

            # Default
            (r'[^#]', Text),
            (r'.*\n', Text)
        ]
    }


class RoboconfInstancesLexer(RegexLexer):
    """
    Lexer for Roboconf instances files.

    .. versionadded:: 2.1
    """
    name = 'Roboconf Instances'
    aliases = ['roboconf-instances']
    filenames = ['*.instances']

    flags = re.IGNORECASE | re.MULTILINE
    tokens = {
        'root': [

            # Skip white spaces
            (r'\s+', Text),

            # Keywords
            (words(('instance of', 'import'), suffix=r'\s*\b', prefix=r'\b'), Keyword),
            (words(('name', 'count'), suffix=r's*:?', prefix=r'\b'), Name),
            (r'\s*[\w.-]+\s*:', Name),

            # Comments
            (r'#.*\n', Comment),

            # Default
            (r'[^#]', Text),
            (r'.*\n', Text)
        ]
    }
