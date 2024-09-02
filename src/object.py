from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Dict, List

class ObjectType(Enum):
    BOOLEAN = auto()
    BUILTIN = auto()
    ERROR = auto()
    FUNCTION = auto()
    NULL= auto()
    RETURN= auto()
    STRING= auto()
    INTEGER= auto()

class Object(ABC):
    @abstractmethod
    def type(self) -> ObjectType:
        pass

    @abstractmethod
    def inspect(self) -> str:
        pass

class Integer(Object):
    def __init__(self, value: int):
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.INTEGER

    def inspect(self) -> str:
        return str(self.value)

class Boolean(Object):
    def __init__(self, value: bool):
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN

    def inspect(self) -> str:
        return str(self.value).lower()

class Null(Object):
    def type(self) -> ObjectType:
        return ObjectType.NULL

    def inspect(self) -> str:
        return "null"
    
class Return(Object):
    def __init__(self, value: Object):
        print(value)
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.RETURN

    def inspect(self) -> str:
        return self.value.inspect()

class Error(Object):
    def __init__(self, message: str):
        self.message = message

    def type(self) -> ObjectType:
        return ObjectType.ERROR

    def inspect(self) -> str:
        return f'Error: {self.message}'

class Environment:
    def __init__(self):
        self.store: Dict[str, Object] = {}

    def get(self, name: str) -> Object:
        obj = self.store.get(name)
        if obj is None:
            return Null()
        return obj

    def set(self, name: str, value: Object):
        self.store[name] = value

class Function(Object):
    def __init__(self, parameters: List[str], body: str, env: Environment):
        self.parameters = parameters
        self.body = body
        self.env = env

    def type(self) -> ObjectType:
        return ObjectType.FUNCTION

    def inspect(self) -> str:
        return f'fn({", ".join(self.parameters)}) {self.body}'

class String(Object):
    def __init__(self, value: str):
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.STRING

    def inspect(self) -> str:
        return self.value
    
class BuiltinFunction:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args):
        return self.fn(*args)
    
class Builtin(Object):
    def __init__(self, fn):
        self.fn = fn

    def type(self) -> ObjectType:
        return ObjectType.BUILTIN

    def inspect(self) -> str:
        return "builtin function"

    def __call__(self, *args):
        return self.fn(*args)