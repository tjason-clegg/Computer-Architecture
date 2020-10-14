"""CPU functionality."""
import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """
            ** Construct a new CPU. **
            What we need:
                - RAM
                - Register for fast memory access
                - PC iterator
                - Running state
        """
        self.running = False
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

        self.opcodes = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100010: self.MUL,
            0b10100011: self.DIV,
            0b10100000: self.ADD,
            0b10100001: self.SUB
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print(sys.argv)
            print("Usage: python ls8.py examples/filename")
            sys.exit(1)

        try:
            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        n = int(n, 2)

                    except ValueError:
                        print(f"Invalid number '{n}'")
                        sys.exit(1)

                    self.ram[address] = n
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def LDI(self):  # converts value to int
        reg_num = self.ram_read(self.pc+1)
        value = self.ram_read(self.pc+2)
        self.reg[reg_num] = value

    def PRN(self):  # prints to console
        reg_num = self.ram_read(self.pc+1)
        print(self.reg[reg_num])

    def HLT(self):
        self.running = False
        self.pc += 1

    def MUL(self):
        self.alu('MULT', self.ram_read(self.pc + 1),
                 self.ram_read(self.pc + 2))

    def SUB(self):
        self.alu('SUB', self.ram_read(self.pc + 1),
                 self.ram_read(self.pc + 2))

    def ADD(self):
        self.alu('ADD', self.ram_read(self.pc + 1),
                 self.ram_read(self.pc + 2))

    def DIV(self):
        self.alu('MULT', self.ram_read(self.pc + 1),
                 self.ram_read(self.pc + 2))

    def ram_read(self, ind):
        return self.ram[ind]

    def ram_write(self, val, ind):
        self.ram[ind] = val

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()

    def run(self):
        """
            Run the CPU ->
            While Loop
        """
        self.running = True
        self.trace()

        while self.running:
            ir = self.ram_read(self.pc)
            # print(ir)
            self.opcodes[ir]()
            number_of_operands = (ir & 0b11000000) >> 6
            how_far_to_move_pc = number_of_operands + 1
            self.pc += how_far_to_move_pc
