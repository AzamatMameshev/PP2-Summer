
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INT;
BEGIN
    
    SELECT id INTO v_contact_id FROM contacts WHERE username = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
    v_contact_id INT;
BEGIN
   
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;

    SELECT id INTO v_contact_id FROM contacts WHERE username = p_contact_name;
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    
    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    r_id INT,
    r_username VARCHAR,
    r_email VARCHAR,
    r_birthday DATE,
    r_group_name VARCHAR,
    r_phones TEXT
) 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name AS group_name,
        COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), 'No phones') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.username ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$;