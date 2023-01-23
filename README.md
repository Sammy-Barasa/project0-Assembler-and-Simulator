![GitHub](https://img.shields.io/github/license/Sammy-Barasa/project0-Assembler-and-Simulator) ![GitHub contributors](https://img.shields.io/github/contributors/Sammy-Barasa/project0-Assembler-and-Simulator)

# project0-Assembler-and-Simulator
## **project0 PesaPal Challange 2023**. 

project0 is implementing an assembler following provided machine instruction set. The project has two parts
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

git clone the repo

# How to use

## can be used in 3 modes

Only mode one is complete

### **1. see complete preprocessed assembly file infomation**

Displays informatio of preprocessed assembly file. Preprocessing is the first step that the assembly file goes through where comments are eliminated, subroutines identified among other steps.

```sh
 python3 run.py read test.txt
```

### **2. compile an assembly file source code to byte code**

Specify the source file and destination file.

```sh
python3 run.py make filename.txt filename.s/filename.obj
```

### **3. Run simulator to prosses byte code or obj file**

Coming soon.

# Credits

## Work by Sammy Barasa [(https://github.com/Sammy-Barasa/MIPS-Assembler)](https://github.com/Sammy-Barasa/MIPS-Assembler)

My refernce stems from some work I did earlier on a MIPS-Assembler [(https://github.com/Sammy-Barasa/MIPS-Assembler)](https://github.com/Sammy-Barasa/MIPS-Assembler) see details on this link.

project0 features a unique instruction set, an improved program structure and documentation, a more efficient preprocessing stage, tests and a simulator.

## The Art of Assembly Language, 2nd Edition by Randall Hyde

One of my fundamental learning material used for referencing and understanding the assembler. The Art of Assembly Language has provided a comprehensive, plain-English, and patient introduction to 32-bit x86 assembly for non-assembly programmers. Hyde's primary teaching tool, High Level Assembler (or HLA), incorporates many of the features found in high-level languages (like C, C++, and Java) to help you quickly grasp basic assembly concepts. HLA lets you write true low-level code while enjoying the benefits of high-level language programming.

# How to contribute [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Sammy-Barasa/project0-Assembler-and-Simulator#how-to-contribute-)

1. Add an issue
2. Clone the repo
3. Add your contribution
4. Make sure the tests run
5. Submit a pull request
