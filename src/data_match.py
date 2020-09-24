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
    用法：./{script} source_file target_file save_file
    source_file: 格式 号码|用户名|邮箱
    target_file:  号码
    save_file：保存的文件目录
    '''
    print(hs)


@timer
def main(argv):
    source_file, target_file, save_file = input_check(argv)

    source_df = load_source_data(source_file)
    target_df = load_target_data(target_file)

    intersection_users = get_intersection_users(source_df, target_df)

    result_df = get_result_df(source_df, target_df)

    if len(intersection_users) != len(result_df.user):
        print("Warning, len(intersection_users)=%s, but len(result_df)=%s".format(len(intersection_users),
                                                                                  len(result_df.user)))
    else:
        print("Data checking is over.length is %s"%len(intersection_users) )

    result_df.to_csv(save_file, sep='|', header=False, index=False)


@timer
def load_source_data(source_file):
    print("loading source file...")
    return pd.read_csv(source_file, sep='|', error_bad_lines=False, header=0, names=['number', 'username', 'email'])


@timer
def load_target_data(target_file):
    print("loading target file...")
    return pd.read_csv(target_file, sep='|', error_bad_lines=False, header=0, names=['number'])

@timer
def get_result_df(source_df, target_df):
    print("Merging data ....")
    print("Please record the running time !!!")
    return pd.merge(source_df, target_df, on='number')


@timer
def get_intersection_users(source_df, target_df):
    print("geting intersection users ....")
    print("Please record the running time !!!")
    source_users = set(source_df.user)
    target_users = set(target_df.user)
    return source_users & target_users


@timer
def input_check(argv):
    if len(argv) != 4:
        print('input error')
        help_info()
        exit(1)

    source_file = argv[1]
    target_file = argv[2]
    save_file = argv[3]

    if not os.path.exists(source_file):
        print(source_file, ' is not exists')
        exit(1)
    if not os.path.exists(target_file):
        print(target_file, ' is not exists')
        exit(1)

    print("source_file = %s \n"%source_file,
          "target_file = %s \n"%target_file,
          "save_file = %s \n"%save_file,)

    return source_file, target_file, save_file


if __name__ == '__main__':
    main(sys.argv)
    # main([1, './data/sample_41.txt', '1'])

