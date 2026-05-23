#!/bin/bash
set -e
pip install -r requirements.txt
export BASE_URL="https://short.example.com"
export DB_PATH="/var/lib/url-shortener/urls.db"
mkdir -p "$(dirname "$DB_PATH")"
gunicorn -w 4 -b 0.0.0.0:8000 app:app