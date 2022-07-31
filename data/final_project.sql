DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    uid serial NOT NULL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    date_registered TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO users (username, password) VALUES ( 'test_user1', 'test_pw1' );
INSERT INTO users (username, password) VALUES ( 'test_user2', 'test_pw2' );

DROP TABLE IF EXISTS files;
CREATE TABLE files (
    file_id serial NOT NULL PRIMARY KEY,
    uploader serial NOT NULL,
--     image TEXT NOT NULL DEFAULT 'test image',
--     video TEXT NOT NULL DEFAULT 'test video',
    letter TEXT NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (uploader) REFERENCES users(uid)
);

INSERT INTO files (uploader, letter) VALUES ( 1, 'asdf' );
INSERT INTO files (uploader, letter) VALUES ( 2, 'abcd' );
