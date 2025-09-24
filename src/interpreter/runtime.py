from typing import List, Tuple, Union, Optional, cast
from src.astNode import (
    Block, Expression, Statement
)   
from src.config.environment import Environment
from src.config.object import (
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
    """Singleton objects and truth utilities for the language runtime.
    
    This class provides centralized access to primitive runtime values
    and utilities for boolean operations and truthiness evaluation.
    """
    
    # Singleton instances for primitive values
    TRUE = Boolean(True)
    FALSE = Boolean(False)
    NULL = Null()
    
    def __new__(cls, *args, **kwargs):
        """Prevent instantiation of this utility class."""
        raise TypeError(f"{cls.__name__} is a utility class and cannot be instantiated")

    @classmethod
    def to_boolean_object(cls, value: bool) -> Boolean:
        """Convert a Python boolean to a runtime Boolean object.
        
        Args:
            value: Python boolean value to convert
            
        Returns:
            Boolean: Runtime Boolean object (TRUE or FALSE singleton)
        """
        return cls.TRUE if value else cls.FALSE

    @classmethod
    def is_truthy(cls, obj: Object) -> bool:
        """Evaluate the truthiness of a runtime object.
        
        Truthiness rules:
        - NULL is falsy
        - Boolean objects: TRUE is truthy, FALSE is falsy
        - All other objects are truthy
        
        Args:
            obj: Runtime object to evaluate
            
        Returns:
            bool: True if the object is truthy, False otherwise
        """
        if obj is cls.NULL:
            return False
            
        if isinstance(obj, Boolean):
            # Handle both singleton and non-singleton Boolean instances
            return obj is cls.TRUE or getattr(obj, 'value', False) is True
            
        return True

class InfixOperations:
    """Handles infix operators for different object types.
    
    This class provides static methods to evaluate binary operations
    between runtime objects, with proper type checking and error handling.
    """
    
    # Mapping of operators to their implementation methods
    _INTEGER_OPERATORS = {
        '+': lambda l, r: l + r,
        '-': lambda l, r: l - r,
        '*': lambda l, r: l * r,
        '/': lambda l, r: l // r,  # Integer division
        '<': lambda l, r: l < r,
        '>': lambda l, r: l > r,
        '==': lambda l, r: l == r,
        '!=': lambda l, r: l != r,
    }
    
    _STRING_OPERATORS = {
        '+': lambda l, r: l + r,
        '==': lambda l, r: l == r,
        '!=': lambda l, r: l != r,
    }

    @staticmethod
    def integer_infix(operator: str, left: Object, right: Object) -> Object:
        """Evaluate infix operations between two Integer objects.
        
        Args:
            operator: The infix operator as a string
            left: Left operand (must be Integer)
            right: Right operand (must be Integer)
            
        Returns:
            Object: Result of the operation or error object
        """
        left_value = cast(Integer, left).value
        right_value = cast(Integer, right).value

        # Handle division by zero
        if operator == '/' and right_value == 0:
            return new_error(DIVISION_BY_ZERO, [])
        
        # Get the operation function
        operation = InfixOperations._INTEGER_OPERATORS.get(operator)
        if operation is None:
            return new_error(UNKNOWN_INFIX_OPERATOR, 
                           [left.type().name, operator, right.type().name])
        
        result = operation(left_value, right_value)
        
        # Return appropriate object type based on operation
        if operator in ['<', '>', '==', '!=']:
            return RuntimePrimitives.to_boolean_object(result)
        
        return Integer(result)

    @staticmethod
    def string_infix(operator: str, left: Object, right: Object) -> Object:
        """Evaluate infix operations between two String objects.
        
        Args:
            operator: The infix operator as a string
            left: Left operand (must be String)
            right: Right operand (must be String)
            
        Returns:
            Object: Result of the operation or error object
        """
        left_value = cast(String, left).value
        right_value = cast(String, right).value

        # Get the operation function
        operation = InfixOperations._STRING_OPERATORS.get(operator)
        if operation is None:
            return new_error(UNKNOWN_INFIX_OPERATOR, 
                           [left.type().name, operator, right.type().name])
        
        result = operation(left_value, right_value)
        
        # Return appropriate object type based on operation
        if operator in ['==', '!=']:
            return RuntimePrimitives.to_boolean_object(result)
        
        return String(result)

class PrefixOperations:
    """Handles prefix (unary) operators for the language.
    
    This class provides static methods to evaluate unary operations
    on runtime objects with proper semantic rules.
    """

    @staticmethod
    def logical_not(operand: Object) -> Object:
        """Evaluate logical NOT operator (!).
        
        Semantic rules:
        - !TRUE → FALSE
        - !FALSE → TRUE  
        - !NULL → TRUE
        - !anything_else → FALSE
        
        Args:
            operand: The object to negate
            
        Returns:
            Boolean: Result of logical negation
        """
        # Use truthiness evaluation for consistent behavior
        is_truthy = RuntimePrimitives.is_truthy(operand)
        return RuntimePrimitives.to_boolean_object(not is_truthy)

    @staticmethod
    def arithmetic_negation(operand: Object) -> Object:
        """Evaluate arithmetic negation operator (-).
        
        Args:
            operand: The object to negate (must be Integer)
            
        Returns:
            Object: Negated Integer or error object
        """
        if not isinstance(operand, Integer):
            return new_error(UNKNOWN_PREFIX_OPERATOR, 
                           ['-', operand.type().name])
        
        original_value = cast(Integer, operand).value
        return Integer(-original_value)

    # Legacy method names for backward compatibility
    @staticmethod
    def bang(right: Object) -> Object:
        """Legacy alias for logical_not. Use logical_not instead."""
        return PrefixOperations.logical_not(right)

    @staticmethod
    def minus(right: Object) -> Object:
        """Legacy alias for arithmetic_negation. Use arithmetic_negation instead."""
        return PrefixOperations.arithmetic_negation(right)

class FunctionsOperations:
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