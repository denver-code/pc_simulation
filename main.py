class RAM:
    def __init__(self, size):
        self.size = size
        self.memory = [0] * size

    def read(self, address):
        if address < 0 or address >= self.size:
            raise ValueError(f"Address {address} is out of bounds.")
        return self.memory[address]

    def write(self, address, value):
        if address < 0 or address >= self.size:
            raise ValueError(f"Address {address} is out of bounds.")
        if not (0 <= value < 256):  # 8-bit value
            raise ValueError(f"Invalid value: {value}. Must be an 8-bit integer.")
        self.memory[address] = value

    def dump(self, start=0, length=16):
        """Print the contents of RAM from a given start address, for debugging."""
        end = min(start + length, self.size)
        return [f"{x:08b}" for x in self.memory[start:end]]  # Display as binary


class LogicGates:
    @staticmethod
    def AND(a, b):
        return a & b

    @staticmethod
    def OR(a, b):
        return a | b

    @staticmethod
    def NOT(a):
        return ~a & 0xFF  # Mask to 8 bits

    @staticmethod
    def NAND(a, b):
        return LogicGates.NOT(LogicGates.AND(a, b))

    @staticmethod
    def NOR(a, b):
        return LogicGates.NOT(LogicGates.OR(a, b))

    @staticmethod
    def XOR(a, b):
        return a ^ b


