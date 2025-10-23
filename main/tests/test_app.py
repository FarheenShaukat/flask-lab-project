import os
import sys
import json

# Ensure the main/ directory is on sys.path so `from app import app` works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Some environments install a werkzeug package without a __version__ attribute
# which Flask's test client expects. Provide a safe fallback so tests can run.
try:
    import werkzeug
    if not hasattr(werkzeug, "__version__"):
        werkzeug.__version__ = "0.0.0"
except Exception:
    # if werkzeug isn't importable it's okay; Flask import will produce a clearer error
    pass

from app import app


def test_home():
    response = app.test_client().get("/")
    assert response.status_code == 200


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert b"OK" in response.data


def test_data_post():
    payload = {"name": "tester", "value": 123}
    response = app.test_client().post(
        "/data", data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["processed"] is True
    assert data["received"]["name"] == "tester"
