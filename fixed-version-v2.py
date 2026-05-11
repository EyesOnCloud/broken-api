@app.route('/employee/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    auth_header = request.headers.get('Authorization', '')

    if not auth_header.startswith('Bearer '):
        return jsonify({"error": "Token required"}), 401

    token = auth_header.split(' ')[1]

    try:
        decoded = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

    # ── EXTRACT USER INFO FROM JWT ───────────────────────────
    requesting_username = decoded.get('username')
    requesting_user_role = decoded.get('role')

    # ── FIND EMPLOYEE RECORD LINKED TO THIS USER ─────────────
    conn_check = get_db()
    cursor_check = conn_check.cursor()

    cursor_check.execute("""
        SELECT employee_id
        FROM users
        WHERE username = ?
    """, (requesting_username,))

    user_record = cursor_check.fetchone()
    conn_check.close()

    if not user_record:
        return jsonify({"error": "User mapping not found"}), 404

    requesting_employee_id = user_record['employee_id']

    # ── AUTHORIZATION CHECK ──────────────────────────────────
    # Allow:
    #   - own employee record
    #   - admins
    if requesting_employee_id != emp_id and requesting_user_role != 'admin':
        return jsonify({
            "error": "Access denied. You are not authorized to view this record."
        }), 403

    # ── FETCH EMPLOYEE RECORD ────────────────────────────────
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM employees WHERE id = ?",
        (emp_id,)
    )

    employee = cursor.fetchone()
    conn.close()

    if employee:
        return jsonify(dict(employee))
    else:
        return jsonify({"error": "Employee not found"}), 404
