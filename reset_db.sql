CREATE DATABASE chat_room;

\c chat_room

CREATE TABLE users(id SERIAL PRIMARY KEY, email TEXT, firstname TEXT NULL, hashedpassword TEXT);

CREATE TABLE messages(id SERIAL PRIMARY KEY, content TEXT, attime TIMESTAMP, fromuser INT, touser INT,FOREIGN KEY (fromuser) REFERENCES users(id),FOREIGN KEY  (touser) REFERENCES users(id));