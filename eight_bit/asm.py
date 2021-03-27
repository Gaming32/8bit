import ast
import string
from io import StringIO, BytesIO


def parse_number(val: str) -> tuple[bool, int]:
    """Returns (is_address, value)"""
    i = len(val) - 1
    while i >= 0:
        if val[i] not in string.hexdigits:
            break
        i -= 1
    i += 1
    directives, raw = val[:i], val[i:]
    if '$' in directives or 'h' in directives:
        base = 16
    elif '%' in directives or 'b' in directives:
        base = 2
    elif 'o' in directives:
        base = 8
    else:
        base = 10
    is_address = '#' not in directives
    return is_address, int(raw, base)


def parse_literal(val: str, labels: dict[str, int], constants: dict[str, str]) -> tuple[bool, int]:
    """Returns (is_address, value)"""
    if val[0] == "'" and val[-1] == "'":
        res = ast.literal_eval('b' + val)
        if len(res) != 1:
            raise ValueError('char literal cannot have more than one character')
        return False, res[0]
    elif val in constants:
        return parse_literal(constants[val], labels, constants)
    elif val in labels:
        return True, labels[val]
    return parse_number(val)


def parse(code: str) -> bytes:
    from eight_bit.asm_symbols import symbols
    labels = {}
    constants = {}
    result = BytesIO(b'\0' * 65536)
    offset = 0

    for line in StringIO(code):
        line = line.rstrip()
        stripped = line.lstrip().split(';', 1)[0].rstrip() # Strip comments
        if not stripped: # Skip empty/comment lines
            continue

        elif line[0] == '.': # Interpret compiler directives
            if ' ' in stripped:
                directive, arg = stripped[1:].split(' ', 1)
            else:
                directive, arg = stripped[1:], ''
            if directive == 'offset':
                offset = parse_number(arg)[1]
            elif directive == 'length':
                result.truncate(parse_number(arg)[1])
            elif directive == 'truncate':
                result.truncate(result.tell())
            elif directive == 'put':
                putval = ast.literal_eval(arg)
                if isinstance(putval, int):
                    result.write(putval.to_bytes((putval.bit_length() + 7) // 8, 'big', signed=False))
                elif isinstance(putval, str):
                    result.write(putval.encode('utf-8'))
                else:
                    result.write(putval)
            elif directive == 'org':
                dest = parse_number(arg)[1]
                result.seek(dest)
                offset = dest

        elif line[0] in string.whitespace: # Interpret symbols
            if ' ' in stripped:
                name, args = stripped.split(' ', 1)
            else:
                name, args = stripped, ''
            symbols[name](name, args, result, labels, constants)

        elif line[-1] == ':': # Interpret labels
            label_name = stripped.rstrip(':')
            labels[label_name] = offset + result.tell()

        elif '=' in line: # Interpret constants
            name, value = stripped.split('=', 1)
            constants[name.strip()] = value.strip()

    return result.getvalue()


if __name__ == '__main__':
    import sys
    import os
    if len(sys.argv) == 1:
        print('Usage: python -m eight_bit.asm <input_asm> [out_file]')
        exit()
    try:
        if len(sys.argv) == 2:
            infile = sys.argv[1]
            outfile = os.fdopen(sys.stdout.fileno(), 'wb')
        else:
            infile = sys.argv[1]
            outfile = open(sys.argv[2], 'wb')
        with open(infile) as fp:
            contents = fp.read()
        outfile.write(parse(contents))
    finally:
        if outfile.fileno() != sys.stdout.fileno():
            outfile.close()
