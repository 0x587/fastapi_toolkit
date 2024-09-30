from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from fastapi.testclient import TestClient
from app import app
from app.db import get_db_sync

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQLModel.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db_sync] = override_get_db
client = TestClient(app)


def test_get_one_404():
    response = client.post("/user/get_one", params={
        'user_ident': 1
    })
    assert response.status_code == 404