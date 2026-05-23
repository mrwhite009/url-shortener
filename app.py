from flask import Flask, request, redirect, jsonify
import shortuuid
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB = os.getenv("DB_PATH", "urls.db")
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS urls (
        code TEXT PRIMARY KEY,
        original TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        clicks INTEGER DEFAULT 0
    )""")
    conn.commit()

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL required"}), 400
    code = shortuuid.uuid()[:8]
    conn = get_db()
    conn.execute("INSERT INTO urls (code, original) VALUES (?, ?)", (code, url))
    conn.commit()
    return jsonify({"short_url": f"{BASE_URL}/{code}", "code": code}), 201

@app.route("/<code>")
def redirect_url(code):
    conn = get_db()
    row = conn.execute("SELECT original FROM urls WHERE code = ?", (code,)).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE code = ?", (code,))
    conn.commit()
    return redirect(row["original"], code=301)

@app.route("/stats/<code>")
def stats(code):
    conn = get_db()
    row = conn.execute("SELECT code, original, created_at, clicks FROM urls WHERE code = ?", (code,)).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)