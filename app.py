from flask import Flask, request, redirect, jsonify
import shortuuid
import sqlite3
import os

app = Flask(__name__)
DB = os.getenv("DB_PATH", "urls.db")

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS urls (
        code TEXT PRIMARY KEY,
        original TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        clicks INTEGER DEFAULT 0
    )""")
    conn.commit()
    return conn

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL required"}), 400
    code = shortuuid.uuid()[:8]
    conn = init_db()
    conn.execute("INSERT INTO urls (code, original) VALUES (?, ?)", (code, url))
    conn.commit()
    return jsonify({"short_url": f"http://localhost:5000/{code}", "code": code})

@app.route("/<code>")
def redirect_url(code):
    conn = sqlite3.connect(DB)
    row = conn.execute("SELECT original FROM urls WHERE code = ?", (code,)).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE code = ?", (code,))
    conn.commit()
    return redirect(row[0], code=301)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)