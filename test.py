import unittest
import run

class TestRun(unittest.TestCase):
    
    def test_extra_make_input_arguments(self):
        # testing extra input arguments for "make" command option
        self.assertEqual(run.run(["run.py","make","filename.s","filename.obj","extra.p"]),"Too many arguments")

    def test_missing_make_input_arguments(self):
        # testing missing input arguments for "make" command option
        self.assertEqual(run.run(["run.py","make","filename.s"]),"Missing argument")

    def test_extra_read_input_arguments(self):
        # testing extra input arguments for "read" command option
        self.assertEqual(run.run(["run.py","read","filename.s","extra.txt"]),"Too many arguments")

    def test_missing_read_input_arguments(self):
        # testing missing input arguments for "read" command option
        self.assertEqual(run.run(["run.py","read"]),"Missing argument")

    # missing file test

    

if __name__ == "__main__":
    unittest.main()