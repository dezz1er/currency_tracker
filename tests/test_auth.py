from httpx import AsyncClient


from tests.errors import OPERATION_FAIL, DATA_CONVERT_FAIL


global access_token, refresh_token
access_token: str | None = None
refresh_token: str | None = None


async def test_registration(ac: AsyncClient):
    response = await ac.post("/auth/signin", json={
        "username": "user_test",
        "password": "password_test"
    }
    )
    assert response.status_code == 200, OPERATION_FAIL
    assert response.json().get("username") == "user_test", DATA_CONVERT_FAIL
