#!/bin/env python3
# -*- coding = utf8 -*-

from tempfile import TemporaryFile
from tempfile import NamedTemporaryFile
import multiprocessing as mp


def save_file(dataset):
    f = TemporaryFile(mode="w+")
    for line in dataset:
        print("element:", line)
        f.write(line)
        f.write('\n')
    # 这是读取文件的关键，把光标移动到前面
    f.seek(0)
    print("in func:", f.readlines())

    return [f]


def save_file_with_file_name(dataset):
    print("=======测试 save_file_with_file_name ========")
    tmp_f = NamedTemporaryFile(mode="w+", dir="../temp", delete=False)
    for line in dataset:
        print("element:", line)
        tmp_f.write(line)
        tmp_f.write('\n')
    # 这是读取文件的关键，把光标移动到前面
    tmp_f.seek(0)
    print("in func:", tmp_f.readlines())
    tmp_f.close()
    return tmp_f.name


def t(x):
    x = int(x)
    return x*x*x


if __name__ == '__main__':
    data = ["1", "2", "3"]
    f = save_file(data)
    f = f[0]
    f.seek(0)
    print("file name:", f.name)
    # 以f.name 打开文件失败
    # f1 = f.name
    # with open(f1, 'r') as ff:
    #     print("open file with filename:", ff.readlines())
    # print(f.readlines())
    f.close()
    # 引入多进程
    print("--------多进程开始------------")
    cores = mp.cpu_count()
    pool = mp.Pool(processes=cores)

    # 此种方式，失败
    data = []
    for i in range(5):
        tmp = []
        for n in range(5):
            tmp.append(str(n))
        data.append(tmp)
    print("data:", data)
    # result = pool.map_async(save_file, data)
    # print(result.get())

    # 在输入为实数的时候，成功了
    for d in data:
        re = pool.map_async(t, d)
        print(re.get())

    f = save_file_with_file_name(data[0])
    with open(f, 'r') as f1:
        print("用文件的方式打开临时文件")
        print(f1.readlines())

    # 成功了，但是会不会还是引起IO问题,需要清理
    print("================开始用命名的临时文件并行处理===========")
    data = []
    for i in range(5):
        tmp = []
        for n in range(5):
            tmp.append(str(n))
        data.append(tmp)
    print("data:", data)
    result = pool.map_async(save_file_with_file_name, data)
    print("result:", result.get())

    # for i in result._vlues:
    #     file = i.get()
    #     file.seek(0)
    #     print(file.read())


