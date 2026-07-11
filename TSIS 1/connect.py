import psycopg2
from config import load_config

def fix_table_structure():
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                print("Connecting to base for patching...")
                
                # Добавляем недостающие колонки в старую таблицу contacts
                alter_query = """
                ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email VARCHAR(100);
                ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday DATE;
                ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id) ON DELETE SET NULL;
                ALTER TABLE contacts ADD COLUMN IF NOT EXISTS date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                """
                cur.execute(alter_query)
                print("Table 'contacts' successfully updated with new columns!")
                
            conn.commit()
    except Exception as e:
        print(f"Error during patch execution: {e}")

if __name__ == "__main__":
    fix_table_structure()