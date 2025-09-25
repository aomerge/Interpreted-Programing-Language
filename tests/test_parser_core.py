"""Tests para el núcleo del parser modular."""

import unittest
from unittest.mock import Mock, patch, MagicMock

from src.parser.parser_core import ModularParser, Parser
from src.astNode import Program, Statement
from src.config.token_1 import Token, TokenType
from src.parser.precedence import Precedence


class TestModularParser(unittest.TestCase):
    """Tests para la clase ModularParser."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.mock_lexer = Mock()
        self.mock_token1 = Mock(spec=Token)
        self.mock_token1.type = TokenType.LET
        self.mock_token1.literal = "let"
        
        self.mock_token2 = Mock(spec=Token)
        self.mock_token2.type = TokenType.IDENT
        self.mock_token2.literal = "x"
        
        self.eof_token = Mock(spec=Token)
        self.eof_token.type = TokenType.EOF
        self.eof_token.literal = ""

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_init_initializes_components(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test que __init__ inicializa todos los componentes correctamente."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        
        # Act
        parser = ModularParser(self.mock_lexer)
        
        # Assert
        self.assertIsNotNone(parser.statement_parser)
        self.assertIsNotNone(parser.expression_parser)
        self.assertIsNotNone(parser.function_parser)
        self.assertEqual(parser.errors, [])

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_init_reads_first_two_tokens(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test que __init__ lee los primeros dos tokens."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        
        # Act
        parser = ModularParser(self.mock_lexer)
        
        # Assert
        self.assertEqual(self.mock_lexer.next_token.call_count, 2)
        self.assertEqual(parser._current_token, self.mock_token1)
        self.assertEqual(parser._peek_token, self.mock_token2)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_next_token_advances_tokens(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test que _next_token avanza los tokens correctamente."""
        # Arrange
        third_token = Mock(spec=Token)
        third_token.type = TokenType.ASSIGN
        third_token.literal = "="
        
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2, third_token]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        parser._next_token()
        
        # Assert
        self.assertEqual(parser._current_token, self.mock_token2)
        self.assertEqual(parser._peek_token, third_token)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_expected_tokens_success(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _expected_tokens cuando el token es el esperado."""
        # Arrange
        third_token = Mock(spec=Token)
        third_token.type = TokenType.ASSIGN
        
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2, third_token]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        result = parser._expected_tokens(TokenType.IDENT)
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(parser._current_token, self.mock_token2)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_expected_tokens_failure(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _expected_tokens cuando el token no es el esperado."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        result = parser._expected_tokens(TokenType.ASSIGN)
        
        # Assert
        self.assertFalse(result)
        self.assertTrue(parser.has_errors())
        self.assertIn("Expected next token to be", parser.errors[0])

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_current_precedence_found(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _current_precedence cuando encuentra la precedencia."""
        # Arrange
        plus_token = Mock(spec=Token)
        plus_token.type = TokenType.PLUS
        
        self.mock_lexer.next_token.side_effect = [plus_token, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        precedence = parser._current_precedence()
        
        # Assert
        self.assertEqual(precedence, Precedence.SUM)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_current_precedence_not_found(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _current_precedence cuando no encuentra la precedencia."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        precedence = parser._current_precedence()
        
        # Assert
        self.assertEqual(precedence, Precedence.LOWEST)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_peek_precedence_found(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _peek_precedence cuando encuentra la precedencia."""
        # Arrange
        plus_token = Mock(spec=Token)
        plus_token.type = TokenType.PLUS
        
        self.mock_lexer.next_token.side_effect = [self.mock_token1, plus_token]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        precedence = parser._peek_precedence()
        
        # Assert
        self.assertEqual(precedence, Precedence.SUM)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_add_expected_token_error(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _add_expected_token_error agrega error correctamente."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        parser._add_expected_token_error(TokenType.ASSIGN, TokenType.IDENT)
        
        # Assert
        self.assertEqual(len(parser.errors), 1)
        self.assertIn("Expected next token to be TokenType.ASSIGN", parser.errors[0])

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_add_no_prefix_parse_fn_error(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _add_no_prefix_parse_fn_error agrega error correctamente."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        parser._add_no_prefix_parse_fn_error(TokenType.ASSIGN)
        
        # Assert
        self.assertEqual(len(parser.errors), 1)
        self.assertIn("No prefix parse function for TokenType.ASSIGN found", parser.errors[0])

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_has_errors_true(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test has_errors retorna True cuando hay errores."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        parser.errors.append("Test error")
        
        # Act & Assert
        self.assertTrue(parser.has_errors())

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_has_errors_false(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test has_errors retorna False cuando no hay errores."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        
        # Act & Assert
        self.assertFalse(parser.has_errors())

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_get_errors_returns_copy(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test get_errors retorna una copia de los errores."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        parser.errors.append("Test error")
        
        # Act
        errors = parser.get_errors()
        errors.append("Modified error")
        
        # Assert
        self.assertEqual(len(parser.errors), 1)
        self.assertEqual(len(errors), 2)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_parse_statement_let_statement(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _parse_statement con declaración let."""
        # Arrange
        mock_statement_parser_instance = Mock()
        mock_stmt_parser.return_value = mock_statement_parser_instance
        
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        
        mock_statement = Mock()
        mock_statement_parser_instance.parse_let_statement.return_value = mock_statement
        
        # Act
        result = parser._parse_statement()
        
        # Assert
        self.assertEqual(result, mock_statement)
        mock_statement_parser_instance.parse_let_statement.assert_called_once()

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_parse_statement_return_statement(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _parse_statement con declaración return."""
        # Arrange
        mock_statement_parser_instance = Mock()
        mock_stmt_parser.return_value = mock_statement_parser_instance
        
        return_token = Mock(spec=Token)
        return_token.type = TokenType.RETURN
        return_token.literal = "return"
        
        self.mock_lexer.next_token.side_effect = [return_token, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        
        mock_statement = Mock()
        mock_statement_parser_instance.parse_return_statement.return_value = mock_statement
        
        # Act
        result = parser._parse_statement()
        
        # Assert
        self.assertEqual(result, mock_statement)
        mock_statement_parser_instance.parse_return_statement.assert_called_once()

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_parse_statement_expression_statement(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _parse_statement con declaración de expresión (default)."""
        # Arrange
        mock_statement_parser_instance = Mock()
        mock_stmt_parser.return_value = mock_statement_parser_instance
        
        int_token = Mock(spec=Token)
        int_token.type = TokenType.INT
        int_token.literal = "42"
        
        self.mock_lexer.next_token.side_effect = [int_token, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        
        mock_statement = Mock()
        mock_statement_parser_instance.parse_expression_statement.return_value = mock_statement
        
        # Act
        result = parser._parse_statement()
        
        # Assert
        self.assertEqual(result, mock_statement)
        mock_statement_parser_instance.parse_expression_statement.assert_called_once()

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_parse_program_empty(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test parse_program con programa vacío (solo EOF)."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.eof_token, self.eof_token]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        program = parser.parse_program()
        
        # Assert
        self.assertIsInstance(program, Program)
        self.assertEqual(len(program.statements), 0)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_parse_program_single_statement(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test parse_program con una sola declaración."""
        # Arrange
        mock_statement_parser_instance = Mock()
        mock_stmt_parser.return_value = mock_statement_parser_instance
        
        mock_statement = Mock()
        mock_statement_parser_instance.parse_let_statement.return_value = mock_statement
        
        # Configurar tokens para que el bucle termine correctamente
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2, self.eof_token, self.eof_token]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        program = parser.parse_program()
        
        # Assert
        self.assertIsInstance(program, Program)
        self.assertGreaterEqual(len(program.statements), 1)  # Al menos una declaración
        # Verificar que se llamó al parser de let
        mock_statement_parser_instance.parse_let_statement.assert_called()

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_parse_program_with_none_statement(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test parse_program cuando una declaración retorna None."""
        # Arrange
        mock_statement_parser_instance = Mock()
        mock_stmt_parser.return_value = mock_statement_parser_instance
        
        mock_statement_parser_instance.parse_let_statement.return_value = None
        
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2, self.eof_token]
        parser = ModularParser(self.mock_lexer)
        
        # Act
        program = parser.parse_program()
        
        # Assert
        self.assertIsInstance(program, Program)
        self.assertEqual(len(program.statements), 0)  # None statements no se agregan

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_read_token_handles_stop_iteration(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test _read_token maneja StopIteration correctamente."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token2]
        parser = ModularParser(self.mock_lexer)
        
        # Simular StopIteration en la siguiente llamada
        self.mock_lexer.next_token.side_effect = StopIteration()
        
        # Act
        token = parser._read_token()
        
        # Assert
        self.assertEqual(token.type, TokenType.EOF)
        self.assertEqual(token.literal, "")


class TestParser(unittest.TestCase):
    """Tests para la clase Parser (wrapper de compatibilidad)."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.mock_lexer = Mock()
        self.mock_token1 = Mock(spec=Token)
        self.mock_token1.type = TokenType.EOF
        self.mock_token1.literal = ""

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_parser_inherits_from_modular_parser(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test que Parser hereda de ModularParser."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token1]
        
        # Act
        parser = Parser(self.mock_lexer)
        
        # Assert
        self.assertIsInstance(parser, ModularParser)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_get_program_calls_parse_program(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test que getProgram() llama a parse_program()."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token1]
        parser = Parser(self.mock_lexer)
        
        with patch.object(parser, 'parse_program') as mock_parse:
            mock_program = Mock()
            mock_parse.return_value = mock_program
            
            # Act
            result = parser.getProgram()
            
            # Assert
            mock_parse.assert_called_once()
            self.assertEqual(result, mock_program)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')
    @patch('src.parser.parser_core.FunctionParser')
    def test_get_program_returns_program(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test que getProgram() retorna un Program."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token1]
        parser = Parser(self.mock_lexer)
        
        # Act
        program = parser.getProgram()
        
        # Assert
        self.assertIsInstance(program, Program)

    @patch('src.parser.parser_core.StatementParser')
    @patch('src.parser.parser_core.ExpressionParser')  
    @patch('src.parser.parser_core.FunctionParser')
    def test_parser_maintains_compatibility(self, mock_func_parser, mock_expr_parser, mock_stmt_parser):
        """Test que Parser mantiene la compatibilidad con el código existente."""
        # Arrange
        self.mock_lexer.next_token.side_effect = [self.mock_token1, self.mock_token1]
        parser = Parser(self.mock_lexer)
        
        # Act & Assert - Verifica que tiene todos los métodos necesarios
        self.assertTrue(hasattr(parser, 'getProgram'))
        self.assertTrue(hasattr(parser, 'parse_program'))
        self.assertTrue(hasattr(parser, 'statement_parser'))
        self.assertTrue(hasattr(parser, 'expression_parser'))
        self.assertTrue(hasattr(parser, 'function_parser'))


if __name__ == '__main__':
    unittest.main()