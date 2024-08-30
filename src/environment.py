class Environment:
    def __init__(self):
        self.store = {}

    def get(self, name: str):
        if name in self.store:
            return self.store[name]
        else:
            raise NameError(f"Variable '{name}' no está definida.")

    def set(self, name: str, value):
        self.store[name] = value

    def __repr__(self) -> str:
        return f"Environment({self.store})"
