# backend/seed_demo_user.py
"""
Tạo tài khoản demo an toàn (nếu chưa tồn tại) trong SQLite.
Cách chạy:
    python backend\\seed_demo_user.py [email] [password]
Mặc định: doctor@example.com 123456
"""
import os
import sys
import sqlite3

# Thêm project root vào sys.path để import backend.*
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)

from backend.auth import register_user


def main():
    email = sys.argv[1] if len(sys.argv) > 1 else "doctor@example.com"
    password = sys.argv[2] if len(sys.argv) > 2 else "123456"
    try:
        register_user(email, password)
        print(f"Created demo user: {email} / {password}")
    except sqlite3.IntegrityError:
        print(f"User already exists: {email}")
    except Exception as e:
        print(f"Failed to create user: {e}")
        raise


if __name__ == "__main__":
    main()
