from typing import Any, List
from src.object import Error

# Mensajes centralizados
NOT_A_FUNCTION = 'No es una funcion: {}'
TYPE_MISMATCH = 'Discrepancia de tipos: {} {} {}'
UNKNOWN_PREFIX_OPERATOR = 'Operador desconocido: {}{}'
UNKNOWN_INFIX_OPERATOR = 'Operador desconocido: {} {} {}'
UNKNOWN_IDENTIFIER = 'Identificador no encontrado: {}'
DIVISION_BY_ZERO = "División por cero"


def new_error(message: str, args: List[Any]) -> Error:
    return Error(message.format(*args))
