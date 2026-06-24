import pytest
from fastapi.testclient import TestClient
from core.database import engine, Base, SessionLocal
from models.role_model import Role


@pytest.fixture
def client():
    # Import `app` here so the test DB fixture (`create_test_db`) runs first
    from main import app
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_token(client):
    db = SessionLocal()
    try:
        if not db.query(Role).filter(Role.name == "EMPLOYEE").first():
            db.add(Role(name="EMPLOYEE"))
            db.commit()
    finally:
        db.close()

    client.post("/auth/register", json={"username": "testuser", "email": "test@test.com", "password": "Password@123", "role_name": "EMPLOYEE"})
    resp = client.post("/auth/login", data={"username":"test@test.com", "password":"Password@123"})
    if resp.status_code == 200:
        return resp.json().get("access_token")
    return None


@pytest.fixture(autouse=True, scope="session")
def create_test_db():
    # Import all model modules so their tables are registered in metadata
    import importlib, os
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    try:
        for fname in os.listdir(models_dir):
            if fname.endswith(".py") and fname != "__init__.py":
                mod_name = fname[:-3]
                importlib.import_module(f"models.{mod_name}")
    except Exception:
        pass

    # Ensure the in-memory database has all tables for tests
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)