class CPU:
    def __init__(self, ram: RAM, verbose: bool = False):
        self.ram = ram
        self.registers = [0] * 8  # 8 registers
        self.logic_gates = LogicGates()
        self.verbose = verbose

    def execute(self, instruction):
        # Remove comments and strip whitespace
        parts = instruction.split(";")[0].strip().split()
        if not parts:
            return True  # Skip empty instructions

        opcode = parts[0]

        if opcode == "LOAD":
            if len(parts) != 3:
                raise ValueError(f"LOAD instruction must have 3 parts: {instruction}")
            _, reg, address = parts
            reg_index = int(reg[1])  # R0, R1, etc.
            self.registers[reg_index] = self.ram.read(
                int(address[1:-1], 16)
            )  # Remove brackets
            if self.verbose:
                print(f"LOAD: Loaded R{reg_index} = {self.registers[reg_index]:08b}")

        elif opcode == "VER":
            if len(parts) != 3:
                raise ValueError(f"VER instruction must have 2 parts: {instruction}")
            _, _, verbose_value = parts
            verbose_value = int(verbose_value)

            if verbose_value not in [1, 0]:
                raise ValueError(f"VER instruction must contain 1 or 0: {instruction}")

            self.verbose = bool(verbose_value)

            if self.verbose:
                print(f"VER: VER = {verbose_value} -> SET")

        elif opcode == "ADD":
            if len(parts) != 4:
                raise ValueError(f"ADD instruction must have 4 parts: {instruction}")
            _, r1, r2, r3 = parts
            r1_val = self.registers[int(r1[1])]
            r2_val = self.registers[int(r2[1])]
            self.registers[int(r3[1])] = (
                r1_val + r2_val
            ) % 256  # Simulating 8-bit overflow
            if self.verbose:
                print(
                    f"ADD: R{r1[1]} + R{r2[1]} = R{r3[1]} -> {self.registers[int(r3[1])]:08b}"
                )

        elif opcode == "STORE":
            if len(parts) != 3:
                raise ValueError(f"STORE instruction must have 3 parts: {instruction}")
            _, reg, address = parts
            reg_index = int(reg[1])
            self.ram.write(
                int(address[1:-1], 16), self.registers[reg_index]
            )  # Remove brackets
            if self.verbose:
                print(
                    f"STORE: R{reg[1]} stored at {address} -> {self.registers[reg_index]:08b}"
                )

        elif opcode == "INIT":
            # Format: INIT [address] = [value]
            if len(parts) != 4 or parts[2] != "=":
                raise ValueError(
                    f"INIT instruction must be in format INIT [address] = [value]: {instruction}"
                )
            _, address, _, value = parts  # Get the address and value
            self.ram.write(
                int(address[1:-1], 16), int(value.strip(), 2)
            )  # Remove brackets and write binary value
            if self.verbose:
                print(f"INIT: Set memory {address} to {value.strip()} (binary)")

        elif opcode == "CLEAR":
            if len(parts) != 2:
                raise ValueError(f"CLEAR instruction must have 2 parts: {instruction}")
            _, address = parts

            if address.startswith("R"):
                reg = int(address[1])
                self.registers[reg] = 0

                return
            
            self.ram.write(
                int(address[1:-1], 16), 0
            )  # Clear memory at the specified address
            if self.verbose:
                print(f"CLEAR: Cleared memory at {address}")

        elif opcode == "OUT":
            if len(parts) != 2:
                raise ValueError(f"OUT instruction must have 2 parts: {instruction}")
            _, value = parts
            if value.startswith("R"):
                reg = int(value[1])

                out_message = f"REG R{reg}={self.registers[reg]:08b}"
            else:
                value = int(value, 2)
                out_message = f"Value {value:08b}"

            print(f"OUT: {out_message}")  # Print in binary

        elif opcode == "HALT":
            return False

        elif opcode == "AND":
            if len(parts) != 4:
                raise ValueError(f"AND instruction must have 4 parts: {instruction}")
            _, r1, r2, r3 = parts
            self.registers[int(r3[1])] = self.logic_gates.AND(
                self.registers[int(r1[1])], self.registers[int(r2[1])]
            )

            if self.verbose:
                print(
                    f"AND: R{r1[1]} AND R{r2[1]} = R{r3[1]} -> {self.registers[int(r3[1])]:08b}"
                )

        elif opcode == "OR":
            if len(parts) != 4:
                raise ValueError(f"OR instruction must have 4 parts: {instruction}")
            _, r1, r2, r3 = parts
            self.registers[int(r3[1])] = self.logic_gates.OR(
                self.registers[int(r1[1])], self.registers[int(r2[1])]
            )
            if self.verbose:
                print(
                    f"OR: R{r1[1]} OR R{r2[1]} = R{r3[1]} -> {self.registers[int(r3[1])]:08b}"
                )

        elif opcode == "NOT":
            if len(parts) != 3:
                raise ValueError(f"NOT instruction must have 3 parts: {instruction}")
            _, reg, target_reg = parts
            self.registers[int(target_reg[1])] = self.logic_gates.NOT(
                self.registers[int(reg[1])]
            )
            if self.verbose:
                print(
                    f"NOT: R{reg[1]} -> R{target_reg[1]} -> {self.registers[int(target_reg[1])]:08b}"
                )

        elif opcode == "NAND":
            if len(parts) != 4:
                raise ValueError(f"NAND instruction must have 4 parts: {instruction}")
            _, r1, r2, r3 = parts
            self.registers[int(r3[1])] = self.logic_gates.NAND(
                self.registers[int(r1[1])], self.registers[int(r2[1])]
            )
            if self.verbose:
                print(
                    f"NAND: R{r1[1]} NAND R{r2[1]} = R{r3[1]} -> {self.registers[int(r3[1])]:08b}"
                )

        elif opcode == "NOR":
            if len(parts) != 4:
                raise ValueError(f"NOR instruction must have 4 parts: {instruction}")
            _, r1, r2, r3 = parts
            self.registers[int(r3[1])] = self.logic_gates.NOR(
                self.registers[int(r1[1])], self.registers[int(r2[1])]
            )
            if self.verbose:
                print(
                    f"NOR: R{r1[1]} NOR R{r2[1]} = R{r3[1]} -> {self.registers[int(r3[1])]:08b}"
                )

        elif opcode == "XOR":
            if len(parts) != 4:
                raise ValueError(f"XOR instruction must have 4 parts: {instruction}")
            _, r1, r2, r3 = parts
            self.registers[int(r3[1])] = self.logic_gates.XOR(
                self.registers[int(r1[1])], self.registers[int(r2[1])]
            )
            if self.verbose:
                print(
                    f"XOR: R{r1[1]} XOR R{r2[1]} = R{r3[1]} -> {self.registers[int(r3[1])]:08b}"
                )

        elif opcode == "IF":
            if "THEN" not in instruction:
                raise ValueError(f"IF instruction must contain THEN: {instruction}")

            condition, then_clause = instruction.split("THEN")
            condition = condition.strip()
            then_clause = then_clause.strip()

            # Check for ELSE in the THEN clause
            if "ELSE" in then_clause:
                then_clause, else_clause = then_clause.split("ELSE")
                then_clause = then_clause.strip()
                else_clause = else_clause.strip()
            else:
                else_clause = None

            condition_parts = condition.split()

            if len(condition_parts) != 4 or condition_parts[2] not in (
                "==",
                "!=",
                ">",
                "<",
                ">=",
                "<=",
            ):
                raise ValueError(f"Invalid IF condition: {condition.strip()}")

            _, reg1, operator, value = condition_parts
            reg1_value = self.registers[int(reg1[1])]

            if value.startswith("R"):
                value = self.registers[int(value[1])]
            elif value.startswith("["):
                value = self.ram.read(int(value[1:-1], 16))
            else:
                value = int(value, 2)

            # Evaluate the condition
            condition_met = False
            if operator == "==":
                condition_met = reg1_value == value
            elif operator == "!=":
                condition_met = reg1_value != value
            elif operator == ">":
                condition_met = reg1_value > value
            elif operator == "<":
                condition_met = reg1_value < value
            elif operator == ">=":
                condition_met = reg1_value >= value
            elif operator == "<=":
                condition_met = reg1_value <= value

            if condition_met:
                if self.verbose:
                    print(
                        f"IF condition met: {reg1} {operator} {value:08b}, executing {then_clause}"
                    )
                self.execute(then_clause)
            elif else_clause:
                if self.verbose:
                    print(f"IF condition not met, executing ELSE clause: {else_clause}")
                self.execute(else_clause)
            else:
                if self.verbose:
                    print(
                        f"IF condition not met: {reg1} {operator} {value:08b}, skipping THEN clause"
                    )

        else:
            raise ValueError(f"Unknown instruction: {instruction}")

        return True

    def run(self, program):
        for instruction in program:
            instruction = instruction.strip()  # Remove leading/trailing whitespace
            if not instruction:  # Skip empty lines
                continue
            if not self.execute(instruction):
                break


