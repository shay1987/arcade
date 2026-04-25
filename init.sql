CREATE DATABASE IF NOT EXISTS mydb;
USE mydb;

CREATE TABLE IF NOT EXISTS accounts (
    username          VARCHAR(50)  PRIMARY KEY,
    full_name         VARCHAR(100) NOT NULL,
    password          VARCHAR(100) NOT NULL,
    security_question VARCHAR(200) NOT NULL,
    security_answer   VARCHAR(100) NOT NULL,
    last_login        DATETIME     NULL
);

CREATE TABLE IF NOT EXISTS admins (
    username VARCHAR(50)  PRIMARY KEY,
    password VARCHAR(100) NOT NULL
);
