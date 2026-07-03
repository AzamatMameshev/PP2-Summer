import psycopg2
from config import load_config

def create_tables():
    """ Creates the contacts table in the PostgreSQL database if it doesn't exist """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            phone_number VARCHAR(50) NOT NULL
        )
        """,
    )
    config = load_config()
    conn = None
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        # Execute SQL commands one by one
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        print("Database and contacts table successfully initialized.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database initialization error: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()