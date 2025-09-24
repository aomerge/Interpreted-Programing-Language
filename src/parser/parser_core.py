"""Núcleo del parser modular."""

from typing import Optional, List
from src.astNode import Program, Statement
from src.lexer.lexer import Lexer
from src.config.token_1 import Token, TokenType
from .precedence import Precedence, PRECEDENCES
from .statement_parser import StatementParser
from .expression_parser import ExpressionParser
from .function_parser import FunctionParser


class ModularParser:
    """Parser modular dividido en componentes especializados."""
    
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self.errors: List[str] = []
        
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None
        
        # Inicializar componentes especializados
        self.statement_parser = StatementParser(self)
        self.expression_parser = ExpressionParser(self)
        self.function_parser = FunctionParser(self)
        
        # Leer los primeros dos tokens
        self._next_token()
        self._next_token()
    
    def parse_program(self) -> Program:
        """Parsea el programa completo."""
        program = Program(statements=[])
        
        while not self._current_token.type == TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                program.statements.append(statement)
            self._next_token()
        
        return program
    
    def _parse_statement(self) -> Optional[Statement]:
        """Parsea una declaración según su tipo."""
        assert self._current_token is not None
        
        if self._current_token.type == TokenType.LET:
            return self.statement_parser.parse_let_statement()
        elif self._current_token.type == TokenType.RETURN:
            return self.statement_parser.parse_return_statement()
        else:
            return self.statement_parser.parse_expression_statement()
    
    def _next_token(self) -> None:
        """Avanza al siguiente token."""
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()
    
    def _expected_tokens(self, expected_type: TokenType) -> bool:
        """Verifica y consume un token esperado."""
        assert self._peek_token is not None
        
        if self._peek_token.type == expected_type:
            self._next_token()
            return True
        else:
            self._add_expected_token_error(expected_type, self._peek_token.type)
            return False
    
    def _current_precedence(self) -> Precedence:
        """Obtiene la precedencia del token actual."""
        assert self._current_token is not None
        return PRECEDENCES.get(self._current_token.type, Precedence.LOWEST)
    
    def _peek_precedence(self) -> Precedence:
        """Obtiene la precedencia del siguiente token."""
        assert self._peek_token is not None
        return PRECEDENCES.get(self._peek_token.type, Precedence.LOWEST)
    
    def _add_expected_token_error(self, expected: TokenType, actual: TokenType) -> None:
        """Agrega un error de token esperado."""
        message = f"Expected next token to be {expected}, got {actual} instead"
        self.errors.append(message)
    
    def _add_no_prefix_parse_fn_error(self, token_type: TokenType) -> None:
        """Agrega un error de función de parseo prefijo no encontrada."""
        message = f"No prefix parse function for {token_type} found"
        self.errors.append(message)
    
    def has_errors(self) -> bool:
        """Verifica si hay errores de parseo."""
        return len(self.errors) > 0
    
    def get_errors(self) -> List[str]:
        """Obtiene la lista de errores."""
        return self.errors.copy()


# Clase de compatibilidad con el parser original
class Parser(ModularParser):
    """Wrapper para mantener compatibilidad con el código existente."""
    
    def getProgram(self) -> Program:
        """Método para compatibilidad con el parser original."""
        return self.parse_program()