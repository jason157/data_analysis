-- create database
 CREATE DATABASE IF NOT EXISTS DATASET;

-- create source table
USE DATASET;
CREATE TABLE SOURCE_DATASET(
    number VARCHAR(13) not null ,
    username VARCHAR(14) not null ,
    email VARCHAR(30)  not null -- ,
    -- UNIQUE INDEX(number)
);

-- create index
CREATE INDEX index_SOURCE_DATASET ON SOURCE_DATASET(number);


-- create target table
USE DATASET;
CREATE TABLE TARGET_DATASET(
    number VARCHAR(13) not null
);

-- create index fot target dataset
CREATE INDEX index_TARGET_DATASET ON TARGET_DATASET(number)


-- match data
CREATE TABLE RESULT AS
SELECT s.number,s.username,s.email
FROM SOURCE_DATASET s
    INNER JOIN TARGET_DATASET t
ON
    s.number = t.number

