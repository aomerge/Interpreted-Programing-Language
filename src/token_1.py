from enum import (
    auto,
    Enum,
    unique
)
from typing import  NamedTuple
@unique
class TokenType(Enum):
    ASSING = auto()
    COMMA = auto()
    EOF = auto()
    FUNCTION = auto()
    IDENT = auto()
    ILLEGAL = auto()
    INT = auto()
    LBRACE = auto()
    LET = auto()
    LPAREN = auto()
    PLUS = auto()
    RBRACE = auto()
    RPAREN = auto()
    SEMICOLON = auto()

class Token(NamedTuple):
    type: TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type: {self.type}, Literal: {self.literal}\n'