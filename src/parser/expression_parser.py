"""Parser especializado en expresiones."""

from typing import Optional, List, Callable, Dict
from src.ast import (
    Expression, Prefix, Infix,
    Integer, Boolean, Identifier, Call,
    StringLiteral, Function, Block
)
from src.token_1 import Token, TokenType
from .precedence import Precedence, PRECEDENCES


class ExpressionParser:
    """Maneja el análisis sintáctico de expresiones."""
    
    def __init__(self, parser_core):
        self.core = parser_core
        self._prefix_parse_fns: Dict[TokenType, Callable[[], Optional[Expression]]] = {
            TokenType.IDENT: self._parse_identifier,
            TokenType.INT: self._parse_integer_literal,
            TokenType.STRING: self._parse_string_literal,
            TokenType.BANG: self._parse_prefix_expression,
            TokenType.MINUS: self._parse_prefix_expression,
            TokenType.TRUE: self._parse_boolean,
            TokenType.FALSE: self._parse_boolean,
            TokenType.LPAREN: self._parse_grouped_expression,
            TokenType.FUNCTION: self._parse_function_literal
        }
        
        self._infix_parse_fns: Dict[TokenType, Callable[[Expression], Optional[Expression]]] = {
            TokenType.PLUS: self._parse_infix_expression,
            TokenType.MINUS: self._parse_infix_expression,
            TokenType.DIVISION: self._parse_infix_expression,
            TokenType.MULTIPLICATION: self._parse_infix_expression,
            TokenType.EQUAL: self._parse_infix_expression,
            TokenType.NOT_EQUAL: self._parse_infix_expression,
            TokenType.LT: self._parse_infix_expression,
            TokenType.GT: self._parse_infix_expression,
            TokenType.LPAREN: self._parse_call_expression
        }
    
    def parse_expression(self, precedence: Precedence) -> Optional[Expression]:
        """Método principal para parsear expresiones."""
        assert self.core._current_token is not None
        
        prefix_parse_fn = self._prefix_parse_fns.get(self.core._current_token.type)
        if prefix_parse_fn is None:
            self.core._add_no_prefix_parse_fn_error(self.core._current_token.type)
            return None
        
        left_expression = prefix_parse_fn()
        
        assert self.core._peek_token is not None
        while (self.core._peek_token.type != TokenType.SEMICOLON and 
               precedence < self.core._peek_precedence()):
            infix_parse_fn = self._infix_parse_fns.get(self.core._peek_token.type)
            if infix_parse_fn is None:
                return left_expression
            
            self.core._next_token()
            left_expression = infix_parse_fn(left_expression)
        
        return left_expression
    
    def _parse_identifier(self) -> Optional[Identifier]:
        """Parsea identificadores."""
        assert self.core._current_token is not None
        return Identifier(token=self.core._current_token, value=self.core._current_token.literal)
    
    def _parse_integer_literal(self) -> Optional[Integer]:
        """Parsea literales enteros."""
        assert self.core._current_token is not None
        
        literal = Integer(token=self.core._current_token)
        try:
            literal.value = int(self.core._current_token.literal)
        except ValueError:
            message = f"could not parse {self.core._current_token.literal} as integer"
            self.core.errors.append(message)
            return None
        
        return literal
    
    def _parse_string_literal(self) -> Optional[StringLiteral]:
        """Parsea literales de cadena."""
        assert self.core._current_token is not None
        return StringLiteral(token=self.core._current_token, value=self.core._current_token.literal)
    
    def _parse_boolean(self) -> Optional[Boolean]:
        """Parsea valores booleanos."""
        assert self.core._current_token is not None
        return Boolean(token=self.core._current_token, value=self.core._current_token.type == TokenType.TRUE)
    
    def _parse_prefix_expression(self) -> Optional[Prefix]:
        """Parsea expresiones prefijas."""
        assert self.core._current_token is not None
        
        expression = Prefix(token=self.core._current_token, operator=self.core._current_token.literal)
        self.core._next_token()
        expression.right = self.parse_expression(Precedence.PREFIX)
        
        return expression
    
    def _parse_infix_expression(self, left: Expression) -> Optional[Infix]:
        """Parsea expresiones infijas."""
        assert self.core._current_token is not None
        
        expression = Infix(
            token=self.core._current_token,
            left=left,
            operator=self.core._current_token.literal
        )
        
        precedence = self.core._current_precedence()
        self.core._next_token()
        expression.right = self.parse_expression(precedence)
        
        return expression
    
    def _parse_grouped_expression(self) -> Optional[Expression]:
        """Parsea expresiones agrupadas entre paréntesis."""
        self.core._next_token()
        expression = self.parse_expression(Precedence.LOWEST)
        
        if not self.core._expected_tokens(TokenType.RPAREN):
            return None
        
        return expression
    
    def _parse_call_expression(self, function: Expression) -> Optional[Call]:
        """Parsea llamadas a funciones."""
        assert self.core._current_token is not None
        
        expression = Call(token=self.core._current_token, function=function)
        expression.arguments = self._parse_call_arguments()
        
        return expression
    
    def _parse_call_arguments(self) -> Optional[List[Expression]]:
        """Parsea argumentos de llamadas a funciones."""
        args: List[Expression] = []
        
        assert self.core._peek_token is not None
        if self.core._peek_token.type == TokenType.RPAREN:
            self.core._next_token()
            return args
        
        self.core._next_token()
        argument = self.parse_expression(Precedence.LOWEST)
        if argument:
            args.append(argument)
        
        while self.core._peek_token.type == TokenType.COMMA:
            self.core._next_token()
            self.core._next_token()
            argument = self.parse_expression(Precedence.LOWEST)
            if argument:
                args.append(argument)
        
        if not self.core._expected_tokens(TokenType.RPAREN):
            return None
        
        return args
    
    def _parse_function_literal(self) -> Optional[Function]:
        """Parsea literales de función."""
        assert self.core._current_token is not None
        
        literal = Function(token=self.core._current_token)
        
        if not self.core._expected_tokens(TokenType.LPAREN):
            return None
        
        literal.parameters = self._parse_function_parameters()
        
        if not self.core._expected_tokens(TokenType.LBRACE):
            return None
        
        literal.body = self.core.statement_parser.parse_block_statement()
        
        return literal
    
    def _parse_function_parameters(self) -> Optional[List[Identifier]]:
        """Parsea parámetros de función."""
        identifiers: List[Identifier] = []
        
        assert self.core._peek_token is not None
        if self.core._peek_token.type == TokenType.RPAREN:
            self.core._next_token()
            return identifiers
        
        self.core._next_token()
        
        assert self.core._current_token is not None
        identifier = Identifier(token=self.core._current_token, value=self.core._current_token.literal)
        identifiers.append(identifier)
        
        while self.core._peek_token.type == TokenType.COMMA:
            self.core._next_token()
            self.core._next_token()
            
            assert self.core._current_token is not None
            identifier = Identifier(token=self.core._current_token, value=self.core._current_token.literal)
            identifiers.append(identifier)
        
        if not self.core._expected_tokens(TokenType.RPAREN):
            return None
        
        return identifiers