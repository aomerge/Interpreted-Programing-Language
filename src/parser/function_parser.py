"""Parser especializado en funciones y llamadas."""

from typing import Optional, List
from src.astNode import Function, Call, Identifier, Expression
from src.config.token_1 import TokenType
from .precedence import Precedence


class FunctionParser:
    """Maneja el análisis sintáctico específico de funciones."""
    
    def __init__(self, parser_core):
        self.core = parser_core
    
    def parse_function_definition(self) -> Optional[Function]:
        """Parsea definiciones de función completas."""
        assert self.core._current_token is not None
        
        function_literal = Function(token=self.core._current_token)
        
        # Esperar '('
        if not self.core._expected_tokens(TokenType.LPAREN):
            return None
        
        # Parsear parámetros
        function_literal.parameters = self._parse_parameters()
        if function_literal.parameters is None:
            return None
        
        # Esperar '{'
        if not self.core._expected_tokens(TokenType.LBRACE):
            return None
        
        # Parsear cuerpo de la función
        function_literal.body = self.core.statement_parser.parse_block_statement()
        
        return function_literal
    
    def parse_function_call(self, function: Expression) -> Optional[Call]:
        """Parsea llamadas a función."""
        assert self.core._current_token is not None
        
        call_expression = Call(token=self.core._current_token, function=function)
        call_expression.arguments = self._parse_call_arguments()
        
        return call_expression
    
    def _parse_parameters(self) -> Optional[List[Identifier]]:
        """Parsea lista de parámetros de función."""
        parameters: List[Identifier] = []
        
        assert self.core._peek_token is not None
        
        # Función sin parámetros: fn() {}
        if self.core._peek_token.type == TokenType.RPAREN:
            self.core._next_token()
            return parameters
        
        # Primer parámetro
        self.core._next_token()
        assert self.core._current_token is not None
        
        if self.core._current_token.type != TokenType.IDENT:
            self.core.errors.append(f"Expected identifier, got {self.core._current_token.type}")
            return None
        
        first_param = Identifier(
            token=self.core._current_token,
            value=self.core._current_token.literal
        )
        parameters.append(first_param)
        
        # Parámetros adicionales separados por comas
        while self.core._peek_token.type == TokenType.COMMA:
            self.core._next_token()  # consumir ','
            self.core._next_token()  # ir al siguiente identificador
            
            assert self.core._current_token is not None
            
            if self.core._current_token.type != TokenType.IDENT:
                self.core.errors.append(f"Expected identifier, got {self.core._current_token.type}")
                return None
            
            param = Identifier(
                token=self.core._current_token,
                value=self.core._current_token.literal
            )
            parameters.append(param)
        
        # Esperar ')'
        if not self.core._expected_tokens(TokenType.RPAREN):
            return None
        
        return parameters
    
    def _parse_call_arguments(self) -> Optional[List[Expression]]:
        """Parsea argumentos de llamada a función."""
        arguments: List[Expression] = []
        
        assert self.core._peek_token is not None
        
        # Llamada sin argumentos: fn()
        if self.core._peek_token.type == TokenType.RPAREN:
            self.core._next_token()
            return arguments
        
        # Primer argumento
        self.core._next_token()
        first_arg = self.core.expression_parser.parse_expression(Precedence.LOWEST)
        if first_arg is None:
            return None
        arguments.append(first_arg)
        
        # Argumentos adicionales separados por comas
        while self.core._peek_token.type == TokenType.COMMA:
            self.core._next_token()  # consumir ','
            self.core._next_token()  # ir a la siguiente expresión
            
            arg = self.core.expression_parser.parse_expression(Precedence.LOWEST)
            if arg is None:
                return None
            arguments.append(arg)
        
        # Esperar ')'
        if not self.core._expected_tokens(TokenType.RPAREN):
            return None
        
        return arguments
    
    def validate_function_signature(self, parameters: List[Identifier]) -> bool:
        """Valida que la signatura de función sea correcta."""
        # Verificar que no hay parámetros duplicados
        param_names = [param.value for param in parameters]
        if len(param_names) != len(set(param_names)):
            self.core.errors.append("Duplicate parameter names in function definition")
            return False
        
        # Verificar que todos los parámetros son identificadores válidos
        for param in parameters:
            if not param.value or not param.value.replace('_', '').isalnum():
                self.core.errors.append(f"Invalid parameter name: {param.value}")
                return False
        
        return True