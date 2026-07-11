"""
Fresh Food Coolmine - Issue & Vulnerability Tracker API
A REST API built with Flask for tracking software bugs and security
vulnerabilities. Data is stored persistently in a SQLite database.
"""

from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = "issues.db"


def init_db():
    """
    Creates the issues table if it doesn't already exist.
    Using 'IF NOT EXISTS' means this is safe to run every time the
    app starts, without wiping existing data.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT,
            severity TEXT,
            status TEXT,
            affected_system TEXT,
            reporter TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_db_connection():
    """
    Opens a new database connection for a single request.
    row_factory lets us access columns by name (e.g. row["title"])
    instead of by numeric index, which makes converting to JSON easier.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    """Simple health-check route to confirm the API is running."""
    return jsonify({"message": "Issue Tracker API is running"})


# ---------- READ ----------
@app.route("/issues", methods=["GET"])
def get_issues():
    """
    Returns all issues, with optional filtering via query parameters:
    /issues?status=Open
    /issues?severity=High
    /issues?category=Bug
    Filters can be combined, e.g. /issues?status=Open&severity=High
    """
    status = request.args.get("status")
    severity = request.args.get("severity")
    category = request.args.get("category")

    # "WHERE 1=1" is a harmless always-true condition that lets us
    # safely append "AND ..." clauses only for filters that were provided
    query = "SELECT * FROM issues WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if severity:
        query += " AND severity = ?"
        params.append(severity)
    if category:
        query += " AND category = ?"
        params.append(category)

    conn = get_db_connection()
    issues = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(issue) for issue in issues])


# ---------- CREATE ----------
@app.route("/issues", methods=["POST"])
def create_issue():
    """
    Creates a new issue. Requires a valid title, category, and severity.
    New issues always start with status "Open".
    """
    data = request.get_json()

    # Validation: reject the request early if required fields are missing
    # or invalid, before touching the database.
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    if not data.get("category") or data.get("category") not in ["Bug", "Vulnerability"]:
        return jsonify({"error": "Category must be 'Bug' or 'Vulnerability'"}), 400

    if not data.get("severity") or data.get("severity") not in ["Low", "Medium", "High", "Critical"]:
        return jsonify({"error": "Severity must be Low, Medium, High, or Critical"}), 400

    conn = get_db_connection()
    # Using "?" placeholders (parameterised queries) instead of building
    # the SQL string directly protects against SQL injection attacks.
    cursor = conn.execute(
        """INSERT INTO issues (title, description, category, severity, status, affected_system, reporter)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            data.get("title"),
            data.get("description"),
            data.get("category"),
            data.get("severity"),
            "Open",
            data.get("affected_system"),
            data.get("reporter"),
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": new_id, **data, "status": "Open"}), 201


# ---------- UPDATE ----------
@app.route("/issues/<int:issue_id>", methods=["PUT"])
def update_issue(issue_id):
    """
    Updates an existing issue by ID. Only fields included in the request
    body are changed; any field left out keeps its current value.
    Returns 404 if no issue with that ID exists.
    """
    data = request.get_json()
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()

    if existing is None:
        conn.close()
        return jsonify({"error": "Issue not found"}), 404

    conn.execute(
        """UPDATE issues SET title=?, description=?, category=?, severity=?, status=?, affected_system=?, reporter=?
           WHERE id=?""",
        (
            data.get("title", existing["title"]),
            data.get("description", existing["description"]),
            data.get("category", existing["category"]),
            data.get("severity", existing["severity"]),
            data.get("status", existing["status"]),
            data.get("affected_system", existing["affected_system"]),
            data.get("reporter", existing["reporter"]),
            issue_id,
        ),
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
    conn.close()

    return jsonify(dict(updated)), 200


# ---------- DELETE ----------
@app.route("/issues/<int:issue_id>", methods=["DELETE"])
def delete_issue(issue_id):
    """
    Deletes an issue by ID. Returns 404 if no issue with that ID exists,
    otherwise confirms the deletion.
    """
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()

    if existing is None:
        conn.close()
        return jsonify({"error": "Issue not found"}), 404

    conn.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Issue {issue_id} deleted"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)