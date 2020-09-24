#!/bin/env python3
# -*- coding = utf8 -*-

"""
Author: jason157
Date  : 2020-09-23
使用pyMySQL客户端操作数据库，实现导入导出
"""
import MySQLdb


def import_data(data_file_name, table):
    """
    实现加载磁盘的文件（以|分割）并插入到现有的mysql表中
    :param data_file:
    :return:
    """
    # 默认是本地数据库，密码简单为root123 ,需要时修改
    db = get_connection('localhost', "root123")
    cursor = db.cursor()

    with open(data_file_name, 'r', encoding='utf8') as f:
        n = 0
        for line in f:
            number, username, email = line.strip("\n").split("|")
            sql = """
            INSERT INTO SOURCE_DATASET(number,username,email) VALUES ( %s, %s, %s )
            """ % (number, username, email)
            n = n + 1
            try:
                cursor.execute(sql)
                if n == 1000000:
                    n = 0
                    db.commit()
            except:
                db.rollback()

    print("import data done!")

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
                    str = '|'.join(e)
                f.write(str)
                f.write("\n")
        except:
            print("fetch data error! ")
    print("export data done! ")

def get_connection(HOST, PASSWORD):
    return MySQLdb.connet(HOST, "root", PASSWORD, "DATASET", charset='utf8')
