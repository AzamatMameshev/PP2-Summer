import csv
import psycopg2
from config import load_config
from connect import create_tables

def insert_or_update_contact(username, phone_number):
    """ Calls the stored procedure 'upsert_contact' """
    config = load_config()
    conn = None
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        # Calling the procedure from procedures.sql
        cur.execute("CALL upsert_contact(%s, %s);", (username, phone_number))
        conn.commit()
        cur.close()
        print(f"Contact '{username}' successfully processed via Stored Procedure.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error executing procedure: {error}")
    finally:
        if conn is not None:
            conn.close()

def import_from_csv_bulk(file_path):
    """ Reads CSV data and passes arrays into the bulk insert procedure with validation """
    config = load_config()
    conn = None
    usernames = []
    phones = []
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                usernames.append(row['username'])
                phones.append(row['phone_number'])
                
        conn = psycopg2.connect(**config)
        # Enable autocommit to catch NOTICE logs from PostgreSQL immediately
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Calling the bulk insert procedure from procedures.sql
        cur.execute("CALL insert_bulk_contacts(%s, %s);", (usernames, phones))
        
        # Display validation warnings sent from the database via RAISE NOTICE
        if conn.notices:
            print("\n[Validation Warnings from DB]:")
            for notice in conn.notices:
                print(notice.strip())
            conn.notices.clear()
            
        cur.close()
        print("Bulk import operation completed.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Bulk import error: {error}")
    finally:
        if conn is not None:
            conn.close()

def search_by_pattern(pattern):
    """ Calls the database function 'get_contacts_by_pattern' """
    config = load_config()
    conn = None
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        # Querying the function from functions.sql
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
        rows = cur.fetchall()
        cur.close()
        print(f"\n--- Search Results for '{pattern}' ---")
        if not rows:
            print("No contacts found.")
        for row in rows:
            print(f"Name: {row[0]} | Phone: {row[1]}")
        print("---------------------------------------\n")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Search function error: {error}")
    finally:
        if conn is not None:
            conn.close()

def search_paginated(limit, offset):
    """ Calls the database function 'get_contacts_paginated' using LIMIT and OFFSET """
    config = load_config()
    conn = None
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        # Querying the pagination function from functions.sql
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
        rows = cur.fetchall()
        cur.close()
        print(f"\n--- Paginated Results (Limit: {limit}, Offset: {offset}) ---")
        if not rows:
            print("No more records found on this page.")
        for row in rows:
            print(f"Name: {row[0]} | Phone: {row[1]}")
        print("----------------------------------------------------------\n")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Pagination error: {error}")
    finally:
        if conn is not None:
            conn.close()

def delete_via_procedure(search_value, by_phone=False):
    """ Calls the stored procedure 'delete_contact_by_value' """
    config = load_config()
    conn = None
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        # Calling the delete procedure from procedures.sql
        cur.execute("CALL delete_contact_by_value(%s, %s);", (search_value, by_phone))
        conn.commit()
        cur.close()
        print(f"Delete procedure executed for value: '{search_value}'.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Delete procedure error: {error}")
    finally:
        if conn is not None:
            conn.close()

def main():
    # Make sure tables are initialized on startup
    create_tables()
    
    while True:
        print("=== Phonebook App (Practice 8: Stored Logic) ===")
        print("1. Bulk Import from CSV (with validation procedure)")
        print("2. Add/Update contact (Upsert procedure)")
        print("3. Pattern search (Function)")
        print("4. Paginated search (Function)")
        print("5. Delete contact by name (Procedure)")
        print("6. Delete contact by phone (Procedure)")
        print("7. Exit")
        choice = input("Select an option (1-7): ").strip()
        
        if choice == '1':
            file_path = input("Enter CSV file path (e.g., contacts.csv): ").strip()
            import_from_csv_bulk(file_path)
        elif choice == '2':
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            if name and phone:
                insert_or_update_contact(name, phone)
            else:
                print("Name and phone cannot be empty!")
        elif choice == '3':
            pattern = input("Enter search pattern (part of name or number): ").strip()
            search_by_pattern(pattern)
        elif choice == '4':
            try:
                limit = int(input("Enter page size (LIMIT): ").strip())
                offset = int(input("Enter start index (OFFSET): ").strip())
                search_paginated(limit, offset)
            except ValueError:
                print("Please enter valid integers for pagination.")
        elif choice == '5':
            name = input("Enter exact name to delete: ").strip()
            delete_via_procedure(name, by_phone=False)
        elif choice == '6':
            phone = input("Enter exact phone number to delete: ").strip()
            delete_via_procedure(phone, by_phone=True)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid selection, please try again.\n")

if __name__ == '__main__':
    main()