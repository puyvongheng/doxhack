from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'students.json'

# Load existing students
def load_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save students to JSON
def save_students(students):
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=2)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    
    # Extract only expected fields
    name = data.get("name")
    ip = data.get("latinName")  # coming as IP
    date = data.get("dateOfBirth")

    if not name or not ip:
        return jsonify({"error": "Missing name or IP"}), 400

    students = load_students()
    new_id = max([s.get("id", 0) for s in students], default=0) + 1

    student = {
        "id": new_id,
        "name": name,
        "ip": ip,
        "date": date
    }

    students.append(student)
    save_students(students)

    return jsonify({"message": "Data received", "id": new_id}), 201

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(load_students())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get PORT from environment or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
