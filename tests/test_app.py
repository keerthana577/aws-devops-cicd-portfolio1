import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
from main import app

def test_home_endpoint():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["application"] == "devops-demo-app"

def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_metrics_endpoint():
    client = app.test_client()
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.data
