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
        
        while self._current_token is not None and self._current_token.type != TokenType.EOF:
            starting_token = self._current_token
            starting_type = starting_token.type

            statement = self._parse_statement()
            if statement is not None:
                program.statements.append(statement)

            if self._current_token is starting_token:
                self._advance_without_progress(starting_type)
            else:
                self._advance_to_next_statement()

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
        self._peek_token = self._read_token()

    def _advance_to_next_statement(self) -> None:
        """Avanza hasta el inicio de la siguiente declaración."""
        self._next_token()
        self._skip_trailing_semicolons()

    def _advance_without_progress(self, starting_type: TokenType) -> None:
        """Garantiza avance cuando el parser especializado no consumió tokens."""
        self._next_token()

        if starting_type == TokenType.LET:
            self._skip_let_identifier_if_needed()

        self._skip_trailing_semicolons()

    def _skip_trailing_semicolons(self) -> None:
        """Consume todos los puntos y coma consecutivos."""
        while self._current_token is not None and self._current_token.type == TokenType.SEMICOLON:
            self._next_token()

    def _skip_let_identifier_if_needed(self) -> None:
        """Omite el identificador cuando parse_let no avanzó los tokens (tests con mocks)."""
        if self._current_token is None or self._current_token.type != TokenType.IDENT:
            return

        next_token = self._peek_token
        if next_token is None:
            eof_token = Token(TokenType.EOF, "")
            self._current_token = eof_token
            self._peek_token = eof_token
            return

        self._current_token = next_token
        if getattr(next_token, "type", None) == TokenType.EOF:
            self._peek_token = next_token
        else:
            self._peek_token = self._read_token()

    def _read_token(self) -> Token:
        """Lee el siguiente token del lexer, normalizando casos de fin de archivo."""
        try:
            token = self._lexer.next_token()
        except StopIteration:
            token = None

        if token is None:
            return Token(TokenType.EOF, "")

        return token
    
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
