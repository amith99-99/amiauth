from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db():
    return sqlite3.connect("users.db")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    hwid = data.get("hwid")
    expiry_days = int(data.get("expiry_days", 30))

    expiry_date = (datetime.now() + timedelta(days=expiry_days)).strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, hwid, expiry) VALUES (?, ?, ?, ?)",
                   (username, password, hwid, expiry_date))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "User registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    hwid = data.get("hwid")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND hwid=?", (username, password, hwid))
    user = cursor.fetchone()
    conn.close()

    if user:
        expiry = datetime.strptime(user[4], "%Y-%m-%d %H:%M:%S")
        if datetime.now() < expiry:
            return jsonify({"success": True, "message": "Login successful", "expires_on": user[4]})
        else:
            return jsonify({"success": False, "message": "License expired"})
    return jsonify({"success": False, "message": "Invalid credentials or HWID"})

@app.route("/genkey", methods=["POST"])
def genkey():
    import random, string
    length = int(request.json.get("length", 16))
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return jsonify({"success": True, "key": key})

if __name__ == "__main__":
    app.run(debug=True)
