import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'employees.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT,
    employee_id INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    salary INTEGER,
    email TEXT,
    position TEXT
)
''')

cursor.execute("DELETE FROM users")
cursor.execute("DELETE FROM employees")

employees = [
    ('alice', 'Management', 150000, 'alice@company.local', 'CTO'),
    ('bob', 'IT', 65000, 'bob@company.local', 'System Engineer'),
    ('charlie', 'HR', 70000, 'charlie@company.local', 'HR Manager'),
    ('david', 'Finance', 95000, 'david@company.local', 'Finance Lead')
]

cursor.executemany('''
INSERT INTO employees (name, department, salary, email, position)
VALUES (?, ?, ?, ?, ?)
''', employees)

users = [
    ('alice', 'password123', 'admin', 1),
    ('bob', 'bobpass', 'user', 2),
    ('charlie', 'charliepass', 'user', 3)
]

cursor.executemany('''
INSERT INTO users (username, password, role, employee_id)
VALUES (?, ?, ?, ?)
''', users)

conn.commit()
conn.close()

print("Database initialized successfully")
