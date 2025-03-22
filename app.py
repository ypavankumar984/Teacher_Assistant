from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load users from JSON file
if os.path.exists("users.json"):
    with open("users.json", "r") as file:
        users = json.load(file)
else:
    users = {}

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email in users:
        return jsonify({"message": "User already exists"}), 400

    users[email] = password

    with open("users.json", "w") as file:
        json.dump(users, file)

    return jsonify({"message": "User registered successfully"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email in users and users[email] == password:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@app.route('/submit', methods=['POST'])
def submit_text():
    data = request.get_json()
    text = data.get("text")

    # Write the received text to p1.py
    with open("p1.py", "w") as file:
        file.write(f"data = '{text}'\n")
    
    return jsonify({"message": "Text saved successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
