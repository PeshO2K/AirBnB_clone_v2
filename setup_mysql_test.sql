--  a script that creates the database hbnb_test_db and the user hbnb_test.
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'Hbnb_test_pwd1';
GRANT ALL PRIVILEGES ON  hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
