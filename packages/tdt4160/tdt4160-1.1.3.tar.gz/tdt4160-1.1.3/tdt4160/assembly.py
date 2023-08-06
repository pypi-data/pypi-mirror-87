import functools
import inspect
import sys
from .uninitialized import *


class Reg:
    """
    Registry class. Although it's a bit inconvenient to force passing this class, it's VERY convenient to be able to
    pass things by reference and to keep a name for the registry.
    """

    def __init__(self, name: str, val: [int, Uninitialized]) -> None:
        """
        Initialize the registry object.

        :param name: What you want the registry to be called when using it
        :param val: The value the registry contains
        """
        self.val = int(val)
        self.name = name

    """
    Not all arithmetic operators are implemented to hopefully avoid seemingly innocuous assignments like R0 = R2 + R3,
    which wouldn't work while keeping the name field. Unary operators are implemented because they have no ambiguity in
    regards to the name.
    """

    def __abs__(self):
        copy = Reg(self.name, abs(self.val))
        return copy

    def __bool__(self) -> bool:
        return bool(self.val)

    def __ceil__(self):
        copy = Reg(self.name, self.val.__ceil__())
        return copy

    def __divmod__(self, other: any) -> [int, int]:
        return divmod(self.val, other)

    def __eq__(self, other: any) -> bool:
        return self.val == other

    def __float__(self) -> float:
        return float(self.val)

    def __floor__(self):
        copy = Reg(self.name, self.val.__floor__())
        return copy

    def __format__(self, fmt: str) -> str:
        """
        Must be implemented in order to format with arbitrary f-strings.

        :param fmt: Format string to use
        :return: Formatted string
        """
        return f"{self.val:{fmt}}"

    def __ge__(self, other: any) -> bool:
        return self.val >= other

    def __gt__(self, other: any) -> bool:
        return self.val > other

    def __index__(self) -> int:
        """
        Used for indexing and in functions for coercion, such as if you wanted to call, say, oct() or bin() on the
        registry.

        :return: Integer value in registry
        """
        return self.__int__()

    def __int__(self) -> int:
        return self.val

    def __invert__(self):
        copy = Reg(self.name, ~self.val)
        return copy

    def __le__(self, other: any) -> bool:
        return self.val <= other

    def __lt__(self, other) -> bool:
        return self.val < other

    def __ne__(self, other) -> bool:
        return self.val != other

    def __neg__(self):
        copy = Reg(self.name, self.val.__neg__())
        return copy

    def __pos__(self):
        copy = Reg(self.name, self.val.__pos__())
        return copy

    def __rdivmod__(self, other):
        return self.val.__rdivmod__(other)

    def __repr__(self) -> str:
        """
        Hex is probably more expected here than decimal is, so using that as the string value.

        :return: The value of the registry as a hexadecimal number
        """
        return str(self)

    def __round__(self, n=None):
        copy = Reg(self.name, self.val.__round__(n))
        return copy

    def __str__(self) -> str:
        """
        Hex is probably more expected here than decimal is, so using that as the string value.

        :return: The value of the registry as a hexadecimal number
        """
        return f"0x{self.val:08X}"

    def __trunc__(self):
        copy = Reg(self.name, self.val.__trunc__())
        return copy

    @property
    def val(self) -> int:
        return self._val

    @val.setter
    def val(self, value) -> None:
        self._val = value


assembly_sequence: {int, functools.partial} = {}
asm_addresses: {int, int} = {}
Zflag: Reg = Reg("Z-flag", 0)
return_stack: list = []
touched_registries = {}


def set_asm_addresses(address_space: dict) -> None:
    """
    Set the value at one or several memory addresses to use for further operations

    :param address_space: Dict containing address-value pairs to be added to the global address space
    :return: None
    """
    global asm_addresses
    for address in address_space:
        asm_addresses[int(address)] = int(address_space[address])


