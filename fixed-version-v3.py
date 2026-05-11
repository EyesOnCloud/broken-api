def verify_admin_token(request):
    """
    Helper function that extracts and validates the JWT token from the
    Authorization header, then checks that the user has the admin role.
    Returns the decoded token payload if valid admin, raises Exception otherwise.
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise Exception("No token provided")

    token = auth_header.split(' ')[1]

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except Exception:
        raise Exception("Invalid token")

    if decoded.get('role') != 'admin':
        raise Exception("Admin role required")

    return decoded


@app.route('/admin/report', methods=['POST'])
def admin_report():
    # FIXED: authentication and role check runs before any logic
    try:
        verify_admin_token(request)
    except Exception as e:
        return jsonify({"error": str(e)}), 403

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
