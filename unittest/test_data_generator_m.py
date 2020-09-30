import unittest
from src.data_generator_m import main


class MultiDataGenTestCase(unittest.TestCase):
    def test_data_generator_m(self):
        print("test source data generate!")
        dataset_type = ("source", "target_number", "target_username")
        quantity = 5000
        save_file_name = ("../data/test_source.txt", "../data/test_target_number.txt",
                          "../data/test_target_username.txt")
        for (d_type, file_name) in zip(dataset_type, save_file_name):
            print(d_type, file_name)
            argv = ("test_data_generator_m.py", d_type, quantity, file_name)
            main(argv)

        # for file in save_file_name:
        #     with open(file, 'r') as f:
        #         print(str(file))
        #         print(f.readline())


if __name__ == '__main__':
    unittest.main()
