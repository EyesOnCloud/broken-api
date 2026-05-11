from flask import Flask, request, jsonify
import sqlite3
import os
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey123'

DB_PATH = '/app/data/employees.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── HEALTH CHECK ──────────────────────────────────────────────
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "running", "message": "Employee Records API is up"})


# ── LOGIN ─────────────────────────────────────────────────────
# VULNERABILITY 1: SQL Injection — username and password are
# concatenated directly into the SQL query string.
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    conn = get_db()
    cursor = conn.cursor()

    # VULNERABLE: direct string concatenation — never do this
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    print(f"[DEBUG] Executing query: {query}")   # debug leak — shows raw SQL in logs

    try:
        cursor.execute(query)
        user = cursor.fetchone()
    except Exception as e:
        return jsonify({"error": str(e), "query": query}), 500   # leaks full query on error
    finally:
        conn.close()

    if user:
        token = jwt.encode({
            'user_id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"token": token, "role": user['role'], "message": "Login successful"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# ── EMPLOYEE DETAIL ───────────────────────────────────────────
# VULNERABILITY 2: Broken Object Level Authorization (BOLA) —
# any authenticated user can fetch any employee record by ID.
# There is no check that the requesting user owns that record.
@app.route('/employee/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({"error": "Token required"}), 401

    token = auth_header.split(' ')[1]
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

    # VULNERABLE: no check — any valid token can request any ID
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
    employee = cursor.fetchone()
    conn.close()

    if employee:
        return jsonify(dict(employee))
    else:
        return jsonify({"error": "Employee not found"}), 404


# ── ADMIN REPORT ──────────────────────────────────────────────
# VULNERABILITY 3: Missing Authentication — the TODO was never
# implemented. Any request (even with no token) reaches the logic.
@app.route('/admin/report', methods=['POST'])
def admin_report():
    # TODO: verify admin role   <-- intentionally left unimplemented
    data = request.get_json() or {}
    report_type = data.get('report_type', 'summary')

    conn = get_db()
    cursor = conn.cursor()

    if report_type == 'all_employees':
        cursor.execute("SELECT * FROM employees")
    elif report_type == 'payroll':
        cursor.execute("SELECT name, department, salary FROM employees")
    elif report_type == 'credentials':
        cursor.execute("SELECT username, password, role FROM users")
    else:
        cursor.execute("SELECT COUNT(*) as total FROM employees")

    results = cursor.fetchall()
    conn.close()

    return jsonify({

        "report_type": report_type,
        "generated_at": datetime.datetime.utcnow().isoformat(),
        "data": [dict(r) for r in results]
    })


# ── START ─────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)   # MISCONFIGURATION: debug=True
