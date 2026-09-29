from fastapi.testclient import TestClient


def test_get_me_profile(client: TestClient):
    response = client.get(
        "/api/users/me",
        headers={"api-key": "alice"},
    )
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
    assert response.status_code == 200
    data = response.json()
    print(data['user']['following'][1])
    assert data["result"] is True
    assert data["user"]["name"] == "alice"


def test_follow_user(client: TestClient):
    response = client.post(
        "/api/users/2/follow",
        headers={"api-key": "alice"},
    )
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["result"] is True


def test_unfollow(client: TestClient):
    follow_resp = client.post(
        "/api/users/2/follow",
        headers={"api-key": "alice"},)
    unfollow_resp = client.delete("/api/users/2/follow",
        headers={"api-key": "alice"},)
    assert unfollow_resp.status_code == 200
    data = unfollow_resp.json()
    print(data)
    assert data["result"] is True


def test_get_prof(client: TestClient):
    response = client.get("/api/users/2")
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True

