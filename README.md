# ![GitHub](https://img.shields.io/github/license/Sammy-Barasa/project0-Assembler-and-Simulator) ![GitHub contributors](https://img.shields.io/github/contributors/Sammy-Barasa/project0-Assembler-and-Simulator)  [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Sammy-Barasa/project0-Assembler-and-Simulator#how-to-contribute-)

## project0-Assembler-and-Simulator

# **project0 PesaPal Challange 2023**

project0 is implementing an assembler following provided machine instruction set by PesaPal Careers Portal for Junior Developer . The project has two parts

### **1. Assembler**

Has five registers and 64K of memory in a 32-bit address space, from ***0x00000000–0x0000FFFF***  

Has five registers consist of three general purpose **(R1, R2, R3)**, program counter (instruction pointer) register **(PC)**, and a conditional register **(COND)**

Each instruction is encoded in a half word (16 bits) in little endian *(stores the least-significant byte at the smallest address)*

* first 4 bits (half byte)- contain the instruction number
* second, third and fourth half-bytes (4 bit sections) contain register numbers

 Takes text assembly program written for the above instruction set and produces the output as a set of 16-bit numbers, bytecode format

### **2. Simulator to process assembler output**

The program takes the output of the assembler and execute it, correctly.

# How to install and run

**1. git clone the repo**

```sh
git clone [past git clone link here]
```
**NB: branch dev is ahead**   

**2. see help for options**

```sh
  python3 run.py -h
```

Instructions shown below will be presented:

```sh
usage: run.py [-h] [--inter INTERMIDIATE] [program_action ...]

positional arguments:
  program_action        argument for selecting either: read, make or sim; and providing input filename, output filename

options:
  -h, --help            show this help message and exit
  --inter INTERMIDIATE  flag for creating intermediate file
```

# How to use

## can be used in 3 modes

Only mode one and two are complete

### **1. see complete preprocessed assembly file infomation**

Displays informatio of preprocessed assembly file. Preprocessing is the first step that the assembly file goes through where comments are eliminated, subroutines identified among other steps.

```sh
 python3 run.py read test.txt
```

test.txt should be a file containing assembly source code an example is shown below:

```s
; a simple counter program.
li R1 0x00000000
; end
li R2 0x0000FFFF
; memory location of loop start
li R3 loop
loop:
  ; store the contents of R1 at the memory location pointed by R1
  sw R1 R1
  ; increment the counter
  inc R1
  ; loop if the counter hasn't yet reached the end
  bne R1 R2 R3
  ; end program
  halt
```

### **2. compile an assembly file source code to byte code**

Specify the source file and destination file.

```sh
python3 run.py make test.txt compiled.s
```

or

```sh
python3 run.py make test.txt compiled.obj
```

Intermediate compiled file is first generated and then converted into instruction in bytes.
  
Intermediate compiled file result looks as shown below:

```sh
 0x02 0x00 0x00000000
 0x02 0x01 0x0000FFFF
 0x02 0x02 0x60
 0x04 0x00 0x00
 0x0D 0x00
 0x0C 0x00 0x01 0x02
 0x00
```

Byte code file is generated in 16 word binary and is shown below:

```sh
0010000000000000
0010000111111111
0010001001100000
0100000000000000
1101000000000000
1100000000010010
0000000000000000
```

### **3. Run simulator to prosses byte code or obj file**

The register table is displayed showing the register data after every line is executed. The registers value begin empty with value `xxxx` and are updated as each line is executed

Out of the 16 instructions, only the first 7 have been implemented.

**Completed instruction: 7/16**

The register table looks as shown below:

```sh
___________________________________
 -| R1  |  R2  |  R3  |  PC  | COND
___________________________________
 1|0x00 | xxxx | xxxx | 0x10 | xxxx
 2|0x00 | 0xff | xxxx | 0x20 | xxxx
 3|0x00 | 0xff | 0x30 | 0x30 | xxxx
 4|0x00 | 0xff | 0x30 | 0x30 | xxxx
 5|0x00 | 0xff | 0x30 | 0x30 | xxxx
 6|0x00 | 0xff | 0x30 | 0x30 | xxxx
 7|0x00 | 0xff | 0x30 | 0x50 | xxxx

```

# Credits

### Work by Sammy Barasa [(https://github.com/Sammy-Barasa/MIPS-Assembler)](https://github.com/Sammy-Barasa/MIPS-Assembler)

My refernce stems from some work I did earlier on a MIPS-Assembler [(https://github.com/Sammy-Barasa/MIPS-Assembler)](https://github.com/Sammy-Barasa/MIPS-Assembler) see details on this link.

project0 features a unique instruction set, an improved program structure and documentation, a more efficient preprocessing stage, tests and a simulator.

[(Binary mathematics reference)](https://levelup.gitconnected.com/computing-binary-numbers-with-python-a6e00be69bea)

### The Art of Assembly Language, 2nd Edition by Randall Hyde

One of my fundamental learning material used for referencing and understanding the assembler. The Art of Assembly Language has provided a comprehensive, plain-English, and patient introduction to 32-bit x86 assembly for non-assembly programmers. Hyde's primary teaching tool, High Level Assembler (or HLA), incorporates many of the features found in high-level languages (like C, C++, and Java) to help you quickly grasp basic assembly concepts. HLA lets you write true low-level code while enjoying the benefits of high-level language programming.

# How to contribute 

1. Add an issue
2. Clone the repo
3. change to branch dev
4. create brach with name: "your_name/isntruction_or_part_you_are_working_on"
5. Add your contribution
6. write your test
7. Make sure the tests run
8. Submit a pull request with the branch you created.
9. If pull request accepted, I will merge to dev and finally merge dev to main
10. If working on an existing branch, switch to dev, witch to that branch and create branch with name: "your_name/isntruction_or_part_you_are_working_on"
11. Add your contribution
12. write your test
13. Make sure the tests run
14. Submit a pull request with the branch you created.