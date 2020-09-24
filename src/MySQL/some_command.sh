# mysql mysqlimport command
mysqlimport -u root -pPassword --local DATASET source_dataset.txt --fields-terminated-by='|'


# export mysqldump
mysqldump -uroot -proot --databases DATASET --tables RESULT --fields-terminated-by='|' >result.txt