from typing import Generic, TypeVar

T = TypeVar("T")
M = TypeVar("M")
class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

class IntBox(Box[int]):
    pass

class MyBox(Box[T], Generic[T]):
    pass


m: MyBox[str] = MyBox("hello")

