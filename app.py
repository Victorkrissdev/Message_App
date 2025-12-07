from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB_NAME = "messages.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            category TEXT,
            urgency TEXT,
            message TEXT NOT NULL,
            permission TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    req_type = request.form.get("type")
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    category = request.form.get("category")
    urgency = request.form.get("urgency")
    message = request.form.get("message")
    permission = request.form.get("permission")

    # ✅ Limit message length to 300 characters (backend protection)
    if message and len(message) > 100:
        message = message[:100]  # Trim extra characters safely

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO messages (type, name, email, phone, category, urgency, message, permission)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (req_type, name, email, phone, category, urgency, message, permission))
    
    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/admin", methods=["GET"])
def admin():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT id, type, name, email, phone, category, urgency, message, permission, created_at
        FROM messages ORDER BY created_at DESC
    """)
    messages = c.fetchall()
    conn.close()

    return render_template("admin.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
