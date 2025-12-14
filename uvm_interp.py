# uvm_interp.py — Вариант №16
import argparse
import csv

def bitreverse32(x):
    # Обрабатываем как 32-битное беззнаковое
    x &= 0xFFFFFFFF
    return int(f"{x:032b}"[::-1], 2)

def execute(bytecode):
    stack = []
    memory = [0] * 1024  # объединённая память

    i = 0
    while i < len(bytecode):
        op = bytecode[i] & 0x0F
        if op == 0:  # load_const
            if i + 3 > len(bytecode):
                raise ValueError("Truncated load_const")
            word = int.from_bytes(bytecode[i:i+3], 'little')
            const = (word >> 4) & 0x7FFF  # 15 бит
            stack.append(const)
            i += 3
        elif op == 2:  # read_value
            if i + 3 > len(bytecode):
                raise ValueError("Truncated read_value")
            word = int.from_bytes(bytecode[i:i+3], 'little')
            offset = (word >> 4) & 0x3FFF  # 14 бит
            addr = stack.pop()
            val = memory[addr + offset]
            stack.append(val)
            i += 3
        elif op == 5:  # write_value
            value = stack.pop()
            addr = stack.pop()
            memory[addr] = value
            i += 1
        elif op == 11:  # bitreverse
            if i + 3 > len(bytecode):
                raise ValueError("Truncated bitreverse")
            word = int.from_bytes(bytecode[i:i+3], 'little')
            offset = (word >> 4) & 0x3FFF  # 14 бит
            addr = stack.pop()
            # Берём значение из памяти по этому адресу
            val = memory[addr]
            rev = bitreverse32(val)
            # Пишем по адресу (addr + offset)
            memory[addr + offset] = rev
            i += 3
        else:
            raise ValueError(f"Unknown opcode {op} at pos {i}")
    return memory

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-r', '--range', required=True)
    args = parser.parse_args()

    with open(args.input, 'rb') as f:
        bytecode = f.read()

    memory = execute(bytecode)

    r_from, r_to = map(int, args.range.split('-'))
    dump = memory[r_from:r_to]

    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['address', 'value'])
        for idx, val in enumerate(dump, start=r_from):
            writer.writerow([idx, val])

if __name__ == '__main__':
    main()