CREATE TABLE users(
    id INT,
    username VARCHAR(255) NOT NULL,
    contact_number INT UNIQUE NOT NULL CHECK(contact_number >= 80000000 AND contact_number < 99999999), -- write check for contact number
    email VARCHAR(255) UNIQUE NOT NULL CHECK(email  LIKE '%@%'),
    password VARCHAR(255) NOT NULL,
    percentage_preference JSON NOT NULL, -- TODO: check that all values add up to 100%, and each value between 0 to 1
    PRIMARY KEY (id)
);

CREATE TABLE holdings(
    user_id INT,
    ticker VARCHAR(255),
    price NUMERIC,
    number_of_shares NUMERIC,
    last_update_date DATE,
    PRIMARY KEY (user_id, ticker),
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- trigger to validate the json data in percentage preferences
CREATE OR REPLACE FUNCTION validate_percentage_preference_tr()
RETURNS TRIGGER AS $$
DECLARE
    total NUMERIC := 0;
    val NUMERIC := 0;

BEGIN
    FOR val IN
            SELECT value::NUMERIC
            FROM json_each_text(NEW.percentage_preference)
        LOOP
        IF val <= 0 or val > 1 THEN
            RAISE EXCEPTION 'Each value must be > 0 and <= 1';
        END IF;
        total := total + val;
    END LOOP;

    IF total != 1 THEN
        RAISE EXCEPTION 'Values must sum to exactly 1. Got: %', total;
    END IF;

    RETURN NEW;

END;
$$ LANGUAGE plpgsql;

-- attach trigger to table
CREATE TRIGGER validate_percentage_preference
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION validate_percentage_preference_tr();