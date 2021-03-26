from typing import Optional


class ModuleMeta(type):
    def __new__(metacls, cls, bases, classdict, **kwds):
        if 'module_name' not in classdict:
            classdict['module_name'] = classdict['__qualname__'].rsplit('.', 1)[-1].removesuffix('Module') or 'Module'
        return type.__new__(metacls, cls, bases, classdict, **kwds)


class Module(metaclass=ModuleMeta):
    module_name: str

    start: int
    length: int

    active: bool
    write: bool
    pointer: int
    data: int

    def __init__(self, **config) -> None:
        self.active = False
        self.write = False
        self.pointer = 0
        self.data = 0
        self.init(**config)

    def init(self, *, start: int, length: int, **config) -> None:
        self.start = start
        self.length = length

    def cycle(self) -> Optional[int]:
        pass

    def perform_cycle(self) -> None:
        result = self.cycle()
        if result is not None:
            self.data = result