# Initializing these to uninitialized, so you don't have to care about them if they don't have a value yet
R0 = Reg("R0", Uninitialized())
R1 = Reg("R1", Uninitialized())
R2 = Reg("R2", Uninitialized())
R3 = Reg("R3", Uninitialized())
R4 = Reg("R4", Uninitialized())
R5 = Reg("R5", Uninitialized())
R6 = Reg("R6", Uninitialized())
R7 = Reg("R7", Uninitialized())
R8 = Reg("R8", Uninitialized())
R9 = Reg("R9", Uninitialized())
R10 = Reg("R10", Uninitialized())
R11 = Reg("R11", Uninitialized())
R12 = Reg("R12", Uninitialized())
R13 = Reg("R13", Uninitialized())
R14 = Reg("R14", Uninitialized())
R15 = Reg("R15", Uninitialized())
R16 = Reg("R16", Uninitialized())
R17 = Reg("R17", Uninitialized())
R18 = Reg("R18", Uninitialized())
R19 = Reg("R19", Uninitialized())
R20 = Reg("R20", Uninitialized())
R21 = Reg("R21", Uninitialized())
R22 = Reg("R22", Uninitialized())
R23 = Reg("R23", Uninitialized())
R24 = Reg("R24", Uninitialized())
R25 = Reg("R25", Uninitialized())
R26 = Reg("R26", Uninitialized())
R27 = Reg("R27", Uninitialized())
R28 = Reg("R28", Uninitialized())
R29 = Reg("R29", Uninitialized())
R30 = Reg("R30", Uninitialized())
R31 = Reg("R31", Uninitialized())


def set_asm_registries(**kwargs) -> None:
    """
    Set the value of the registries to use in operations. Use this to ensure they stay a registry class and accessible
    on a module level

    :param kwargs: key=value pair of registries, e.g R0=0x00000001
    :return: None
    """
    for reg in kwargs:
        real_reg = getattr(sys.modules[__name__], reg)
        real_reg.val = kwargs[reg]


def LOAD(Ri: Reg, Rj: Reg) -> None:
    """
    Load a value from the primary memory address pointed to by the registry Rj into the registry Ri.

    :param Ri: The registry the value in memory should be loaded into
    :param Rj: The registry containing the memory address the value in memory should be loaded from
    :return: None
    """
    Ri.val = asm_addresses[Rj.val]
    print(f"Loaded value {Ri.val:08X} into {Ri.name} from address {Rj.val:08X}")
    return None


def STORE(Ri: Reg, Rj: Reg) -> None:
    """
    Store the value contained in the registry Ri into the primary memory address pointed to by the registry Rj.

    :param Ri: The registry containing the value which should be stored
    :param Rj: The registry containing the memory address the value should be stored at
    :return: None
    """
    asm_addresses[Rj.val] = Ri.val
    print(f"Stored value {Ri.val:08X} into address {Rj.val:08X}")
    return None


def ADD(Ri: Reg, Rj: Reg, Rk: Reg) -> None:
    """
    Add the values stored in the registry Rj and the registry Rk together and store the result in the registry Ri.

    As with all arithmetic operations, sets the Z-flag if the result of this operation is 0. Otherwise, clears it.

    :param Ri: The registry to store the result of the operation in
    :param Rj: Registry containing the left hand operand
    :param Rk: Registry containing the right hand operand
    :return: None
    """
    print(f"Added {Rj.name}={Rj.val:08X}+{Rk.name}={Rk.val:08X}")
    Ri.val = Rj.val + Rk.val
    Zflag.val = 0
    if Ri.val == 0:
        Zflag.val = 1
    print(f"Result {Ri.val:08X} stored in {Ri.name}")
    return None


def NAND(Ri: Reg, Rj: Reg, Rk: Reg) -> None:
    """
    Perform a bitwise NAND between the values stored in the registry Rj and the registry Rk and store the result in the
    registry Ri.

    As with all arithmetic operations, sets the Z-flag if the result of this operation is 0. Otherwise, clears it.

    :param Ri: The registry to store the result of the operation in
    :param Rj: Registry containing the left hand operand
    :param Rk: Registry containing the right hand operand
    :return: None
    """
    print(f"Bitwise NAND with ~({Rj.name}={Rj.val:08X}&{Rk.name}={Rk.val:08X})")
    Ri.val = ~(Rj.val & Rk.val)
    Zflag.val = 0
    if Ri.val == 0:
        Zflag.val = 1
    print(f"Result {Ri.val:08X} stored in {Ri.name}")
    return None


