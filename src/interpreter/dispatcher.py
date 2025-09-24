from typing import Optional
import src.astNode as ast
from src.config.environment import Environment
from src.config.object import Object
from .interfaces import IEvaluator
from src.interpreter.eval_expressions import ExpressionEvaluator
from src.interpreter.eval_statements import StatementEvaluator

class Dispatcher(IEvaluator):
    """Punto único de evaluación que coordina statements y expressions."""
    def __init__(self):
        self.expressions = ExpressionEvaluator(self)
        self.statements = StatementEvaluator(self)

    def evaluate(self, node: ast.ASTNode, env: Environment) -> Optional[Object]:
        # Prioridad: statements primero (program, block, let, return, expr stmt)
        result = self.statements.evaluate(node, env)
        if result is not None:
            return result
        # Si no fue una sentencia, tratar como expresión
        return self.expressions.evaluate(node, env)
