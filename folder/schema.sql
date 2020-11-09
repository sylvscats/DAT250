DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    password TEXT,
    personnumber INTEGER,
    address TEXT,
    AvailableBalance INTEGER,
    email TEXT
    );