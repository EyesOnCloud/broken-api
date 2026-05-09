from flask import Flask, request, jsonify
    conn = get_db_connection()
    cursor = conn.cursor()

    # BOLA VULNERABILITY
    query = f"SELECT * FROM employees WHERE id = {employee_id}"

    print(f"Executing query: {query}")

    cursor.execute(query)
    employee = cursor.fetchone()

    conn.close()

    if employee:
        return jsonify(dict(employee))

    return jsonify({'error': 'Employee not found'}), 404


@app.route('/employees/search', methods=['GET'])
def search_employees():

    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({'error': 'Missing token'}), 401

    token = auth_header.split(' ')[1]
    user = verify_token(token)

    if not user:
        return jsonify({'error': 'Invalid token'}), 401

    name = request.args.get('name', '')

    conn = get_db_connection()
    cursor = conn.cursor()

    # VULNERABLE SQL QUERY
    query = "SELECT * FROM employees WHERE name LIKE '%" + name + "%'

    print(f"Executing query: {query}")

    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in results])


@app.route('/admin/report', methods=['POST'])
def admin_report():

    # TODO: add auth check

    data = request.get_json()
    report_type = data.get('report_type')

    conn = get_db_connection()
    cursor = conn.cursor()

    if report_type == 'all_employees':
        cursor.execute("SELECT * FROM employees")
        results = cursor.fetchall()

    elif report_type == 'payroll':
        cursor.execute("SELECT name, salary FROM employees")
        results = cursor.fetchall()

    elif report_type == 'credentials':
        cursor.execute("SELECT username, password FROM users")
        results = cursor.fetchall()

    else:
        return jsonify({'error': 'Unknown report type'}), 400

    conn.close()

    return jsonify([dict(row) for row in results])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
