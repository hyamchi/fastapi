
import pytest
from jose import jwt
from app import schemas
# from .database import client, session
from app.config import settings

# def test_read_main(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello World"}

def test_create_user(client):
    res = client.post("/users/", json={"email": "john@gmail.com", "password": "password"})
    
    new_user = schemas.UserOut(**res.json())
    print(res.json())
    assert new_user.email == "john@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password', 403), ('john@gmail.com', 'wrong password', 403), (None, 'password', 422)])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    # assert res.json().get('detail') == "Invalid Credentials"
    assert res.status_code == status_code