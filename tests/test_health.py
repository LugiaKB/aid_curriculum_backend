"""
Test health check endpoint
"""


def test_health_check(client):
    """
    Test health check endpoint returns 200
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "version" in response.json()
