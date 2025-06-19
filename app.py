from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('users.db')
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, hwid) VALUES (?, ?, ?)", 
                (data['username'], data['password'], data['hwid']))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "User registered"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=? AND hwid=?", 
                (data['username'], data['password'], data['hwid']))
    user = cur.fetchone()
    conn.close()
    if user:
        return jsonify({"success": True, "message": "Login success"})
    return jsonify({"success": False, "message": "Invalid credentials"})

if __name__ == '__main__':
    app.run()

