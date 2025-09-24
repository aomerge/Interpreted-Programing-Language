from __future__ import annotations
from typing import Optional, List, cast, Type
from unittest import case
import src.astNode as ast
from src.config.environment import Environment
from src.config.object import Object, Error, Return, Function, String, Integer
from .runtime import RuntimePrimitives, InfixOperations, PrefixOperations, FunctionsOperations
from .errors import (
    TYPE_MISMATCH, UNKNOWN_INFIX_OPERATOR, UNKNOWN_IDENTIFIER, new_error
)
from .interfaces import IEvaluator

import importlib

try:
    builtins_module = importlib.import_module("src.builtins")
    BUILTINS = getattr(builtins_module, "BUILTINS", {})
except ModuleNotFoundError:
    BUILTINS = {}

class ExpressionEvaluator:
    """Evalúa expresiones (no programa/sentencias)."""
    def __init__(self, dispatcher: IEvaluator):
        self.dispatcher = dispatcher  # acceso a evaluación genérica

    def evaluate(self, node: ast.ASTNode, environment: Environment) -> Optional[Object]:
        node_type: Type = type(node)

        match node_type:
            case ast.Integer:
                integer_node = cast(ast.Integer, node)
                return Integer(integer_node.value)
            case ast.StringLiteral:
                string_node = cast(ast.StringLiteral, node)
                return String(string_node.value)
            case ast.Identifier:
                return self.eval_IdentifierExpression(node, environment)
            case ast.Prefix:
                return self.eval_PrefixExpression(node, environment)
            case ast.Infix:
                return self.eval_InfixExpression(node, environment)
            case ast.If:
                return self.eval_BinaryExpression(node, environment)
            case ast.Function:
                function_node = cast(ast.Function, node)                
                return Function(function_node.parameters, function_node.body, environment)
            case ast.Call:
                return self.eval_CallExpression(node, environment)
            case ast.Block:
                return self.dispatcher.statements.evaluate(node, environment)
            case _:
                return None

    def eval_IdentifierExpression(self, node: ast.Identifier, environment: Environment) -> Optional[Object]:
        identifier_node = cast(ast.Identifier, node)
        value = environment.get(identifier_node.value)
        if value is not None:
            return value
        return BUILTINS.get(identifier_node.value, new_error(UNKNOWN_IDENTIFIER, [identifier_node.value]))

    def eval_PrefixExpression(self, node: ast.Prefix, environment: Environment) -> Optional[Object]:
        prefix_node = cast(ast.Prefix, node)
        right_value = self.dispatcher.evaluate(prefix_node.right, environment)
        assert right_value is not None
        if prefix_node.operator == '!':
            return PrefixOperations.bang(right_value)
        if prefix_node.operator == '-':
            return PrefixOperations.minus(right_value)
        return new_error(UNKNOWN_INFIX_OPERATOR, [prefix_node.operator, right_value.type().name])

    def eval_InfixExpression(self, node: ast.Infix, environment: Environment) -> Optional[Object]:
        infix_node = cast(ast.Infix, node)
        left_value = self.dispatcher.evaluate(infix_node.left, environment)
        right_value = self.dispatcher.evaluate(infix_node.right, environment)
        assert left_value is not None and right_value is not None

        if left_value.type().name == "INTEGER" and right_value.type().name == "INTEGER":
            return InfixOperations.integer_infix(infix_node.operator, left_value, right_value)
        
        if left_value.type().name == "STRING" and right_value.type().name == "STRING":
            return InfixOperations.string_infix(infix_node.operator, left_value, right_value)

        if infix_node.operator == '==':
            return RuntimePrimitives.to_boolean_object(left_value is right_value)
        if infix_node.operator == '!=':
            return RuntimePrimitives.to_boolean_object(left_value is not right_value)
        if left_value.type() != right_value.type():
            return new_error(TYPE_MISMATCH, [left_value.type().name, infix_node.operator, right_value.type().name])

        return new_error(UNKNOWN_INFIX_OPERATOR, [left_value.type().name, infix_node.operator, right_value.type().name])

    def eval_BinaryExpression(self, node: ast.BinaryExpression, environment: Environment) -> Optional[Object]:
        if_node = cast(ast.If, node)
        condition_value = self.dispatcher.evaluate(if_node.condition, environment)
        assert condition_value is not None
        if RuntimePrimitives.is_truthy(condition_value):
            return self.dispatcher.evaluate(if_node.consequence, environment)
        if if_node.alternative is not None:
            return self.dispatcher.evaluate(if_node.alternative, environment)
        return RuntimePrimitives.NULL

    def eval_CallExpression(self, node: ast.CallExpression, environment: Environment) -> Optional[Object]:
        call_node = cast(ast.Call, node)
        function_object = self.dispatcher.evaluate(call_node.function, environment)
        arguments = [self.dispatcher.evaluate(argument, environment) for argument in call_node.arguments]
        assert function_object is not None and all(argument is not None for argument in arguments)                
        apply_result = FunctionsOperations.apply_function(function_object, cast(List[Object], arguments))  # type: ignore
        if isinstance(apply_result, Object):  # Error
            return apply_result
        block_node, extended_environment = apply_result
        result = self.dispatcher.evaluate(block_node, extended_environment)
        assert result is not None
        return FunctionsOperations.unwrap_return_value(result)
