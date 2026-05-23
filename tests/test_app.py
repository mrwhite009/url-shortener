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
    assert "url-shortener" in r.get_json()["service"]

def test_shorten_no_url(client):
    r = client.post("/shorten", json={})
    assert r.status_code == 400

def test_shorten_invalid(client):
    r = client.post("/shorten", json={"url": "not-a-url"})
    assert r.status_code == 400