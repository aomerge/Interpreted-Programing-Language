"""Configuración de precedencias para operadores."""

from enum import IntEnum
from typing import Dict
from src.config.token_1 import TokenType


class Precedence(IntEnum):
    """Precedencia de operadores para el análisis sintáctico."""
    LOWEST = 1
    EQUALS = 2
    LESSGREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7


PRECEDENCES: Dict[TokenType, Precedence] = {
    TokenType.EQUAL: Precedence.EQUALS,
    TokenType.NOT_EQUAL: Precedence.EQUALS,
    TokenType.LT: Precedence.LESSGREATER,
    TokenType.GT: Precedence.LESSGREATER,
    TokenType.PLUS: Precedence.SUM,
    TokenType.MINUS: Precedence.SUM,
    TokenType.DIVISION: Precedence.PRODUCT,
    TokenType.MULTIPLICATION: Precedence.PRODUCT,
    TokenType.LPAREN: Precedence.CALL
}