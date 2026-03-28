import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "12345678"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login():
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "12345678"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]

def test_upload_file():
    token = test_login()
    with open("test.txt", "wb") as f:
        f.write(b"test content")
    
    with open("test.txt", "rb") as f:
        response = client.post(
            "/files/upload",
            files={"file": ("test.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"

def test_get_files():
    token = test_login()
    response = client.get(
        "/files/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_download_file():
    token = test_login()
    # First upload a file
    with open("test_download.txt", "wb") as f:
        f.write(b"test download")
    
    with open("test_download.txt", "rb") as f:
        upload = client.post(
            "/files/upload",
            files={"file": ("test_download.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {token}"}
        )
    
    file_id = upload.json()["file_id"]
    
    # Download it
    response = client.get(
        f"/files/{file_id}/download",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_delete_file():
    token = test_login()
    # Upload a file first
    with open("test_delete.txt", "wb") as f:
        f.write(b"test delete")
    
    with open("test_delete.txt", "rb") as f:
        upload = client.post(
            "/files/upload",
            files={"file": ("test_delete.txt", f, "text/plain")},
            headers={"Authorization": f"Bearer {token}"}
        )
    
    file_id = upload.json()["file_id"]
    
    # Delete it
    response = client.delete(
        f"/files/{file_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200