import re
from collections import namedtuple

"""

    Represents a token parsed from a discord chat message,
    as defined by its TokenType and source text.

"""

Token = namedtuple('Token', ['type','instance'])