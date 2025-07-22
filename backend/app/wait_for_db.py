# wait_for_db.py
import time
import psycopg2
import os

DB_NAME = os.environ.get("DB_NAME", "creditdb")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "ykpostdb")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")

print("⏳ Waiting for database...")

while True:
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.close()
        break
    except psycopg2.OperationalError:
        print("Database unavailable, waiting 1 second...")
        time.sleep(1)

print("✅ Database is ready!")
