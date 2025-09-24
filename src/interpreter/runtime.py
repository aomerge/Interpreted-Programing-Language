from typing import List, Tuple, Union, Optional, cast
from src.ast import (
    Block, Expression, Statement
)   
from src.confg.environment import Environment
from src.confg.object import (
    Boolean, Null, Object, Integer, Return, Function, String, ObjectType
)

ApplyResult = Union[
    Tuple[Block, Environment], 
    Object                     
]

from .errors import (
    UNKNOWN_INFIX_OPERATOR,
    UNKNOWN_PREFIX_OPERATOR,
    DIVISION_BY_ZERO,
    new_error
)

class RuntimePrimitives:
    """"Singletons y utilidades de verdad del lenguaje."""
    TRUE = Boolean(True)
    FALSE = Boolean(False)
    NULL = Null()
    def __new__(cls, *args, **kwargs):
        raise TypeError("RuntimePrimitives no se instancia; use atributos de clase.")

    @classmethod
    def to_boolean_object(cls, value: bool) -> Boolean:
        return cls.TRUE if value else cls.FALSE

    @classmethod
    def is_truthy(cls, obj: Object) -> bool:
        if obj is cls.NULL:
            return False
        if isinstance(obj, Boolean):
            # Admite singletons y otras instancias Boolean
            return obj is cls.TRUE or getattr(obj, "value", False) is True
        return True

class InfixOps:
    """Operadores infijos por tipo."""

    @staticmethod
    def integer_infix(operator: str, left: Object, right: Object) -> Object:
        l = cast(Integer, left).value
        r = cast(Integer, right).value

        if operator == '+':  return Integer(l + r)
        if operator == '-':  return Integer(l - r)
        if operator == '*':  return Integer(l * r)
        if operator == '/':
            if r == 0:
                return new_error(DIVISION_BY_ZERO, [])
            return Integer(l // r)
        if operator == '<':  return RuntimePrimitives.to_boolean_object(l < r)
        if operator == '>':  return RuntimePrimitives.to_boolean_object(l > r)
        if operator == '==': return RuntimePrimitives.to_boolean_object(l == r)
        if operator == '!=': return RuntimePrimitives.to_boolean_object(l != r)

        return new_error(UNKNOWN_INFIX_OPERATOR, [left.type().name, operator, right.type().name])

    @staticmethod
    def string_infix(operator: str, left: Object, right: Object) -> Object:
        l = cast(String, left).value
        r = cast(String, right).value

        if operator == '+':  return String(l + r)
        if operator == '==': return RuntimePrimitives.to_boolean_object(l == r)
        if operator == '!=': return RuntimePrimitives.to_boolean_object(l != r)

        return new_error(UNKNOWN_INFIX_OPERATOR, [left.type().name, operator, right.type().name])

class PrefixOps:
    """Operadores prefijos del lenguaje."""

    @staticmethod
    def bang(right: Object) -> Object:
        # !x — semántica: NULL y FALSE → TRUE; TRUE → FALSE; otro → FALSE
        if right is RuntimePrimitives.TRUE:   return RuntimePrimitives.FALSE
        if right is RuntimePrimitives.FALSE:  return RuntimePrimitives.TRUE
        if right is RuntimePrimitives.NULL:   return RuntimePrimitives.TRUE
        return RuntimePrimitives.FALSE

    @staticmethod
    def minus(right: Object) -> Object:
        if not isinstance(right, Integer):
            return new_error(UNKNOWN_PREFIX_OPERATOR, ['-', right.type().name])
        return Integer(-cast(Integer, right).value)

class Functions:
    """Aplicación de funciones y manejo de entornos."""

    @staticmethod
    def extend_function_environment(fn: Function, args: List[Object]) -> Environment:
        """
        Crea un entorno hijo de la clausura de `fn` y liga parámetros -> argumentos.
        Precondición: len(args) == len(fn.parameters)
        """
        env = Environment(outer=fn.env)
        for param, arg in zip(fn.parameters, args):
            env.set(param.value, arg)
        return env

    @staticmethod
    def unwrap_return_value(obj: Object) -> Object:
        """
        Si el resultado es un Return, destapa su valor. Si value es None (permitido en tu AST),
        se normaliza a Runtime.NULL para coherencia semántica.
        """
        if isinstance(obj, Return):
            value: Optional[Object] = cast(Return, obj).value
            return value if value is not None else Runtime.NULL
        return obj

    @staticmethod
    def apply_function(fn: Object, args: List[Object]) -> ApplyResult:
        """
        Prepara la ejecución de una Function definida en el lenguaje:
        - Verifica tipo (Function) y aridad.
        - Extiende entorno con ligaduras param->arg.
        - Devuelve (bloque_cuerpo, env_extendido) para que el evaluador lo ejecute.
        En caso de error, retorna un Error (Object).
        """
        if not isinstance(fn, Function):
            return new_error(NOT_A_FUNCTION, [fn.type().name])

        expected = len(fn.parameters)
        received = len(args)
        if expected != received:
            return new_error(WRONG_ARITY, [expected, received])

        extended_env = Functions.extend_function_environment(fn, args)
        # Importante: NO evaluamos aquí para evitar acoplamientos/ciclos.
        return fn.body, extended_env