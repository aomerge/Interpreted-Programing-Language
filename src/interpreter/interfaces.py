# src/interpreter/interfaces.py
from typing import Optional, Protocol
import src.astNode as ast
from src.config.environment import Environment
from src.config.object import Object

class IEvaluator(Protocol):
    def evaluate(self, node: ast.ASTNode, env: Environment) -> Optional[Object]: ...
