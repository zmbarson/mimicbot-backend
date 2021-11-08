from typing import Iterable, Optional

from .chat_token import Token
from .chat_token_type import TokenType


class ChatTokenizer:

    """
        
        Converts strings into an iterable of Tokens using patterns defined
        in the corresponding TokenType enumeration.
    
    """

    def __init__(self) -> None:
        self._reset()

    def tokenize(self, string: str) -> Iterable[Token]:
        if string:
            for token in str(string).split():
                self._reset(token)
                while not self._end_of_string():
                    if(self._parse(TokenType.EMOJI)
                    or self._parse(TokenType.MENTION)
                    or self._parse(TokenType.PUNCTUATION)
                    or self._parse(TokenType.URL)
                    or self._parse(TokenType.WORD)):
                        yield self._last_token
                    else:
                        self._offset += 1
        else: raise TypeError('Attempted to tokenize a null or empty string.')

    def _reset(self, string: Optional[str]=None) -> None:
        self._string = string
        self._offset = 0
        self._last_token = None

    def _end_of_string(self) -> bool:
        return (self._offset == len(self._string) 
                    if self._string is not None 
                  else True)

    def _parse(self, kind: TokenType) -> bool:
        match = kind.match(self._string, self._offset)
        if match is not None:
            self._offset = match.end()
            self._last_token = Token(kind, match.group(0))
            return True
        return False
