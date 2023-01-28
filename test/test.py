import unittest
import run
from simulator import Simulator
from pathlib import Path
from assembler import update_line_information


sim = Simulator(Path().resolve())
sim.read_bytecode("test/compiled_test.s")
update_line_information(sim.initial_temp_mem_location,sim.bytecode_lines,sim.bytecode_lines_info)
sim.break_bytecodeline_fours(sim.bytecode_lines)

class TestRun(unittest.TestCase):
    
    def test_extra_make_input_arguments(self):
        # testing extra input arguments for "make" command option
        self.assertEqual(run.run(["run.py","make","filename.s","filename.obj","extra.p"],[]),"Too many arguments")

    def test_missing_make_input_arguments(self):
        # testing missing input arguments for "make" command option
        self.assertEqual(run.run(["run.py","make","filename.s"],[]),"Missing argument")

    def test_extra_read_input_arguments(self):
        # testing extra input arguments for "read" command option
        self.assertEqual(run.run(["run.py","read","filename.s","extra.txt"],[]),"Too many arguments")

    def test_missing_read_input_arguments(self):
        # testing missing input arguments for "read" command option
        self.assertEqual(run.run(["run.py","read"],[]),"Missing argument")

    # missing file test

    def test_instruction_mul(self):
        res = sim.process_bytecode_line(sim.bytecode_lines[6],6)
        
        # self.assertEqual("0x"+f"{int(sim.bytecode_lines[6][0],2):02x}","0x07")
        # self.assertEqual(res,"0x00")

    def test_instruction_beq(self):
        res = sim.process_bytecode_line(sim.bytecode_lines[10],10)
        self.assertEqual(res["result"],False)
        # self.assertEqual(res,"0x00")

    def test_instruction_bne(self):
        res = sim.process_bytecode_line(sim.bytecode_lines[11],11)
        self.assertEqual(res["result"],True)
        # self.assertEqual(res,"0x00")   

    def test_instruction_inc(self):
        res = sim.process_bytecode_line(sim.bytecode_lines[12],12)
        # self.assertEqual(res["result"],False)
        # self.assertEqual(res,"0x00")  

    def test_instruction_dec(self):
        res = sim.process_bytecode_line(sim.bytecode_lines[13],13)
        # self.assertEqual(res["result"],False)
        # self.assertEqual(res,"0x00") 

    def test_instruction_jr(self):
        res = sim.process_bytecode_line(sim.bytecode_lines[9],9)
        print(sim.register_state)
        # self.assertEqual(res["result"],False)
        # self.assertEqual(res,"0x00") 
    

if __name__ == "__main__":
    unittest.main()