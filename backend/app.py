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


if __name__ == "__main__":
    app.run(debug=True)