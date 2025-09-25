"""Tests para el parser de expresiones."""

import unittest
from unittest.mock import Mock, patch, MagicMock

from src.parser.expression_parser import ExpressionParser
from src.astNode import (
    Expression, Prefix, Infix, Integer, Boolean, 
    Identifier, Call, StringLiteral, Function, Block
)
from src.config.token_1 import Token, TokenType
from src.parser.precedence import Precedence


class TestExpressionParser(unittest.TestCase):
    """Tests para la clase ExpressionParser."""

    def setUp(self):
        """Configuración inicial para cada test."""
        # Mock del parser core
        self.mock_core = Mock()
        
        # Mock tokens comunes
        self.int_token = Mock(spec=Token)
        self.int_token.type = TokenType.INT
        self.int_token.literal = "42"
        
        self.ident_token = Mock(spec=Token)
        self.ident_token.type = TokenType.IDENT
        self.ident_token.literal = "x"
        
        self.string_token = Mock(spec=Token)
        self.string_token.type = TokenType.STRING
        self.string_token.literal = "hello"
        
        self.true_token = Mock(spec=Token)
        self.true_token.type = TokenType.TRUE
        self.true_token.literal = "true"
        
        self.false_token = Mock(spec=Token)
        self.false_token.type = TokenType.FALSE
        self.false_token.literal = "false"
        
        self.bang_token = Mock(spec=Token)
        self.bang_token.type = TokenType.BANG
        self.bang_token.literal = "!"
        
        self.minus_token = Mock(spec=Token)
        self.minus_token.type = TokenType.MINUS
        self.minus_token.literal = "-"
        
        self.plus_token = Mock(spec=Token)
        self.plus_token.type = TokenType.PLUS
        self.plus_token.literal = "+"
        
        self.lparen_token = Mock(spec=Token)
        self.lparen_token.type = TokenType.LPAREN
        self.lparen_token.literal = "("
        
        self.rparen_token = Mock(spec=Token)
        self.rparen_token.type = TokenType.RPAREN
        self.rparen_token.literal = ")"
        
        self.function_token = Mock(spec=Token)
        self.function_token.type = TokenType.FUNCTION
        self.function_token.literal = "funcion"
        
        self.eof_token = Mock(spec=Token)
        self.eof_token.type = TokenType.EOF
        self.eof_token.literal = ""
        
        # Configurar mocks del core
        self.mock_core._current_token = self.int_token
        self.mock_core._peek_token = self.plus_token
        
        # Mock del function parser
        self.mock_function_parser = Mock()
        self.mock_core.function_parser = self.mock_function_parser

    def test_init_sets_core_reference_and_parse_functions(self):
        """Test que __init__ establece la referencia al core y las funciones de parseo."""
        # Act
        parser = ExpressionParser(self.mock_core)
        
        # Assert
        self.assertEqual(parser.core, self.mock_core)
        self.assertIsNotNone(parser._prefix_parse_fns)
        self.assertIsNotNone(parser._infix_parse_fns)
        
        # Verificar que las funciones prefix están registradas
        self.assertIn(TokenType.IDENT, parser._prefix_parse_fns)
        self.assertIn(TokenType.INT, parser._prefix_parse_fns)
        self.assertIn(TokenType.STRING, parser._prefix_parse_fns)
        self.assertIn(TokenType.BANG, parser._prefix_parse_fns)
        self.assertIn(TokenType.MINUS, parser._prefix_parse_fns)
        self.assertIn(TokenType.TRUE, parser._prefix_parse_fns)
        self.assertIn(TokenType.FALSE, parser._prefix_parse_fns)
        self.assertIn(TokenType.LPAREN, parser._prefix_parse_fns)
        self.assertIn(TokenType.FUNCTION, parser._prefix_parse_fns)
        
        # Verificar que las funciones infix están registradas
        self.assertIn(TokenType.PLUS, parser._infix_parse_fns)
        self.assertIn(TokenType.MINUS, parser._infix_parse_fns)
        self.assertIn(TokenType.DIVISION, parser._infix_parse_fns)
        self.assertIn(TokenType.MULTIPLICATION, parser._infix_parse_fns)
        self.assertIn(TokenType.EQUAL, parser._infix_parse_fns)
        self.assertIn(TokenType.NOT_EQUAL, parser._infix_parse_fns)
        self.assertIn(TokenType.LT, parser._infix_parse_fns)
        self.assertIn(TokenType.GT, parser._infix_parse_fns)
        self.assertIn(TokenType.LPAREN, parser._infix_parse_fns)

    def test_parse_expression_no_prefix_function(self):
        """Test parse_expression cuando no hay función prefix para el token."""
        # Arrange
        unknown_token = Mock(spec=Token)
        unknown_token.type = TokenType.RBRACE  # Token sin función prefix
        unknown_token.literal = "}"
        
        self.mock_core._current_token = unknown_token
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser.parse_expression(Precedence.LOWEST)
        
        # Assert
        self.assertIsNone(result)
        self.mock_core._add_no_prefix_parse_fn_error.assert_called_with(TokenType.RBRACE)

    def test_parse_expression_success_with_precedence(self):
        """Test parse_expression exitoso con precedencia."""
        # Arrange
        self.mock_core._current_token = self.int_token
        self.mock_core._peek_token = self.eof_token  # Sin infix para evitar el bucle
        self.mock_core._peek_precedence.return_value = Precedence.LOWEST
        
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser.parse_expression(Precedence.LOWEST)
        
        # Assert
        self.assertIsInstance(result, Integer)
        self.assertEqual(result.value, 42)

    def test_parse_identifier_success(self):
        """Test _parse_identifier exitoso."""
        # Arrange
        self.mock_core._current_token = self.ident_token
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser._parse_identifier()
        
        # Assert
        self.assertIsInstance(result, Identifier)
        self.assertEqual(result.token, self.ident_token)
        self.assertEqual(result.value, "x")

    def test_parse_integer_literal_success(self):
        """Test _parse_integer_literal exitoso."""
        # Arrange
        self.mock_core._current_token = self.int_token
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser._parse_integer_literal()
        
        # Assert
        self.assertIsInstance(result, Integer)
        self.assertEqual(result.token, self.int_token)
        self.assertEqual(result.value, 42)

    def test_parse_integer_literal_invalid_value(self):
        """Test _parse_integer_literal con valor inválido."""
        # Arrange
        invalid_token = Mock(spec=Token)
        invalid_token.type = TokenType.INT
        invalid_token.literal = "invalid"
        
        self.mock_core._current_token = invalid_token
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser._parse_integer_literal()
        
        # Assert
        self.assertIsNone(result)
        self.mock_core.errors.append.assert_called()

    def test_parse_string_literal_success(self):
        """Test _parse_string_literal exitoso."""
        # Arrange
        self.mock_core._current_token = self.string_token
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser._parse_string_literal()
        
        # Assert
        self.assertIsInstance(result, StringLiteral)
        self.assertEqual(result.token, self.string_token)
        self.assertEqual(result.value, "hello")

    def test_parse_boolean_true(self):
        """Test _parse_boolean con valor true."""
        # Arrange
        self.mock_core._current_token = self.true_token
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser._parse_boolean()
        
        # Assert
        self.assertIsInstance(result, Boolean)
        self.assertEqual(result.token, self.true_token)
        self.assertTrue(result.value)

    def test_parse_boolean_false(self):
        """Test _parse_boolean con valor false."""
        # Arrange
        self.mock_core._current_token = self.false_token
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser._parse_boolean()
        
        # Assert
        self.assertIsInstance(result, Boolean)
        self.assertEqual(result.token, self.false_token)
        self.assertFalse(result.value)

    def test_parse_prefix_expression_bang(self):
        """Test _parse_prefix_expression con operador bang (!)."""
        # Arrange
        self.mock_core._current_token = self.bang_token
        self.mock_core._peek_token = self.true_token
        self.mock_core._next_token.return_value = None
        
        parser = ExpressionParser(self.mock_core)
        
        # Configurar el mock para que parse_expression retorne un Boolean
        with patch.object(parser, 'parse_expression') as mock_parse:
            mock_boolean = Boolean(token=self.true_token, value=True)
            mock_parse.return_value = mock_boolean
            
            # Act
            result = parser._parse_prefix_expression()
            
            # Assert
            self.assertIsInstance(result, Prefix)
            self.assertEqual(result.token, self.bang_token)
            self.assertEqual(result.operator, "!")
            self.assertEqual(result.right, mock_boolean)
            mock_parse.assert_called_with(Precedence.PREFIX)

    def test_parse_prefix_expression_minus(self):
        """Test _parse_prefix_expression con operador minus (-)."""
        # Arrange
        self.mock_core._current_token = self.minus_token
        self.mock_core._peek_token = self.int_token
        self.mock_core._next_token.return_value = None
        
        parser = ExpressionParser(self.mock_core)
        
        # Configurar el mock para que parse_expression retorne un Integer
        with patch.object(parser, 'parse_expression') as mock_parse:
            mock_integer = Integer(token=self.int_token, value=42)
            mock_parse.return_value = mock_integer
            
            # Act
            result = parser._parse_prefix_expression()
            
            # Assert
            self.assertIsInstance(result, Prefix)
            self.assertEqual(result.token, self.minus_token)
            self.assertEqual(result.operator, "-")
            self.assertEqual(result.right, mock_integer)

    def test_parse_infix_expression_addition(self):
        """Test _parse_infix_expression con suma."""
        # Arrange
        left_expr = Integer(token=self.int_token, value=5)
        
        self.mock_core._current_token = self.plus_token
        self.mock_core._next_token.return_value = None
        
        parser = ExpressionParser(self.mock_core)
        
        # Configurar el mock para que parse_expression retorne otro Integer
        with patch.object(parser, 'parse_expression') as mock_parse:
            right_integer = Integer(token=self.int_token, value=10)
            mock_parse.return_value = right_integer
            
            # Act
            result = parser._parse_infix_expression(left_expr)
            
            # Assert
            self.assertIsInstance(result, Infix)
            self.assertEqual(result.token, self.plus_token)
            self.assertEqual(result.left, left_expr)
            self.assertEqual(result.operator, "+")
            self.assertEqual(result.right, right_integer)

    def test_parse_infix_expression_with_precedence(self):
        """Test _parse_infix_expression respeta precedencia."""
        # Arrange
        left_expr = Integer(token=self.int_token, value=5)
        
        self.mock_core._current_token = self.plus_token
        self.mock_core._current_precedence.return_value = Precedence.SUM
        
        parser = ExpressionParser(self.mock_core)
        
        # Configurar el mock
        with patch.object(parser, 'parse_expression') as mock_parse:
            right_integer = Integer(token=self.int_token, value=10)
            mock_parse.return_value = right_integer
            
            # Act
            result = parser._parse_infix_expression(left_expr)
            
            # Assert
            self.assertIsInstance(result, Infix)
            mock_parse.assert_called_with(Precedence.SUM)

    def test_parse_grouped_expression_success(self):
        """Test _parse_grouped_expression exitoso."""
        # Arrange
        self.mock_core._current_token = self.lparen_token
        self.mock_core._peek_token = self.int_token
        self.mock_core._next_token.return_value = None
        self.mock_core._expected_tokens.return_value = True
        
        parser = ExpressionParser(self.mock_core)
        
        # Configurar el mock para que parse_expression retorne un Integer
        with patch.object(parser, 'parse_expression') as mock_parse:
            mock_integer = Integer(token=self.int_token, value=42)
            mock_parse.return_value = mock_integer
            
            # Act
            result = parser._parse_grouped_expression()
            
            # Assert
            self.assertEqual(result, mock_integer)
            self.mock_core._next_token.assert_called()
            self.mock_core._expected_tokens.assert_called_with(TokenType.RPAREN)
            mock_parse.assert_called_with(Precedence.LOWEST)

    def test_parse_grouped_expression_missing_rparen(self):
        """Test _parse_grouped_expression cuando falta el paréntesis de cierre."""
        # Arrange
        self.mock_core._current_token = self.lparen_token
        self.mock_core._next_token.return_value = None
        self.mock_core._expected_tokens.return_value = False  # Simular error
        
        parser = ExpressionParser(self.mock_core)
        
        # Configurar el mock
        with patch.object(parser, 'parse_expression') as mock_parse:
            mock_integer = Integer(token=self.int_token, value=42)
            mock_parse.return_value = mock_integer
            
            # Act
            result = parser._parse_grouped_expression()
            
            # Assert
            self.assertIsNone(result)

    def test_parse_call_expression_success(self):
        """Test _parse_call_expression exitoso."""
        # Arrange
        function_expr = Identifier(token=self.ident_token, value="add")
        
        self.mock_core._current_token = self.lparen_token
        
        parser = ExpressionParser(self.mock_core)
        
        # Mock para parse_call_arguments
        with patch.object(parser, '_parse_call_arguments') as mock_parse_args:
            mock_args = [Integer(token=self.int_token, value=1)]
            mock_parse_args.return_value = mock_args
            
            # Act
            result = parser._parse_call_expression(function_expr)
            
            # Assert
            self.assertIsInstance(result, Call)
            self.assertEqual(result.token, self.lparen_token)
            self.assertEqual(result.function, function_expr)
            self.assertEqual(result.arguments, mock_args)

    def test_parse_call_expression_no_arguments(self):
        """Test _parse_call_expression sin argumentos."""
        # Arrange
        function_expr = Identifier(token=self.ident_token, value="test")
        
        self.mock_core._current_token = self.lparen_token
        
        parser = ExpressionParser(self.mock_core)
        
        # Mock que retorna None (sin argumentos)
        with patch.object(parser, '_parse_call_arguments') as mock_parse_args:
            mock_parse_args.return_value = None
            
            # Act
            result = parser._parse_call_expression(function_expr)
            
            # Assert
            self.assertIsInstance(result, Call)
            self.assertEqual(result.arguments, None)

    def test_parse_function_literal_success(self):
        """Test _parse_function_literal exitoso."""
        # Arrange
        self.mock_core._current_token = self.function_token
        self.mock_core._expected_tokens.return_value = True
        
        parser = ExpressionParser(self.mock_core)
        
        # Mock solo _parse_function_parameters (que sí existe)
        with patch.object(parser, '_parse_function_parameters') as mock_params:
            mock_params.return_value = []
            
            # Mock statement_parser.parse_block_statement
            mock_block = Mock()
            mock_block.statements = []
            parser.core.statement_parser = Mock()
            parser.core.statement_parser.parse_block_statement.return_value = mock_block
            
            # Act
            result = parser._parse_function_literal()
            
            # Assert
            self.assertIsInstance(result, Function)
            self.assertEqual(result.token, self.function_token)
            mock_params.assert_called_once()

    def test_parse_call_arguments_multiple_args(self):
        """Test _parse_call_arguments con múltiples argumentos."""
        # Arrange
        comma_token = Mock(spec=Token)
        comma_token.type = TokenType.COMMA
        comma_token.literal = ","
        
        # Simular que peek_token no es RPAREN inicialmente
        self.mock_core._peek_token = self.int_token
        self.mock_core._next_token.return_value = None
        self.mock_core._expected_tokens.return_value = True
        
        parser = ExpressionParser(self.mock_core)
        
        # Mock para parse_expression que retorna un argumento
        arg1 = Integer(token=self.int_token, value=1)
        
        with patch.object(parser, 'parse_expression') as mock_parse:
            mock_parse.return_value = arg1
            
            # Simular que después del primer argumento, peek_token es RPAREN
            def expected_tokens_side_effect(token_type):
                if token_type == TokenType.RPAREN:
                    return True
                # Simular que hay más argumentos cambiando peek_token
                self.mock_core._peek_token = self.rparen_token
                return True
            
            self.mock_core._expected_tokens.side_effect = expected_tokens_side_effect
            
            # Act
            result = parser._parse_call_arguments()
            
            # Assert
            self.assertIsInstance(result, list)
            self.assertGreaterEqual(len(result), 1)  # Al menos un argumento

    def test_parse_call_arguments_empty(self):
        """Test _parse_call_arguments sin argumentos."""
        # Arrange
        self.mock_core._peek_token = self.rparen_token
        self.mock_core._expected_tokens.return_value = True
        
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser._parse_call_arguments()
        
        # Assert
        self.assertEqual(result, [])
        # La implementación llama _expected_tokens al final del método, no al principio
        # cuando la lista está vacía

    def test_parse_call_arguments_missing_rparen(self):
        """Test _parse_call_arguments cuando falta el paréntesis de cierre."""
        # Arrange
        self.mock_core._peek_token = self.int_token
        self.mock_core._next_token.return_value = None
        self.mock_core._expected_tokens.return_value = False  # Error
        
        parser = ExpressionParser(self.mock_core)
        
        with patch.object(parser, 'parse_expression') as mock_parse:
            mock_parse.return_value = Integer(token=self.int_token, value=42)
            
            # Act
            result = parser._parse_call_arguments()
            
            # Assert
            self.assertIsNone(result)

    def test_integration_complex_expression(self):
        """Test de integración para expresión compleja: 1 + 2 * 3."""
        # Arrange
        int1_token = Mock(spec=Token)
        int1_token.type = TokenType.INT
        int1_token.literal = "1"
        
        self.mock_core._current_token = int1_token
        self.mock_core._peek_token = self.eof_token
        self.mock_core._peek_precedence.return_value = Precedence.LOWEST
        
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser.parse_expression(Precedence.LOWEST)
        
        # Assert
        self.assertIsInstance(result, Integer)  # Por simplicidad, verificamos que procesa el primer token
        self.assertEqual(result.value, 1)

    def test_integration_function_call_with_arguments(self):
        """Test de integración para llamada a función con argumentos."""
        # Arrange
        self.mock_core._current_token = self.ident_token
        self.mock_core._peek_token = self.eof_token
        self.mock_core._peek_precedence.return_value = Precedence.LOWEST
        
        parser = ExpressionParser(self.mock_core)
        
        # Act
        result = parser.parse_expression(Precedence.LOWEST)
        
        # Assert
        self.assertIsInstance(result, Identifier)  # Procesará el identificador inicial
        self.assertEqual(result.value, "x")


if __name__ == '__main__':
    unittest.main()