import sqlite3
import os

DB_PATH = '/app/data/employees.db'

def init_db():
    os.makedirs('/app/data', exist_ok=True)

    # OPTIONAL: remove old DB for clean rebuild during lab/testing
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ── USERS TABLE ───────────────────────────────────────────
    # employee_id explicitly maps login users to employee records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'employee',
            employee_id INTEGER,
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    ''')

    # ── EMPLOYEES TABLE ───────────────────────────────────────
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

    # ── SEED EMPLOYEE RECORDS ────────────────────────────────
    employees = [
        (1, 'Alice Johnson',   'IT Security',  120000, 'alice@company.com',   '+1-555-0101', 'NID-100001', 'admin'),
        (2, 'Bob Martinez',    'Operations',    65000, 'bob@company.com',     '+1-555-0102', 'NID-100002', 'employee'),
        (3, 'Charlie Singh',   'Finance',       85000, 'charlie@company.com', '+1-555-0103', 'NID-100003', 'employee'),
        (4, 'Diana Fernandez', 'HR',            75000, 'diana@company.com',   '+1-555-0104', 'NID-100004', 'employee'),
        (5, 'Eric Wang',       'Engineering',   95000, 'eric@company.com',    '+1-555-0105', 'NID-100005', 'employee'),
    ]

    cursor.executemany(
        '''
        INSERT INTO employees
        (id, name, department, salary, email, phone, national_id, role)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        employees
    )

    # ── SEED USERS ───────────────────────────────────────────
    # employee_id maps user accounts to employee records
    users = [
        ('admin',   'adminpass123', 'admin',    None),
        ('alice',   'password123',  'admin',    1),
        ('bob',     'bobpass',      'employee', 2),
        ('charlie', 'charliepass',  'employee', 3),
    ]

    cursor.executemany(
        '''
        INSERT INTO users
        (username, password, role, employee_id)
        VALUES (?, ?, ?, ?)
        ''',
        users
    )

    conn.commit()
    conn.close()

    print("[INIT] Database initialized with corrected user ↔ employee mapping.")

if __name__ == '__main__':
    init_db()
