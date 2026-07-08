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

if __name__ == "__main__":
    app.run(debug=True)