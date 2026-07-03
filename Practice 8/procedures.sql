-- 1. Procedure to insert a new user by name and phone; if the user already exists, update their phone
CREATE OR REPLACE PROCEDURE upsert_contact(p_username VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE username = p_username) THEN
        UPDATE contacts SET phone_number = p_phone WHERE username = p_username;
    ELSE
        INSERT INTO contacts(username, phone_number) VALUES(p_username, p_phone);
    END IF;
END;
$$;

-- 2. Procedure to delete data from the table by username or phone
CREATE OR REPLACE PROCEDURE delete_contact_by_value(p_value VARCHAR, p_by_phone BOOLEAN)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_by_phone THEN
        DELETE FROM contacts WHERE phone_number = p_value;
    ELSE
        DELETE FROM contacts WHERE username = p_value;
    END IF;
END;
$$;

-- 3. Procedure to insert many new users from a list of names and phones with validation
CREATE OR REPLACE PROCEDURE insert_bulk_contacts(p_usernames VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    v_phone VARCHAR;
BEGIN
    FOR i IN 1..cardinality(p_usernames) LOOP
        v_phone := p_phones[i];
        
        -- Basic validation: check if phone contains numbers and is long enough
        IF v_phone SIMILAR TO '\+?[0-9\- \(\)]+' AND length(v_phone) >= 5 THEN
            INSERT INTO contacts(username, phone_number) 
            VALUES(p_usernames[i], v_phone)
            ON CONFLICT (username) DO UPDATE SET phone_number = EXCLUDED.phone_number;
        ELSE
            -- Send validation warning back to client (Python)
            RAISE NOTICE 'Validation failed for user: %, invalid phone format: %', p_usernames[i], v_phone;
        END IF;
    END LOOP;
END;
$$;