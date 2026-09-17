import os

import psycopg2
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


try:
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    print("✅ Successfully connected to PostgreSQL!")

    cursor = conn.cursor()

    cursor.execute("SELECT version();")
    result = cursor.fetchone()

    print("PostgreSQL version:")
    print(result[0])

    cursor.close()
    conn.close()

    print("✅ Connection closed successfully.")

except Exception as e:
    print("❌ PostgreSQL connection failed!")
    print(e)