from typing import Generator, Any


class Registry:
    def __init__(self, value):
        if isinstance(value, list):
            self.value = value
        else:
            self.value = [value]

    def get(self) -> Generator[Any, None, None]:
        return (i for i in self.value)