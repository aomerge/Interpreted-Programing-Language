"""Tests for Dispatcher class."""

import unittest
from unittest.mock import Mock, patch
import src.astNode as ast
from src.config.environment import Environment
from src.config.object import Object, Integer
from src.interpreter.dispatcher import Dispatcher


class TestDispatcher(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('src.interpreter.dispatcher.StatementEvaluator') as mock_stmt, \
             patch('src.interpreter.dispatcher.ExpressionEvaluator') as mock_expr:
            
            self.dispatcher = Dispatcher()
            self.env = Environment()
            
            # Get the mock instances
            self.mock_statements = mock_stmt.return_value
            self.mock_expressions = mock_expr.return_value
            
            # Replace the actual evaluators with mocks
            self.dispatcher.statements = self.mock_statements
            self.dispatcher.expressions = self.mock_expressions
    
    @patch('src.interpreter.dispatcher.StatementEvaluator')
    @patch('src.interpreter.dispatcher.ExpressionEvaluator')
    def test_init(self, mock_expr_eval, mock_stmt_eval):
        """Test Dispatcher initialization."""
        dispatcher = Dispatcher()
        
        # Verify evaluators are created with dispatcher as parameter
        mock_expr_eval.assert_called_once_with(dispatcher)
        mock_stmt_eval.assert_called_once_with(dispatcher)
        
        self.assertEqual(dispatcher.expressions, mock_expr_eval.return_value)
        self.assertEqual(dispatcher.statements, mock_stmt_eval.return_value)
    
    def test_evaluate_statement_success(self):
        """Test evaluation when statement evaluator succeeds."""
        node = Mock(spec=ast.ASTNode)
        expected_result = Integer(42)
        
        # Mock statement evaluator to return a result
        self.mock_statements.evaluate.return_value = expected_result
        
        result = self.dispatcher.evaluate(node, self.env)
        
        self.assertEqual(result, expected_result)
        self.mock_statements.evaluate.assert_called_once_with(node, self.env)
        # Expression evaluator should not be called
        self.mock_expressions.evaluate.assert_not_called()
    
    def test_evaluate_expression_fallback(self):
        """Test evaluation falls back to expression evaluator."""
        node = Mock(spec=ast.ASTNode)
        expected_result = Integer(42)
        
        # Mock statement evaluator to return None
        self.mock_statements.evaluate.return_value = None
        # Mock expression evaluator to return a result
        self.mock_expressions.evaluate.return_value = expected_result
        
        result = self.dispatcher.evaluate(node, self.env)
        
        self.assertEqual(result, expected_result)
        self.mock_statements.evaluate.assert_called_once_with(node, self.env)
        self.mock_expressions.evaluate.assert_called_once_with(node, self.env)
    
    def test_evaluate_both_return_none(self):
        """Test evaluation when both evaluators return None."""
        node = Mock(spec=ast.ASTNode)
        
        # Mock both evaluators to return None
        self.mock_statements.evaluate.return_value = None
        self.mock_expressions.evaluate.return_value = None
        
        result = self.dispatcher.evaluate(node, self.env)
        
        self.assertIsNone(result)
        self.mock_statements.evaluate.assert_called_once_with(node, self.env)
        self.mock_expressions.evaluate.assert_called_once_with(node, self.env)
    
    def test_evaluate_with_different_node_types(self):
        """Test evaluation with different AST node types."""
        # Test with Program node (should be handled by statement evaluator)
        program_node = Mock(spec=ast.Program)
        result_obj = Integer(10)
        self.mock_statements.evaluate.return_value = result_obj
        
        result = self.dispatcher.evaluate(program_node, self.env)
        
        self.assertEqual(result, result_obj)
        self.mock_statements.evaluate.assert_called_with(program_node, self.env)
    
    def test_evaluate_with_expression_node(self):
        """Test evaluation with expression node."""
        # Test with Integer node (should fall back to expression evaluator)
        int_node = Mock(spec=ast.Integer)
        result_obj = Integer(5)
        
        self.mock_statements.evaluate.return_value = None
        self.mock_expressions.evaluate.return_value = result_obj
        
        result = self.dispatcher.evaluate(int_node, self.env)
        
        self.assertEqual(result, result_obj)
        self.mock_expressions.evaluate.assert_called_with(int_node, self.env)
    
    def test_evaluate_priority_statements_first(self):
        """Test that statements have priority over expressions."""
        node = Mock(spec=ast.ASTNode)
        stmt_result = Integer(100)
        expr_result = Integer(200)
        
        # Both evaluators return results
        self.mock_statements.evaluate.return_value = stmt_result
        self.mock_expressions.evaluate.return_value = expr_result
        
        result = self.dispatcher.evaluate(node, self.env)
        
        # Should return statement result, not expression result
        self.assertEqual(result, stmt_result)
        self.mock_statements.evaluate.assert_called_once_with(node, self.env)
        # Expression evaluator should not be called since statement succeeded
        self.mock_expressions.evaluate.assert_not_called()
    
    def test_evaluate_with_environment_passed_through(self):
        """Test that environment is properly passed to evaluators."""
        node = Mock(spec=ast.ASTNode)
        custom_env = Environment()
        result_obj = Integer(7)
        
        self.mock_statements.evaluate.return_value = None
        self.mock_expressions.evaluate.return_value = result_obj
        
        result = self.dispatcher.evaluate(node, custom_env)
        
        self.assertEqual(result, result_obj)
        self.mock_statements.evaluate.assert_called_once_with(node, custom_env)
        self.mock_expressions.evaluate.assert_called_once_with(node, custom_env)
    
    def test_multiple_evaluations(self):
        """Test multiple evaluations work correctly."""
        node1 = Mock(spec=ast.ASTNode)
        node2 = Mock(spec=ast.ASTNode)
        result1 = Integer(1)
        result2 = Integer(2)
        
        # First evaluation: statement succeeds
        self.mock_statements.evaluate.return_value = result1
        result = self.dispatcher.evaluate(node1, self.env)
        self.assertEqual(result, result1)
        
        # Reset for second evaluation
        self.mock_statements.evaluate.return_value = None
        self.mock_expressions.evaluate.return_value = result2
        
        # Second evaluation: expression succeeds
        result = self.dispatcher.evaluate(node2, self.env)
        self.assertEqual(result, result2)
        
        # Verify call counts
        self.assertEqual(self.mock_statements.evaluate.call_count, 2)
        self.assertEqual(self.mock_expressions.evaluate.call_count, 1)


if __name__ == '__main__':
    unittest.main()