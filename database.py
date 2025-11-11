# backend/database.py
import sqlite3

def create_database():
    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT
        );
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS patient_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            diagnosis TEXT,
            treatment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (email) REFERENCES users(email)
        );
    ''')

    conn.commit()
    conn.close()

# Tạo cơ sở dữ liệu và bảng
create_database()
