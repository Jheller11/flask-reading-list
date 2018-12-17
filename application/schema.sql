DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS list_item;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE list_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL DEFAULT 'Title not found',
    url TEXT NOT NULL,
    read INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (author_id) REFERENCES user (id)
);