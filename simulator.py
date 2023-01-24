class Simulator():
    BASE_DIR = ""
    registers_names = {'R1':0,'R2':1,'R3':2,'PC':3,'COND':4} # registers
    register = [[],[],[],[],[],[]]

    def __init__(self,base_dir) -> None:
        self.BASE_DIR = base_dir
        
    def process_opcode(self, instructions):
        '''
        Update registers with values as we read the byte code.
        
        '''
        # change line to half-bytes [[opcode][R1][R2][R3][PC][COND]
		
        for j in range(0,len(instructions)):
            '''
            b5 for NULL/EMPTY register, b0 for FALSE, b1 TRUE
            '''
            if instructions[j][0] == '0x00':
                start_memory = self.all_lines_info[str((j-1))]["start"]
                register[0][:]=f"{eval(instructions[j][0]):04b}"
                register[4]=f"{eval(start_memory):04b}"

            elif instructions[j][0] == '0x01':
                register[0][:]=f"{eval(instructions[j][0]):04b}"

            elif instructions[j][0] == '0x02':
                # li R1 0x00000000
                start_memory = self.all_lines_info[str((j+1))]["start"]
                register[0][:]=f"{eval(instructions[j][0]):04b}"
                register[4]=f"{eval(start_memory):04b}"
                register[5]=f"{5:04b}" # COND b5 for NULL/EMPTY, b0 for FALSE, b1 TRUE
                register[6]=f"{0:04b}"
                register[7]=f"{0:04b}"
                if instructions[j][1] == 'R1':
                    register[1]=f"{eval(instructions[j][2]):04b}"
                    register[2]=f"{5:04b}"
                    register[3]=f"{5:04b}"
                elif instructions[j][1] == 'R2':
                    register[1]=f"{5:04b}"
                    register[2]=f"{eval(instructions[j][2]):04b}"
                    register[3]=f"{5:04b}"
                elif instructions[j][1] == 'R3':
                    register[1]=f"{5:04b}"
                    register[2]=f"{5:04b}"
                    register[3]=f"{eval(instructions[j][2]):04b}"
                
            elif instructions[j][0] == '0x03':
                # lw R1 R2
                register[0][:]=f"{eval(instructions[j][0]):04b}"
            
            elif instructions[j][0] == '0x04':
                register[0][:]=f"{eval(instructions[j][0]):04b}"

            elif instructions[j][0] == '0x05':
                register[0][:]=f"{eval(instructions[j][0]):04b}"
            
            elif instructions[j][0] == '0x06':
                register[0][:]=f"{eval(instructions[j][0]):04b}"
            
            elif instructions[j][0] == '0x07':
                register[0][:]=f"{eval(instructions[j][0]):04b}"

            elif instructions[j][0] == '0x08':
                register[0][:]=f"{eval(instructions[j][0]):04b}"
            
            elif instructions[j][0] == '0x09':
                register[0][:]=f"{eval(instructions[j][0]):04b}"
            
            elif instructions[j][0] == '0x0A':
                register[0][:]=f"{eval(instructions[j][0]):04b}"
            
            elif instructions[j][0] == '0x0B':
                register[0][:]=f"{eval(instructions[j][0]):04b}"
            
            elif instructions[j][0] == '0x0C':
                register[0][:]=f"{eval(instructions[j][0]):04b}"

            elif instructions[j][0] == '0x0D':
                register[0][:]=f"{eval(instructions[j][0]):04b}"

            elif instructions[j][0] == '0x0E':
                register[0][:]=f"{eval(instructions[j][0]):04b}"

            elif instructions[j][0] == '0x0F':
                register[0][:]=f"{eval(instructions[j][0]):04b}"

            print(register)
            register = [[],[],[],[],[],[],[],[]]
