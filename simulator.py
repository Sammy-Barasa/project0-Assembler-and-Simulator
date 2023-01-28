import os
from assembler import Utils

utils = Utils()
class Simulator():
    BASE_DIR = ""
    registers_names = {'0x00':['R1',0],'0x01':['R2',1],'0x02':['R3',2],'0x03':['PC',3],'0x04':['COND',0]} # registers
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

            if self.registers_names[code1][0] == 'R1':
                self.register_state[0]=code2_code3

            elif self.registers_names[code1][0] == 'R2':
                self.register_state[1]=code2_code3

            elif self.registers_names[code1][0] == 'R3':
                self.register_state[2]=code2_code3
            
        elif opcode == '0x03':
            # lw R1 R2
            memory_next_instr = self.bytecode_lines_info[str((j+1))]["start"]
            first = code1 # destination
            second = "0x"+f"{int(code2,2):02x}" # source

            self.register_state[3]=memory_next_instr

            if self.registers_names[first][0]=="R1"  and self.registers_names[second][0]=="R2" :
                self.register_state[0] = self.register_state[1]
            elif self.registers_names[first][0]=="R2"  and self.registers_names[second][0]=="R1":
                self.register_state[1] = self.register_state[0]
            elif self.registers_names[first][0]=="R1"  and self.registers_names[second][0]=="R3":
                self.register_state[0] = self.register_state[2]
            elif self.registers_names[first][0]=="R3"  and self.registers_names[second][0]=="R1":
                self.register_state[2] = self.register_state[0]
            elif self.registers_names[first][0]=="R2"  and self.registers_names[second][0]=="R3":
                self.register_state[1] = self.register_state[2]
            elif self.registers_names[first][0]=="R3"  and self.registers_names[second][0]=="R2":
                self.register_state[2] = self.register_state[1]
        
        elif opcode == '0x04':
            # lw R1 R2

            memory_next_instr = self.bytecode_lines_info[str((j+1))]["start"]            
            first = code1 # destination
            second = "0x"+f"{int(code2,2):02x}" # source
            self.register_state[3]=memory_next_instr

            if self.registers_names[first][0]=="R1"  and self.registers_names[second][0]=="R2" :
                self.register_state[0] = self.register_state[1]
            elif self.registers_names[first][0]=="R2"  and self.registers_names[second][0]=="R1":
                self.register_state[1] = self.register_state[0]
            elif self.registers_names[first][0]=="R1"  and self.registers_names[second][0]=="R3":
                self.register_state[0] = self.register_state[2]
            elif self.registers_names[first][0]=="R3"  and self.registers_names[second][0]=="R1":
                self.register_state[2] = self.register_state[0]
            elif self.registers_names[first][0]=="R2"  and self.registers_names[second][0]=="R3":
                self.register_state[1] = self.register_state[2]
            elif self.registers_names[first][0]=="R3"  and self.registers_names[second][0]=="R2":
                self.register_state[2] = self.register_state[1]
                
        elif opcode == '0x05':
            # add R3 R1 R2
            # 0101001000010000
            #      1  2  3

            memory_next_instr = self.bytecode_lines_info[str((j+1))]["start"]
            self.register_state[3]=memory_next_instr

            op1 = code1
            op2 = "0x"+f"{int(instructions[2],2):02x}"
            op3 = "0x"+f"{int(instructions[3],2):02x}"
            sum = "0x"+f"{int(op3, 16) + int(op2, 16):02x}"
            # print(f"sum is {sum} at {self.registers_names[op1][0]}")
            self.register_state[self.registers_names[op1][1]] = sum
                    
        elif opcode == '0x06':
            # sub R3 R1 R2
            # 0110001000010000
            # 0110001000010011
            #      1  2  3
            memory_next_instr = self.bytecode_lines_info[str((j+1))]["start"]
            self.register_state[3]=memory_next_instr

            op1 = code1
            op2 = "0x"+f"{int(instructions[2],2):02x}"
            op3 = "0x"+f"{int(instructions[3],2):02x}"
            diff = hex(int(op2, 16) - int(op3, 16))
            if diff[0]=="-":
                # print("negative result")
                pass # not changing the format of resentation
            else:
               diff = "0x"+f"{int(op2, 16) - int(op3, 16):02x}"
            # print(f"difference is {diff} at {self.registers_names[op1][0]}")
            self.register_state[self.registers_names[op1][1]] = diff
        
        elif opcode == '0x07':
            # mult R3 R1 R2
            # 0111001000010000

            memory_next_instr = self.bytecode_lines_info[str((j+1))]["start"]
            self.register_state[3]=memory_next_instr

            op1 = code1
            op2 = "0x"+f"{int(instructions[2],2):02x}"
            op3 = "0x"+f"{int(instructions[3],2):02x}"
            mul = "0x"+f"{int(op2, 16) *int(op3, 16):02x}"
            # print(f"difference is {mul} at {self.registers_names[op1][0]}")
            self.register_state[self.registers_names[op1][1]] = mul
            return mul
            

        elif opcode == '0x08':
            # div R3 R1 R2
            # Divide R1 by R2 and store the result in R3

            memory_next_instr = self.bytecode_lines_info[str((j+1))]["start"]
            self.register_state[3]=memory_next_instr
            # self.register_state[0]=opcode
            
            store_to = code1
            div1 = int(instructions[2],2)
            div2 = int(instructions[3],2)
            # print("from div:")
            # print(div1)
            # print(div2)
            # print(store_to)
            ab = utils.to_binary(div1)
            bb = utils.to_binary(div2)
            r = utils.division(ab, bb)
            self.register_state[self.registers_names[store_to][1]] = "0x"+f"{int(r,2):02x}"


        elif opcode == '0x09':
            # j 0x00000000
            
            mem_to_jump = code1 # memory location
            self.register_state[3] = mem_to_jump
            return self.register_state[3]
        
        elif opcode == '0x0a':
            # jr R1         
            mem_to_jump_in_reg = code1 # register
            if self.registers_names[mem_to_jump_in_reg][0]:
                self.register_state[3] = self.register_state[self.registers_names[mem_to_jump_in_reg][1]]
                return self.register_state[3]
            
            
        
        elif opcode == '0x0b':
            # beq R1 R2 R3
            op1 = code1
            op2 = "0x"+f"{int(instructions[2],2):02x}"
            op3 = "0x"+f"{int(instructions[3],2):02x}"
            boolresult = int(op1, 16)==int(op2, 16)
            # print(f"difference is {mul} at {self.registers_names[op1][0]}")
            if boolresult is True:
              self.register_state[4] = "0x01" # store true in cindition register
            else:
              self.register_state[4] = "0x00" # store false in conditional register

            if self.register_state[4]== "0x01":
                self.register_state[3] = op3  # change program counter register to memory location of R3
            return {"result":boolresult,"PC":self.register_state[3]}

        
        elif opcode == '0x0c':
            # bne R1 R2 R3
            
            op1 = code1
            op2 = "0x"+f"{int(instructions[2],2):02x}"
            op3 = "0x"+f"{int(instructions[3],2):02x}"
            boolresult = int(op1, 16)!=int(op2, 16)
            # print(f"difference is {mul} at {self.registers_names[op1][0]}")
            if boolresult is True:
              self.register_state[4] = "0x01" # store true in cindition register
            else:
              self.register_state[4] = "0x00" # store false in conditional register

            if self.register_state[4]== "0x01":
                self.register_state[3] = op3  # change program counter register to memory location of R3
            return {"result":boolresult,"PC":self.register_state[3]}

        elif opcode == '0x0d':
            # inc R1
            memory_next_instr = self.bytecode_lines_info[str((j+1))]["start"]            
            first = code1 # register

            if self.registers_names[first][0]=="R1":
                inc_result = "0x"+f"{int(first, 16)+1:02x}"
                self.register_state[0] = inc_result
                return inc_result
            elif self.registers_names[first][0]=="R2":
                inc_result = "0x"+f"{int(first, 16)+1:02x}"
                self.register_state[1] = inc_result
                return inc_result
            elif self.registers_names[first][0]=="R3":
                inc_result = "0x"+f"{int(first, 16)+1:02x}"
                self.register_state[2] = inc_result
                return inc_result


        elif opcode == '0x0E':
            # inc R1
            memory_next_instr = self.bytecode_lines_info[str((j+1))]["start"]            
            first = code1 # register

            if self.registers_names[first][0]=="R1":
                dec_result = "0x"+f"{int(first, 16)-1:02x}"
                self.register_state[0] = dec_result
                return dec_result
            elif self.registers_names[first][0]=="R2":
                dec_result = "0x"+f"{int(first, 16)-1:02x}"
                self.register_state[1] = dec_result
                return dec_result
            elif self.registers_names[first][0]=="R3":
                dec_result = "0x"+f"{int(first, 16)-1:02x}"
                self.register_state[2] = dec_result
                return dec_result


    def break_bytecodeline_fours(self,bytecode_lines):
        for i in range(0,len(bytecode_lines)):
            bytecode_lines[i] = bytecode_lines[i].strip()
            halfbyte0 = bytecode_lines[i][0:4]
            halfbyte1 = bytecode_lines[i][4:8]
            halfbyte2 = bytecode_lines[i][8:12]
            halfbyte3 = bytecode_lines[i][12:16]
            bytecode_lines[i] = [halfbyte0,halfbyte1,halfbyte2,halfbyte3]

    def simulate(self,file):
        self.read_bytecode(file)
        utils.update_line_information(self.initial_temp_mem_location,self.bytecode_lines,self.bytecode_lines_info)
        bytecode_lines=self.bytecode_lines

        print("___________________________________")
        print(f" -| R1  |  R2  |  R3  |  PC  | COND ")
        print("___________________________________")

        self.break_bytecodeline_fours(bytecode_lines)
        
        for i in range(0,len(bytecode_lines)):
            self.process_bytecode_line(bytecode_lines[i],i)

            # print(self.bytecode_lines)
            
            state = f" {i+1}|{self.register_state[0]} | {self.register_state[1]} | {self.register_state[2]} | {self.register_state[3]} | {self.register_state[4]}"
            print(state)
            state = f""
