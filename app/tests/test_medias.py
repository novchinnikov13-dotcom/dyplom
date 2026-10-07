import io

from fastapi.testclient import TestClient


def test_upload_media(client: TestClient):
    # Создаём тестовую картинку в памяти
    image_data = io.BytesIO(b"fake png content")
    image_data.name = "test.png"

    response = client.post(
        "/api/medias/upload",
        files={"file": ("test.png", image_data, "image/png")},
        headers={"api-key": "alice"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert "media_id" in data
    assert isinstance(data["media_id"], int)
