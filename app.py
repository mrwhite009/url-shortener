from flask import Flask, request, redirect, jsonify
import shortuuid
import sqlite3
import os
import re
from datetime import datetime, timezone

app = Flask(__name__)
DB = os.getenv("DB_PATH", "urls.db")
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
URL_PATTERN = re.compile(r'^https?://.+\..+')

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
        clicks INTEGER DEFAULT 0,
        last_clicked TIMESTAMP
    )""")
    conn.commit()

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.route("/")
def index():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM urls").fetchone()[0]
    return jsonify({"service": "url-shortener", "urls_shortened": count})

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL required"}), 400
    if not URL_PATTERN.match(url):
        return jsonify({"error": "Invalid URL format"}), 400
    code = shortuuid.uuid()[:8]
    conn = get_db()
    conn.execute("INSERT INTO urls (code, original) VALUES (?, ?)", (code, url))
    conn.commit()
    return jsonify({"short_url": f"{BASE_URL}/{code}", "code": code}), 201