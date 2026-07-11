import os
import csv
import json
from datetime import datetime
import psycopg2
from config import load_config

def print_menu():
    print("\n--- TSIS 1: Extended PhoneBook Management ---")
    print("1. Bulk Import from CSV")
    print("2. Export to JSON File")
    print("3. Import from JSON File")
    print("4. Add Extra Phone to Existing Contact")
    print("5. Move Contact to Another Group")
    print("6. Search & Filter Contacts (with Pagination/Sorting)")
    print("7. Exit")

def add_phone_to_contact(cur):
    username = input("Enter contact username: ").strip()
    phone = input("Enter new phone number: ").strip()
    p_type = input("Enter phone type (home, work, mobile): ").strip().lower()
    
    if p_type not in ['home', 'work', 'mobile']:
        print("Invalid type! Choose home, work, or mobile.")
        return
        
    try:
        cur.execute("CALL add_phone(%s, %s, %s);", (username, phone, p_type))
        print(f"Phone number '{phone}' successfully added to {username}!")
    except Exception as e:
        print(f"Error: {e}")

def move_contact_group(cur):
    username = input("Enter contact username: ").strip()
    group_name = input("Enter target group name (e.g., Family, Work, Friend): ").strip()
    
    try:
        cur.execute("CALL move_to_group(%s, %s);", (username, group_name))
        print(f"Contact '{username}' successfully moved to group '{group_name}'!")
    except Exception as e:
        print(f"Error: {e}")

def export_to_json(cur):
    filename = input("Enter JSON file name for export (e.g., contacts.json): ").strip()
    
    cur.execute("SELECT * FROM search_contacts('');")
    rows = cur.fetchall()
    
    contacts_list = []
    for row in rows:
        contacts_list.append({
            "username": row[1],
            "email": row[2],
            "birthday": str(row[3]) if row[3] else None,
            "group": row[4],
            "phones": row[5]
        })
        
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(contacts_list, f, indent=4, ensure_ascii=False)
        print(f"Successfully exported {len(contacts_list)} contacts to {filename}!")
    except Exception as e:
        print(f"File writing error: {e}")

def import_from_json(conn, cur):
    filename = input("Enter JSON file name for import: ").strip()
    if not os.path.exists(filename):
        print("File not found.")
        return
        
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"JSON Parsing error: {e}")
        return

    for item in data:
        username = item.get("username", "")
        username = username.strip() if username else ""
        
        email = item.get("email", "")
        email = email.strip() if email else None
        
        bday = item.get("birthday", "")
        bday = bday.strip() if bday else None
        
        group_name = item.get("group", "")
        group_name = group_name.strip() if group_name else "Other"
        
        if not username:
            continue

        cur.execute("SELECT id FROM contacts WHERE username = %s;", (username,))
        exists = cur.fetchone()
        
        action = "insert"
        if exists:
            choice = input(f"Contact '{username}' already exists. Overwrite or Skip? (o/s): ").strip().lower()
            if choice == 'o':
                action = "update"
            else:
                print(f"Skipping {username}...")
                continue
                
        cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
        g_row = cur.fetchone()
        if not g_row:
            cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id;", (group_name,))
            group_id = cur.fetchone()[0]
        else:
            group_id = g_row[0]
            
        if action == "insert":
            cur.execute(
                "INSERT INTO contacts (username, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id;",
                (username, email, bday, group_id)
            )
            c_id = cur.fetchone()[0]
        else:
            c_id = exists[0]
            cur.execute(
                "UPDATE contacts SET email = %s, birthday = %s, group_id = %s WHERE id = %s;",
                (email, bday, group_id, c_id)
            )
            cur.execute("DELETE FROM phones WHERE contact_id = %s;", (c_id,))
            
        phone_str = item.get("phones", "")
        if phone_str and phone_str != "No phones":
            for p_part in phone_str.split(','):
                p_part = p_part.strip()
                if not p_part:
                    continue
                if '(' in p_part:
                    parts = p_part.split('(')
                    p_num = parts[0].strip()
                    p_type = parts[1].replace(')', '').strip().lower()
                    if p_type not in ['home', 'work', 'mobile']:
                        p_type = 'mobile'
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);", (c_id, p_num, p_type))
                else:
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);", (c_id, p_part, 'mobile'))
                    
    conn.commit()
    print("JSON import process finished.")

