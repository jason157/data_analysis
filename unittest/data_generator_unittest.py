import unittest
from src.data_generator import *


class data_generatorTestCase(unittest.TestCase):
    def test_random_string_generator(self):
        print("====random_string_generator 测试 ====")
        print("输出9个数字：", random_string_generator(0, 9))
        print("输出8个字母：", random_string_generator(1, 8))
        print("输出字母和数字混合，长度10：", random_string_generator(2, 10))

    def test_source_data_string_generator(self):
        print("====source_data_string_generator 测试 ====")
        print("输出一行源数据集：", source_data_string_generator())

    def test_target_dataset_string_generator(self):
        print("====target_dataset_string_generator 测试 ====")
        print("一个号码：", target_dataset_string_generator("number"))
        print("一个名字：", target_dataset_string_generator("username"))

    def test_target_dataset_generator_number(self):
        print("====target_dataset_generator_number 测试 ====")
        print("目标数据集生成, 号码：")
        for i in target_dataset_generator_number(5):
            print(i)

    def test_target_dataset_generator_username(self):
        print("====target_dataset_generator_username 测试 ====")
        print("目标数据集生成, 用户名：")
        for i in target_dataset_generator_username(5):
            print(i)

    def test_source_dataset_generator(self):
        print("====source_dataset_generator 测试 ====")
        print("源数据集生成测试：")
        for i in source_dataset_generator(5):
            print(i)


    def test_save_file(self):
        print("====save_file 测试 ====")
        save_file(source_dataset_generator(50), "../data/test.txt")



if __name__ == '__main__':
    unittest.main()
    #print(source_data_string_generator())