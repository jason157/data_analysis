# MySQL数据库处理数据

##总体思路
1. 首先安装好数据库，并使用`CREATE_TABLE.SQL`创建数据库和表部分，做好准备工作
2. 批量导入，并创建索引。记录创建索引时间
3. 使用`CREATE_TABLE.SQL`数据匹配的部分匹配数据，记录时间
4. 批量导出数据，记录时间
5. 对时间进行分析，尝试优化


# 工具
参阅 OTHERS.SQL 和 some_command.sh
1. 批量导入工具
* load data in file

   load data infile "data/mysql/source.txt" into table e fields terminated by '|';
   
* mysqlimport

mysqlimport -u root -pPassword [--local] dbname filename.txt [OPTION]

mysqlimport -u root -pPassword --local DATASET source.txt --fields-terminated-by='|'

其中，“Password”参数是root用户的密码，必须与-p选项紧挨着；“--local”是在本地计算机中查找文本文件时使用的（指定 --local 后，文本文件可以放在任何地方进行导入，否则只能放在mysql的data目录下）；“dbname”参数表示数据库的名称；“filename.txt”参数指定了文本文件的路径和称，文件里的数据插入到文件名去掉后缀后剩余名字对应的表中；“OPTION”为可选参数选项，其常见的取值有：

--fields-terminated-by=字符串：设置字符串为字段之间的分隔符，可以为单个或多个字符。默认值为制表符“\t”。

--fields-enclosed-by=字符：设置字符来括住字段的值，只能为单个字符。

--fields-optionally-enclosed-by=字符：设置字符括住CHAR、VARCHAR和TEXT等字符型字段，只能为单个字符。

--fields-escaped-by=字符：设置转义字符，默认值为反斜线“\”。

--lines-terminated-by=字符串：设置每行数据结尾的字符，可以为单个或多个字符，默认值为“\n”。

--ignore-lines=n：表示可以忽略前n行。


2. 批量导出工具

SELECT   columnlist   FROM   table   WHERE   condition    INTO   OUTFILE   'filename'   [OPTION]







