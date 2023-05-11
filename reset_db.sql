CREATE DATABASE chat_room;

\c chat_room

CREATE TABLE users(id SERIAL PRIMARY KEY, email TEXT, firstname TEXT NULL, hashedpassword TEXT);

CREATE TABLE messages(id SERIAL PRIMARY KEY, content TEXT, attime TIMESTAMP, fromuser INT, touser INT,FOREIGN KEY (fromuser) REFERENCES users(id),FOREIGN KEY  (touser) REFERENCES users(id));

ALTER TABLE messages ADD CONSTRAINT fk_xyz FOREIGN KEY (xyz) REFERENCES ChildTable (xyz) ON DELETE CASCADE;

ALTER TABLE messages DROP CONSTRAINT IF EXISTS messages_fromuser_fkey;
ALTER TABLE messages DROP CONSTRAINT IF EXISTS messages_touser_fkey;


ALTER TABLE messages ADD CONSTRAINT "messages_fromuser_fkey" FOREIGN KEY (fromuser) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE messages ADD CONSTRAINT "messages_touser_fkey" FOREIGN KEY (touser) REFERENCES users(id) ON DELETE CASCADE;
