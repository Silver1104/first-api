from sqlmodel import create_engine, Session, SQLModel, select
import pytest
from app import model
from app.main import app
from app.config import settings
from app.database import get_session
from fastapi.testclient import TestClient

from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# Create engine for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL)

@pytest.fixture()
def session():
    # Drop and recreate all tables
    print("Data base reset for testing")
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    
    # Create session
    with Session(engine) as db:
        yield db

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_session] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {
        "name": "hello123",
        "email": "hello123@gmail.com",
        "password": "12345678",
    }
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_user2(client):
    user_data = {
        "name": "raghav123",
        "email": "raghav@gmail.com",
        "password": "87654321",
    }
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token2(test_user2):
    return create_access_token(data={"user_id": test_user2["id"]})

@pytest.fixture
def authorized_client2(client, token2):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token2}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    post_data = [
        model.Post(title="First Post", content="Content of first post", owner_id=test_user["id"]),
        model.Post(title="Second Post", content="Content of second post", owner_id=test_user["id"]),
        model.Post(title="Third Post", content="Content of third post", owner_id=test_user["id"]),
    ]
    session.add_all(post_data)
    session.commit()
    all_posts = session.exec(select(model.Post)).all()
    return all_posts