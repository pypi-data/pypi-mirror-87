# CS147DVPyParser
This program is intended for students of Kaushik Patra's San Jose State University CS147 - Computer Architecture class. It can be used to quickly convert CS147DV Assembly language instructions to hexadecimal machine code. It may not work as intended if CS147DV has been changed/updated since it was last updated in December of 2019.

## CS147DV Instruction Set Architecture
This architecture is created and maintained by Mr. Kaushik Patra for his CS147 - Computer Architecture class. His contact information is:

    Kaushik Patra, Lecturer,
    Department Of Computer Science,
    San Jose State University,
    One Washington Square,
    San Jose, CA.
    
    email: kaushik.patra@sjsu.edu


## Requirements
The program is known to work with Python2.7+ and 3.7+. The package does not rely on any external dependencies.

# Quick set-up
The fastest and easiest way to get this package is to downlaod and install it with pip
```
$ pip install cs147dvparser
```
The above command will download the package to your machine. The package can be `import`ed to your own python script. It also contains a command line interface (CLI). Thus there are two ways to interact with this package:
1. [from the command line](#1-run-the-program-from-the-command-line) 
2. [imported as a module](#2-import-the-program-as-a-module)

## 1. Run the program from the command line

The program can be run directly from the command line. It contains a number of options, which can be broken down into three main modes: 
1. [type Assembly instructions interactively](#a-interactive-mode)
2. [pass in Assembly instructions as command-line arguments](#b-pass-in-instructions-as-command-line-arguments)
3. [read Assembly instructions from a file](#c-read-instructions-from-a-file)

---
### a) interactive mode
  When run with no arguments, the CLI will enter interactive mode:
      
  ```python
  $ cs147DVParser

  WELCOME TO CS147DV INTERACTIVE INSTRUCTION PARSER!
  ENTER IN YOUR INSTRUCTIONS ONE AT A TIME
  THE RESULT WILL BE PRINTED TO THE SCREEN
  INPUT SHOULD BE OF THE TYPE:
    R-Type:  <mnemonic> <rd>,<rs>,<rt|shamt>
    I-Type:  <mnemonic> <rt>,<rs>, <imm>
    J-Type:  <mnemonic> <address>
  OUTPUT WILL BE A 32 BIT HEXADECIMAL NUMBER
  PRESS ctrl-c TO EXIT AT ANY TIME
  
  enter your intruction: _
  ```

  Interactive mode can also be evoked explicitly with the `-i` flag:
      
      $ cs147DVParser -i
---
### b) pass in instructions as command line arguments

In this mode, the user can pass in any valid CS147DV assembly code instruction to the program as a command-line argument:

 One instruction:
   ```python
   $ cs147DVParser "addi r2 r3 5"
   ``` 
  
More than one instruction:  
  
    $ cs147DVParser "<instruction1>" "<instruction2>"

Assembly instructions will be parsed one at a time in the order they are passed in on the command line from left to right.

---
### c) read instructions from a file

In this mode, a text file contatining a list of instructions are passed in to the program. The file must consist of a single instruction on each line of the file. The instructions are parsed one at a time from top to bottom.
    
    $ cs147DVParser -f instructions.txt  
---
**note:** Modes can be mixed and matched. You can even run all three modes at once:

    $ cs147DVParser "addi r1 r2 3" -f instructions.txt -i 

When mixing and matching modes, the instructions will be processed in the following order
1. from the command line
2. from a file
3. from interactive mode.

---
### Output
output from parsing an instruction will look similar to this:
```
 R-Type detected
 <mnemonic> <rd> <rs> <rt|shamt> [base]

 input: add r1 r2 r3
  _____________________________________
 |opcode| rs  | rt  | rd  |shamt| funct|
 |______|_____|_____|_____|_____|______|

 opcode rs      rt      rd      shamt   funct
 000000 00010   00011   00001   00000   100000

 binary_string:
 0000 0000 0100 0011 0000 1000 0010 0000

 hexadecimal_string result:
 00430820
 ```

---
### options

additional options include:

- `-o, --outfile (outfile)`: specify a file to write the hexadecimal output from each instruction parse. The current contents of `<outfile>` will be completely overwritten.
- `-a, --append`: append the results of each instruction to `<outfile>` instead of overwriting the file. This option does nothing if not combined with the `-o` option.
- `-q, --quiet`: suppress all other [output](#output) except for the hexadecimal parse of each instruction.

other arguments include:

* `-h, --help` : display help information and exit
* `-f, --file` : parse instructions from a file
* `-i, --interactive` : evoke interactive mode.

click here for information on proper [CS147DV Assembly Instruction formatting](#CS147DV-Instruction-Format)

---
---
## 2. import the program as a module    
AssemblyParser.py can be `import`ed as a module into another program. The main point of entry is the `parse_instruction()` function

```python
import AssemblyParser
hex_result = AssemblyParser.parse_instruction('addi r2 r3 5')
print(hex_result)
```
The above script will output:
```
20620005
```

To see meta-data about each instruction, set the verbose printer, `vprint` to `'verbose'`:
```python
import AssemblyParser
hex_result = AssemblyParser.parse_instruction('addi r2 r3 5', vprint='verbose')
print('\nhex result')
print(hex_result)
```
which will output:
```
I-Type
<mnemonic> <rt> <rs> <imm> [base]
input: addi r2 r3 5
 ___________________________________
|opcode| rs  | rt  |   immediate    |
|______|_____|_____|________________|

opcode  rs      rt      imm
001000  00011   00010   0000000000000101

binary_string
0010 0000 0110 0010 0000 0000 0000 0101

hex result
20620005
```


To parse many instructions:

```python
import AssemblyParser

instructions = ['addi r12 r12 12','addi r14 r14 14', 'sll r2 r2 5']
for i in instructions:
  hex_result = AssemblyParser.parse_instructions(i)
  print(hex_result)
```
---
---
# CS147DV Instruction Format

Instructions must be of the form:
* R-Type :
    * \<mnemonic> \<rd> \<rs> \<rt|shamt> [base]
    * \<mnemonic> \<rd>, \<rs>, \<rt|shamt> [base]

    examples: 
    
    * `"add r2 r3 r4"`
    * `"and r2, r3, r4"`
    * `"or r2,r3,r4"`
    * `"sll r2 R3,0x08"`
    * `"srl R2,3, 10 bin"`
    * `"SLL r2 R3 10 decimal"`
    * `"SRL R2 r3 10 hex"`
    * `"jr r15"`

* I-Type :
  * \<mnemonic> \<rt> \<rs> \<immediate> [base]
  * \<mnemonic>,\<rt>,\<rs>,\<immediate> [base]

  examples
 
  * `"addi r2 r2 3"`
  * `"lui, r5,5"`
  * `"beq,r5,r6,0xaf"`
  * `"lw r10 r11 1010,bin"`

* J-Type :
  * \<mnemonic> \<address> [base]
  * \<mnemonic>, \<address> [base]

  examples:
  * `"jmp 0x2b3da9f"`
  * `"push"`

---  

Registers must begin with an `r` or an `R` and must be followed by a decimal number.
`r10` will always map to register 10d: `001010b` and never register 10b: `000010b` or register 10h `010000b`

If you choose an R-type instruction that requires a shift amount `shamt` instead of a register `rt`, the script will fail if the value passed in begins with an `[rR]`

example:
 ```
enter your intruction: sll r2 r3 r4
shift operations require a shamt, not a register
try again


enter your intruction: sll r2 r3 4

R-Type
<mnemonic> <rd> <rs> <rt|shamt> [base]
input: sll r2 r3 4
 _____________________________________
|opcode| rs  | rt  | rd  |shamt| funct|
|______|_____|_____|_____|_____|______|

opcode  rs      rt      rd      shamt   funct
000000  00011   00000   00010   00100   000001

binary_string
0000 0000 0110 0000 0001 0001 0000 0001

hexadecimal_string result:
00601101
```

---

`[base]` is used to directly specify what your data type is.

it can be applied to the following fields:
* `<shamt>`
* `<immediate>`
* `<address>`

Options for `[base]`:
* `bin`, `binary`
* `decimal`
* `hex`, `hexadecimal`

`dec` can not be used to specify a decimal since the string `'dec'` is a valid hexadecimal number (3564d).

**note:** you can also simply prefix a hexadecimal with `0x` to ensure it is converted to hexadecimal


If not specified, the script will attempt to convert any number to binary in the following order:
1. binary
2. decimal
3. hexadecimal

**note**: This order is necessary since all binary strings are also valid decimal and hexadecimal strings.

example. Pay close attention to the `shamt` amount as different `base`s are specified for the number string `'10'`:
* `[base]` not specified: 
  ```
  enter your intruction: sll r2 r3 10
  
  R-Type
  <mnemonic> <rd> <rs> <rt|shamt> [base]
  input: sll r2 r3 10
   _____________________________________
  |opcode| rs  | rt  | rd  |shamt| funct|
  |______|_____|_____|_____|_____|______|
  
  opcode  rs      rt      rd      shamt   funct
  000000  00011   00000   00010   00010   000001
  
  binary_string
  0000 0000 0110 0000 0001 0000 1000 0001
  
  hexadecimal_string result:
  00601081
  ```

* `[base]` set to binary (same as above):
  ```
  enter your intruction: sll r2 r3 10 bin
  
  R-Type
  <mnemonic> <rd> <rs> <rt|shamt> [base]
  input: sll r2 r3 10
   _____________________________________
  |opcode| rs  | rt  | rd  |shamt| funct|
  |______|_____|_____|_____|_____|______|
  
  opcode  rs      rt      rd      shamt   funct
  000000  00011   00000   00010   00010   000001
  
  binary_string
  0000 0000 0110 0000 0001 0000 1000 0001
  
  hexadecimal_string result:
  00601081
  ```
* with `[base]` set to decimal:
  ```
  enter your intruction: sll r2 r3 10 decimal

  R-Type
  <mnemonic> <rd> <rs> <rt|shamt> [base]
  input: sll r2 r3 10 d
   _____________________________________
  |opcode| rs  | rt  | rd  |shamt| funct|
  |______|_____|_____|_____|_____|______|
  
  opcode  rs      rt      rd      shamt   funct
  000000  00011   00000   00010   01010   000001
  
  binary_string
  0000 0000 0110 0000 0001 0010 1000 0001
  
  hexadecimal_string result:
  00601281
  ```
* with `[base]` set to hexadecimal:
  ```
  R-Type
  <mnemonic> <rd> <rs> <rt|shamt> [base]
  input: sll r2 r3 10 hex
   _____________________________________
  |opcode| rs  | rt  | rd  |shamt| funct|
  |______|_____|_____|_____|_____|______|
  
  opcode  rs      rt      rd      shamt   funct
  000000  00011   00000   00010   10000   000001
  
  binary_string
  0000 0000 0110 0000 0001 0100 0000 0001
  
  hexadecimal_string result:
  00601401
  ```
  
Notice how the value of `shamt` and thus the `binary_string` and `hexadecmal_string result` change as the `[base]` is specified.

More information and gifs of the tool in action can be found at the
[CS147DVPyParser website](https://rdeamici.github.io/CS147DVParser)
