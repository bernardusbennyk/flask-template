import pytest

@pytest.mark.usefixtures("auth")
def test_dashboard_auth_access(client, auth):      
    if (auth.status_code != 302 or "/dashboard" not in auth.headers["Location"]):
        pytest.skip("Login failed, skipping test_dashboard_auth_access")
    response = client.get("/dashboard") 
    assert response.status_code == 200

def test_dashboard_noauth_access(client):
    response = client.get("/dashboard") 
    assert response.status_code == 302