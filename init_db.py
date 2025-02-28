import os
import psycopg2

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    balance INTEGER DEFAULT 0,
    last_signin TIMESTAMP
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS warnings (
    user_id BIGINT PRIMARY KEY,
    count INTEGER DEFAULT 0
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bans (
    user_id BIGINT PRIMARY KEY
);
""")

conn.commit()
cursor.close()
conn.close()

print("Database initialized successfully.")
