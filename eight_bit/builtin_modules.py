import sys
from typing import Optional

from eight_bit.module import Module


class IOModule(Module):
    stream: bool
    mode: bool

    def init(self, config: dict) -> None:
        super().init(config)
        self.stream = False
        self.mode = False

    def print(self):
        if self.stream:
            stream = sys.stderr
        else:
            stream = sys.stdout
        if self.mode:
            to_print = str(self.data)
        else:
            to_print = chr(self.data)
        stream.write(to_print)

    def read(self) -> int:
        if self.mode:
            return int(input().strip())
        else:
            return ord(sys.stdin.read(1))

    def cycle(self) -> Optional[int]:
        if not self.active:
            return
        if self.write:
            if self.pointer == 0:
                self.print()
            else:
                self.stream = self.data & 0b10
                self.mode = self.data & 0b01
        else:
            return self.read()
