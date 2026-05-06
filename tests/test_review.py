import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.auth.jwt_handler import create_access_token

@pytest.fixture
def auth_headers():
    token = create_access_token({"sub": "testuser"})
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_review_endpoint(auth_headers, monkeypatch):
    async def mock_review(code, language, context):
        from app.models.schemas import CodeReviewResponse
        return CodeReviewResponse(
            summary="Test review",
            issues=[],
            score=90,
            improved_code=None
        )
    monkeypatch.setattr("app.routers.review.review_code", mock_review)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/review",
            json={"code": "def foo(): pass", "language": "python"},
            headers=auth_headers
        )
    assert response.status_code == 200
    assert response.json()["score"] == 90
