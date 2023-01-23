import sys
from pathlib import Path
from assembler import Assembler

def run():
    base_dir = Path().resolve()
    assembler_obj = Assembler(base_dir) # assembler object
    # compile_assembly.startProgram()


    cmd = sys.argv
    if len(cmd) > 4:
        print("use commands:")
        print("[read filename.txt]")
        print("[make filename.txt filename.s/filename.obj]")
        print("[sim run filename.obj/filename.s]")
        print(cmd)
    
    elif cmd[1]== "read":
        # read file with assembly source code *.txt *.asm *.s file
        
        assembler_obj.readLines(cmd[2])
        assembler_obj.preprocess(assembler_obj.all_lines)
        assembler_obj.printLines(assembler_obj.all_lines)

    elif cmd[1]== "make" and len(cmd)==4:
        # compile assembly source code to assembly requires: source file, destination file
        # self.readLines(cmd[2])
        assembler_obj.readLines(cmd[2])
        assembler_obj.preprocess(assembler_obj.all_lines)
        assembler_obj.compile(cmd[3])
        # self.printLines(self.all_lines)
    
    elif cmd[1]== "run":
        # run simulator on assembled byte code *.obj file
        # self.readLines(cmd[2])
        # self.convert(self.all_lines)
        # self.printLines(self.all_lines)
        pass

    else:
        print("PLEASE PROVIDE ALL THE ARGUMENTS REQUIRED!!!")
        print("read filename.s")
        print("make filename.s filename.obj")
        print("sim run generate filename.txt")
        print("make test.txt compile.s")

        sys.exit()


if __name__ == "__main__":
    run()
