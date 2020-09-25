import unittest
from src.MySQL.mysql_data_handle import *


class MySQLTestCase(unittest.TestCase):
    def test_get_connection(self):
        print("===== test get_connection =======")
        HOST = "192.168.10.134"
        PASSWORD = "jason"
        db = get_connection(HOST, PASSWORD)
        cursor = db.cursor()
        insert_sql = """insert into SOURCE_DATASET(number, username, email) values ( '%s', '%s', '%s');""" \
                     % ("8612312345680", "jason11", "jason@123.com")
        cursor.execute(insert_sql)
        cursor.execute("commit;")
        cursor.execute("select count(*) from SOURCE_DATASET ;")
        result = cursor.fetchall()
        print(result)
        print(type(cursor))


    def test_import_data(self):
        print("===== test import_data =======")
        # import_data("../data/source_test1.txt", "SOURCE_DATASET")

    def test_main(self):
        print("===== test main =======")
        main(("script_name", "../data/source_test1.txt", "SOURCE_DATASET"))


if __name__ == '__main__':
    unittest.main()
