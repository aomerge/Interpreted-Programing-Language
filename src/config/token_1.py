from enum import (
    auto,
    Enum,
    unique
)
from typing import  NamedTuple

@unique
class TokenType(Enum):
    ABSTRACT = auto()
    AND = auto()
    ASSIGN = auto()
    ASTERISK = auto()
    BACKSLASH = auto()
    BANG = auto()
    CLASS = auto()
    COLON = auto()
    COMMA = auto()
    COMMENT = auto()
    CONDITIONAL = auto()
    CONST = auto()
    DOT = auto()
    EOF = auto()
    EQ = auto()
    EQUAL = auto()
    EXTENDS = auto()
    FALSE = auto()
    FOR_ = auto()
    FUNCTION = auto()
    GT = auto()
    GTE = auto()
    GreaterThan = auto()
    IDENT = auto()
    ILLEGAL = auto()
    IN = auto()
    INT = auto()
    LBRACE = auto()
    LBRACKET = auto()
    LET = auto()
    LOOP = auto()
    LPAREN = auto()
    LT = auto()
    LTE = auto()
    LessThan = auto()
    MINUS = auto()
    NAMESPACES = auto()
    NOT_EQUAL = auto()
    OR = auto()
    PLUS = auto()
    PRIVATE = auto()
    PROTECTED = auto()
    PUBLIC = auto()
    QUOTE = auto()
    RBRACE = auto()
    RBRACKET = auto()
    RETURN = auto()
    RPAREN = auto()
    SELF = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STATIC = auto()
    STRING = auto()
    SUPER = auto()
    TRUE = auto()
    DIVISION = auto()    
    MULTIPLICATION = auto()
    NEGATION = auto()
    ELSE = auto()



class Token(NamedTuple):
    type: TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type: {self.type}, Literal: {self.literal}\n'

