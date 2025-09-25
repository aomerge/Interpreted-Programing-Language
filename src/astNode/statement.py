"""Nodos de declaraciones del AST."""

from typing import List, Optional
from src.config.token_1 import Token
from .astNode import Statement
from .expression import Identifier, Expression


class LetStatement(Statement):
    """Declaración de asignación let."""
    
    def __init__(self, token: Token, name: Optional[Identifier] = None,
                 value: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.name = name
        self.value = value

    def __str__(self) -> str:
        out = f'{self.token_literal()} {str(self.name)} = {str(self.value)};'
        return out


class ReturnStatement(Statement):
    """Declaración de retorno."""
    
    def __init__(self, token: Token, return_value: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.return_value = return_value
        print("class ReturnStatement", return_value, Token)

    def __str__(self) -> str:
        out = f'{self.token_literal()} {str(self.return_value)};'
        return out


class ExpressionStatement(Statement):
    """Declaración de expresión."""
    
    def __init__(self, token: Token, expression: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression)


class Block(Statement):
    """Bloque de declaraciones."""
    
    def __init__(self, token: Token, statements: List[Statement]) -> None:
        super().__init__(token)
        self.statements = statements

    def __str__(self) -> str:
        out: List[str] = [str(statement) for statement in self.statements]
        return ''.join(out)