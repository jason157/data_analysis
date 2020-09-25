#!/bin/env python3
# -*- coding = utf8 -*-

"""
Author: jason157
Date  : 2020-09-23
使用pyMySQL客户端操作数据库，实现导入导出
"""
import pymysql
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


@timer
def import_data(data_file_name, table):
    """
    实现加载磁盘的文件（以|分割）并插入到现有的mysql表中
    :param data_file_name: 导入的文件名
    :param table: 导入文件到哪个表
    :return: False :导入失败 True :导入成功
    """
    # 默认是本地数据库，密码简单为root123 ,需要时修改
    HOST = "192.168.10.134"
    PASSWD = "jason"
    db = get_connection(HOST, PASSWD)
    cursor = db.cursor()

    # 判断表是否存在
    cursor.execute("show tables;")
    tables = cursor.fetchall()[0][0]
    if table not in tables:
        print(" Error : %s not in database tables" % table)
        return False

    with open(data_file_name, 'r', encoding='utf8') as f:
        n = 0
        print("start importing!")
        for line in f:
            number, username, email = line.strip("\n").split("|")
            sql = """
            INSERT INTO DATASET.SOURCE_DATASET (number,username,email) VALUES ( '%s', '%s', '%s' )
            """ % (number, username, email)
            # print(sql)
            n = n + 1
            try:
                cursor.execute(sql)
                if n == 100000:
                    n = 0
                    db.commit()
            except Exception as e:
                db.rollback()
                print("import error! ")
                return False
        db.commit()

    print("import data done!")
    return True


def export_data(save_file_name, table):
    """
    实现从数据库表获取数据并写到文件中
    :param save_file_name:
    :param table:
    :return:
    """

    db = get_connection('localhost', "root123")
    cursor = db.cursor()

    with open(save_file_name, 'w', encoding='utf8') as f :
        sql = "SELECT * FROM RESULT"
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                for e in row:
                    tmp = '|'.join(e)
                f.write(tmp)
                f.write("\n")
        except:
            print("fetch data error! ")
    print("export data done! ")


def get_connection(host, password):
    return pymysql.connect(host, "jason", password, "DATASET", charset='utf8')


def main(argv):
    import os
    help_string = """Usage:
        %s import_file_name import_table
        import_file_name:要导入的文件名
        import_table： 要导入到的表格
        """ % argv[0]

    if len(argv) != 3:
        print("输入参数不对，请参考帮助")
        print(help_string)
        exit(2)

    import_file_name = argv[1]
    import_table = argv[2]

    if not os.path.exists(import_file_name):
        print("输入的文件不存在!")
        print(help_string)
        exit(3)

    return import_data(import_file_name, import_table)


if __name__ == '__main__':
    import sys
    main(sys.argv)
