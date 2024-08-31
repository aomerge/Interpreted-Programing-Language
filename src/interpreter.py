import src.ast as ast
from src.environment import Environment
from typing import (
    Any,
    cast,
    List,
    Optional,
    Type
)

from src.object import(
    Boolean,
    Null,
    Object,
    Integer
)

class Interpreter:

    TRUE = Boolean(True)
    FALSE = Boolean(False)
    NULL = Null()

    _NOT_A_FUNCTION = 'No es una funcion: {}'
    _TYPE_MISMATCH = 'Discrepancia de tipos: {} {} {}'
    _UNKNOWN_PREFIX_OPERATOR = 'Operador desconocido: {}{}'
    _UNKNOWN_INFIX_OPERATOR = 'Operador desconocido: {} {} {}'
    _UNKNOWN_IDENTIFIER = 'Identificador no encontrado: {}'

    def __init__(self):
        self.environment = Environment()

    def interpret(self, program: ast.Program)->Optional[Object]:
        env = self.environment
        return self._eval_Program(program, env)

    def _evaluate(self, node: ast.ASTNode , env: Environment)->Optional[Object]:
        node_type: Type = type(node).__name__
        
        if node_type == ast.Program.__name__:
            return self._eval_Program(cast(ast.Program, node), self.environment)
        elif node_type == ast.ExpressionStatement.__name__:
            node = cast(ast.ExpressionStatement, node)
            assert node.expression is not None
            return self._evaluate(node.expression, env)
        elif node_type == ast.Integer.__name__:
            node = cast(ast.Integer, node)
            assert node.value is not None
            return Integer(node.value)
        elif node_type == ast.Boolean.__name__:
            node = cast(ast.Boolean, node)
            assert node.value is not None
            return self.TRUE if node.value else self.FALSE
        elif node_type == ast.Prefix.__name__:
            node = cast(ast.Prefix, node)
            assert node.right is not None
            right = self._evaluate(node.right, env)
            if type(right).__name__ == 'Error':
                return right
            return self._eval_PrefixExpression(node.operator, right)

    def no_method_found(self, node):
        return Exception(f'No se encontró un método de evaluación para el nodo: {type(node).__name__}')

    def _eval_Program(self, node: ast.Program, env: Environment)->Optional[Object]:
        result: Optional[Object] = None

        for statement in node.statements:
            result = self._evaluate(statement, env)
            if type(result).__name__ == 'Return':
                return result.value
            if type(result).__name__ == 'Error':
                return result            
        return result

    def eval_LetStatement(self, node: ast.LetStatement):
        value = self.evaluate(node.value)
        self.environment.set(node.name.value, value)
        return value

    def eval_ReturnStatement(self, node: ast.ReturnStatement):
        return self.evaluate(node.return_value)    

    def eval_Identifier(self, node: ast.Identifier):
        return self.environment.get(node.value)

    def eval_Integer(self, node: ast.Integer):
        return node.value

    def _eval_PrefixExpression(self, node: ast.Prefix):
        right = self.evaluate(node.right)
        if node.operator == '-':
            return -right
        elif node.operator == '!':
            return not right
        else:
            raise Exception(f'Operador prefix no soportado: {node.operator}')

    def eval_Infix(self, node: ast.Infix):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.operator == '+':
            return left + right
        elif node.operator == '-':
            return left - right
        elif node.operator == '*':
            return left * right
        elif node.operator == '/':
            if right == 0:
                raise ZeroDivisionError('División por cero no permitida.')
            return left / right
        elif node.operator == '==':
            return left == right
        elif node.operator == '!=':
            return left != right
        elif node.operator == '<':
            return left < right
        elif node.operator == '>':
            return left > right
        else:
            raise Exception(f'Operador infix no soportado: {node.operator}')
