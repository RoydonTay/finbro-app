CREATE TABLE users(
    id INT,
    username VARCHAR(255) NOT NULL,
    contact_number INT UNIQUE NOT NULL CHECK(contact_number >= 80000000 AND contact_number < 99999999), -- write check for contact number
    email VARCHAR(255) UNIQUE NOT NULL CHECK(email  LIKE '%@%'),
    password VARCHAR(255) NOT NULL,
    percentage_preference JSON NOT NULL,
    PRIMARY KEY (id),
);

CREATE TABLE holdings(
    user_id INT,
    ticker VARCHAR(255),
    price MONEY,
    number_of_shares NUMERIC,
    last_update_date DATE,
    PRIMARY KEY (user_id, ticker),
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);