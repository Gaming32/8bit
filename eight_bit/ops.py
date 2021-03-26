from typing import Any, Callable
from eight_bit.computer import Computer


def nop(comp: Computer):
    pass


opcodes: list[Callable[[Computer], Any]] = [nop]
