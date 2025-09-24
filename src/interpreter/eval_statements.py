from __future__ import annotations
from typing import Optional, cast, Type
import src.ast as ast
from src.confg.environment import Environment
from src.confg.object import Object, Error, Return
from .interfaces import IEvaluator

class StatementEvaluator:
    """Evalúa sentencias, bloques y programa."""
    def __init__(self, dispatcher: IEvaluator):
        self.dispatcher = dispatcher

    return_statement_node: cast = None

    def evaluate(self, node: ast.ASTNode, environment: Environment) -> Optional[Object]:
        node_type: Type = type(node)
        match node_type:
            case ast.Program:
                return self.eval_ProgramExpression(node, environment)
            case ast.Block:
                return self.eval_BlockExpression(node, environment)

            case ast.ExpressionStatement:
                expression_statement_node = cast(ast.ExpressionStatement, node)
                return self.dispatcher.evaluate(expression_statement_node.expression, environment)

            case ast.ReturnStatement:
                self.return_statement_node = cast(ast.ReturnStatement, node)
                return_value = self.dispatcher.evaluate(self.return_statement_node.return_value, environment)
                return Return(return_value)

            case ast.LetStatement:
                self.return_statement_node = cast(ast.LetStatement, node)
                value = self.dispatcher.evaluate(self.return_statement_node.value, environment)
                environment.set(self.return_statement_node.name.value, value)
                return value

    def eval_ProgramExpression(self, node: ast.Program, environment: Environment) -> Optional[Object]:
        program_node = cast(ast.Program, node)
        result: Optional[Object] = None
        for statement in program_node.statements:
            result = self.dispatcher.evaluate(statement, environment)
            if isinstance(result, Return):
                return cast(Return, result).value
            if isinstance(result, Error):
                return result
        return result

    def eval_BlockExpression(self, node: ast.Block, environment: Environment) -> Optional[Object]:
        block_node = cast(ast.Block, node)
        result: Optional[Object] = None
        for statement in block_node.statements:
            result = self.dispatcher.evaluate(statement, environment)
            if result is not None and (result.type().name in ("RETURN", "ERROR")):
                return result
        return result        