class BIOS:
    def __init__(self, cpu):
        self.cpu = cpu

    def prompt(self):
        while True:
            command = input("BIOS> ")
            if command == "exit":
                break

            elif command.startswith("address"):
                parts = command.split(" ")
                if len(parts) != 2:
                    print("Please enter the address you'd like to gather!")
                    return

                print(
                    f"Value at address {parts[1]}: {self.cpu.ram.read(int(parts[1], 16)):08b}"
                )

            elif command.startswith("memory_dump"):
                parts = command.split()

                dump = self.cpu.ram.dump(length=256)

                if "not-empty" in parts:
                    not_empty_values = []
                print("Memory Dump:\n" + "\n".join(dump))

            elif command.endswith(".asm"):
                self.run_program(command)

    def run_program(self, filename):
        try:
            with open(filename, "r") as file:
                program = file.readlines()
            program = [
                line.strip() for line in program if line.strip()
            ]  # Remove empty lines
            print(f"Running program: {filename}")
            self.cpu.run(program)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")


class PowerSupply:
    def __init__(self, motherboard):
        self.motherboard = motherboard

    def power_on(self):
        print("Powering on the system...")
        self.motherboard.power_on()


class Motherboard:
    def __init__(self, ram, cpu):
        self.ram = ram
        self.cpu = cpu

    def power_on(self):
        print("System Powered On")
        bios = BIOS(self.cpu)
        bios.prompt()


if __name__ == "__main__":
    ram_size = 256
    ram = RAM(ram_size)
    cpu = CPU(ram)
    motherboard = Motherboard(ram, cpu)
    power_supply = PowerSupply(motherboard)

    power_supply.power_on()
