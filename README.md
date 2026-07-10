# Fresh Food Coolmine — Issue & Vulnerability Tracker

A REST API for tracking software bugs and security vulnerabilities for **Fresh Food Coolmine (Fresh Halal Food LTD)**, built with Flask and SQLite as part of the B9IS121 Network Systems and Administration assignment at Dublin Business School.

## Overview

This system allows issues (bugs or security vulnerabilities) to be created, viewed, updated, deleted, and filtered via a REST API. It was developed incrementally using Git/GitHub, and tested using Postman.

## Tech Stack

- **Backend:** Python 3 / Flask
- **Database:** SQLite
- **Testing:** Postman
- **Version control:** Git / GitHub

## Data Requirements

Each issue record contains:

| Field | Type | Description |
|---|---|---|
| id | Integer (auto) | Unique identifier, assigned by the database |
| title | Text (required) | Short summary of the issue |
| description | Text | Full detail of the problem |
| category | Text | `Bug` or `Vulnerability` |
| severity | Text | `Low`, `Medium`, `High`, or `Critical` |
| status | Text | `Open`, `In Progress`, `Resolved`, `Closed` (defaults to `Open`) |
| affected_system | Text | The system/component affected |
| reporter | Text | Person who reported the issue |

## Setup Instructions

1. Clone the repository:
git clone https://github.com/huzaifamalik786/fresh-food-Coolmine-issue-tracker.git
2. Install Flask:
py -m pip install flask
3. Run the server:
py backend/app.py
4. The API will be available at `http://127.0.0.1:5000`. A SQLite database file (`issues.db`) is created automatically on first run.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/issues` | Get all issues |
| GET | `/issues?status=Open` | Filter issues by status |
| GET | `/issues?severity=High` | Filter issues by severity |
| GET | `/issues?category=Bug` | Filter issues by category |
| POST | `/issues` | Create a new issue |
| PUT | `/issues/<id>` | Update an existing issue |
| DELETE | `/issues/<id>` | Delete an issue |

### Example: Create an issue (POST /issues)

Request body:
```json
{
 "title": "Login page not loading",
 "description": "Blank screen on Chrome",
 "category": "Bug",
 "severity": "High",
 "affected_system": "Customer Portal",
 "reporter": "Huzaifa Malik"
}

Validation rules: title is required; category must be Bug or Vulnerability; severity must be Low, Medium, High, or Critical. Invalid requests return HTTP 400 with an error message.
Testing
All endpoints were manually tested using Postman, covering both successful requests (correct data, valid IDs) and failure cases (missing fields, invalid values, non-existent IDs), confirming correct HTTP status codes (200, 201, 400, 404) throughout.
Attribution Summary
Every commit in this repository’s history is individually attributed. The pattern used is:
<description of change> - <source>
Where self means the code was typed independently, and self, AI-assisted means the code was generated with guidance from Claude and then reviewed and applied by the author.

The following commits make up this repository's development history.
 Commit 1 added the Flask app skeleton with a test route, attributed to self, AI-assisted. 
 Commit 2 added the GET /issues endpoint with in-memory storage, attributed to self, AI-assisted. Commit 3 added the POST /issues endpoint for creating issues, attributed to self, AI-assisted.
 Commit 4 added the PUT and DELETE endpoints to complete CRUD, attributed to self, AI-assisted.
 Commit 5 migrated the system from in-memory storage to a SQLite database for persistence, attributed to self, AI-assisted.
 Commit 6 added a .gitignore file to exclude the database and cache files, attributed to self.
 Commit 7 added input validation for title, category, and severity on the POST endpoint, attributed to self, AI-assisted.
 Commit 8 added filtering by status, severity, and category to the GET /issues endpoint, attributed to self, AI-assisted .

No third-party code libraries beyond Flask and Python's built-in sqlite3 module were used in this project. Flask itself is an open-source framework released under the BSD-3-Clause licence and is used here as a standard dependency, not copied or adapted into the codebase.
