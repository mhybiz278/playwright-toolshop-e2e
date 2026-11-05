"""Authentication over the API."""
from services.api_client import ApiClient


class AuthService:
    def __init__(self, api: ApiClient):
        self.api = api

    def register(self, user: dict):
        return self.api.post(
            "/users/register",
            {
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "address": {
                    "street": user["street"],
                    "house_number": user["house_number"],
                    "city": user["city"],
                    "state": user["state"],
                    "country": user["country"],
                    "postal_code": user["postal_code"],
                },
                "phone": user["phone"],
                "dob": user["dob"],
                "password": user["password"],
                "email": user["email"],
            },
        )

    def login(self, email: str, password: str):
        res = self.api.post("/users/login", {"email": email, "password": password})
        if res.status_code == 200:
            self.api.set_token(res.json().get("access_token") or res.json().get("token"))
        return res
