from http.client import responses
from fastapi.testclient import TestClient


def test_create_tweet(client: TestClient):
    response = client.post("/api/tweets", json = {"tweet_data": "Test tweet from alice", "tweet_media_ids": None},
        headers={"api-key": "alice"},
    )
    assert response.status_code == 200
    data = response.json()
    print('DDD', response.text)
    assert data["result"] is True
    assert "tweet_id" in data


def test_get_tweets(client: TestClient):
    response = client.get( "/api/tweets",
        headers={"api-key": "alice"},)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["result"] is True
    tweets = data["tweets"]
    contents = [t["content"] for t in tweets]
    assert "Here Bob" in contents
    assert "Hello world" in contents


def test_delete_own_tweet(client: TestClient):
    create_resp = client.post( "/api/tweets",
        json={"tweet_data": "Tweet to delete", "tweet_media_ids": None},
        headers={"api-key": "alice"},)
    tweet_id = create_resp.json()["tweet_id"]
    del_resp = client.delete(f"/api/tweets/{tweet_id}",  headers={"api-key": "alice"},)
    assert del_resp.status_code == 200
    data = del_resp.json()
    assert data["result"] is True


def test_tweet_like(client: TestClient):
    create_resp = client.post("/api/tweets/2/likes", headers={"api-key": "alice"}, )
    assert create_resp.status_code == 200
    data = create_resp.json()
    print(data)
    assert data["result"] is True


def test_tweet_unlike(client: TestClient):
    del_resp = client.delete("/api/tweets/2/likes", headers={"api-key": "alice"}, )
    assert del_resp.status_code == 200
    data = del_resp.json()
    print(data)
    assert data["result"] is True
