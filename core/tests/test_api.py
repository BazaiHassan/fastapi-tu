from fastapi.testclient import TestClient
from core.main import app
from core.src.config import settings


client = TestClient(app)


def test_get_current_user_no_cookie_returns_401():
    response = client.get(f"{settings.API_VERSION}/user/current")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}