import sqlite3
from typing import List, Dict, Optional

DB_PATH = 'database/data.db'

PATIENTS_SCHEMA = '''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    symptoms TEXT,
    diagnosis TEXT,
    exam_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email) REFERENCES users(email)
);
'''

def _get_conn():
    return sqlite3.connect(DB_PATH)


def init_table() -> None:
    conn = _get_conn()
    try:
        c = conn.cursor()
        c.execute(PATIENTS_SCHEMA)
        conn.commit()
    finally:
        conn.close()


def save_patient(email: Optional[str], name: str, age: int, gender: str,
                 symptoms: str, diagnosis: str, exam_date: Optional[str]) -> int:
    """Insert one patient record and return the new row id."""
    init_table()
    conn = _get_conn()
    try:
        c = conn.cursor()
        c.execute(
            'INSERT INTO patients (email, name, age, gender, symptoms, diagnosis, exam_date) VALUES (?,?,?,?,?,?,?)',
            (email, name, age, gender, symptoms, diagnosis, exam_date or '')
        )
        conn.commit()
        return int(c.lastrowid)
    finally:
        conn.close()


def list_patients(email: Optional[str] = None, limit: int = 100) -> List[Dict]:
    init_table()
    conn = _get_conn()
    try:
        c = conn.cursor()
        if email:
            c.execute('SELECT id, email, name, age, gender, symptoms, diagnosis, exam_date, created_at FROM patients WHERE email=? ORDER BY created_at DESC LIMIT ?', (email, limit))
        else:
            c.execute('SELECT id, email, name, age, gender, symptoms, diagnosis, exam_date, created_at FROM patients ORDER BY created_at DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        cols = [d[0] for d in c.description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()
