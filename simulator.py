class Simulator():
    BASE_DIR = ""
    registers = {'R1':0,'R2':1,'R3':2,'PC':3,'COND':4} # registers


    def __init__(self,base_dir) -> None:
        self.BASE_DIR = base_dir
        
    def process_opcode(self, instruction):
        '''
        Update registers with values as we read the byte code.
        
        '''

        return instruction