def AND(Ri: Reg, Rj: Reg, Rk: Reg) -> None:
    """
    Perform a bitwise AND between the values stored in the registry Rj and the registry Rk and store the result in the
    registry Ri.

    As with all arithmetic operations, sets the Z-flag if the result of this operation is 0. Otherwise, clears it.

    :param Ri: The registry to store the result of the operation in
    :param Rj: Registry containing the left hand operand
    :param Rk: Registry containing the right hand operand
    :return: None
    """
    print(f"Bitwise AND with {Rj.name}={Rj.val:08X}&{Rk.name}={Rk.val:08X}")
    Ri.val = Rj.val & Rk.val
    Zflag.val = 0
    if Ri.val == 0:
        Zflag.val = 1
    print(f"Result {Ri.val:08X} stored in {Ri.name}")
    return None


def OR(Ri: Reg, Rj: Reg, Rk: Reg) -> None:
    """
    Perform a bitwise OR between the values stored in the registry Rj and the registry Rk and store the result in the
    registry Ri.

    As with all arithmetic operations, sets the Z-flag if the result of this operation is 0. Otherwise, clears it.

    :param Ri: The registry to store the result of the operation in
    :param Rj: Registry containing the left hand operand
    :param Rk: Registry containing the right hand operand
    :return: None
    """
    print(f"Bitwise OR with {Rj.name}={Rj.val:08X}|{Rk.name}={Rk.val:08X}")
    Ri.val = Rj.val | Rk.val
    Zflag.val = 0
    if Ri.val == 0:
        Zflag.val = 1
    print(f"Result {Ri.val:08X} stored in {Ri.name}")
    return None


def NOR(Ri: Reg, Rj: Reg, Rk: Reg) -> None:
    """
    Perform a bitwise NOR between the values stored in the registry Rj and the registry Rk and store the result in the
    registry Ri.

    As with all arithmetic operations, sets the Z-flag if the result of this operation is 0. Otherwise, clears it.

    :param Ri: The registry to store the result of the operation in
    :param Rj: Registry containing the left hand operand
    :param Rk: Registry containing the right hand operand
    :return: None
    """
    print(f"Bitwise NOR with ~({Rj.name}={Rj.val:08X}|{Rk.name}={Rk.val:08X})")
    Ri.val = ~(Rj.val | Rk.val)
    Zflag.val = 0
    if Ri.val == 0:
        Zflag.val = 1
    print(f"Result {Ri.val:08X} stored in {Ri.name}")


def INV(Ri: Reg, Rj: Reg) -> None:
    """
    Perform a bitwise inversion on the value stored in the registry Rj and store the result in the registry Ri.

    As with all arithmetic operations, sets the Z-flag if the result of this operation is 0. Otherwise, clears it.

    :param Ri: The registry to store the result in
    :param Rj: The registry containing the value to invert
    :return: None
    """
    print(f"Logical INV with {Rj.name}=~{Rj.val:08X}")
    Ri.val = (~Rj.val & 0xFFFFFFFF)  # Ensure 32 bits, Python uses some weird "number" thing
    Zflag.val = 0
    if Ri.val == 0:
        Zflag.val = 1
    print(f"Result {Ri.val:08X} stored in {Ri.name}")
    return None


def INC(Ri: Reg, Rj: Reg) -> None:
    """
    Increment the value stored in the registry Rj by one and store the result in the registry Ri.

    As with all arithmetic operations, sets the Z-flag if the result of this operation is 0. Otherwise, clears it.

    :param Ri: The registry to store the result in
    :param Rj: The registry containing the value to increment by one
    :return: None
    """
    print(f"Increment with {Rj.name}={Rj.val:08X} + 1")
    Ri.val = Rj.val + 1
    Zflag.val = 0
    if Ri.val == 0:
        Zflag.val = 1
    print(f"Result {Ri.val:08X} stored in {Ri.name}")
    return None


