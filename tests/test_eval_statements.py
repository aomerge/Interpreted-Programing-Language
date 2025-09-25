"""Tests unitarios para StatementEvaluator."""

import unittest
from unittest.mock import Mock, patch
from typing import Optional, List

# Imports del sistema
import src.astNode as ast
from src.config.environment import Environment
from src.config.object import (
    Object, Integer, Boolean, String, Error, Return
)
from src.interpreter.eval_statements import StatementEvaluator
from src.interpreter.interfaces import IEvaluator


class TestStatementEvaluator(unittest.TestCase):
    """Test suite para StatementEvaluator."""

    def setUp(self):
        """Configurar el entorno de pruebas."""
        self.mock_dispatcher = Mock(spec=IEvaluator)
        self.evaluator = StatementEvaluator(self.mock_dispatcher)
        self.environment = Environment()

    def test_evaluate_program_single_statement(self):
        """Test evaluación de programa con una sola declaración."""
        # Arrange
        statement1 = Mock()
        program_node = ast.Program(statements=[statement1])
        expected_result = Integer(42)
        self.mock_dispatcher.evaluate.return_value = expected_result
        
        # Act
        result = self.evaluator.eval_program_expression(program_node, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(statement1, self.environment)
        self.assertEqual(result, expected_result)

    def test_evaluate_program_multiple_statements(self):
        """Test evaluación de programa con múltiples declaraciones."""
        # Arrange
        statement1 = Mock()
        statement2 = Mock()
        statement3 = Mock()
        program_node = ast.Program(statements=[statement1, statement2, statement3])
        
        results = [Integer(1), Integer(2), Integer(3)]
        self.mock_dispatcher.evaluate.side_effect = results
        
        # Act
        result = self.evaluator.eval_program_expression(program_node, self.environment)
        
        # Assert
        self.assertEqual(self.mock_dispatcher.evaluate.call_count, 3)
        self.assertEqual(result.value, 3)  # Comparar valor en lugar de instancia

    def test_evaluate_program_with_return_statement(self):
        """Test evaluación de programa que contiene return."""
        # Arrange
        statement1 = Mock()
        statement2 = Mock()  # Este no debería ejecutarse
        program_node = ast.Program(statements=[statement1, statement2])
        
        return_obj = Return(Integer(99))
        self.mock_dispatcher.evaluate.side_effect = [return_obj, Integer(2)]
        
        # Act
        result = self.evaluator.eval_program_expression(program_node, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(statement1, self.environment)
        self.assertEqual(result.value, 99)  # Comparar valor en lugar de instancia

    def test_evaluate_program_with_error(self):
        """Test evaluación de programa que contiene error."""
        # Arrange
        statement1 = Mock()
        statement2 = Mock()  # Este no debería ejecutarse
        program_node = ast.Program(statements=[statement1, statement2])
        
        error_obj = Error("Test error")
        self.mock_dispatcher.evaluate.side_effect = [error_obj, Integer(2)]
        
        # Act
        result = self.evaluator.eval_program_expression(program_node, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(statement1, self.environment)
        self.assertEqual(result, error_obj)

    def test_evaluate_program_empty(self):
        """Test evaluación de programa vacío."""
        # Arrange
        program_node = ast.Program(statements=[])
        
        # Act
        result = self.evaluator.eval_program_expression(program_node, self.environment)
        
        # Assert
        self.assertIsNone(result)
        self.mock_dispatcher.evaluate.assert_not_called()

    def test_evaluate_block_single_statement(self):
        """Test evaluación de bloque con una sola declaración."""
        # Arrange
        statement1 = Mock()
        block_node = ast.Block(token=Mock(), statements=[statement1])
        expected_result = Integer(42)
        self.mock_dispatcher.evaluate.return_value = expected_result
        
        # Act
        result = self.evaluator.eval_block_expression(block_node, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(statement1, self.environment)
        self.assertEqual(result, expected_result)

    def test_evaluate_block_multiple_statements(self):
        """Test evaluación de bloque con múltiples declaraciones."""
        # Arrange
        statement1 = Mock()
        statement2 = Mock()
        statement3 = Mock()
        block_node = ast.Block(token=Mock(), statements=[statement1, statement2, statement3])
        
        results = [Integer(1), Integer(2), Integer(3)]
        self.mock_dispatcher.evaluate.side_effect = results
        
        # Act
        result = self.evaluator.eval_block_expression(block_node, self.environment)
        
        # Assert
        self.assertEqual(self.mock_dispatcher.evaluate.call_count, 3)
        self.assertEqual(result.value, 3)  # Comparar valor

    def test_evaluate_block_with_return_statement(self):
        """Test evaluación de bloque que contiene return."""
        # Arrange
        statement1 = Mock()
        statement2 = Mock()  # Este no debería ejecutarse debido al early return
        block_node = ast.Block(token=Mock(), statements=[statement1, statement2])
        
        return_obj = Return(Integer(99))
        # Configurar el mock para que type() retorne un objeto con name="RETURN"
        type_mock = Mock()
        type_mock.name = "RETURN"
        return_obj.type = Mock(return_value=type_mock)
        
        # Solo el primer statement debería ejecutarse
        self.mock_dispatcher.evaluate.return_value = return_obj
        
        # Act
        result = self.evaluator.eval_block_expression(block_node, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(statement1, self.environment)
        self.assertEqual(result, return_obj)

    def test_evaluate_block_with_error(self):
        """Test evaluación de bloque que contiene error."""
        # Arrange
        statement1 = Mock()
        statement2 = Mock()  # Este no debería ejecutarse debido al early return
        block_node = ast.Block(token=Mock(), statements=[statement1, statement2])
        
        error_obj = Error("Test error")
        # Configurar el mock para que type() retorne un objeto con name="ERROR"
        type_mock = Mock()
        type_mock.name = "ERROR"
        error_obj.type = Mock(return_value=type_mock)
        
        # Solo el primer statement debería ejecutarse
        self.mock_dispatcher.evaluate.return_value = error_obj
        
        # Act
        result = self.evaluator.eval_block_expression(block_node, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(statement1, self.environment)
        self.assertEqual(result, error_obj)

    def test_evaluate_block_empty(self):
        """Test evaluación de bloque vacío."""
        # Arrange
        block_node = ast.Block(token=Mock(), statements=[])
        
        # Act
        result = self.evaluator.eval_block_expression(block_node, self.environment)
        
        # Assert
        self.assertIsNone(result)
        self.mock_dispatcher.evaluate.assert_not_called()

    def test_evaluate_expression_statement(self):
        """Test evaluación de declaración de expresión."""
        # Arrange
        expression = Mock()
        expression_statement = ast.ExpressionStatement(token=Mock(), expression=expression)
        expected_result = Integer(42)
        self.mock_dispatcher.evaluate.return_value = expected_result
        
        # Act
        result = self.evaluator.evaluate(expression_statement, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(expression, self.environment)
        self.assertEqual(result, expected_result)

    def test_evaluate_return_statement(self):
        """Test evaluación de declaración return."""
        # Arrange
        return_value = Mock()
        return_statement = ast.ReturnStatement(token=Mock(), return_value=return_value)
        expected_value = Integer(99)
        self.mock_dispatcher.evaluate.return_value = expected_value
        
        # Act
        result = self.evaluator.evaluate(return_statement, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(return_value, self.environment)
        self.assertIsInstance(result, Return)
        self.assertEqual(result.value, expected_value)

    def test_evaluate_return_statement_with_none_value(self):
        """Test evaluación de declaración return con valor None."""
        # Arrange
        return_value = Mock()
        return_statement = ast.ReturnStatement(token=Mock(), return_value=return_value)
        self.mock_dispatcher.evaluate.return_value = None
        
        # Act
        result = self.evaluator.evaluate(return_statement, self.environment)
        
        # Assert
        self.assertIsInstance(result, Return)
        self.assertIsNone(result.value)

    def test_evaluate_let_statement(self):
        """Test evaluación de declaración let."""
        # Arrange
        name = ast.Identifier(token=Mock(), value="x")
        value_expr = Mock()
        let_statement = ast.LetStatement(token=Mock(), name=name, value=value_expr)
        expected_value = Integer(42)
        self.mock_dispatcher.evaluate.return_value = expected_value
        
        # Act
        result = self.evaluator.evaluate(let_statement, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(value_expr, self.environment)
        self.assertEqual(result, expected_value)
        # Verificar que se estableció en el entorno
        self.assertEqual(self.environment.get("x"), expected_value)

    def test_evaluate_let_statement_overwrites_existing(self):
        """Test que let statement sobreescribe variables existentes."""
        # Arrange
        self.environment.set("x", Integer(1))  # Valor inicial
        name = ast.Identifier(token=Mock(), value="x")
        value_expr = Mock()
        let_statement = ast.LetStatement(token=Mock(), name=name, value=value_expr)
        new_value = Integer(42)
        self.mock_dispatcher.evaluate.return_value = new_value
        
        # Act
        result = self.evaluator.evaluate(let_statement, self.environment)
        
        # Assert
        self.assertEqual(result, new_value)
        self.assertEqual(self.environment.get("x"), new_value)

    def test_evaluate_program_node_through_evaluate(self):
        """Test evaluación de programa a través del método evaluate principal."""
        # Arrange
        statement1 = Mock()
        program_node = ast.Program(statements=[statement1])
        expected_result = Integer(42)
        self.mock_dispatcher.evaluate.return_value = expected_result
        
        # Act
        result = self.evaluator.evaluate(program_node, self.environment)
        
        # Assert
        self.assertEqual(result, expected_result)

    def test_evaluate_block_node_through_evaluate(self):
        """Test evaluación de bloque a través del método evaluate principal."""
        # Arrange
        statement1 = Mock()
        block_node = ast.Block(token=Mock(), statements=[statement1])
        expected_result = Integer(42)
        self.mock_dispatcher.evaluate.return_value = expected_result
        
        # Act
        result = self.evaluator.evaluate(block_node, self.environment)
        
        # Assert
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
        expression = Mock()
        expression_statement = ast.ExpressionStatement(token=Mock(), expression=expression)
        expected_result = String("test")
        self.mock_dispatcher.evaluate.return_value = expected_result
        
        # Act
        result = self.evaluator.evaluate(expression_statement, self.environment)
        
        # Assert
        self.mock_dispatcher.evaluate.assert_called_once_with(expression, self.environment)
        self.assertEqual(result, expected_result)

    def test_return_statement_node_attribute_updated(self):
        """Test que return_statement_node se actualiza correctamente."""
        # Arrange
        return_value = Mock()
        return_statement = ast.ReturnStatement(token=Mock(), return_value=return_value)
        self.mock_dispatcher.evaluate.return_value = Integer(42)
        
        # Act
        self.evaluator.evaluate(return_statement, self.environment)
        
        # Assert
        self.assertEqual(self.evaluator.return_statement_node, return_statement)

    def test_let_statement_node_attribute_updated(self):
        """Test que return_statement_node se actualiza correctamente para let."""
        # Arrange
        name = ast.Identifier(token=Mock(), value="y")
        value_expr = Mock()
        let_statement = ast.LetStatement(token=Mock(), name=name, value=value_expr)
        self.mock_dispatcher.evaluate.return_value = Integer(42)
        
        # Act
        self.evaluator.evaluate(let_statement, self.environment)
        
        # Assert
        self.assertEqual(self.evaluator.return_statement_node, let_statement)

    def test_integration_program_with_mixed_statements(self):
        """Test de integración con programa que tiene diferentes tipos de declaraciones."""
        # Arrange
        let_stmt = Mock()
        expr_stmt = Mock()
        return_stmt = Mock()
        program_node = ast.Program(statements=[let_stmt, expr_stmt, return_stmt])
        
        return_obj = Return(String("final"))
        self.mock_dispatcher.evaluate.side_effect = [
            Integer(1),    # let statement
            Integer(2),    # expression statement  
            return_obj     # return statement
        ]
        
        # Act
        result = self.evaluator.eval_program_expression(program_node, self.environment)
        
        # Assert
        self.assertEqual(self.mock_dispatcher.evaluate.call_count, 3)
        self.assertEqual(result.value, "final")  # Comparar valor

    def test_integration_nested_blocks(self):
        """Test de integración con bloques anidados."""
        # Arrange
        inner_stmt = Mock()
        inner_block = ast.Block(token=Mock(), statements=[inner_stmt])
        outer_stmt = Mock()
        outer_block = ast.Block(token=Mock(), statements=[outer_stmt, inner_block])
        
        self.mock_dispatcher.evaluate.side_effect = [
            Integer(1),    # outer statement
            Integer(2)     # inner block result
        ]
        
        # Act
        result = self.evaluator.eval_block_expression(outer_block, self.environment)
        
        # Assert
        self.assertEqual(result.value, 2)  # Comparar valor


if __name__ == '__main__':
    unittest.main()