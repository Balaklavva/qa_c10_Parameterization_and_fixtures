import os
import uuid

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


@pytest.fixture
def courier():
    login = f"TODO_{uuid.uuid4().hex[:8]}"

    courier_data = {
        "login": login,
        "password": "1234",
        "firstName": "Test",
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/courier",
        json=courier_data,
    )
    assert response.status_code == 201, f"Ошибка при создании курьера: {response.text}"
    

    login_response = requests.post(
        f"{BASE_URL}/api/v1/courier/login",
        json={
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
    )
    assert login_response.status_code == 200, f"Ошибка авторизации: {login_response.text}"
    courier_id = login_response.json()["id"]
    
    yield {
        "login": courier_data["login"],
        "password": courier_data["password"],
        "id": courier_id,
    }
    requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")