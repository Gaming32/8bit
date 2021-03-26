import base64
import secrets
import sys
from typing import Optional

from eight_bit.module import Module


class RAMModule(Module):
    memory: bytearray

    def init(self, *, length: int, **config) -> None:
        super().init(length=length, **config)
        self.data = bytearray(secrets.token_bytes(length))

    def cycle(self) -> Optional[int]:
        if not self.active:
            return
        if self.write:
            self.memory[self.pointer] = self.data
        else:
            return self.memory[self.pointer]


class ROMModule(Module):
    memory: bytes

    def init(self, *, start: int, length: int, **config) -> None:
        super().init(start=start, length=length, **config)
        if (filename := config.pop('filename', None)) is not None:
            with open(filename, 'rb') as fp:
                self.memory = fp.read()
        elif (base64_data := config.pop('base64', None)) is not None:
            self.memory = base64.b64decode(base64_data)
        elif (raw_data := config.pop('raw', None)) is not None:
            self.memory = raw_data
        if len(self.memory) < length:
            self.memory += secrets.token_bytes(length - len(self.memory))
        elif len(self.memory) > length:
            self.memory = self.memory[:length]

    def cycle(self) -> Optional[int]:
        if not self.active:
            return
        return self.memory[self.pointer]


class IOModule(Module):
    stream: bool
    mode: bool

    def init(self, **config) -> None:
        super().init(**config)
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
