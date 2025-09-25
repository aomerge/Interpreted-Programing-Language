"""Nodos base del AST."""

from abc import ABC, abstractmethod
from typing import List
from src.config.token_1 import Token


class ASTNode(ABC):
    """Clase base abstracta para todos los nodos del AST."""
    
    def __init__(self, token: Token):
        self.token = token

    @abstractmethod
    def token_literal(self) -> str:
        """Retorna el literal del token asociado."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Representación en cadena del nodo."""
        pass


class Statement(ASTNode):
    """Clase base para todas las declaraciones."""
    
    def __init__(self, token: Token):
        super().__init__(token)

    def token_literal(self) -> str:
        return self.token.literal


class Expression(ASTNode):
    """Clase base para todas las expresiones."""
    
    def __init__(self, token: Token) -> None:
        super().__init__(token)

    def token_literal(self) -> str:
        return self.token.literal


class Program(ASTNode):
    """Nodo raíz del programa que contiene todas las declaraciones."""
    
    def __init__(self, statements: List['Statement']):
        # Program no tiene un token específico, usamos el primer statement si existe
        if statements and len(statements) > 0:
            super().__init__(statements[0].token)
        else:
            # Token dummy para cuando no hay statements
            from src.config.token_1 import TokenType
            dummy_token = Token(TokenType.EOF, "")
            super().__init__(dummy_token)
        
        self.statements = statements

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def __str__(self) -> str:
        out: List[str] = []
        for statement in self.statements:
            out.append(str(statement))
        return ''.join(out)