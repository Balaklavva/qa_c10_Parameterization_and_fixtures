import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


class TestCourierLogin:

    @pytest.mark.parametrize(
        "login_type, password_type, expected_status",
        [
            ("valid", "valid", 200),
            ("missing", "valid", 400),
            ("valid", "missing", 400),
            ("unknown", "valid", 404),
        ]
    )
    def test_courier_login(
        self,
        courier,
        login_type,
        password_type,
        expected_status,
    ):
        if login_type == "valid":
            login = courier["login"]
        elif login_type == "unknown":
            login = "loginerror"
        else:
            login = ""
        
        if password_type == "valid":
            password = courier["password"]
        else:
            password = ""

        payload = {
            "login": login,
            "password": password,
        }


        response = requests.post(f"{BASE_URL}/api/v1/courier/login", json=payload)
        assert response.status_code == expected_status

        response_json = response.json()
        if expected_status == 200:
            assert "id" in response_json
        if expected_status in (400, 404):
            assert "message" in response_json
