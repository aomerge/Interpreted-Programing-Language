from typing import Optional
import src.astNode as ast
from src.config.environment import Environment
from src.config.object import Object
from .dispatcher import Dispatcher

class Interpreter:
    """
    Punto de entrada externo conservando la API original:
    - interpret(program: ast.Program) -> Optional[Object]
    """
    def __init__(self):
        self._dispatcher = Dispatcher()

    def interpret(self, program: ast.Program) -> Optional[Object]:
        env = Environment()
        return self._dispatcher.evaluate(program, env)
