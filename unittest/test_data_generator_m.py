import unittest
from src.data_generator_m import main


class MultiDataGenTestCase(unittest.TestCase):
    def test_data_generator_m(self):
        dataset_type = "source"
        quantity = 5000000
        save_file_name = "../data/test1.txt"
        argv = ("test_data_generator_m.py", dataset_type, quantity, save_file_name)
        main(argv)


if __name__ == '__main__':
    unittest.main()
