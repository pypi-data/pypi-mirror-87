# TDT4160 1.1.0

`tdt4160` is an emulator for IJVM-microinstructions and pseudo-assembly, as 
is commonly seen in the [NTNU subject TDT4160](https://www.ntnu.no/studier/emner/TDT4160),
particularly on its exams.

There are two main components to this package. `tdt4160.assembly` and `tdt4160.ijvm`.
Both function by letting you set registries, memory addresses and queue instructions
before executing them. During execution, each individual instruction is stepped through,
with lots of information printed so you can easily see what's going on. Technically
requires Python >= 3.7 to be conformant, but should probably work with any version >= 3.6. 
There are no external dependencies besides the standard library.

[View on PyPI](http://pypi.python.org/pypi/tdt4160) |
[Fork me on gitgud](https://gitgud.io/fish/tdt4160)


## Installation

To install `tdt4160`, run:

```
$ python3 -m pip install tdt4160
```

or to install from source:

```
$ python3 setup.py install
```

## Introduction

Due to COVID-19, most NTNU classes switched from exams in exam halls with no
external help/tools allowed to home exams with all tools allowed. I thought it
would be pretty funny if you could just automate the exams now that you're
allowed to use tools.

I was right, it was pretty funny.

## Example usage

### Pseudo-assembly
```python
# This example from the Autumn 2020 exam, task 6

from tdt4160.assembly import *

# First set the registries as specified in the task
set_asm_registries(
    R0=0xFFFF0000,
    R7=0xFFFF0001,
    R8=0xFFFF0002,
    R9=0xFFFF0003,
)

# Then set the memory addresses as specified
set_asm_addresses({
    0xFFFF0000: 0x00000001,
    0xFFFF0001: 0x00000002,
    0xFFFF0002: 0x00000003,
    0xFFFF0003: 0x00000004,
    0xFFFF0004: 0xFFFF0005
})

# Queue all the instructions to be performed
assemble(0x0000FFFE, LOAD, R8, R0)
assemble(0x0000FFFF, MOVC, R7, 1)
assemble(0x00010000, ADD, R0, R0, R7)
assemble(0x00010001, LOAD, R9, R0)
assemble(0x00010002, MUL, R9, R8, R9)
assemble(0x00010003, ADD, R9, R9, R8)
assemble(0x00010004, ADD, R0, R0, R7)
assemble(0x00010005, LOAD, R8, R0)
assemble(0x00010006, ADD, R8, R9, R8)

# Then actually run them
execute_assembly(0x0000FFFE)

# This function prints all the registries used in the task
# In this case, we're looking for R8, which is 6
print_asm_regs()
```

This outputs the following:

```
=============================== MEMORY: 0000FFFE ===============================
INSTRUCTION: LOAD R8=FFFF0002, R0=FFFF0000
Loaded value 00000001 into R8 from address FFFF0000
=============================== MEMORY: 0000FFFF ===============================
INSTRUCTION: MOVC R7=FFFF0001, Constant=00000001
Moved value 00000001 into R7
=============================== MEMORY: 00010000 ===============================
INSTRUCTION: ADD R0=FFFF0000, R0=FFFF0000, R7=00000001
Added R0=FFFF0000+R7=00000001
Result FFFF0001 stored in R0
=============================== MEMORY: 00010001 ===============================
INSTRUCTION: LOAD R9=FFFF0003, R0=FFFF0001
Loaded value 00000002 into R9 from address FFFF0001
=============================== MEMORY: 00010002 ===============================
INSTRUCTION: MUL R9=00000002, R8=00000001, R9=00000002
Multiplied R8=00000001*R9=00000002
Result 00000002 stored in R9
=============================== MEMORY: 00010003 ===============================
INSTRUCTION: ADD R9=00000002, R9=00000002, R8=00000001
Added R9=00000002+R8=00000001
Result 00000003 stored in R9
=============================== MEMORY: 00010004 ===============================
INSTRUCTION: ADD R0=FFFF0001, R0=FFFF0001, R7=00000001
Added R0=FFFF0001+R7=00000001
Result FFFF0002 stored in R0
=============================== MEMORY: 00010005 ===============================
INSTRUCTION: LOAD R8=00000001, R0=FFFF0002
Loaded value 00000003 into R8 from address FFFF0002
=============================== MEMORY: 00010006 ===============================
INSTRUCTION: ADD R8=00000003, R9=00000003, R8=00000003
Added R9=00000003+R8=00000003
Result 00000006 stored in R8
================================================================================
R0  = 0xFFFF0002
R7  = 0x00000001
R8  = 0x00000006
R9  = 0x00000003
```

### IJVM
```Python
# This example from the Autumn 2020 exam, task 4

from tdt4160.ijvm import *

# Set the registries as specified
set_ijvm_registries(
    SP=0x10101010,
    LV=0x30000000,
    CPP=0x10000001,
    TOS=0xFF000000,
    OPC=0xABCDE000,
    H=0x12345678,
    MAR=0xA5A5A5A5,
    MDR=0x5A5A5A5A,
    PC=0x55AA55AA
)

# Queue the microinstructions to run
ijvm(0b000001000, 0b000001001, 0b000, 0b00010000, 0b100000000, 0b000, 0b1111)
ijvm(0b000001001, 0b000001011, 0b000, 0b00111001, 0b100000000, 0b000, 0b1100)
ijvm(0b000001010, 0b000010000, 0b001, 0b01011000, 0b010101010, 0b000, 0b0001)
ijvm(0b000001011, 0b000001100, 0b000, 0b00111100, 0b100000000, 0b000, 0b0101)
ijvm(0b000001100, 0b000000000, 0b000, 0b00111100, 0b000010000, 0b000, 0b0101)
ijvm(0b000001101, 0b000001110, 0b000, 0b00110010, 0b001000101, 0b100, 0b1000)

# Actually run them
execute_ijvm(0b000001000)

# Print the value of all the registries after execution
# In this case, we're looking for several registries, so just check the ones you want
print_all_ijvm()
```

This outputs the following:

```
======================= Instruction address: 0x000001000 =======================
next=0b000001001 JAM=0b000 ALU=0b00010000 C=0b100000000 Mem=0b000 B=0b1111
ALU is 0b010000, function: 0
Result of operation: 0x00000000
Final result: 0x00000000
C is 0b100000000
The following registries take the value of 0x00000000
H
Mem is 0b000
Mem is 0, don't touch memory
Next instruction: 0b000001001
======================= Instruction address: 0x000001001 =======================
next=0b000001011 JAM=0b000 ALU=0b00111001 C=0b100000000 Mem=0b000 B=0b1100
ALU is 0b111001, function: A + 1
A is always H=0x00000000
Result of operation: 0x00000001
Final result: 0x00000001
C is 0b100000000
The following registries take the value of 0x00000001
H
Mem is 0b000
Mem is 0, don't touch memory
Next instruction: 0b000001011
======================= Instruction address: 0x000001011 =======================
next=0b000001100 JAM=0b000 ALU=0b00111100 C=0b100000000 Mem=0b000 B=0b0101
ALU is 0b111100, function: A + B
A is always H=0x00000001
B is 0b0101 (5), yielding LV=0x30000000
Result of operation: 0x30000001
Final result: 0x30000001
C is 0b100000000
The following registries take the value of 0x30000001
H
Mem is 0b000
Mem is 0, don't touch memory
Next instruction: 0b000001100
======================= Instruction address: 0x000001100 =======================
next=0b000000000 JAM=0b000 ALU=0b00111100 C=0b000010000 Mem=0b000 B=0b0101
ALU is 0b111100, function: A + B
A is always H=0x30000001
B is 0b0101 (5), yielding LV=0x30000000
Result of operation: 0x60000001
Final result: 0x60000001
C is 0b000010000
The following registries take the value of 0x60000001
LV
Mem is 0b000
Mem is 0, don't touch memory
Next instruction: 0b000000000
================================================================================
Next instruction is 0. We're done
SP = 0x10101010
LV = 0x60000001
CPP = 0x10000001
TOS = 0xFF000000
OPC = 0xABCDE000
H = 0x30000001
MAR = 0xA5A5A5A5
MDR = 0x5A5A5A5A
PC = 0x55AA55AA
MBR = 0xUNINITIALIZED
MBRU = 0xUNINITIALIZED
MPC = 0x00000000
```

Note the uninitialized values were never touched, so they remain uninitialized.
That's okay as long as we don't use them after.

# På Norsk

`tdt4160` er en emulator for IJVM-mikronstruksjoner og pseudo-assemblykode,
som den man ofte ser i [NTNU faget TDT4160](https://www.ntnu.no/studier/emner/TDT4160)
sine eksamener.

Det er to hoveddeler i pakkken. `tdt4160.assembly` og `tdt4160.ijvm`.
Begge lar deg sette opp registre, minneaddresser, og sette instruksjoner i kø,
før de blir utført. Mens instruksjonene kjører printes det masse informasjon ut
om hva som faktisk utføres, slik at det blir lettere å se hva som skjer. Pakken
krever teknisk sett en Pythonversjon som er >= 3.7, men bør fungere fint med alt >= 3.6.
Pakken har ingen andre avhengigheter enn standardbiblioteket.

[Se på PyPI](http://pypi.python.org/pypi/tdt4160) |
[Gafle meg på gitgud](https://gitgud.io/fish/tdt4160)


## Installering

For å installere `tdt4160`, kjør:

```
$ python3 -m pip install tdt4160
```

eller for å installere fra kildekode:

```
$ python3 setup.py install
```

## Introduksjon

Pga. COVID-19 har de fleste fag på NTNU byttet fra eksamen i eksamenshaller
uten hjelpemidler til hjemmeeksamener med alle hjelpemidler tillat. Jeg
syntes det hadde vært litt morsomt hvis man bare hadde noe verktøy som
gjorde hele eksamenen for deg, nå som du kan bruke det du vil.

Hadde rett, det var ganske morsomt.

## Eksempel

### Pseudo-assembly
```python
# Dette eksempelet er fra Høsteksamen 2020, oppgave 6

from tdt4160.assembly import *

# Først, sett opp alle registre som det står i oppgaven
set_asm_registries(
    R0=0xFFFF0000,
    R7=0xFFFF0001,
    R8=0xFFFF0002,
    R9=0xFFFF0003,
)

# Så sett opp alle minneaddresser
set_asm_addresses({
    0xFFFF0000: 0x00000001,
    0xFFFF0001: 0x00000002,
    0xFFFF0002: 0x00000003,
    0xFFFF0003: 0x00000004,
    0xFFFF0004: 0xFFFF0005
})

# Legg alle instruksjonene i kø for utførsel
assemble(0x0000FFFE, LOAD, R8, R0)
assemble(0x0000FFFF, MOVC, R7, 1)
assemble(0x00010000, ADD, R0, R0, R7)
assemble(0x00010001, LOAD, R9, R0)
assemble(0x00010002, MUL, R9, R8, R9)
assemble(0x00010003, ADD, R9, R9, R8)
assemble(0x00010004, ADD, R0, R0, R7)
assemble(0x00010005, LOAD, R8, R0)
assemble(0x00010006, ADD, R8, R9, R8)

# Kjør instruksjonene
execute_assembly(0x0000FFFE)


# Denne funksjonen printer alle registre som ble brukt i utførselen
# I dette tilfellet ser vi etter R8, som bør være 6
print_asm_regs()
```

Koden spytter ut følgende:

```
=============================== MEMORY: 0000FFFE ===============================
INSTRUCTION: LOAD R8=FFFF0002, R0=FFFF0000
Loaded value 00000001 into R8 from address FFFF0000
=============================== MEMORY: 0000FFFF ===============================
INSTRUCTION: MOVC R7=FFFF0001, Constant=00000001
Moved value 00000001 into R7
=============================== MEMORY: 00010000 ===============================
INSTRUCTION: ADD R0=FFFF0000, R0=FFFF0000, R7=00000001
Added R0=FFFF0000+R7=00000001
Result FFFF0001 stored in R0
=============================== MEMORY: 00010001 ===============================
INSTRUCTION: LOAD R9=FFFF0003, R0=FFFF0001
Loaded value 00000002 into R9 from address FFFF0001
=============================== MEMORY: 00010002 ===============================
INSTRUCTION: MUL R9=00000002, R8=00000001, R9=00000002
Multiplied R8=00000001*R9=00000002
Result 00000002 stored in R9
=============================== MEMORY: 00010003 ===============================
INSTRUCTION: ADD R9=00000002, R9=00000002, R8=00000001
Added R9=00000002+R8=00000001
Result 00000003 stored in R9
=============================== MEMORY: 00010004 ===============================
INSTRUCTION: ADD R0=FFFF0001, R0=FFFF0001, R7=00000001
Added R0=FFFF0001+R7=00000001
Result FFFF0002 stored in R0
=============================== MEMORY: 00010005 ===============================
INSTRUCTION: LOAD R8=00000001, R0=FFFF0002
Loaded value 00000003 into R8 from address FFFF0002
=============================== MEMORY: 00010006 ===============================
INSTRUCTION: ADD R8=00000003, R9=00000003, R8=00000003
Added R9=00000003+R8=00000003
Result 00000006 stored in R8
================================================================================
R0  = 0xFFFF0002
R7  = 0x00000001
R8  = 0x00000006
R9  = 0x00000003
```

### IJVM
```Python
# Dette eksempelet er fra Høsteksamen 2020, oppgave 4

from tdt4160.ijvm import *

# Sett opp registre som det står i oppgaven
set_ijvm_registries(
    SP=0x10101010,
    LV=0x30000000,
    CPP=0x10000001,
    TOS=0xFF000000,
    OPC=0xABCDE000,
    H=0x12345678,
    MAR=0xA5A5A5A5,
    MDR=0x5A5A5A5A,
    PC=0x55AA55AA
)

# Skriv inn alle mikronstruksjonene
ijvm(0b000001000, 0b000001001, 0b000, 0b00010000, 0b100000000, 0b000, 0b1111)
ijvm(0b000001001, 0b000001011, 0b000, 0b00111001, 0b100000000, 0b000, 0b1100)
ijvm(0b000001010, 0b000010000, 0b001, 0b01011000, 0b010101010, 0b000, 0b0001)
ijvm(0b000001011, 0b000001100, 0b000, 0b00111100, 0b100000000, 0b000, 0b0101)
ijvm(0b000001100, 0b000000000, 0b000, 0b00111100, 0b000010000, 0b000, 0b0101)
ijvm(0b000001101, 0b000001110, 0b000, 0b00110010, 0b001000101, 0b100, 0b1000)

# Kjør instruksjonene
execute_ijvm(0b000001000)

# Skriv ut verdien til alle registrene etter at programmet har kjørt
# I dette tilfellet ser vi etter flere registre, plukk ut de du vil
print_all_ijvm()
```

Denne koden gir:

```Python
======================= Instruction address: 0x000001000 =======================
next=0b000001001 JAM=0b000 ALU=0b00010000 C=0b100000000 Mem=0b000 B=0b1111
ALU is 0b010000, function: 0
Result of operation: 0x00000000
Final result: 0x00000000
C is 0b100000000
The following registries take the value of 0x00000000
H
Mem is 0b000
Mem is 0, don't touch memory
Next instruction: 0b000001001
======================= Instruction address: 0x000001001 =======================
next=0b000001011 JAM=0b000 ALU=0b00111001 C=0b100000000 Mem=0b000 B=0b1100
ALU is 0b111001, function: A + 1
A is always H=0x00000000
Result of operation: 0x00000001
Final result: 0x00000001
C is 0b100000000
The following registries take the value of 0x00000001
H
Mem is 0b000
Mem is 0, don't touch memory
Next instruction: 0b000001011
======================= Instruction address: 0x000001011 =======================
next=0b000001100 JAM=0b000 ALU=0b00111100 C=0b100000000 Mem=0b000 B=0b0101
ALU is 0b111100, function: A + B
A is always H=0x00000001
B is 0b0101 (5), yielding LV=0x30000000
Result of operation: 0x30000001
Final result: 0x30000001
C is 0b100000000
The following registries take the value of 0x30000001
H
Mem is 0b000
Mem is 0, don't touch memory
Next instruction: 0b000001100
======================= Instruction address: 0x000001100 =======================
next=0b000000000 JAM=0b000 ALU=0b00111100 C=0b000010000 Mem=0b000 B=0b0101
ALU is 0b111100, function: A + B
A is always H=0x30000001
B is 0b0101 (5), yielding LV=0x30000000
Result of operation: 0x60000001
Final result: 0x60000001
C is 0b000010000
The following registries take the value of 0x60000001
LV
Mem is 0b000
Mem is 0, don't touch memory
Next instruction: 0b000000000
================================================================================
Next instruction is 0. We're done
SP = 0x10101010
LV = 0x60000001
CPP = 0x10000001
TOS = 0xFF000000
OPC = 0xABCDE000
H = 0x30000001
MAR = 0xA5A5A5A5
MDR = 0x5A5A5A5A
PC = 0x55AA55AA
MBR = 0xUNINITIALIZED
MBRU = 0xUNINITIALIZED
MPC = 0x00000000
```

Merk at to av registrene aldri ble satt, verken i oppsettet eller i koden, så
de er bare `UNINITIALIZED`. Det er greit så lenge de aldri brukes til noe.