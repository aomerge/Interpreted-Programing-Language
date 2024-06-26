from abc import (
    ABC, # type: ignore 
    abstractmethod # type: ignore
)
from typing import (
    List,
    Optional
)

from src.token_1 import (
    Token,
    TokenType
)

class ASTNode(ABC):
    def __init__(self, token: Token):
        self.token = token

    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

class Statement(ASTNode):
    def __init__(self, token: Token):
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

class Expression(ASTNode):
    def __init__(self, token: Token)-> None:
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

class Program(ASTNode):
    def __init__(self, statements: list[Statement]):
        self.statements = statements

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def __str__(self) -> str:
        out:List[str] = []
        for statement in self.statements:
            out.append(str(statement))
        return ''.join(out)
    
class Identifier(Expression):
    def __init__(self, token: Token, value: str)-> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return self.value
    
class LetStatement(Statement):
    def __init__(self, token: Token, name: Optional[Identifier] = None , value: Optional[Expression] = None)-> None:
        super().__init__(token)        
        self.name = name
        self.value = value    

    def __str__(self) -> str:
        out = f'{self.token_literal()} {str(self.name)} = {str(self.value)};'
        return out

class ReturnStatement(Statement):
    def __init__(self, token: Token, return_value: Optional[Expression] = None)-> None:
        super().__init__(token)
        self.return_value = return_value

    def __str__(self) -> str:
        out = f'{self.token_literal()} {str(self.return_value)};'
        return out
    
class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Optional[Expression] = None)-> None:
        super().__init__(token)
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression)
     