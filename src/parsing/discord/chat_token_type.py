import re
from enum import Enum
from typing import Match, Optional


class TokenType(Enum):

    """
    
        Represents distinct types of textual elements in 
        a Discord chat message and the patterns used to identify them.

    """
    
    EMOJI       = 1, '<a?:\w+:\d+>'
    MENTION     = 2, '<@!?\d+>|@here|@everyone'
    URL         = 3, 'https?://[^\s]+'
    PUNCTUATION = 4, '[\.,!?:*^"]'
    WORD        = 5, '[^\.,!?:*^"\s]+'

    def __init__(self, flag: int, pattern: str) -> None:
        super().__init__()
        self.flag = flag
        self.regex = re.compile(fr'{pattern}')
        
    def match(self, haystack: str, offset:int = 0) -> Optional[Match[str]]:
        return self.regex.match(haystack, offset)