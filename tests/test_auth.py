from core.database import SessionLocal
from models.role_model import Role


def ensure_role(role_name: str):
    db = SessionLocal()
    try:
        if not db.query(Role).filter(Role.name == role_name).first():
            db.add(Role(name=role_name))
            db.commit()
    finally:
        db.close()


def test_register(client):
    ensure_role("EMPLOYEE")
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test@test.com", "password": "Password@123", "role_name": "EMPLOYEE"}
    )
    assert response.status_code in [200, 201]


def test_login(client):
    ensure_role("EMPLOYEE")
    client.post(
        "/auth/register",
        json={"username": "testuser", "email": "test@test.com", "password": "Password@123", "role_name": "EMPLOYEE"}
    )
    response = client.post("/auth/login", data={"username":"test@test.com", "password":"Password@123"})
    assert response.status_code == 200