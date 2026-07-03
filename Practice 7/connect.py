import psycopg2
from config import load_config

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            phone_number VARCHAR(20) NOT NULL
        )
        """,
    )
    config = load_config()
    conn = None
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
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