# uvm_asm.py — Вариант №16 (стековая, 3/1 байт команды)
import argparse
import sys

def encode_load_const(const):
    A = 0
    B = const
    word = A | (B << 4)
    return word.to_bytes(3, 'little')

def encode_read_value(offset):
    A = 2
    B = offset
    word = A | (B << 4)
    return word.to_bytes(3, 'little')

def encode_write_value():
    A = 5
    return bytes([A])  # 1 байт

def encode_bitreverse(offset):
    A = 11
    B = offset
    word = A | (B << 4)
    return word.to_bytes(3, 'little')

def parse_program(text):
    IR = []
    for line_num, line in enumerate(text.strip().splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith(';'):
            continue
        parts = line.split()
        op = parts[0]
        try:
            if op == 'load_const':
                val = int(parts[1])
                if not (0 <= val <= 0x7FFF):
                    raise ValueError(f"Constant out of range: {val}")
                IR.append(('load_const', val))
            elif op == 'read_value':
                offset = int(parts[1])
                if not (0 <= offset <= 0x3FFF):
                    raise ValueError(f"Offset out of range: {offset}")
                IR.append(('read_value', offset))
            elif op == 'write_value':
                IR.append(('write_value',))
            elif op == 'bitreverse':
                offset = int(parts[1])
                if not (0 <= offset <= 0x3FFF):
                    raise ValueError(f"Offset out of range: {offset}")
                IR.append(('bitreverse', offset))
            else:
                raise ValueError(f"Unknown opcode: {op}")
        except (IndexError, ValueError) as e:
            raise ValueError(f"Line {line_num}: {e}")
    return IR

def assemble(IR):
    bytecode = b''
    for instr in IR:
        if instr[0] == 'load_const':
            bytecode += encode_load_const(instr[1])
        elif instr[0] == 'read_value':
            bytecode += encode_read_value(instr[1])
        elif instr[0] == 'write_value':
            bytecode += encode_write_value()
        elif instr[0] == 'bitreverse':
            bytecode += encode_bitreverse(instr[1])
        else:
            raise ValueError(f"Unknown instr: {instr}")
    return bytecode

def test():
    # load_const 460 → 0xC0, 0x1C, 0x00
    assert list(encode_load_const(460)) == [0xC0, 0x1C, 0x00]
    # read_value 1000 → 0x82, 0x3E, 0x00
    assert list(encode_read_value(1000)) == [0x82, 0x3E, 0x00]
    # write_value → 0x05
    assert list(encode_write_value()) == [0x05]
    # bitreverse 255 → 0xFB, 0x0F, 0x00
    assert list(encode_bitreverse(255)) == [0xFB, 0x0F, 0x00]

def main():
    test()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-t', '--test', required=True)
    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        text = f.read()

    IR = parse_program(text)
    bytecode = assemble(IR)

    with open(args.output, 'wb') as f:
        f.write(bytecode)

    print(len(bytecode))  # размер в байтах

    if args.test == '1':
        print("IR:", IR)
        print("Bytecode:", ' '.join(f'0x{b:02X}' for b in bytecode))

if __name__ == '__main__':
    main()