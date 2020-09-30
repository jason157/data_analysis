import unittest
from src.data_match import main


class DataMatchTestCase(unittest.TestCase):
    def test_main(self):
        print("start testing!!")
        script_file = 'data_match.py'
        source_file = "../data/test_source_data.txt"
        target_file = "../data/test_target_number.txt"
        save_file = "../data/test_output.txt"
        key = "number"
        argv = (script_file, source_file, target_file, save_file, key)
        main(argv)
        with open(save_file, 'r') as f:
            lines = len(f.readlines())
            self.assertEqual(lines, 100)


if __name__ == '__main__':
    unittest.main()