def DEC(Ri: Reg, Rj: Reg) -> None:
    """
    Decrement the value stored in the registry Rj by one and store the result in the registry Ri.

    As with all arithmetic operations, sets the Z-flag if the result of this operation is 0. Otherwise, clears it.

    :param Ri: The registry to store the result in
    :param Rj: The registry containing the value to decrement by one
    :return: None
    """
    print(f"Decrement with {Rj.name}={Rj.val:08X} - 1")
    Ri.val = (Rj.val - 1) & 0xFFFFFFFF
    Zflag.val = 0
    if Ri.val == 0:
        Zflag.val = 1
    print(f"Result {Ri.val:08X} stored in {Ri.name}")
    return None


def MUL(Ri: Reg, Rj: Reg, Rk: Reg) -> None:
    """
    Multiply the values stored in the registry Rj and the registry Rk together and store the result in the registry Ri.

    As with all arithmetic operations, sets the Z-flag if the result of this operation is 0. Otherwise, clears it.

    :param Ri: The registry to store the result of the operation in
    :param Rj: Registry containing the left hand operand
    :param Rk: Registry containing the right hand operand
    :return: None
    """
    print(f"Multiplied {Rj.name}={Rj.val:08X}*{Rk.name}={Rk.val:08X}")
    Ri.val = Rj.val * Rk.val
    Zflag.val = 0
    if Ri.val == 0:
        Zflag.val = 1
    print(f"Result {Ri.val:08X} stored in {Ri.name}")
    return None


def CMP(Ri: Reg, Rj: Reg) -> None:
    """
    Compare the values in the registry Ri and Rj. Sets the Z-flag if they are equal, otherwise, clears it.

    :param Ri: Registry containing the left hand operand
    :param Rj: Registry containing the right hand operand
    :return: None
    """
    Zflag.val = 0
    if Ri.val == Rj.val:
        print(f"{Ri.name}={Ri:08X} is EQUAL TO {Rj.name}={Rj:08X}")
        print("Z-flag set")
        Zflag.val = 1
    else:
        print(f"{Ri.name}={Ri:08X} is NOT EQUAL TO {Rj.name}={Rj:08X}")
    return None


def CP(Ri: Reg, Rj: Reg) -> None:
    """
    Copy the value in the registry Rj into the registry Ri.

    :param Ri: The registry to copy the value to
    :param Rj: The registry to copy the value from
    :return: None
    """
    print(f"Copied value of {Rj.name}={Rj.val:08X} into {Ri.name}")
    Ri.val = Rj.val
    return None


def NOP() -> None:
    """
    Do nothing. In real life, this would be used to cause delays. Here it has no effect.

    :return: None
    """
    print("NOP")
    return None


def MOVC(Ri: Reg, constant: [int, Reg]) -> None:
    """
    Move the constant value into the registry Ri.

    :param Ri: The registry to store the value in
    :param constant: The value itself
    :return: None
    """
    # Note, the instance thing is an implementation detail to better be able to print variables during command execution
    # This function is REALLY only supposed to take constant integer values, not other registries
    Ri.val = constant.val if isinstance(constant, Reg) else constant
    Ri.val &= 0xFFFFFFFF
    print(f"Moved value {Ri.val:08X} into {Ri.name}")
    return None


def BZ(Ri: Reg) -> [int, None]:
    """
    Branch to the instruction pointed to by the registry Ri if the Z-flag was set in the previous operation.

    :param Ri: The registry containing the value of the memory address to potentially branch to
    :return: None if there is no branching, otherwise the address to branch to
    """
    print(f"Branch to {Ri.name}={Ri.val:08X} if last operation set the Z-flag (result was 0)")
    if Zflag.val:
        return Ri.val
    return None


def BNZ(Ri: Reg) -> [int, None]:
    """
    Branch to the instruction pointed to by the registry Ri if the Z-flag was cleared in the previous operation.


    :param Ri: The registry containing the value of the memory address to potentially branch to
    :return: None if there is no branching, otherwise the address to branch to
    """

    print(f"Branch to {Ri.name}={Ri.val:08X} if last operation did not set the Z-flag (result was not 0)")
    if not Zflag.val:
        return Ri.val
    return None


def RT() -> int:
    """
    Return from a function call. There's no way to push any kind of return address or read a registry here, so this will
    always throw for now, but theoretically you'd be able to push a return address on the stack, go do a function, then
    return with this instruction.

    :return: The top of the return stack
    """
    print("RETURN TRIGGERED!")
    return return_stack.pop()


