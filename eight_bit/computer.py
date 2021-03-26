import bisect
import random
from typing import Optional

from eight_bit.module import Module


class Computer:
    modules: list[Module]
    memory_indices: list[int]

    pc: int
    sp: int
    regx: int
    regy: int
    accum: int

    write: bool
    _pointer: int
    data: int

    cur_module: Module

    running: bool

    def __init__(self, modules: list[Module]) -> None:
        self.modules = []
        self.memory_indices = []
        for module in modules:
            pos = bisect.bisect(self.memory_indices, module.start)
            self.modules.insert(pos // 2, module)
            self.memory_indices.insert(pos, module.start)
            self.memory_indices.insert(pos + 1, module.start + module.length)
        self.reset()

    def reset(self, pc: int = 0x8000, sp: int = 0x7000):
        self.pc = 0x8000
        self.sp = 0x0700
        self.regx = random.randrange(256)
        self.regy = random.randrange(256)
        self.accum = random.randrange(256)
        self.pointer = random.randrange(65536)
        self.data = random.randrange(256)
        self.write = False
        self.running = True
    
    @property
    def pointer(self) -> int:
        return self._pointer
    @pointer.setter
    def pointer(self, ptr: int) -> None:
        self._pointer = ptr
        module_id = bisect.bisect(self.memory_indices, ptr)
        if module_id % 2 == 0:
            self.cur_module = Module(start=0, length=0)
        else:
            self.cur_module = self.modules[(module_id - 1) // 2]

    def getat(self, ptr: int):
        self.write = False
        self.pointer = ptr
        self.fullcycle()
        return self.cur_module.data

    def setat(self, ptr: int, data: int):
        self.write = True
        self.pointer = ptr
        self.data = data
        self.fullcycle()
        return self.cur_module.data

    def fullcycle(self, data: Optional[int] = None):
        for module in self.modules:
            module.active = module is self.cur_module
            module.write = self.write
            module.data = self.data
            if module.active:
                module.pointer = self._pointer - module.start
            module.perform_cycle()

    def run(self):
        from eight_bit.ops import opcodes
        while self.running:
            opcode = self.getat(self.pc)
            func = opcodes[opcode % len(opcodes)]
            func(self)
            self.pc += 1


if __name__ == '__main__':
    from eight_bit.builtin_modules import *
    pc = Computer([
        IOModule(start=0, length=2),
        RAMModule(start=2, length=0x7ffe),
        ROMModule(start=0x8000, length=0x8000, raw=(
            # init
            b'\x03\x00'     # ldx #$00
            b'\x05\x01'     # ldy #$01
            # print
            b'\x0c\x01\x01' # sti $01 #$01
            b'\x09\x00'     # stx $00
            b'\x0c\x01\x00' # sti $01 #$00
            b'\x0c\x00\x0a' # sti $00 #$0a
            # calculate
            b'\x09\x02'     # stx $02
            b'\x0a\x03'     # sty $03
            b'\x04\x03'     # ldx $03
            b'\x08\x02'     # lda $02
            b'\x11\x03'     # add $03
            b'\x0b\x02'     # sta $02
            b'\x06\x02'     # ldy $02
            # loop
            b'\x01\x80\x04' # jmp $8004
            b'\x02'         # end
        ))
    ])
    pc.run()
