import pytest
import jwt
from enum import Enum
from api import create_app
from lib.db_connect import RDSManager, MySQLManager

RDSManager = RDSManager()
MySQLManager = MySQLManager()


class Mock(Enum):
    """Mock data for testing"""
    EMAIL = "test@test.com"
    NAME = "김테스트"
    PASSWORD = "testest111!!"
    TOKEN_KEY = "fADAADSFVADF!@1231455AAA"


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="module", autouse=True)
def cleanup(request):
    """Clean Mock data on db after testing."""
    def remove_test_data():
        RDSManager.delete_user_dek(Mock.EMAIL.value)
        MySQLManager.delete_user_auth(Mock.EMAIL.value)

    request.addfinalizer(remove_test_data)


@pytest.mark.order(1)
def test_user_create(client):
    resp = client.post("/user/create", json={
        "email": Mock.EMAIL.value,
        "name": Mock.NAME.value,
        "password": Mock.PASSWORD.value
    })
    assert resp.status_code == 200
    assert resp.json["status"] == "OK"
    assert resp.json["result"] == Mock.NAME.value


@pytest.mark.order(2)
def test_user_create_error(client):
    resp = client.post("/user/create", json={
        "email": Mock.EMAIL.value,
        "password": Mock.PASSWORD.value
    })
    assert resp.status_code == 400
    assert resp.json["status"] == "Fail"
    assert resp.json["message"] == "['name'] was not entered. Please check form."

    resp = client.post("/user/create", json={
        "email": Mock.EMAIL.value,
        "name": Mock.NAME.value,
        "password": Mock.PASSWORD.value
    })
    assert resp.status_code == 400
    assert resp.json["status"] == "Fail"
    assert resp.json["message"] == "This email already exists. Please log in with your existing account."


@pytest.mark.order(3)
def test_user_login(client):
    resp = client.post("/auth/login", json={
        "email": Mock.EMAIL.value,
        "password": Mock.PASSWORD.value
    })
    assert resp.status_code == 200
    assert resp.json["status"] == "OK"
    assert resp.json["result"]["email"] == Mock.EMAIL.value

    token = resp.json["result"]["token"]
    decode_token = jwt.decode(token, Mock.TOKEN_KEY.value, algorithms="HS256")
    assert decode_token["email"] == Mock.EMAIL.value


@pytest.mark.order(4)
def test_user_log_in_success(client):
    resp = client.post("/auth/login", json={
        "email": Mock.EMAIL.value,
        "password": Mock.PASSWORD.value
    })
    token = resp.json["result"]["token"]

    resp = client.get("/user", headers=[("Authorization", token), ("email", Mock.EMAIL.value)], 
                      follow_redirects=True)
    assert resp.status_code == 200
    assert resp.json["status"] == "OK"
    assert resp.json["result"]["email"] == Mock.EMAIL.value
    assert resp.json["result"]["name"] == Mock.NAME.value
    # password not decrypt
    assert resp.json["result"]["password"] != Mock.PASSWORD.value
