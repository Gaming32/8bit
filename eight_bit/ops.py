from typing import Any, Callable
from eight_bit.computer import Computer


def nop(comp: Computer):
    pass


def jmp(comp: Computer):
    comp.pc = comp.getat(comp.pc + 1) * 256 + comp.getat(comp.pc + 2) - 1


def end(comp: Computer):
    comp.running = False


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


def stx(comp: Computer):
    comp.pc += 1
    ptr = comp.getat(comp.pc)
    comp.setat(ptr, comp.regx)


def sty(comp: Computer):
    comp.pc += 1
    ptr = comp.getat(comp.pc)
    comp.setat(ptr, comp.regy)


def sta(comp: Computer):
    comp.pc += 1
    ptr = comp.getat(comp.pc)
    comp.setat(ptr, comp.accum)


def sti(comp: Computer):
    comp.pc += 1
    ptr = comp.getat(comp.pc)
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.setat(ptr, data)


def adx(comp: Computer):
    comp.accum += comp.regx
    comp.accum %= 256


def ady(comp: Computer):
    comp.accum += comp.regy
    comp.accum %= 256


def ada(comp: Computer):
    comp.accum += comp.accum
    comp.accum %= 256


def adi(comp: Computer):
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.accum += data
    comp.accum %= 256


def add(comp: Computer):
    comp.pc += 1
    ptr = comp.getat(comp.pc)
    data = comp.getat(ptr)
    comp.accum += data
    comp.accum %= 256


opcodes: list[Callable[[Computer], Any]] = [
    nop,

    jmp,
    end,

    ldx_imm,
    ldx,
    ldy_imm,
    ldy,
    lda_imm,
    lda,

    stx,
    sty,
    sta,
    sti,

    adx,
    ady,
    ada,
    adi,
    add,
]
