"""Tests unitarios para ExpressionEvaluator."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import Optional, List

# Imports del sistema
import src.astNode as ast
from src.config.environment import Environment
from src.config.object import (
    Object, Integer, Boolean, String, Function, Error, Return
)
from src.interpreter.eval_expressions import ExpressionEvaluator
from src.interpreter.interfaces import IEvaluator
from src.interpreter.runtime import RuntimePrimitives
from src.interpreter.errors import UNKNOWN_IDENTIFIER, TYPE_MISMATCH, UNKNOWN_INFIX_OPERATOR


class TestExpressionEvaluator(unittest.TestCase):
    """Test suite para ExpressionEvaluator."""

    def setUp(self):
        """Configurar el entorno de pruebas."""
        self.mock_dispatcher = Mock(spec=IEvaluator)
        self.evaluator = ExpressionEvaluator(self.mock_dispatcher)
        self.environment = Environment()

    def test_evaluate_integer_literal(self):
        """Test evaluación de literales enteros."""
        # Arrange
        node = ast.Integer(token=Mock(), value=42)
        
        # Act
        result = self.evaluator.evaluate(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Integer)
        self.assertEqual(result.value, 42)

    def test_evaluate_string_literal(self):
        """Test evaluación de literales de cadena."""
        # Arrange
        node = ast.StringLiteral(token=Mock(), value="hello")
        
        # Act
        result = self.evaluator.evaluate(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, String)
        self.assertEqual(result.value, "hello")

    def test_evaluate_identifier_found_in_environment(self):
        """Test evaluación de identificador encontrado en el entorno."""
        # Arrange
        self.environment.set("x", Integer(10))
        node = ast.Identifier(token=Mock(), value="x")
        
        # Act
        result = self.evaluator.eval_identifier_expression(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Integer)
        self.assertEqual(result.value, 10)

    @patch('src.interpreter.eval_expressions.BUILTINS', {'len': Mock()})
    def test_evaluate_identifier_found_in_builtins(self):
        """Test evaluación de identificador encontrado en builtins."""
        # Arrange
        builtin_mock = Mock()
        node = ast.Identifier(token=Mock(), value="len")
        
        # Act
        with patch('src.interpreter.eval_expressions.BUILTINS', {'len': builtin_mock}):
            result = self.evaluator.eval_identifier_expression(node, self.environment)
        
        # Assert
        self.assertEqual(result, builtin_mock)

    def test_evaluate_identifier_not_found(self):
        """Test evaluación de identificador no encontrado."""
        # Arrange
        node = ast.Identifier(token=Mock(), value="unknown")
        
        # Act
        result = self.evaluator.eval_identifier_expression(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Error)
        self.assertIn("unknown", result.message)

    def test_evaluate_prefix_expression_bang(self):
        """Test evaluación de expresión prefija con operador '!'."""
        # Arrange
        right_node = Mock()
        node = ast.Prefix(token=Mock(), operator="!", right=right_node)
        self.mock_dispatcher.evaluate.return_value = RuntimePrimitives.TRUE
        
        # Act
        result = self.evaluator.eval_prefix_expression(node, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(right_node, self.environment)
        self.assertIsInstance(result, Boolean)
        self.assertFalse(result.value)

    def test_evaluate_prefix_expression_minus(self):
        """Test evaluación de expresión prefija con operador '-'."""
        # Arrange
        right_node = Mock()
        node = ast.Prefix(token=Mock(), operator="-", right=right_node)
        self.mock_dispatcher.evaluate.return_value = Integer(5)
        
        # Act
        result = self.evaluator.eval_prefix_expression(node, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(right_node, self.environment)
        self.assertIsInstance(result, Integer)
        self.assertEqual(result.value, -5)

    @patch('src.interpreter.eval_expressions.new_error')
    def test_evaluate_prefix_expression_unknown_operator(self, mock_new_error):
        """Test evaluación de expresión prefija con operador desconocido."""
        # Arrange
        right_node = Mock()
        node = ast.Prefix(token=Mock(), operator="~", right=right_node)
        self.mock_dispatcher.evaluate.return_value = Integer(5)
        error_obj = Error("Unknown operator")
        mock_new_error.return_value = error_obj
        
        # Act
        result = self.evaluator.eval_prefix_expression(node, self.environment)
        
        # Assert
        self.assertEqual(result, error_obj)
        mock_new_error.assert_called_once()

    def test_evaluate_infix_expression_integer_addition(self):
        """Test evaluación de expresión infija con suma de enteros."""
        # Arrange
        left_node = Mock()
        right_node = Mock()
        node = ast.Infix(token=Mock(), left=left_node, operator="+", right=right_node)
        self.mock_dispatcher.evaluate.side_effect = [Integer(3), Integer(5)]
        
        # Act
        result = self.evaluator.eval_infix_expression(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Integer)
        self.assertEqual(result.value, 8)

    def test_evaluate_infix_expression_integer_comparison(self):
        """Test evaluación de expresión infija con comparación de enteros."""
        # Arrange
        left_node = Mock()
        right_node = Mock()
        node = ast.Infix(token=Mock(), left=left_node, operator="<", right=right_node)
        self.mock_dispatcher.evaluate.side_effect = [Integer(3), Integer(5)]
        
        # Act
        result = self.evaluator.eval_infix_expression(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Boolean)
        self.assertTrue(result.value)

    def test_evaluate_infix_expression_string_concatenation(self):
        """Test evaluación de expresión infija con concatenación de strings."""
        # Arrange
        left_node = Mock()
        right_node = Mock()
        node = ast.Infix(token=Mock(), left=left_node, operator="+", right=right_node)
        self.mock_dispatcher.evaluate.side_effect = [String("hello"), String(" world")]
        
        # Act
        result = self.evaluator.eval_infix_expression(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, String)
        self.assertEqual(result.value, "hello world")

    def test_evaluate_infix_expression_equality(self):
        """Test evaluación de expresión infija con operador de igualdad."""
        # Arrange
        left_node = Mock()
        right_node = Mock()
        node = ast.Infix(token=Mock(), left=left_node, operator="==", right=right_node)
        int_obj = Integer(5)
        self.mock_dispatcher.evaluate.side_effect = [int_obj, int_obj]
        
        # Act
        result = self.evaluator.eval_infix_expression(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Boolean)
        self.assertTrue(result.value)

    def test_evaluate_infix_expression_inequality(self):
        """Test evaluación de expresión infija con operador de desigualdad."""
        # Arrange
        left_node = Mock()
        right_node = Mock()
        node = ast.Infix(token=Mock(), left=left_node, operator="!=", right=right_node)
        self.mock_dispatcher.evaluate.side_effect = [Integer(3), Integer(5)]
        
        # Act
        result = self.evaluator.eval_infix_expression(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Boolean)
        self.assertTrue(result.value)

    def test_evaluate_infix_expression_type_mismatch(self):
        """Test evaluación de expresión infija con tipos incompatibles."""
        # Arrange
        left_node = Mock()
        right_node = Mock()
        node = ast.Infix(token=Mock(), left=left_node, operator="+", right=right_node)
        self.mock_dispatcher.evaluate.side_effect = [Integer(3), String("hello")]
        
        # Act
        result = self.evaluator.eval_infix_expression(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Error)

    def test_evaluate_infix_expression_unknown_operator(self):
        """Test evaluación de expresión infija con operador desconocido."""
        # Arrange
        left_node = Mock()
        right_node = Mock()
        node = ast.Infix(token=Mock(), left=left_node, operator="&", right=right_node)
        self.mock_dispatcher.evaluate.side_effect = [Integer(3), Integer(5)]
        
        # Act
        result = self.evaluator.eval_infix_expression(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Error)

    def test_evaluate_binary_expression_true_condition(self):
        """Test evaluación de expresión binaria (if) con condición verdadera."""
        # Arrange
        condition_node = Mock()
        consequence_node = Mock()
        alternative_node = Mock()
        node = ast.If(
            token=Mock(),
            condition=condition_node,
            consequence=consequence_node,
            alternative=alternative_node
        )
        expected_result = Integer(42)
        self.mock_dispatcher.evaluate.side_effect = [RuntimePrimitives.TRUE, expected_result]
        
        # Act
        result = self.evaluator.eval_binary_expression(node, self.environment)
        
        # Assert
        self.assertEqual(result, expected_result)
        self.assertEqual(self.mock_dispatcher.evaluate.call_count, 2)

    def test_evaluate_binary_expression_false_condition_with_alternative(self):
        """Test evaluación de expresión binaria (if) con condición falsa y alternativa."""
        # Arrange
        condition_node = Mock()
        consequence_node = Mock()
        alternative_node = Mock()
        node = ast.If(
            token=Mock(),
            condition=condition_node,
            consequence=consequence_node,
            alternative=alternative_node
        )
        expected_result = Integer(0)
        self.mock_dispatcher.evaluate.side_effect = [RuntimePrimitives.FALSE, expected_result]
        
        # Act
        result = self.evaluator.eval_binary_expression(node, self.environment)
        
        # Assert
        self.assertEqual(result, expected_result)

    def test_evaluate_binary_expression_false_condition_no_alternative(self):
        """Test evaluación de expresión binaria (if) con condición falsa sin alternativa."""
        # Arrange
        condition_node = Mock()
        consequence_node = Mock()
        node = ast.If(
            token=Mock(),
            condition=condition_node,
            consequence=consequence_node,
            alternative=None
        )
        self.mock_dispatcher.evaluate.return_value = RuntimePrimitives.FALSE
        
        # Act
        result = self.evaluator.eval_binary_expression(node, self.environment)
        
        # Assert
        self.assertEqual(result, RuntimePrimitives.NULL)

    def test_evaluate_function_literal(self):
        """Test evaluación de literal de función."""
        # Arrange
        parameters = [Mock()]
        body = Mock()
        node = ast.Function(token=Mock(), parameters=parameters, body=body)
        
        # Act
        result = self.evaluator.evaluate(node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Function)
        self.assertEqual(result.parameters, parameters)
        self.assertEqual(result.body, body)
        self.assertEqual(result.env, self.environment)

    @patch('src.interpreter.eval_expressions.FunctionsOperations')
    def test_evaluate_call_expression_success(self, mock_functions_ops):
        """Test evaluación exitosa de llamada a función."""
        # Arrange
        function_node = Mock()
        arg1_node = Mock()
        arg2_node = Mock()
        node = ast.Call(
            token=Mock(),
            function=function_node,
            arguments=[arg1_node, arg2_node]
        )
        
        function_obj = Mock()
        arg1_obj = Integer(1)
        arg2_obj = Integer(2)
        block_result = Mock()
        extended_env = Mock()
        final_result = Integer(3)
        
        self.mock_dispatcher.evaluate.side_effect = [
            function_obj,      # función
            arg1_obj,         # argumento 1
            arg2_obj,         # argumento 2
            Return(final_result)  # resultado de evaluación del bloque
        ]
        
        mock_functions_ops.apply_function.return_value = (block_result, extended_env)
        mock_functions_ops.unwrap_return_value.return_value = final_result
        
        # Act
        result = self.evaluator.eval_call_expression(node, self.environment)
        
        # Assert
        mock_functions_ops.apply_function.assert_called_once_with(
            function_obj, [arg1_obj, arg2_obj]
        )
        mock_functions_ops.unwrap_return_value.assert_called_once()
        self.assertEqual(result, final_result)

    @patch('src.interpreter.eval_expressions.FunctionsOperations')
    def test_evaluate_call_expression_function_error(self, mock_functions_ops):
        """Test evaluación de llamada a función con error en la función."""
        # Arrange
        function_node = Mock()
        node = ast.Call(
            token=Mock(),
            function=function_node,
            arguments=[]
        )
        
        function_obj = Mock()
        error_obj = Error("Function error")
        
        self.mock_dispatcher.evaluate.return_value = function_obj
        mock_functions_ops.apply_function.return_value = error_obj
        
        # Act
        result = self.evaluator.eval_call_expression(node, self.environment)
        
        # Assert
        self.assertEqual(result, error_obj)

    def test_evaluate_block_expression(self):
        """Test evaluación de expresión de bloque."""
        # Arrange
        block_node = ast.Block(token=Mock(), statements=[])
        expected_result = Integer(42)
        self.mock_dispatcher.statements = Mock()
        self.mock_dispatcher.statements.evaluate.return_value = expected_result
        
        # Act
        result = self.evaluator.evaluate(block_node, self.environment)
        
        # Assert
        self.mock_dispatcher.statements.evaluate.assert_called_once_with(block_node, self.environment)
        self.assertEqual(result, expected_result)

    def test_evaluate_unknown_node_type(self):
        """Test evaluación de tipo de nodo desconocido."""
        # Arrange
        unknown_node = Mock()
        unknown_node.__class__ = type('UnknownNode', (), {})
        
        # Act
        result = self.evaluator.evaluate(unknown_node, self.environment)
        
        # Assert
        self.assertIsNone(result)

    def test_evaluate_with_dispatcher_delegation(self):
        """Test que la evaluación delega correctamente al dispatcher."""
        # Arrange
        node = ast.Prefix(token=Mock(), operator="!", right=Mock())
        self.mock_dispatcher.evaluate.return_value = RuntimePrimitives.TRUE
        
        # Act
        self.evaluator.eval_prefix_expression(node, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once()

    def test_integration_complex_expression(self):
        """Test de integración para expresión compleja."""
        # Arrange
        # Simular: !(5 > 3)
        right_infix = ast.Infix(
            token=Mock(),
            left=Mock(),
            operator=">",
            right=Mock()
        )
        prefix_node = ast.Prefix(
            token=Mock(),
            operator="!",
            right=right_infix
        )
        
        # Mock del dispatcher para devolver los valores correctos
        def side_effect(node, env):
            if isinstance(node, ast.Infix):
                return RuntimePrimitives.TRUE  # 5 > 3 es verdadero
            return RuntimePrimitives.TRUE
        
        self.mock_dispatcher.evaluate.side_effect = side_effect
        
        # Act
        result = self.evaluator.eval_prefix_expression(prefix_node, self.environment)
        
        # Assert
        self.assertIsInstance(result, Boolean)
        self.assertFalse(result.value)  # !(true) = false


if __name__ == '__main__':
    unittest.main()