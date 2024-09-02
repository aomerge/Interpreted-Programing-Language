import src.ast as ast
from src.environment import Environment
from typing import (
    Any,
    cast,
    List,
    Optional,
    Type,
)

from src.object import(
    Boolean,
    Null,
    Object,
    Integer,
    Return,
    Function,
    String,
    ObjectType,
    Error
)


class Interpreter:
    
    logger: List[Object] = []

    TRUE = Boolean(True)
    FALSE = Boolean(False)
    NULL = Null()

    _NOT_A_FUNCTION = 'No es una funcion: {}'
    _TYPE_MISMATCH = 'Discrepancia de tipos: {} {} {}'
    _UNKNOWN_PREFIX_OPERATOR = 'Operador desconocido: {}{}'
    _UNKNOWN_INFIX_OPERATOR = 'Operador desconocido: {} {} {}'
    _UNKNOWN_IDENTIFIER = 'Identificador no encontrado: {}'

    def interpret(self, program: ast.Program) -> Optional[Object]:
        env = Environment()
        return self._evaluate_program(program, env)

    def _evaluate(self, node: ast.ASTNode, env: Environment) -> Optional[Object]:
        node_type: Type = type(node)
        print("s",node_type)        

        if node_type == ast.Program:
            node = cast(ast.Program, node)
            return self._evaluate_program(node, env)
        
        elif node_type == ast.ExpressionStatement:
            node = cast(ast.ExpressionStatement, node)
            assert node.expression is not None
            return self._evaluate(node.expression, env)
        
        elif node_type == ast.Integer:
            node = cast(ast.Integer, node)
            assert node.value is not None
            return Integer(node.value)
        
        elif node_type == ast.Boolean:
            node = cast(ast.Boolean, node)
            assert node.value is not None
            return self._to_boolean_object(node.value)
        
        elif node_type == ast.Prefix:
            node = cast(ast.Prefix, node)
            assert node.right is not None
            right = self._evaluate(node.right, env)
            assert right is not None
            return self._evaluate_prefix_expression(node.operator, right)
        
        elif node_type == ast.Infix:
            node = cast(ast.Infix, node)
            assert node.left is not None and node.right is not None
            left = self._evaluate(node.left, env)
            right = self._evaluate(node.right, env)
            assert right is not None and left is not None
            return self._evaluate_infix_expression(node.operator, left, right)
        
        elif node_type == ast.Block:
            node = cast(ast.Block, node)
            return self._evaluate_block_statement(node, env)
        
        elif node_type == ast.If:
            node = cast(ast.If, node)
            return self._evaluate_if_expression(node, env)
        
        elif node_type == ast.ReturnStatement:
            node = cast(ast.ReturnStatement, node)
            print("mm",node)
            #assert node.return_value is not None
            value = self._evaluate(node.return_value, env)
            #assert value is not None
            return Return(value)
        
        elif node_type == ast.LetStatement:
            node = cast(ast.LetStatement, node)
            assert node.value is not None
            value = self._evaluate(node.value, env)
            assert node.name is not None
            env.set(node.name.value, value)  # Utiliza el método set en lugar de la asignación directa

        elif node_type == ast.Identifier:
            node = cast(ast.Identifier, node)
            return self._evaluate_identifier(node, env)
        
        elif node_type == ast.Function:
            node = cast(ast.Function, node)
            assert node.body is not None
            return Function(node.parameters, node.body, env)
        
        elif node_type == ast.Call:
            node = cast(ast.Call, node)
            function = self._evaluate(node.function, env)
            assert node.arguments is not None
            args = self._evaluate_expression(node.arguments, env)
            assert function is not None
            return self._apply_function(function, args)
        
        elif node_type == ast.StringLiteral:
            node = cast(ast.StringLiteral, node)
            return String(node.value)

        return None

    def _apply_function(self, fn: Object, args: List[Object]) -> Object:
        return self._new_error(self._NOT_A_FUNCTION, [fn.type().name])

    def _extend_function_environment(self, fn: Function, args: List[Object]) -> Environment:
        env = Environment(outer=fn.env)

        for idx, param in enumerate(fn.parameters):
            env.set(param.value, args[idx - 1])

        return env

    def _unwrap_return_value(self, obj: Object) -> Object:
        if type(obj) == Return:
            obj = cast(Return, obj)
            return obj.value

        return obj

    def _evaluate_program(self, program: ast.Program, env: Environment) -> Optional[Object]:
        result: Optional[Object] = None
        print("program",program)
        print("result _evaluate_program",result)

        for statement in program.statements:
            result = self._evaluate(statement, env)

            if isinstance(result, Return):
                result = cast(Return, result)
                return result.value
            elif isinstance(result, Error):  # Manejo de errores
                return result   

        return result

    def _evaluate_bang_operator_expression(self, right: Object) -> Object:
        if right is self.TRUE:
            return self.FALSE
        elif right is self.FALSE:
            return self.TRUE
        elif right is self.NULL:
            return self.TRUE
        else:
            return self.FALSE

    def _evaluate_block_statement(self, block: ast.Block, env: Environment) -> Optional[Object]:
        result: Optional[Object] = None

        for statement in block.statements:
            result = self._evaluate(statement, env)

            if result is not None and \
                    (result.type() == ObjectType.RETURN or result.type() == ObjectType.ERROR):
                return result

        return result

    def _evaluate_expression(self, expressions: List[ast.Expression], env: Environment) -> List[Object]:
        result: List[Object] = []

        for expression in expressions:
            evaluated = self._evaluate(expression, env)
            assert evaluated is not None
            result.append(evaluated)

        return result

    def _evaluate_identifier(self, node: ast.Identifier, env: Environment) -> Object:
        value = env.get(node.value)  # Utiliza el método get para obtener el valor
        if value is not None:
            return value
        else:
            return BUILTINS.get(node.value, self._new_error(self._UNKNOWN_IDENTIFIER, [node.value]))

    def _evaluate_if_expression(self, if_expression: ast.If, env: Environment) -> Optional[Object]:
        assert if_expression.condition is not None
        condition = self._evaluate(if_expression.condition, env)
        assert condition is not None
        if self._is_truthy(condition):
            assert if_expression.consequence is not None
            return self._evaluate(if_expression.consequence, env)
        elif if_expression.alternative is not None:
            return self._evaluate(if_expression.alternative, env)
        else:
            return self.NULL

    def _is_truthy(self, obj: Object) -> bool:
        if obj is self.NULL:
            return False
        elif obj is self.TRUE:
            return True
        elif obj is self.FALSE:
            return False
        else:
            return True

    def _evaluate_infix_expression(self, operator: str, left: Object, right: Object) -> Object:
        if left.type() == ObjectType.INTEGER and right.type() == ObjectType.INTEGER:
            return self._evaluate_integer_infix_expression(operator, left, right)
        elif left.type() == ObjectType.STRING and right.type() == ObjectType.STRING:
            return self._evaluate_string_infix_expression(operator, left, right)
        elif operator == '==':
            return self._to_boolean_object(left is right)
        elif operator == '!=':
            return self._to_boolean_object(left is not right)
        elif left.type() != right.type():
            return self._new_error(self._TYPE_MISMATCH, [left.type().name, operator, right.type().name])
        else:
            return self._new_error(self._UNKNOWN_INFIX_OPERATOR, [left.type().name, operator, right.type().name])

    def _evaluate_string_infix_expression(self, operator: str, left: Object, right: Object) -> Object:
        left_value: str = cast(String, left).value
        right_value: str = cast(String, right).value

        if operator == '+':
            return String(left_value + right_value)
        elif operator == '==':
            return self._to_boolean_object(left_value == right_value)
        elif operator == '!=':
            return self._to_boolean_object(left_value != right_value)
        else:
            return self._new_error(self._UNKNOWN_INFIX_OPERATOR, [left.type().name, operator, right.type().name])

    def _evaluate_integer_infix_expression(self, operator: str, left: Object, right: Object) -> Object:
        left_value: int = cast(Integer, left).value
        right_value: int = cast(Integer, right).value

        if operator == '+':
            return Integer(left_value + right_value)
        elif operator == '-':
            return Integer(left_value - right_value)
        elif operator == '*':
            return Integer(left_value * right_value)
        elif operator == '/':
            return Integer(left_value // right_value)
        elif operator == '<':
            return self._to_boolean_object(left_value < right_value)
        elif operator == '>':
            return self._to_boolean_object(left_value > right_value)
        elif operator == '==':
            return self._to_boolean_object(left_value == right_value)
        elif operator == '!=':
            return self._to_boolean_object(left_value != right_value)
        else:
            return self._new_error(self._UNKNOWN_INFIX_OPERATOR, [left.type().name, operator, right.type().name])

    def _evaluate_minus_operator_expression(self, right: Object) -> Object:
        if type(right) != Integer:
            return self._new_error(self._UNKNOWN_PREFIX_OPERATOR, ['-', right.type().name])

        right = cast(Integer, right)
        return Integer(-right.value)

    def _evaluate_prefix_expression(self, operator: str, right: Object) -> Object:
        if operator == '!':
            return self._evaluate_bang_operator_expression(right)
        elif operator == '-':
            return self._evaluate_minus_operator_expression(right)
        else:
            return self._new_error(self._UNKNOWN_PREFIX_OPERATOR, [operator, right.type().name])

    def _new_error(self, message: str, args: List[Any]) -> Error:
        return Error(message.format(*args))

    def _to_boolean_object(self, value: bool) -> Boolean:
        return self.TRUE if value else self.FALSE

