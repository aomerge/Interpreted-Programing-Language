from src.ast import Program, LetStatement, ReturnStatement, ExpressionStatement, Identifier, Integer, Prefix, Infix
from src.environment import Environment

class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def interpret(self, program: Program):
        result = None
        for statement in program.statements:
            result = self.evaluate(statement)
        return result

    def evaluate(self, node):
        node_type = type(node).__name__
        method_name = f'eval_{node_type}'
        method = getattr(self, method_name, self.no_method_found)
        return method(node)

    def no_method_found(self, node):
        raise Exception(f'No se encontró un método de evaluación para el nodo: {type(node).__name__}')

    def eval_Program(self, node: Program):
        result = None
        for statement in node.statements:
            result = self.evaluate(statement)
        return result

    def eval_LetStatement(self, node: LetStatement):
        value = self.evaluate(node.value)
        self.environment.set(node.name.value, value)
        return value

    def eval_ReturnStatement(self, node: ReturnStatement):
        return self.evaluate(node.return_value)

    def eval_ExpressionStatement(self, node: ExpressionStatement):
        return self.evaluate(node.expression)

    def eval_Identifier(self, node: Identifier):
        return self.environment.get(node.value)

    def eval_Integer(self, node: Integer):
        return node.value

    def eval_Prefix(self, node: Prefix):
        right = self.evaluate(node.right)
        if node.operator == '-':
            return -right
        elif node.operator == '!':
            return not right
        else:
            raise Exception(f'Operador prefix no soportado: {node.operator}')

    def eval_Infix(self, node: Infix):
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
