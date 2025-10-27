import psycopg2
import os

host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
port = os.getenv("DB_PORT")

def connect_db():
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    cur = conn.cursor()
    return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()

def list_tables(cur):
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema='public';
    """)
    return [table[0] for table in cur.fetchall()]