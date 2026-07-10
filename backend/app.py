from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = "issues.db"

# Create the issues table if it doesn't already exist
def init_db():
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
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn

@app.route("/")
def home():
    return jsonify({"message": "Issue Tracker API is running"})

# GET all issues
@app.route("/issues", methods=["GET"])
def get_issues():
    conn = get_db_connection()
    issues = conn.execute("SELECT * FROM issues").fetchall()
    conn.close()
    return jsonify([dict(issue) for issue in issues])


@app.route("/issues", methods=["POST"])
def create_issue():
    data = request.get_json()

    # Validation: required fields
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    if not data.get("category") or data.get("category") not in ["Bug", "Vulnerability"]:
        return jsonify({"error": "Category must be 'Bug' or 'Vulnerability'"}), 400

    if not data.get("severity") or data.get("severity") not in ["Low", "Medium", "High", "Critical"]:
        return jsonify({"error": "Severity must be Low, Medium, High, or Critical"}), 400

    conn = get_db_connection()
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


# UPDATE an existing issue
@app.route("/issues/<int:issue_id>", methods=["PUT"])
def update_issue(issue_id):
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

# DELETE an issue
@app.route("/issues/<int:issue_id>", methods=["DELETE"])
def delete_issue(issue_id):
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