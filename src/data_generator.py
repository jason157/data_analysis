#!/bin/env python3
# -*- coding = utf8 -*-

"""
Author: jason157
Date  : 2020-09-23
生成测试数据集，使用方法：
./{scrip_name} dataset_type  quantity save_file_name
                 dataset_type "source" or "target_number" or "target_username"
                 quantity numbers of the dataset
                 save_file_name :the file name your want to save to
"""
import random
import string
import time


def timer(function):
    """
    装饰器函数timer
    :param function:想要计时的函数
    :return:
    """
    def wrapper(*args, **kwargs):
        time_start = time.time()
        res = function(*args, **kwargs)
        cost_time = time.time() - time_start
        print("【%s】运行时间：【%s】秒" % (function.__name__, cost_time))
        return res

    return wrapper


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


@timer
def source_dataset_generator(quantity):
    """
    源数据集生成器
    :param number:数量
    :return:
    """
    for n in range(quantity):
        yield source_data_string_generator()


@timer
def target_dataset_generator_number(quantity):
    """
    目标数据字符生成,号码
    :param quantity 数量
    :return: 13位手机号码列表
    """
    for n in range(quantity):
        yield target_dataset_string_generator("number")


@timer
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


def save_file(dataset, file_name):
    """
    把生成的数据集写入文件中
    :param dataset: 数据集，必须是可迭代数据类型
    :param file_name: 写入的文件名
    :return:
    """

    with open(file_name,'w',encoding='utf8') as f:
        for line in dataset:
            f.write(line)
            f.write('\n')


@timer
def main():
    import sys
    import os

    help_string = """Usage:
                     ./{scrip_name} dataset_type  quantity save_file_name
                     dataset_type "source" or "target_number" or "target_username"
                     quantity numbers of the dataset 
                     save_file_name :the file name your want to save to 
                     """
    if len(sys.argv) != 4:
        print(help_string)
        exit(2)

    dataset_type = sys.argv[1]
    quantity = int(sys.argv[2])
    save_file_name = sys.argv[3]
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

    if dataset_type == "source":
        save_file(source_dataset_generator(quantity), save_file_name)
    elif dataset_type == "target_number":
        save_file(target_dataset_generator_number(quantity), save_file_name)
    elif dataset_type == "target_username":
        save_file(target_dataset_generator_username(quantity), save_file_name)
    print("done!")


if __name__ == '__main__':
    main()

