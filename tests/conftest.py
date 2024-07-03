import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.db import Base
from app.database.models import Roles

from app.core.config import settings


@pytest.fixture(scope="session")
def engine():
    return create_engine(settings.TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def create_tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine, create_tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def add_roles(session):
    user_role = Roles(role='user')
    admin_role = Roles(role='admin')
    session.add(user_role)
    session.add(admin_role)
    session.commit()
    return user_role, admin_role


@pytest.fixture
def add_roles(session):
    user_role = Roles(role='user')
    admin_role = Roles(role='admin')
    session.add(user_role)
    session.add(admin_role)
    session.commit()
    
    # Проверка
    roles = session.query(Roles).all()
    print("Roles in DB:", [role.role for role in roles])
    
    return user_role, admin_role
