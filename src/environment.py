from typing import Optional

from src.object import Object

class Environment:
    def __init__(self, outer: Optional['Environment'] = None):
        self.store = {}
        self.outer = outer

    def get(self, name: str) -> Optional[Object]:
        """Get the value associated with the name in the current environment or outer environments."""
        if name in self.store:
            return self.store[name]
        elif self.outer:
            return self.outer.get(name)
        else:
            return None

    def set(self, name: str, value: Object) -> Object:
        """Set the value for the name in the current environment."""
        self.store[name] = value
        print(f"Set {name} to {value}")
        return value

