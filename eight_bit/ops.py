from typing import Any, Callable
from eight_bit.computer import Computer


def getat_pages(comp: Computer, pageswitch: bool = False):
    if pageswitch:
        comp.pc += 2
        return comp.getat(comp.pc - 1) * 256 + comp.getat(comp.pc)
    comp.pc += 1
    return comp.getat(comp.pc)


def nop(comp: Computer):
    pass


def jmp(comp: Computer):
    comp.pc = getat_pages(comp) - 1


def jmp2(comp: Computer):
    comp.pc = getat_pages(comp, True) - 1


def end(comp: Computer):
    comp.running = False


def ldx_imm(comp: Computer):
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.regx = data


def ldx(comp: Computer):
    ptr = getat_pages(comp)
    data = comp.getat(ptr)
    comp.regx = data


def ldx2(comp: Computer):
    ptr = getat_pages(comp, True)
    data = comp.getat(ptr)
    comp.regx = data


def ldy_imm(comp: Computer):
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.regy = data


def ldy(comp: Computer):
    ptr = getat_pages(comp)
    data = comp.getat(ptr)
    comp.regy = data


def ldy2(comp: Computer):
    ptr = getat_pages(comp, True)
    data = comp.getat(ptr)
    comp.regy = data


def lda_imm(comp: Computer):
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.accum = data


def lda(comp: Computer):
    ptr = getat_pages(comp)
    data = comp.getat(ptr)
    comp.accum = data


def lda2(comp: Computer):
    ptr = getat_pages(comp, True)
    data = comp.getat(ptr)
    comp.accum = data


def stx(comp: Computer):
    ptr = getat_pages(comp)
    comp.setat(ptr, comp.regx)


def stx2(comp: Computer):
    ptr = getat_pages(comp, True)
    comp.setat(ptr, comp.regx)


def sty(comp: Computer):
    ptr = getat_pages(comp)
    comp.setat(ptr, comp.regy)


def sty2(comp: Computer):
    ptr = getat_pages(comp, True)
    comp.setat(ptr, comp.regy)


def sta(comp: Computer):
    ptr = getat_pages(comp)
    comp.setat(ptr, comp.accum)


def sta2(comp: Computer):
    ptr = getat_pages(comp, True)
    comp.setat(ptr, comp.accum)


def sti(comp: Computer):
    ptr = getat_pages(comp)
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.setat(ptr, data)


def sti2(comp: Computer):
    ptr = getat_pages(comp, True)
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.setat(ptr, data)


def adx(comp: Computer):
    comp.accum += comp.regx
    comp.overflow = comp.accum > 255
    comp.accum %= 256


def ady(comp: Computer):
    comp.accum += comp.regy
    comp.overflow = comp.accum > 255
    comp.accum %= 256


def ada(comp: Computer):
    comp.accum += comp.accum
    comp.overflow = comp.accum > 255
    comp.accum %= 256


def adi(comp: Computer):
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.accum += data
    comp.overflow = comp.accum > 255
    comp.accum %= 256


def add(comp: Computer):
    ptr = getat_pages(comp)
    data = comp.getat(ptr)
    comp.accum += data
    comp.overflow = comp.accum > 255
    comp.accum %= 256


def add2(comp: Computer):
    ptr = getat_pages(comp, True)
    data = comp.getat(ptr)
    comp.accum += data
    comp.overflow = comp.accum > 255
    comp.accum %= 256


def sbx(comp: Computer):
    comp.accum -= comp.regx
    comp.overflow = comp.accum < 0
    comp.accum %= 256


def sby(comp: Computer):
    comp.accum -= comp.regy
    comp.overflow = comp.accum < 0
    comp.accum %= 256


def sba(comp: Computer):
    comp.accum -= comp.accum
    comp.overflow = comp.accum < 0
    comp.accum %= 256


def sbi(comp: Computer):
    comp.pc += 1
    data = comp.getat(comp.pc)
    comp.accum -= data
    comp.overflow = comp.accum < 0
    comp.accum %= 256


def sub(comp: Computer):
    ptr = getat_pages(comp)
    data = comp.getat(ptr)
    comp.accum -= data
    comp.overflow = comp.accum < 0
    comp.accum %= 256


def sub2(comp: Computer):
    ptr = getat_pages(comp, True)
    data = comp.getat(ptr)
    comp.accum -= data
    comp.overflow = comp.accum < 0
    comp.accum %= 256


opcodes: list[Callable[[Computer], None]] = [
    nop,

    jmp,
    jmp2,
    end,

    ldx_imm,
    ldx,
    ldx2,
    ldy_imm,
    ldy,
    ldy2,
    lda_imm,
    lda,
    lda2,

    stx,
    sty,
    sta,
    sti,

    stx2,
    sty2,
    sta2,
    sti2,

    adx,
    ady,
    ada,
    adi,
    add,
    add2,

    sbx,
    sby,
    sba,
    sbi,
    sub,
    sub2,
]
