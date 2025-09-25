"""Nodos de expresiones del AST."""

from typing import List, Optional, TYPE_CHECKING
from src.config.token_1 import Token
from .astNode import Expression

if TYPE_CHECKING:
    from .statement import Block


class Identifier(Expression):
    """Expresión identificador."""
    
    def __init__(self, token: Token, value: str) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return self.value


class Integer(Expression):
    """Expresión literal entero."""
    
    def __init__(self, token: Token, value: Optional[int] = None) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Prefix(Expression):
    """Expresión prefija (ej: -5, !true)."""
    
    def __init__(self, token: Token, operator: str, right: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f'({self.operator}{str(self.right)})'


class Infix(Expression):
    """Expresión infija (ej: 5 + 3, x == y)."""
    
    def __init__(self, token: Token, left: Optional[Expression] = None, 
                 operator: str = "", right: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f'({str(self.left)} {self.operator} {str(self.right)})'


class Boolean(Expression):
    """Expresión booleana."""
    
    def __init__(self, token: Token, value: Optional[bool] = None) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return self.token_literal()


class If(Expression):
    """Expresión condicional if."""
    
    def __init__(self, token: Token, condition: Optional[Expression] = None,
                 consequence: Optional['Block'] = None, alternative: Optional['Block'] = None) -> None:
        super().__init__(token)
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self) -> str:
        out: str = f'si {str(self.condition)} {str(self.consequence)}'
        
        if self.alternative:
            out += f'si_no {str(self.alternative)}'
        
        return out


class Function(Expression):
    """Expresión literal de función."""
    
    def __init__(self, token: Token, parameters: Optional[List[Identifier]] = None,
                 body: Optional['Block'] = None) -> None:
        super().__init__(token)
        self.parameters = parameters if parameters is not None else []
        self.body = body

    def __str__(self) -> str:
        param_list: List[str] = [str(parameter) for parameter in self.parameters]
        params: str = ', '.join(param_list)
        return f'{self.token_literal()}({params}) {str(self.body)}'


class Call(Expression):
    """Expresión de llamada a función."""
    
    def __init__(self, token: Token, function: Expression,
                 arguments: Optional[List[Expression]] = None) -> None:
        super().__init__(token)
        self.function = function
        self.arguments = arguments

    def __str__(self) -> str:
        if self.arguments is not None:
            arg_list: List[str] = [str(argument) for argument in self.arguments]
            args: str = ', '.join(arg_list)
        else:
            args = ""
        
        return f'{str(self.function)}({args})'


class StringLiteral(Expression):
    """Expresión literal de cadena."""
    
    def __init__(self, token: Token, value: str) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return self.value