from .uninitialized import *
import functools
import inspect

ijvmi_addresses = {}


def set_ijvm_addresses(address_space: dict) -> None:
    """
    Set the value at one or several memory addresses to use for further operations

    :param address_space: Dict containing address-value pairs to be added to the global address space
    :return: None
    """
    global ijvm_addresses
    for address in address_space:
        ijvm_addresses[int(address)] = int(address_space[address])


ijvm_registries = {
    "SP": Uninitialized(),
    "LV": Uninitialized(),
    "CPP": Uninitialized(),
    "TOS": Uninitialized(),
    "OPC": Uninitialized(),
    "H": Uninitialized(),
    "MAR": Uninitialized(),
    "MDR": Uninitialized(),
    "PC": Uninitialized(),
    "MBR": Uninitialized(),
    "MBRU": Uninitialized(),
    "MPC": Uninitialized()
}


def set_ijvm_registries(**kwargs):
    """
    Set the values in the registries for the IJVM as a series of key=value pairs.

    Valid keys are:
    SP
    LV
    CPP
    TOS
    OPC
    H
    MAR
    MDR
    PC
    MBR
    MBRU
    MPC


    :param kwargs: key=value pairs for registries
    :return:
    """
    for key, value in kwargs.items():
        ijvm_registries[key] = value

Br = {
    0: "MDR",
    1: "PC",
    2: "MBR",
    3: "MBRU",
    4: "SP",
    5: "LV",
    6: "CPP",
    7: "TOS",
    8: "OPC"
}


