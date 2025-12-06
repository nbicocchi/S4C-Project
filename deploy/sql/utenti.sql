PRAGMA foreign_keys=OFF;
CREATE TABLE utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            ruolo TEXT NOT NULL
        );

-- Insert one default user
INSERT INTO utenti (email, password, ruolo)
VALUES ('admin@example.com', 'admin', 'admin');