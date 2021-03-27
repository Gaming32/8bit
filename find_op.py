import sys
from eight_bit.ops import opcodes

find = sys.argv[1]
for (i, op) in enumerate(opcodes):
    if op.__name__ == find:
        print(f'id for opcode {find}:', hex(i))
        break
else:
    print('opcode not found')