def _alert(message: str) -> str:
    """
    Fill a string to 80 characters evenly on both sides with exclamation points.

    :param message: The message to be centered
    :return: Message padded by exclamation points on both sides
    """
    message = message.rjust(40 + ((len(message) + 1) // 2), '!')
    message = message.ljust(80, '!')
    return message


def reg_b(b: int) -> int:
    """
    Get the value of the registry as selected by the current value in the B registry

    :param b: The value of the B registry
    :return: The value in the registry pointed to by the B registry
    """
    if b > 8:
        print(_alert(" B HAS AN INVALID VALUE! B > 8 "))
        print(f"B is 0b{b:04b}, yielding UNDEFINED=0x{0:08X}")
        return 0
    print(f"B is 0b{b:04b} ({b}), yielding {Br[b]}=0x{ijvm_registries[Br[b]]:08X}")
    return ijvm_registries[Br[b]]


# Let's define these so it's easy to switch on them with a dict
def A(b):
    print(f"A is always H=0x{ijvm_registries['H']:08X}")
    return ijvm_registries["H"]


def B(b): return reg_b(b)


def NOTA(b): return ~A(b)


def NOTB(b): return ~reg_b(b)


def APLUSB(b): return A(b) + reg_b(b)


def APLUSBINC(b): return A(b) + reg_b(b) + 1


def AINC(b): return A(b) + 1


def BINC(b): return reg_b(b) + 1


def BMINUSA(b): return reg_b(b) - A(b)


def BDEC(b): return reg_b(b) - 1


def MINUSA(b): return -A(b)


def AANDB(b): return A(b) & reg_b(b)


def AORB(b): return A(b) | reg_b(b)


def ZERO(b): return 0


def ONE(b): return 1


def MINUSONE(b): return -1


# Then give them better names so we can print them when executing
NOTA.__name__ = "NOT A"
NOTB.__name__ = "NOT B"
APLUSB.__name__ = "A + B"
APLUSBINC.__name__ = "A + B + 1"
AINC.__name__ = "A + 1"
BINC.__name__ = "B + 1"
BMINUSA.__name__ = "B - A"
BDEC.__name__ = "B - 1"
MINUSA.__name__ = "-A"
AANDB.__name__ = "A AND B"
AORB.__name__ = "A OR B"
ZERO.__name__ = "0"
ONE.__name__ = "1"
MINUSONE.__name__ = "-1"

# Finally, define the dict
alu = {
    0b011000: A,
    0b010100: B,
    0b011010: NOTA,
    0b101100: NOTB,
    0b111100: APLUSB,
    0b111101: APLUSBINC,
    0b111001: AINC,
    0b110101: BINC,
    0b111111: BMINUSA,
    0b110110: BDEC,
    0b111011: MINUSA,
    0b001100: AANDB,
    0b011100: AORB,
    0b010000: ZERO,
    0b110001: ONE,
    0b110010: MINUSONE
}

microinstructions = {}


def ijvm(*args, **kwargs) -> None:
    """
    Queue a microinstruction to run with the IJVM architecture. The format is as follows:
    control[optional], next[optional], JAM[optional], ALU, C, Mem, B

    For arguments:

    control is the address to store the instruction

    next is the address of the instruction which should be jumped to after the instruction has been completed

    If no control or next address is specified, control is assumed to be the previous queued instruction + 1, and next
    is assumed to be control + 1. If this is the first instruction, the address is set to 0x1

    JAM is a bitmask representing control flow depending on the result of the operation. 0b1XX means select the next
    address from MBR instead of the next address in the instruction. 0bX1X means set the 9th bit of the MPC if the
    result was negative and 0bXX1 means set the 9th bit of the MPC if the result was zero.

    If no JAM is specified, it is assumed to be 0.

    ALU is a bitset representing the arithmetic operation to perform

    Bit 6 and 7 (the leftmost) of the ALU instructions are masked off and taken as shift instructions. 00 means no
    shift, x1 means shift left by 8 bits and 1x means shift right by 1 bit. The instruction 0b01110001, for instance,
    would mean fetch the number 1, and bitshift it 8 times, resulting in 0b100000000, or 256 in decimal.

    C is a bitmask representing what registries to store the result of the operation in

    Mem is a bitmask representing what to do with the primary memory. The address is stored in MAR, and the mask
    determines what to do about it. 0b1XX means WRITE from the MDR to the address at MAR. 0bX1X means FETCH the next
    instruction to the MBR from the address at MAR, and 0bXX1 means READ to the MDR from the address at MAR.

    B is a 4 bit number representing

    :param args: List of arguments, the rightmost of this is assumed to be whichever hasn't been overwritten by keywords
    :param kwargs: Keywords for addressing the various arguments
    :return: None
    """
    params = {
        "control": Uninitialized(),
        "next": Uninitialized(),
        "JAM": Uninitialized(),
        "ALU": Uninitialized(),
        "C": Uninitialized(),
        "Mem": Uninitialized(),
        "B": Uninitialized()
    }
    for keyword in kwargs:
        if keyword not in params:
            raise KeyError(f"Argument {keyword} is not a supported argument")
        params[keyword] = kwargs[keyword]
    # Insertion order is guaranteed preserved in Python >= 3.7
    remaining = [key for key in params if isinstance(params[key], Uninitialized)]
    assert len(args) <= len(remaining), "There are more arguments provided than can be accepted"
    args = [*args]
    while args:
        params[remaining.pop()] = args.pop()
    # And now for verification
    assert not any(argument in ["ALU", "C", "Mem", "B"] for argument in remaining), \
        "A minimum of ALU, C, Mem and B must be specified to queue an instruction"
    if isinstance(params["control"], Uninitialized):
        inst = tuple(microinstructions.keys())
        params["control"] = inst[-1] + 1 if inst else 1
    if isinstance(params["next"], Uninitialized):
        params["next"] = params["control"] + 1
    if isinstance(params["JAM"], Uninitialized):
        params["JAM"] = 0b000
    assert params["JAM"] <= 0b111, f"JAM is a bitmask with 3 fields and must be less than or equal to 0b111 ({0b111})"
    assert params["ALU"] <= 0b11111111, \
        f"ALU instructions are 6 bits wide with 2 extra bits for shifts and must be less than or equal to " +\
        f"0b11111111 ({0b11111111})"
    assert params["C"] <= 0b111111111, f"C is a bitmask with 9 fields and must be less than or equal to " +\
                                       f"0b111111111 ({0b111111111})"
    assert params["Mem"] <= 0b111, f"Mem is a bitmask with 3 fields and must be less than or equal to 0b111 ({0b111})"
    assert params["B"] <= 0b1111, f"B is a 4-bit number and must be less than or equal to 0b1111 ({0b1111})"
    address = params.pop("control")
    part = functools.partial(execute, *[value for _, value in params.items()])
    microinstructions[address] = part


# Let's define a couple of magic numbers here
L_SHIFT_8 = 0b10000000
R_SHIFT_1 = 0b01000000
ALU_MASK = 0b00111111
H_MASK = 0b100000000
OPC_MASK = 0b010000000
TOS_MASK = 0b001000000
CPP_MASK = 0b000100000
LV_MASK = 0b000010000
SP_MASK = 0b000001000
PC_MASK = 0b000000100
MDR_MASK = 0b000000010
MAR_MASK = 0b000000001
JMPC = 0b100
JAMN = 0b010
JAMZ = 0b001


def set_pc_mode(on : bool = False) -> None:
    """
    In some legacy exams, the C field of the instructions has no mask for PC, they only have 8 fields instead of the 9
    of the current (2020) exams. Use this function to indicate that before executing anything.

    :param on: Whether the PC field should exist or not (False = no PC field)
    :return: None
    """
    global SP_MASK, LV_MASK, CPP_MASK, TOS_MASK, OPC_MASK, H_MASK
    if on:
        H_MASK = 0b100000000
        OPC_MASK = 0b010000000
        TOS_MASK = 0b001000000
        CPP_MASK = 0b000100000
        LV_MASK = 0b000010000
        SP_MASK = 0b000001000
    else:
        H_MASK = 0b10000000
        OPC_MASK = 0b01000000
        TOS_MASK = 0b00100000
        CPP_MASK = 0b00010000
        LV_MASK = 0b00001000
        SP_MASK = 0b00000100


def execute(next, JAM, ALU, C, Mem, B):
    print(f"ALU is 0b{ALU:06b}, function: {alu[ALU & ALU_MASK].__name__}")
    num = alu[ALU & ALU_MASK](B)
    print(f"Result of operation: 0x{num:08X}")
    if ALU & L_SHIFT_8:
        print("ALU has SLL8 bit set, shifting left by 8 bits")
        num = num << 8
    if ALU & R_SHIFT_1:
        print("ALU has SLR1 bit set, shifting right by 1 bit")
        num = num >> 1
    print(f"Final result: 0x{num:08X}")
    print(f"C is 0b{C:09b}")
    if C:
        print(f"The following registries take the value of 0x{num:08X}")
    else:
        print("No registries modified! What was the point of this?")
    if C & H_MASK:
        print("H")
        ijvm_registries["H"] = num
    if C & OPC_MASK:
        print("OPC")
        ijvm_registries["OPC"] = num
    if C & TOS_MASK:
        print("TOS")
        ijvm_registries["TOS"] = num
    if C & CPP_MASK:
        print("CPP")
        ijvm_registries["CPP"] = num
    if C & LV_MASK:
        print("LV")
        ijvm_registries["LV"] = num
    if C & SP_MASK:
        print("SP")
        ijvm_registries["SP"] = num
    if C & PC_MASK:
        print("PC")
        ijvm_registries["PC"] = num
    if C & MDR_MASK:
        print("MDR")
        ijvm_registries["MDR"] = num
    if C & MAR_MASK:
        print("MAR")
        ijvm_registries["MAR"] = num

    print(f"Mem is 0b{Mem:03b}")
    if Mem & 0b001:
        print(f"FETCH! From address MAR: 0x{ijvm_registries['MAR']:08X} into registry MBR.")
        try:
            ijvm_registries["MBR"] = ijvm_addresses[ijvm_registries["MAR"]]
            print(f"MBR now contains 0x{ijvm_registries['MBR']:08X}")
        except KeyError:
            print(_alert(" Fetching from uninitialized memory! MBR not set "))
    elif Mem & 0b010:
        print(f"READ! From address MAR: 0x{ijvm_registries['MAR']:08X}")
        try:
            ijvm_registries["MDR"] = ijvm_addresses[ijvm_registries["MAR"]]
        except KeyError:
            print(_alert(f" Reading from uninitialized memory! MDR not set "))
    elif Mem & 0b100:
        print(f"WRITE! To address MAR: 0x{ijvm_registries['MAR']:08X}, MDR: 0x{ijvm_registries['MDR']:08X}")
    else:
        print("Mem is 0, don't touch memory")

    ijvm_registries["MPC"] = next
    if JAM & JMPC:
        print("JMPC bit set: Fetching next address from MBR instead of using instruction's next address field")
        ijvm_registries["MPC"] = ijvm_registries["MBR"]
    if JAM & JAMN and num < 0:
        print(f"Number 0x{num:08X} ({num}) < 0 and JAMN bit set. Setting high bit in next address")
        ijvm_registries["MPC"] |= 0b100000000
    if JAM & JAMZ and num == 0:
        print(f"Number 0x{num:08X} ({num}) == 0 and JAMZ bit set. Setting high bit in next address")
        ijvm_registries["MPC"] |= 0b100000000
    print(f"Next instruction: 0b{ijvm_registries['MPC']:09b}")
    return ijvm_registries["MPC"]


def execute_ijvm(starting_address: [int, None] = None) -> None:
    """
    Execute all the instructions that have been queued up with the ijvm() function thus far in sequence, starting
    with either the lowest address, or the optional starting_address parameter if specified.

    :param starting_address: Address to start executing from. If this is unspecified, start from the lowest
    :return: None
    """
    k = list(microinstructions.keys())
    k.sort()
    ijvm_registries["MPC"] = starting_address if starting_address else k[0]
    while ijvm_registries["MPC"] != 0:
        try:
            partial: functools.partial = microinstructions[ijvm_registries["MPC"]]
        except KeyError:

            print(_alert(f" Next instruction 0b{ijvm_registries['MPC']:09b} not set "))
            break
        memory_string = f" Instruction address: 0x{ijvm_registries['MPC']:09b} "
        print((80 - len(memory_string)) // 2 * "=", memory_string, (80 - len(memory_string)) // 2 * "=", sep='')
        arg_names = inspect.getfullargspec(partial.func).args
        argsz = {
            "next": 9,
            "JAM": 3,
            "ALU": 8,
            "C": 9,
            "Mem": 3,
            "B": 4
        }
        for i, arg in enumerate(partial.args):
            print(f"{arg_names[i]}=0b{int(arg):0{argsz[arg_names[i]]}b} ", end='')
        print('')
        ijvm_registries["MPC"] = partial()
    print(80 * '=')
    if ijvm_registries["MPC"] == 0:
        print("Next instruction is 0. We're done")
    else:
        print(f"Next instruction was at memory address 0b{ijvm_registries['MPC']:09b}, but it isn't set.")
        print("If you were simply trying to run a few instructions in a row, this is nothing to\nworry about, " +
              "but if you expected this to finish properly, you should validate\nyour input.")


def print_all_ijvm() -> None:
    """
    Print both the values in the memory addresses, and the value of every registry which has been used by a series of
    instructions.

    :return: None
    """
    print_ijvm_mem()
    print_ijvm_regs()


def print_ijvm_regs():
    """
    Print the current values of every IJVM registry

    :return: None
    """
    for key, value in ijvm_registries.items():
        print(f"{key} = 0x{value:08X}")


def print_ijvm_mem():
    """
    Print the value of every memory address used in the IJVM operations, if any were used at all

    :return: None
    """
    for address, value in ijvmi_addresses.items():
        print(f"0x{address:08X}: 0x{value:08X}")
