
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- DROP TABLE IF EXISTS sellers;
-- CREATE TABLE sellers (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (64));

DROP TABLE IF EXISTS buyers;
CREATE TABLE buyers (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, username VARCHAR (64), first_name VARCHAR (64), last_name VARCHAR (64));

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                         name VARCHAR (64),
                         category VARCHAR (64));

DROP TABLE IF EXISTS products;
CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                       name VARCHAR (64),
                       category VARCHAR (64),
                       FOREIGN KEY (category) REFERENCES categories(name));

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;