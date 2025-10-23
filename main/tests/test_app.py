import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home route returns status code 200."""
    response = client.get('/')
    assert response.status_code == 200


def test_health(client):
    """Test the health check endpoint returns OK."""
    response = client.get('/health')
    assert response.status_code == 200
    assert b"healthy" in response.data or b"OK" in response.data


def test_data_post(client):
    """Test POST to /data endpoint."""
    response = client.post('/data', 
                          json={"key": "value"},
                          content_type='application/json')
    assert response.status_code == 201


def test_data_get(client):
    """Test GET from /data endpoint."""
    response = client.get('/data')
    assert response.status_code == 200