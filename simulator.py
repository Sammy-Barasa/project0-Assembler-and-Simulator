import os
from assembler import update_line_information
class Simulator():
    BASE_DIR = ""
    registers_names = {'0x00':'R1','0x01':'R2','0x02':'R3','0x03':'PC','0x04':'COND'} # registers
    register_state = ["xxxx","xxxx","xxxx","xxxx","xxxx","xxxx"] # [[opcode][R1][R2][R3][PC][COND]
    file_name = ""
    bytecode_lines =[]
    bytecode_lines_info={}
    initial_temp_mem_location = 0
    def __init__(self,base_dir) -> None:
        self.BASE_DIR = base_dir


    def read_bytecode(self,file):
        full_file_path = os.path.join(self.BASE_DIR,file)
        self.file_name=file.split(".")[0] # ignore file extension for now
		
        try:
            with open(full_file_path) as f:
                # read lines and store all_lines[]
                self.bytecode_lines=f.readlines()
        except FileNotFoundError:
            info = f"No such file as {file} was found"
            print(info)
            return info
        except:
            raise
        
    def process_bytecode_line(self, instructions,j):
        '''
        Update registers with values as we read the byte code line by line.
        
        '''
        # change line to half-bytes [[opcode][R1][R2][R3][PC][COND]
        opcode = "0x"+f"{int(instructions[0],2):02x}" # "0x"+f"{int('0010',2):02x}"
        code1 = "0x"+f"{int(instructions[1],2):02x}" # is always a register
        code2 = instructions[2]
        code3 = instructions[3]
        
        if opcode == '0x00':
            start_memory = self.bytecode_lines_info[str((j-1))]["start"]
            self.register_state[3]=start_memory

        elif opcode == '0x01':
            pass # do nothing

        elif opcode == '0x02':
            # li R1 0x00000000

            memory_next_instr = self.bytecode_lines_info[str((j+1))]["start"] # memory address of next instruction
            code2_code3 = "0x"+f"{int(code2 + code3,2):02x}"

            # self.register_state[3]=f"{eval(memory_next_instr):04b}"
            self.register_state[3]=memory_next_instr # COND b5 for NULL/EMPTY, b0 for FALSE, b1 TRUE

            if self.registers_names[code1] == 'R1':
                self.register_state[0]=code2_code3

            elif self.registers_names[code1] == 'R2':
                self.register_state[1]=code2_code3

            elif self.registers_names[code1] == 'R3':
                self.register_state[2]=code2_code3
            
        elif opcode == '0x03':
            # lw R1 R2
            # self.register_state[0]=opcode
            first = code1 # destination
            second = "0x"+f"{int(code2,2):02x}" # source

            if self.registers_names[first]=="R1"  and self.registers_names[second]=="R2" :
                self.register_state[0] = self.register_state[1]
            elif self.registers_names[first]=="R2"  and self.registers_names[second]=="R1":
                self.register_state[1] = self.register_state[0]
            elif self.registers_names[first]=="R1"  and self.registers_names[second]=="R3":
                self.register_state[0] = self.register_state[2]
            elif self.registers_names[first]=="R3"  and self.registers_names[second]=="R1":
                self.register_state[2] = self.register_state[0]
            elif self.registers_names[first]=="R2"  and self.registers_names[second]=="R3":
                self.register_state[1] = self.register_state[2]
            elif self.registers_names[first]=="R3"  and self.registers_names[second]=="R2":
                self.register_state[2] = self.register_state[1]
        
        elif opcode == '0x04':
            # self.register_state[0]=opcode
            pass
        elif opcode == '0x05':
            pass
            # self.register_state[0]=opcode
        
        elif opcode == '0x06':
            pass
            # self.register_state[0]=opcode
        
        elif opcode == '0x07':
            pass
            # self.register_state[0]=opcode

        elif opcode == '0x08':
            pass
            # self.register_state[0]=opcode
        
        elif opcode == '0x09':
            pass
            # self.register_state[0]=opcode
        
        elif opcode == '0x0A':
            pass
            # self.register_state[0]=opcode
        
        elif opcode == '0x0B':
            pass
            # self.register_state[0]=opcode
        
        elif opcode == '0x0C':
            self.register_state[0]=opcode

        elif opcode == '0x0D':
            pass
            # self.register_state[0]=opcode

        elif opcode == '0x0E':
            pass
            # self.register_state[0]=opcode

        elif opcode == '0x0F':
            pass
            # self.register_state[0]=opcode


    def simulate(self,file):
        self.read_bytecode(file)
        update_line_information(self.initial_temp_mem_location,self.bytecode_lines,self.bytecode_lines_info)
        bytecode_lines=self.bytecode_lines

        print("___________________________________")
        print(f" -| R1  |  R2  |  R3  |  PC  | COND ")
        print("___________________________________")

        for i in range(0,len(bytecode_lines)):
            bytecode_lines[i] = bytecode_lines[i].strip()
            halfbyte0 = bytecode_lines[i][0:4]
            halfbyte1 = bytecode_lines[i][4:8]
            halfbyte2 = bytecode_lines[i][8:12]
            halfbyte3 = bytecode_lines[i][12:16]
            bytecode_lines[i] = [halfbyte0,halfbyte1,halfbyte2,halfbyte3]
            self.process_bytecode_line(bytecode_lines[i],i)

            # print(self.bytecode_lines)
            
            state = f" {i+1}|{self.register_state[0]} | {self.register_state[1]} | {self.register_state[2]} | {self.register_state[3]} | {self.register_state[4]}"
            print(state)
            state = f""
