@app.route('/employee/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({"error": "Token required"}), 401

    token = auth_header.split(' ')[1]
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

    # FIXED: extract the requesting user's identity from the token
    requesting_user_id = decoded.get('user_id')
    requesting_user_role = decoded.get('role')

    # FIXED: only allow access if the user is requesting their own record
    # OR if the user has the admin role
    if requesting_user_id != emp_id and requesting_user_role != 'admin':
        return jsonify({"error": "Access denied. You are not authorized to view this record."}), 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
    employee = cursor.fetchone()
    conn.close()

    if employee:
        return jsonify(dict(employee))
    else:
        return jsonify({"error": "Employee not found"}), 404
