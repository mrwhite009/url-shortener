# URL Shortener

Simple Flask-based URL shortener with SQLite storage.

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Service info |
| `POST` | `/shorten` | Create short URL |
| `GET` | `/:code` | Redirect to original |
| `GET` | `/stats/:code` | View click statistics |

## Quickstart

```bash
pip install -r requirements.txt
python app.py
```

```bash
curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"url":"https://example.com"}'
```