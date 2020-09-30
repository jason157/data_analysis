#!/home/conda/anaconda3/bin/python
# -*- coding: UTF-8 -*-

"""
脚本名称：data_match.py
用途：处理生成的文件，匹配出最终号码. pandas处理
作者：jason157
时间：2020-08-20
"""

# import numpy as np
import datetime
import sys, os
import time
import pandas as pd


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


def help_info():
    hs = '''
    这个脚本做source_file和target_file的并集，给出存在target_file元素的source_file的所有行，存入save_file中
    用法：./{script} source_file target_file save_file key
    source_file: 格式 号码|用户名|邮箱
    target_file:  号码
    save_file：保存的文件目录
    key : 比较的是number还是username
    '''
    print(hs)

@timer
def load_source_data(source_file):
    print("loading source file...")
    return pd.read_csv(source_file, sep='|', error_bad_lines=False, header=None, names=['number', 'username', 'email'])


@timer
def load_target_data(target_file):
    print("loading target file...")
    return pd.read_csv(target_file, sep='|', error_bad_lines=False, header=None, names=['number'])


@timer
def get_result_df(source_df, target_df):
    print("Merging data ....")
    print("Please record the running time !!!")
    return pd.merge(source_df, target_df, on='number')


@timer
def get_intersection(source_df, target_df, key):
    print("getting intersection of two df ....")
    print("Please record the running time !!!")
    source = set(source_df[key])
    target = set(target_df[key])
    return source & target


@timer
def input_check(argv):
    '''
    检查输入参数并提取参数值
    :param argv: 输出的参数
    :return: source_file, target_file, save_file, compare_key
    '''
    if len(argv) != 5:
        print('input error')
        help_info()
        exit(1)

    source_file = argv[1]
    target_file = argv[2]
    save_file = argv[3]
    compare_key = argv[4]

    if not os.path.exists(source_file):
        print(source_file, ' is not exists')
        exit(1)
    if not os.path.exists(target_file):
        print(target_file, ' is not exists')
        exit(1)
    if compare_key not in ('number','username'):
        print("input key error")
        help_info()
        exit(3)

    print("source_file = %s \n" % source_file,
          "target_file = %s \n" % target_file,
          "save_file = %s \n" % save_file,)

    return source_file, target_file, save_file, compare_key


@timer
def main(argv):
    source_file, target_file, save_file, compare_key = input_check(argv)

    source_df = load_source_data(source_file)
    target_df = load_target_data(target_file)

    print("start intersecting!")
    intersection = get_intersection(source_df, target_df, 'number')

    print("start merging!")
    result_df = get_result_df(source_df, target_df)

    if len(intersection) != len(result_df[compare_key]):
        print("Warning, len(intersection_users)=%d, but len(result_df)=%d"
              % len(intersection), len(result_df[compare_key]))
    else:
        print("Data checking is over.length is %s" % len(intersection))

    result_df.to_csv(save_file, sep='|', header=False, index=False)


if __name__ == '__main__':
    test_flag = False
    if test_flag:
        script_file = 'data_match.py'
        source_file = "../data/test_source_data.txt"
        target_file = "../data/test_target_number.txt"
        save_file = "../data/test_output.txt"
        key = "number"
        argv = (script_file, source_file, target_file, save_file, key)
        main(argv)
    else:
        main(sys.argv)
        # main([1, './data/sample_41.txt', '1'])

