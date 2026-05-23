# URL Shortener

Simple URL shortener with SQLite backend and REST API.

## Endpoints

- `POST /shorten` — create short URL
- `GET /:code` — redirect to original URL
- `GET /stats/:code` — view click stats