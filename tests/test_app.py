import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_index(client):
    r = client.get("/")
    assert r.status_code == 200

def test_shorten_no_url(client):
    r = client.post("/shorten", json={})
    assert r.status_code == 400

def test_shorten_invalid(client):
    r = client.post("/shorten", json={"url": "not-a-url"})
    assert r.status_code == 400

def test_shorten_valid(client):
    r = client.post("/shorten", json={"url": "https://example.com/page"})
    assert r.status_code == 201
    data = r.get_json()
    assert "short_url" in data
    assert "code" in data

def test_redirect_404(client):
    r = client.get("/nonexistent")
    assert r.status_code == 404