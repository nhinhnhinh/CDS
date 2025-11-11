# backend/auth.py
import sqlite3

def create_table():
    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def register_user(email, password):
    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def reset_password(email: str, new_password: str) -> bool:
    """Đặt lại mật khẩu cho người dùng theo email.
    Trả về True nếu cập nhật thành công hoặc tài khoản tồn tại; False nếu email không tồn tại.
    """
    conn = sqlite3.connect('database/data.db')
    c = conn.cursor()
    # kiểm tra tồn tại
    c.execute('SELECT 1 FROM users WHERE email=?', (email,))
    exists = c.fetchone() is not None
    if not exists:
        conn.close()
        return False
    c.execute('UPDATE users SET password=? WHERE email=?', (new_password, email))
    conn.commit()
    conn.close()
    return True
