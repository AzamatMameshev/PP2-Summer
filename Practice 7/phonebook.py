import csv
import psycopg2
from config import load_config
from connect import create_tables

def insert_contact(username, phone_number):
    sql = """INSERT INTO contacts(username, phone_number) 
             VALUES(%s, %s) ON CONFLICT (username) 
             DO UPDATE SET phone_number = EXCLUDED.phone_number;"""
    config = load_config()
    conn = None
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute(sql, (username, phone_number))
        conn.commit()
        cur.close()
        print(f"Contact '{username}' successfully saved/updated.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Save error: {error}")
    finally:
        if conn is not None:
            conn.close()

def import_from_csv(file_path):
    config = load_config()
    conn = None
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                sql = """INSERT INTO contacts(username, phone_number) 
                         VALUES(%s, %s) ON CONFLICT (username) DO NOTHING;"""
                cur.execute(sql, (row['username'], row['phone_number']))
                if cur.rowcount > 0:
                    count += 1
        conn.commit()
        cur.close()
        print(f"Successfully imported {count} new contacts from CSV.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"CSV import error: {error}")
    finally:
        if conn is not None:
            conn.close()

def update_contact(username, new_phone):
    sql = """UPDATE contacts SET phone_number = %s WHERE username = %s;"""
    config = load_config()
    conn = None
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute(sql, (new_phone, username))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
        if updated_rows > 0:
            print(f"Phone number for '{username}' successfully updated.")
        else:
            print(f"User '{username}' not found.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Update error: {error}")
    finally:
        if conn is not None:
            conn.close()

def query_contacts(search_term="", use_prefix=False):
    config = load_config()
    conn = None
    if use_prefix:
        sql = "SELECT username, phone_number FROM contacts WHERE phone_number LIKE %s ORDER BY username;"
        params = (search_term + '%',)
    else:
        sql = "SELECT username, phone_number FROM contacts WHERE username ILIKE %s ORDER BY username;"
        params = ('%' + search_term + '%',)
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        print("\n--- Search Results ---")
        if not rows:
            print("No contacts found.")
        for row in rows:
            print(f"Name: {row[0]} | Phone: {row[1]}")
        print("----------------------\n")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Search error: {error}")
    finally:
        if conn is not None:
            conn.close()

def delete_contact(search_value, by_phone=False):
    if by_phone:
        sql = "DELETE FROM contacts WHERE phone_number = %s;"
    else:
        sql = "DELETE FROM contacts WHERE username = %s;"
    config = load_config()
    conn = None
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        cur.execute(sql, (search_value,))
        deleted_rows = cur.rowcount
        conn.commit()
        cur.close()
        if deleted_rows > 0:
            print(f"Successfully deleted contacts: {deleted_rows}")
        else:
            print("No matching contacts found to delete.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Delete error: {error}")
    finally:
        if conn is not None:
            conn.close()

def main():
    create_tables()
    while True:
        print("=== Phonebook Application (PostgreSQL) ===")
        print("1. Import contacts from CSV")
        print("2. Add/Update contact manually")
        print("3. Update contact's phone number")
        print("4. Search contacts (by name)")
        print("5. Search contacts (by phone prefix)")
        print("6. Delete contact by name")
        print("7. Delete contact by phone number")
        print("8. Exit")
        choice = input("Select an option (1-8): ").strip()
        
        if choice == '1':
            file_path = input("Enter CSV file path (e.g., contacts.csv): ").strip()
            import_from_csv(file_path)
        elif choice == '2':
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            if name and phone:
                insert_contact(name, phone)
            else:
                print("Name and phone cannot be empty!")
        elif choice == '3':
            name = input("Enter contact name to update: ").strip()
            phone = input("Enter new phone number: ").strip()
            if name and phone:
                update_contact(name, phone)
        elif choice == '4':
            term = input("Enter name (or part of name) to search: ").strip()
            query_contacts(search_term=term, use_prefix=False)
        elif choice == '5':
            prefix = input("Enter phone prefix (e.g., 8707): ").strip()
            query_contacts(search_term=prefix, use_prefix=True)
        elif choice == '6':
            name = input("Enter exact name to delete: ").strip()
            delete_contact(name, by_phone=False)
        elif choice == '7':
            phone = input("Enter exact phone number to delete: ").strip()
            delete_contact(phone, by_phone=True)
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid selection, please try again.\n")

if __name__ == '__main__':
    main()