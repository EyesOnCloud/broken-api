import sqlite3
import os

DB_PATH = '/app/data/employees.db'

def init_db():
    os.makedirs('/app/data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users table — stores login credentials
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'employee'
        )
    ''')

    # Employees table — stores HR records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            national_id TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'employee'
        )
    ''')

    # Seed users — passwords stored in plain text (another misconfiguration, intentional)
    users = [
        ('admin',   'adminpass123', 'admin'),
        ('alice',   'password123',  'admin'),
        ('bob',     'bobpass',      'employee'),
        ('charlie', 'charliepass',  'employee'),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
        users
    )

    # Seed employee records with realistic sensitive data
    employees = [
        (1, 'Alice Johnson',   'IT Security',  120000, 'alice@company.com',   '+1-555-0101', 'NID-100001', 'admin'),
        (2, 'Bob Martinez',    'Operations',    65000, 'bob@company.com',     '+1-555-0102', 'NID-100002', 'employee'),
        (3, 'Charlie Singh',   'Finance',       85000, 'charlie@company.com', '+1-555-0103', 'NID-100003', 'employee'),
        (4, 'Diana Fernandez', 'HR',            75000, 'diana@company.com',   '+1-555-0104', 'NID-100004', 'employee'),
        (5, 'Eric Wang',       'Engineering',   95000, 'eric@company.com',    '+1-555-0105', 'NID-100005', 'employee'),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO employees (id, name, department, salary, email, phone, national_id, role) VALUES (?,?,?,?,?,?,?,?)",
        employees
    )

    conn.commit()
    conn.close()
    print("[INIT] Database initialized with test data.")

if __name__ == '__main__':
    init_db()