def import_extended_csv(conn, cur):
    filename = input("Enter CSV file name: ").strip()
    if not os.path.exists(filename):
        print("File not found.")
        return
        
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                username = row.get("username", "").strip()
                email = row.get("email", "").strip() or None
                bday = row.get("birthday", "").strip() or None
                group_name = row.get("group", "").strip() or "Other"
                phone = row.get("phone", "").strip()
                p_type = row.get("phone_type", "mobile").strip().lower()
                
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (group_name,))
                cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
                group_id = cur.fetchone()[0]
                
                cur.execute("INSERT INTO contacts (username, email, birthday, group_id) VALUES (%s, %s, %s, %s) ON CONFLICT (username) DO NOTHING RETURNING id;", (username, email, bday, group_id))
                res = cur.fetchone()
                if res:
                    c_id = res[0]
                else:
                    cur.execute("SELECT id FROM contacts WHERE username = %s;", (username,))
                    c_id = cur.fetchone()[0]
                    
                if phone:
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);", (c_id, phone, p_type))
            conn.commit()
            print("CSV conversion completed successfully.")
    except Exception as e:
        print(f"CSV Read failure: {e}")

def advanced_search_loop(cur):
    query = input("Enter global search keyword (or leave empty): ").strip()
    group_filter = input("Filter by Group Name (or leave empty): ").strip()
    
    sort_by = input("Sort by (name / birthday / date_added) [Default: name]: ").strip().lower()
    if sort_by not in ['name', 'birthday', 'date_added']:
        sort_by = 'name'
        
    order_col = "c.username" if sort_by == 'name' else f"c.{sort_by}"
    
    limit = 2
    offset = 0
    
    while True:
        sql_base = f"""
            SELECT 
                c.username, c.email, c.birthday, g.name,
                COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), 'No phones')
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE (c.username ILIKE %s OR c.email ILIKE %s OR p.phone ILIKE %s)
        """
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]
        
        if group_filter:
            sql_base += " AND g.name ILIKE %s"
            params.append(f"%{group_filter}%")
            
        sql_base += f" GROUP BY c.id, g.name ORDER BY {order_col} LIMIT %s OFFSET %s;"
        params.extend([limit, offset])
        
        cur.execute(sql_base, params)
        records = cur.fetchall()
        
        print("\n--- Paginated Contact Records ---")
        if not records:
            print("No records available on this page.")
        for idx, r in enumerate(records, start=offset+1):
            print(f"{idx}. Name: {r[0]} | Email: {r[1]} | BDay: {r[2]} | Group: {r[3]} | Phones: {r[4]}")
            
        print("\nNavigation controls: [n]ext page | [p]rev page | [q]uit to main menu")
        nav = input("Command: ").strip().lower()
        if nav == 'n':
            offset += limit
        elif nav == 'p':
            if offset >= limit:
                offset -= limit
            else:
                print("Already on page 1.")
        elif nav == 'q':
            break

def main():
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                while True:
                    print_menu()
                    choice = input("Select an option (1-7): ").strip()
                    if choice == '1':
                        import_extended_csv(conn, cur)
                    elif choice == '2':
                        export_to_json(cur)
                    elif choice == '3':
                        import_from_json(conn, cur)
                    elif choice == '4':
                        add_phone_to_contact(cur)
                        conn.commit()
                    elif choice == '5':
                        move_contact_group(cur)
                        conn.commit()
                    elif choice == '6':
                        advanced_search_loop(cur)
                    elif choice == '7':
                        print("Exiting application. Goodbye!")
                        break
                    else:
                        print("Invalid selection. Try again.")
    except Exception as e:
        print(f"Database Runtime Error: {e}")

if __name__ == "__main__":
    main()