"""CPU functionality."""

import sys


# Machine code:

HLT = 1    # 0b00000001
LDI = 130  # 0b10000010
PRN = 71   # 0b01000111
MUL = 162  # 0b10100010
PUSH = 69  # 0b01000101
POP = 70   # 0b01000110
CALL = 80  # 0b01010000
RET = 17   # 0b00010001
ADD = 160  # 0b10100000
CMP = 167  # 0b10100111
JMP = 84   # 0b01010100
JEQ = 85   # 0b01010101
JNE = 86   # 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # holds 256 bytes of memory
        self.reg = [0] * 8 # 8 general-purpose registers
        self.pc = 0 # Program Counter, address of the currently executing instruction

        self.sp = 7 # Stack Pointer Location is register 7
        self.reg[self.sp] = 0xf4 # 244 # Stack Pointer

        self.fl = 6 # Flag Location is register 6
        self.reg[self.fl] = 0b00000000 # Flag register - `FL` bits: `00000LGE`


    def load(self,filename):
        """Load a program into memory."""

        try:
            address = 0

            with open(filename) as f:
                for line in f:
                    # Process comments:
                    # Ignore anything after a # symbol
                    comment_split = line.split("#") # splits the line at the # symbol
                    # takes the first part of the split
                    num = comment_split[0].strip() # strip() removes all leading and trailing whitespace

                    if num == "": # if blank line, continue
                        continue
                    
                    # Convert any numbers from binary strings to integers
                    try:
                        val = int(num, 2)
                    except ValueError:
                        continue
                    # adds the value to the memory
                    self.ram[address] = val
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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


    # should accept the address to read and return the value stored there.
    def ram_read(self, address):
        return self.ram[address]


    # should accept a value to write, and the address to write it to.
    def ram_write(self, address, value):
        self.ram[address] = value


    def run(self):
        """Run the CPU."""

        running = True

        while running:
            # read the memory address that's stored in register `PC`, and store that result in `IR`
            # Instruction Register, contains a copy of the currently executing instruction
            ir = self.ram_read(self.pc)

            # Using `ram_read()`, read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and `operand_b` in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # exit the loop if a `HLT` instruction is encountered
            # Halt the CPU (and exit the emulator)
            if ir == HLT:
                print("HLT")
                running = False
                self.pc += 1
                sys.exit(1)

            
            # Set the value of a register to an integer
            elif ir == LDI:
                print("LDI")
                self.reg[operand_a] = operand_b
                # print(self.reg[operand_a])
                self.pc += 3


            # Print numeric value stored in the given register
            # Print to the console the decimal integer value that is stored in the given register
            elif ir == PRN:
                print("PRN")
                print(self.reg[operand_a])
                self.pc += 2


            # Multiply the values in two registers together and store the result in registerA
            elif ir == MUL:
                print("MUL")
                # print(self.reg[operand_a])
                # print(self.reg[operand_b])
                self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
                self.pc += 3

            # Push the value in the given register on the stack
            elif ir == PUSH:
                print("PUSH")
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                # Decrement the Stack Pointer
                self.reg[self.sp] -= 1
                # Copy the value in the given register to the address pointed to by Stack Pointer
                self.ram[self.reg[self.sp]] = val
                self.pc += 2

            elif ir == POP:
                print("POP")
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[self.sp]]
                # Copy the value from the address pointed to by SP to the given register.
                self.reg[reg] = val
                # Increment SP.
                self.reg[self.sp] += 1
                self.pc += 2

            elif ir == CALL:
                print("CALL")
                # Push the return address on the stack
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2

                # The PC is set to the address stored in the given register
                reg = self.ram[self.pc +1]
                # We jump to that location in RAM and execute the first instruction in the subroutine
                self.pc = self.reg[reg]

            elif ir == RET:
                # Return from the subroutine
                # Pop the value from the top of the stack and store it in the PC
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1

            elif ir == ADD:
                print("ADD")
                self.reg[operand_a] = self.reg[operand_a] + self.reg[operand_b]
                self.pc += 3

            elif ir == CMP: # Compare the values in two registers
                print("CMP")
                # If they are equal, set the Equal `E` flag to 1
                if self.reg[operand_a] == self.reg[operand_b]:
                    print("EQUALS")
                    self.reg[self.fl] = 0b00000001
                # If registerA is less than registerB, set the Less-than `L` flag to 1
                elif self.reg[operand_a] < self.reg[operand_b]:
                    print("LESS THAN")
                    self.reg[self.fl] = 0b00000100
                # If registerA is greater than registerB, set the Greater-than `G` flag to 1
                elif self.reg[operand_a] > self.reg[operand_b]:
                    print("GREATER THAN")
                    self.reg[self.fl] = 0b00000010

                self.pc += 3

            # Jump to the address stored in the given register
            elif ir == JMP:
                print("JMP")
                # Set the `PC` to the address stored in the given register
                self.pc = self.reg[operand_a]


            elif ir == JEQ:
                print("JEQ")
                # If `equal` flag is set (true), jump to the address stored in the given register
                if self.reg[self.fl] == 0b00000001:
                    print("JEQ True")
                    self.pc = self.reg[operand_a]

                else:
                    print("JEQ False")
                    self.pc += 2


            elif ir == JNE:
                print("JNE")
                # If `E` flag is clear (false, 0), jump to the address stored in the given register
                if self.reg[self.fl] != 0b00000001:
                    print("JNE True")
                    self.pc = self.reg[operand_a]
                else:
                    print("JNE False")
                    self.pc += 2



            else:
                print(f"Unknown instruction: {ir}")
                sys.exit(1)
        
