"""CPU functionality."""

import sys
import re

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.registers = {}
        pass

    def load(self):
        """Load a program into memory."""
        
        address = 0

        # For now, we've just hardcoded a program:
        f = open(f"./ls8/examples/{sys.argv[1]}.ls8", "r").read()
        instructions_array = f.split("\n")
        # for 
        instruction_lines = []
        for line in instructions_array:
            if re.match('[0-1]{7}', line) is not None:
                instruction_lines.append(line)
        program = [f"0b{instruction[:8]}" for instruction in instruction_lines]
        for instruction in program:
            self.ram[address] = instruction[2:]
            address += 1

    def ram_read(self, address):
        return self.ram[address]
        

    def ram_write(self, address, value):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.registers[reg_a] = self.registers[reg_a] * self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()

    def run(self):
        """Run the CPU."""
        ir = self.ram[self.pc]
        num_operands = int(ir[:2], 2)
        operands = []
        for i in range(1, num_operands + 1):
            operands.append(int(self.ram_read(self.pc + i), 2))
        if ir[2] == "1":
            if ir[-4:] == "0010":
                self.alu("MUL", operands[0], operands[1])
        elif ir[-4:] == "0010":
            self.registers[operands[0]] = operands[1]
        elif ir[-4:] == "0111":
            print(self.registers[operands[0]])
        elif ir[-4:] == "0001":
            return
        else:
            return
        self.pc = self.pc + 1 + num_operands
        self.run()