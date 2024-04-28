from abc import (
    ABC, # type: ignore 
    abstractmethod # type: ignore
)
from typing import List

from src.token_1 import Token

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