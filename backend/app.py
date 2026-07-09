from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary in-memory storage for issues (will move to a database later)
issues = []
next_id = 1

@app.route("/")
def home():
    return jsonify({"message": "Issue Tracker API is running"})

# GET all issues
@app.route("/issues", methods=["GET"])
def get_issues():
    return jsonify(issues)

# CREATE a new issue
@app.route("/issues", methods=["POST"])
def create_issue():
    global next_id
    data = request.get_json()

    new_issue = {
        "id": next_id,
        "title": data.get("title"),
        "description": data.get("description"),
        "category": data.get("category"),        # "Bug" or "Vulnerability"
        "severity": data.get("severity"),         # Low/Medium/High/Critical
        "status": "Open",
        "affected_system": data.get("affected_system"),
        "reporter": data.get("reporter")
    }

    issues.append(new_issue)
    next_id += 1

    return jsonify(new_issue), 201


# UPDATE an existing issue
@app.route("/issues/<int:issue_id>", methods=["PUT"])
def update_issue(issue_id):
    data = request.get_json()

    for issue in issues:
        if issue["id"] == issue_id:
            issue["title"] = data.get("title", issue["title"])
            issue["description"] = data.get("description", issue["description"])
            issue["category"] = data.get("category", issue["category"])
            issue["severity"] = data.get("severity", issue["severity"])
            issue["status"] = data.get("status", issue["status"])
            issue["affected_system"] = data.get("affected_system", issue["affected_system"])
            issue["reporter"] = data.get("reporter", issue["reporter"])
            return jsonify(issue), 200

    return jsonify({"error": "Issue not found"}), 404

# DELETE an issue
@app.route("/issues/<int:issue_id>", methods=["DELETE"])
def delete_issue(issue_id):
    for issue in issues:
        if issue["id"] == issue_id:
            issues.remove(issue)
            return jsonify({"message": f"Issue {issue_id} deleted"}), 200

    return jsonify({"error": "Issue not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)