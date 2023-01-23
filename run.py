import sys
from pathlib import Path
from assembler import Assembler

def run():
    base_dir = Path().resolve()
    assembler_obj = Assembler(base_dir) # assembler object
    # compile_assembly.startProgram()


    cmd = sys.argv
    if len(cmd) < 3:
        print("use commands:")
        print("[read filename.txt]")
        print("[make filename.txt filename.s/filename.obj]")
        print("[sim run filename.obj/filename.s]")
        print(cmd)
    
    elif cmd[1]== "read":
        # read file with assembly source code *.txt *.asm *.s file
        
        assembler_obj.readLines(cmd[2])
        assembler_obj.convert(assembler_obj.all_lines)
        assembler_obj.printLines(assembler_obj.all_lines)

    elif cmd[1]== "make":
        # compile assembly source code to assembly requires: source file, destination file
        # self.readLines(cmd[2])
        # self.convert(self.all_lines)
        # self.printLines(self.all_lines)
        pass

    elif cmd[1]== "run":
        # run simulator on assembled byte code *.obj file
        # self.readLines(cmd[2])
        # self.convert(self.all_lines)
        # self.printLines(self.all_lines)
        pass

    else:
        print("[assemble filename.s]")
        print("[assemble read filename.s]")
        print("[assemble generate filename.txt]")
        sys.exit()


if __name__ == "__main__":
    run()
