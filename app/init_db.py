import sqlite3
import os

DB_PATH = "employees.db"

# Remove old DB if exists
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# =========================
# USERS TABLE
# =========================

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT,
    employee_id INTEGER
)
""")

# =========================
# EMPLOYEES TABLE
# =========================

cursor.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT,
    salary INTEGER,
    email TEXT,
    position TEXT
)
""")

# =========================
# INSERT EMPLOYEES
# =========================

employees = [
    ("Alice Johnson", "Management", 150000, "alice@company.local", "CTO"),
    ("Bob Smith", "IT", 70000, "bob@company.local", "System Administrator"),
    ("Charlie Brown", "HR", 65000, "charlie@company.local", "HR Specialist"),
    ("David Wilson", "Finance", 90000, "david@company.local", "Finance Manager")
]

cursor.executemany("""
INSERT INTO employees (name, department, salary, email, position)
VALUES (?, ?, ?, ?, ?)
""", employees)

# =========================
# INSERT USERS
# =========================

users = [
    ("alice", "password123", "admin", 1),
    ("bob", "bobpass", "user", 2),
    ("charlie", "charliepass", "user", 3)
]

cursor.executemany("""
INSERT INTO users (username, password, role, employee_id)
VALUES (?, ?, ?, ?)
""", users)

conn.commit()
conn.close()

print("Database initialized successfully")
