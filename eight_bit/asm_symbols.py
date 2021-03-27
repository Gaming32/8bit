from eight_bit.asm import parse_literal
from io import BytesIO
from typing import Callable


def write_value(value: int, result: BytesIO):
    result.write(value.to_bytes(1, 'big', signed=False))


def write_address(address: int, result: BytesIO, op1: bytes, op2: bytes) -> None:
    if address < 256:
        result.write(op1)
        write_value(address, result)
    else:
        result.write(op2)
        result.write(address.to_bytes(2, 'big', signed=False))


def nop(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    if args:
        raise ValueError('no arguments to nop')
    result.write(b'\x00')


def jmp(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    was_addr, address = parse_literal(args, labels, constants)
    if not was_addr:
        raise ValueError('argument to jmp must be address')
    write_address(address, result, b'\x01', b'\x02')


def end(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    if args:
        raise ValueError('no arguments to end')
    result.write(b'\x03')


def load(args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str], op, op2, op_imm) -> None:
    was_addr, value = parse_literal(args, labels, constants)
    if was_addr:
        write_address(value, result, op, op2)
    else:
        result.write(op_imm)
        write_value(value, result)


def ldx(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    load(args, result, labels, constants, b'\x05', b'\x06', b'\x04')


def ldy(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    load(args, result, labels, constants, b'\x08', b'\x09', b'\x07')


def lda(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    load(args, result, labels, constants, b'\x0b', b'\x0c', b'\x0a')


def store(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str], op, op2) -> None:
    was_addr, value = parse_literal(args, labels, constants)
    if not was_addr:
        raise ValueError(f'argument to {name} must be address')
    write_address(value, result, op, op2)


def stx(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    store(name, args, result, labels, constants, b'\x0d', b'\x11')


def sty(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    store(name, args, result, labels, constants, b'\x0e', b'\x12')


def sta(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    store(name, args, result, labels, constants, b'\x0f', b'\x13')


def sti(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    arg1, arg2 = args.split()[:2]
    was_addr, address = parse_literal(arg1, labels, constants)
    if not was_addr:
        raise ValueError(f'first argument to sti must be address')
    was_addr, value = parse_literal(arg2, labels, constants)
    if was_addr:
        raise ValueError(f'second argument to sti must not be an address')
    write_address(address, result, b'\x10', b'\x14')
    write_value(value, result)


def add_reg(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    if args:
        raise ValueError(f'no arguments to {name}')
    if name == 'adx':
        op = b'\x15'
    elif name == 'ady':
        op = b'\x16'
    elif name == 'ada':
        op = b'\x17'
    elif name == 'sbx':
        op = b'\x1b'
    elif name == 'sby':
        op = b'\x1c'
    elif name == 'sba':
        op = b'\x1d'
    else:
        raise ValueError(f'no add operator called {name}')
    result.write(op)


def adi(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    was_addr, value = parse_literal(args, labels, constants)
    if was_addr:
        raise ValueError(f'argument to adi must not be an address')
    if name == 'adi':
        op = b'\x18'
    else:
        op = b'\x1e'
    result.write(op)
    write_value(value, result)


def add(name: str, args: str, result: BytesIO, labels: dict[str, int], constants: dict[str, str]) -> None:
    was_addr, address = parse_literal(args, labels, constants)
    if not was_addr:
        raise ValueError('argument to add must be address')
    if name == 'add':
        ops = (b'\x19', b'\x1a')
    else:
        ops = (b'\x1f', b'\x20')
    write_address(address, result, *ops)


symbols: dict[str, Callable[[str, str, BytesIO, dict[str, int], dict[str, str]], None]] = {
    'nop': nop,

    'jmp': jmp,
    'end': end,

    'ldx': ldx,
    'ldy': ldy,
    'lda': lda,

    'stx': stx,
    'sty': sty,
    'sta': sta,
    'sti': sti,

    'adx': add_reg,
    'ady': add_reg,
    'ada': add_reg,
    'adi': adi,
    'add': add,

    'sbx': add_reg,
    'sby': add_reg,
    'sba': add_reg,
    'sbi': adi,
    'sub': add,
}