def assemble(*args) -> None:
    """
    Queue an instruction to be executed at a later time. Can optionally take an address, which is required if the
    sequence includes branching to specific addresses. If no address is provided, use the last provided address + 1. If
    no addresses have been provided before, start at 0.

    :param args: An optional address, a function to execute, and its arguments as a SINGLE argument (like a tuple/list)
    :return: None
    """
    assert_string = f"The function must be in the form {assemble.__name__}(address, INSTRUCTION, (operands)) or \
                      in the form {assemble.__name__}(INSTRUCTION, (operands))"
    assert len(args) >= 1, assert_string
    if callable(args[0]):
        func = args[0]
        instructions = tuple(assembly_sequence.keys())
        address = instructions[-1] + 1 if instructions else 0
        validate = args[1:]
    else:
        assert len(args) >= 2, assert_string
        assert isinstance(args[0], int), assert_string
        assert callable(args[1]), assert_string
        address = args[0]
        func = args[1]
        validate = args[2:]

    # Flatten the args and validate them
    def flatten(container):
        for item in container:
            if hasattr(item, "__iter__") and not isinstance(item, str):
                for sub in flatten(item):
                    yield sub
            else:
                yield item

    validate = list(flatten(validate))
    arguments = [arg if isinstance(arg, Reg) else Reg("Constant", arg) for arg in validate]
    arg_amount = len(inspect.signature(func).parameters)
    assert len(arguments) == arg_amount, f"The instruction {func.__name__} has {arg_amount} " + \
                                         f"operand{'s' if arg_amount > 1 else ''}, not {len(arguments)}"
    assembly_sequence[address] = functools.partial(func, *arguments)


def execute_assembly(starting_address: [int, None] = None) -> None:
    """
    Execute all the instructions that have been queued up with the instruction() function thus far in sequence, starting
    with either the lowest address, or the optional starting_address parameter if specified.

    :return: None
    """
    k = list(assembly_sequence.keys())
    k.sort()
    upper = k[-1]
    index = starting_address if starting_address else k[0]
    while index <= upper:
        partial: functools.partial = assembly_sequence[index]
        memory_string = f" MEMORY: {index:08X} "
        print((80 - len(memory_string)) // 2 * "=", memory_string, (80 - len(memory_string)) // 2 * "=", sep='')
        arg_list = [f"{arg.name}={arg:08X}" for arg in partial.args]
        arg_str = ", ".join(arg_list)
        print(f"INSTRUCTION: {partial.func.__name__} {arg_str}")
        res = partial()
        for arg in partial.args:
            # Clamp the values to 32-bit numbers, even negative ones
            arg.val &= 0xFFFFFFFF
            touched_registries[arg.name] = arg
        index += 1
        if res is not None:
            print(f"Branch detected, jumping to: {res:08X}")
            index = res
    print(80 * '=')


def clear_memory() -> None:
    """
    Clear module variables to start again. Clears any queued instructions, any set main memory addresses, clears the
    Z-flag and clears the return stack

    :return: None
    """
    global assembly_sequence, asm_addresses, Zflag, return_stack
    assembly_sequence = {}
    asm_addresses = {}
    Zflag = Reg("Z-flag", 0)
    return_stack = []


def print_all_asm() -> None:
    """
    Print both the values in the memory addresses, and the value of every registry which has been used by a series of
    instructions.

    :return: None
    """
    print_asm_mem()
    print_asm_regs()


def print_asm_regs() -> None:
    """
    Print the value of every registry which has been used in a series of instructions.

    :return: None
    """
    touched_registries.pop("Constant", None)  # Not a real registry
    regs = list(touched_registries.keys())
    regs.sort(key=lambda reggie: int(reggie[1:]))
    for reg in regs:
        print(f"{reg.ljust(3, ' ')} = 0x{touched_registries[reg]:08X}")


def print_asm_mem():
    """
    Print the value in every memory address after a series of instructions.

    :return:
    """
    for address, value in asm_addresses.items():
        print(f"0x{address:08X}: 0x{value:08X}")
