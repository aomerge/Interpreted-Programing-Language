"""Parser especializado en declaraciones (statements)."""

from typing import Optional, List
from src.astNode import (
    Statement, LetStatement, ReturnStatement, 
    ExpressionStatement, Identifier, Block
)
from src.config.token_1 import Token, TokenType
from .precedence import Precedence


class StatementParser:
    """Maneja el análisis sintáctico de declaraciones."""
    
    def __init__(self, parser_core):
        self.core = parser_core
    
    def parse_let_statement(self) -> Optional[LetStatement]:
        """Analiza declaraciones let."""
        assert self.core._current_token is not None
        
        let_statement = LetStatement(token=self.core._current_token)
        
        if not self.core._expected_tokens(TokenType.IDENT):
            return None
        
        let_statement.name = self._parse_identifier_for_let()
        
        if not self.core._expected_tokens(TokenType.ASSIGN):
            return None
        
        self.core._next_token()
        let_statement.value = self.core.expression_parser.parse_expression(Precedence.LOWEST)
        
        if self.core._peek_token.type == TokenType.SEMICOLON:
            self.core._next_token()
        
        return let_statement
    
    def parse_return_statement(self) -> ReturnStatement:
        """Analiza declaraciones return."""
        assert self.core._current_token is not None
        
        statement = ReturnStatement(token=self.core._current_token)
        self.core._next_token()
        
        statement.return_value = self.core.expression_parser.parse_expression(Precedence.LOWEST)
        
        if self.core._peek_token.type == TokenType.SEMICOLON:
            self.core._next_token()
        
        return statement
    
    def parse_expression_statement(self) -> Optional[ExpressionStatement]:
        """Analiza declaraciones de expresión."""
        assert self.core._current_token is not None
        
        expression_statement = ExpressionStatement(token=self.core._current_token)
        expression_statement.expression = self.core.expression_parser.parse_expression(Precedence.LOWEST)
        
        assert self.core._peek_token is not None
        if self.core._peek_token.type == TokenType.SEMICOLON:
            self.core._next_token()
        
        return expression_statement
    
    def parse_block_statement(self) -> Block:
        """Analiza bloques de declaraciones."""
        assert self.core._current_token is not None
        
        block_statement = Block(token=self.core._current_token, statements=[])
        self.core._next_token()
        
        while (not self.core._current_token.type == TokenType.RBRACE and 
               not self.core._current_token.type == TokenType.EOF):
            statement = self.core._parse_statement()
            if statement is not None:
                block_statement.statements.append(statement)
            self.core._next_token()
        
        return block_statement
    
    def _parse_identifier_for_let(self) -> Optional[Identifier]:
        """Auxiliar para parsear identificadores en declaraciones let."""
        assert self.core._current_token is not None
        return Identifier(token=self.core._current_token, value=self.core._current_token.literal)