from app.database.models import Users
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user(session, add_roles):
    user_role, _ = add_roles
    user = Users(
        username='John',
        password='1243',
        role=user_role.role
    )
    session.add(user)
    session.commit()
    retrieved_user = session.query(Users).filter_by(username="John").first()
    assert retrieved_user is not None
    assert retrieved_user.username == "John"
    assert retrieved_user.role == user_role.role


def test_signin(test_user):
    response = client.post("/auth/signin", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert data["username"] == test_user["username"]
