CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(r_username VARCHAR, r_phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT username, phone_number 
    FROM contacts
    WHERE username ILIKE '%' || p_pattern || '%'
       OR phone_number ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Function that queries data from the table with pagination (using LIMIT and OFFSET)
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(r_username VARCHAR, r_phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT username, phone_number 
    FROM contacts 
    ORDER BY username
    LIMIT p_limit 
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;