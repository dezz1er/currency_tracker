from app.database.models import Users


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
