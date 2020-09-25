#!/bin/env python3
# -*- coding = utf8 -*-

"""
Author: jason157
Date  : 2020-09-25
生成测试数据集，使用方法：
./{scrip_name} dataset_type  quantity save_file_name
                 dataset_type "source" or "target_number" or "target_username"
                 quantity numbers of the dataset
                 save_file_name :the file name your want to save to
"""
import os
import time
import string
import random

# from src.data_generator import *
from tempfile import TemporaryFile, NamedTemporaryFile


def random_string_generator(type, length):
    """
    返回指定长度的随机字符串
    :param type: 0 数字 , 1 大小写字母， 2 字母+数字 3 小写字母，4 大写字母
    :param length: 字符串长度
    :return:
    """

    # if type == 1:
    #     string_obj = string.digits
    # elif type == 2:
    #     string_obj = string.ascii_letters
    # elif type == 3:
    #     string_obj = string.ascii_letters + string.digits
    # else:
    #     raise Exception(print("type is error"))
    string_obj = [string.digits, string.ascii_letters, string.ascii_letters + string.digits,
                  string.ascii_lowercase, string.ascii_uppercase]
    if 0 <= type <= len(string_obj):
        return "".join(random.choices(string_obj[type], k=length))
    else:
        raise Exception("para Type Error")


def target_dataset_generator_number(quantity):
    """
    目标数据字符生成,号码
    :param quantity 数量
    :return: 13位手机号码列表
    """
    for n in range(quantity):
        yield target_dataset_string_generator("number")


def target_dataset_generator_username(quantity):
    """
    目标数据字符生成，用户名
    :param quantity 数量
    :return: 用户名列表
    """
    for n in range(quantity):
        yield target_dataset_string_generator("username")


def source_data_string_generator():
    """
    源数据生成，返回一行数据
    :return: 13位手机号码|用户名|邮箱
    """
    number = '861' + random_string_generator(0, 10)
    user_name = random_string_generator(4, 1) \
                + random_string_generator(2, random.randint(4, 13))
    common_top_level_domain_name = [".net", ".com", ".org", ".net"]
    email_domain = random_string_generator(3, random.randint(3, 10))
    email = str(user_name) + '@' + email_domain + random.choice(common_top_level_domain_name)
    return "|".join((number, user_name, email))


def target_dataset_string_generator(type):
    """
    生成目标数据字符，type number 手机号码， username 用户名
    :param type: 1 生成号码列表，2生成用户名列表
    :return: 手机号码或者用户名
    """
    if type == "number":
        return '861' + random_string_generator(0, 10)
    elif type == "username":
        return random_string_generator(4, 1) + random_string_generator(2, random.randint(5, 13))


def save_file(dataset):
    """
    把生成的数据集写入文件中
    :param dataset: 数据集，必须是可迭代数据类型
    :param file_name: 写入的文件名
    :return:
    """
    f = TemporaryFile(mode="w+")
    for line in dataset:
        f.write(line)
        f.write('\n')
    return f


def source_dataset_generator(quantity):
    """
    源数据集生成器
    :param number:数量
    :return:
    """
    start_time = time.time()
    data_list = []
    for n in range(quantity):
        data_list.append(source_data_string_generator())
    print("Timimg recorder : generate %f lines cost %f seconds" % (quantity, time.time() - start_time))
    return data_list


def save_file_with_file_name(dataset):
    # print("=======测试 save_file_with_file_name ========")
    tmp_path = "./tmp"
    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)
    tmp_f = NamedTemporaryFile(mode="w+", dir=tmp_path, delete=False)
    for line in dataset:
        # print("element:", line)
        tmp_f.write(line)
        tmp_f.write('\n')
    # 这是读取文件的关键，把光标移动到前面
    tmp_f.seek(0)
    # print("in func:", tmp_f.readlines())
    tmp_f.close()
    return tmp_f.name


def main(argv):
    import os
    import math
    import multiprocessing
    time1 = time.time()

    help_string = """Usage:
                     ./{scrip_name} dataset_type  quantity save_file_name
                     dataset_type "source" or "target_number" or "target_username"
                     quantity numbers of the dataset 
                     save_file_name :the file name your want to save to 
                     """
    if len(argv) != 4:
        print(help_string)
        exit(2)

    dataset_type = argv[1]
    quantity = int(argv[2])
    save_file_name = argv[3]
    path = os.path.dirname(save_file_name)
    file_name = os.path.basename(save_file_name)

    if dataset_type not in ("source", "target_number", "target_username"):
        print("dataset_type error!")
        print(help_string)
        exit(3)
    elif not isinstance(quantity, int):
        print("quantity error! your input type is %s" % type(quantity))
        print(help_string)
        exit(3)
    elif not os.path.exists(path):
        print("%s does not exist, make it " % path)
        os.mkdir(path)

    # 并行处理

    BASE_LINE_QUANTITY = 500000
    # BASE_LINE_QUANTITY = 5
    LINE_TIMES = math.floor(quantity / BASE_LINE_QUANTITY)
    LINE_REMAINDER = quantity - BASE_LINE_QUANTITY * LINE_TIMES

    cores = multiprocessing.cpu_count()
    pool1 = multiprocessing.Pool(processes=cores)
    pool2 = multiprocessing.Pool(processes=cores)
    data_list = []
    tmp_file_list = []
    argv_list = []
    quantity_list = []

    if LINE_TIMES > 0:
        print("M start ! now the time is %s " % str(time.time() - time1))
        for n in range(LINE_TIMES):
            # data_list.append(source_dataset_generator(LINE_TIMES))
            quantity_list.append(BASE_LINE_QUANTITY)
    # data_list.append(source_dataset_generator(LINE_TIMES))
    quantity_list.append(LINE_REMAINDER)
    res1 = pool1.map_async(source_dataset_generator, quantity_list)
    data_list = res1.get()
    pool1.close()
    print("generator data done! cost time %s" % str(time.time() - time1))
    res = pool2.map_async(save_file_with_file_name, data_list)
    tmp_file_list = res.get()
    print("tmp file dealing done! cost time %s " % str(time.time() - time1))
    with open(save_file_name, 'w') as f:
        for file in tmp_file_list:
            t = open(file, 'r')
            t.seek(0)
            for line in t.readlines():
                f.write(line)
                # f.write("\n")
            t.close()
            os.remove(file)

    print("save file done!cost time %s" % str(time.time() - time1))


if __name__ == '__main__':
    import sys
    time_start = time.time()
    main(sys.argv)
    # 测试
    # argv = ("test_data_generator_m.py", "source", 50, "../data/test1.txt")
    # main(argv)
    cost_time = time.time() - time_start
    print("【%s】运行时间：【%s】秒" % ("main", cost_time))


