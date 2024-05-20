import pytest
from flask_template import app

USER_LOGIN  = {
    "username"  : "benny",
    "password"  : "asdjklal"
}

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth(client):
    return client.post("/login", data=USER_LOGIN)
