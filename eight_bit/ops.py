from typing import Any, Callable
from eight_bit.computer import Computer


def nop(comp: Computer):
    pass


def ldx_imm(comp: Computer):
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.regx = data


def ldx(comp: Computer):
    comp.pc += 1
    ptr = comp.getat(comp.pc)
    data = comp.getat(ptr)
    comp.regx = data


def ldy_imm(comp: Computer):
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.regy = data


def ldy(comp: Computer):
    comp.pc += 1
    ptr = comp.getat(comp.pc)
    data = comp.getat(ptr)
    comp.regy = data


def lda_imm(comp: Computer):
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.accum = data
    

def lda(comp: Computer):
    comp.pc += 1
    ptr = comp.getat(comp.pc)
    data = comp.getat(ptr)
    comp.accum = data


opcodes: list[Callable[[Computer], Any]] = [
    nop,

    ldx_imm,
    ldx,
    ldy_imm,
    ldy,
    lda_imm,
    lda
]
