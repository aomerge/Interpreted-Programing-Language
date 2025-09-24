# src/interpreter/interfaces.py
from typing import Optional, Protocol
import src.ast as ast
from src.environment import Environment
from src.object import Object

class IEvaluator(Protocol):
    def evaluate(self, node: ast.ASTNode, env: Environment) -> Optional[Object]: ...
