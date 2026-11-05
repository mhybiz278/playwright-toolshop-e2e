"""Order reads over the API.

The point of this service is one assertion: that an order actually exists.
A checkout screen saying "payment successful" is the UI reporting the outcome
of a *payment check* — whether the order was created is a separate request, and
a separate fact.
"""
from services.api_client import ApiClient


class OrderService:
    def __init__(self, api: ApiClient):
        self.api = api

    def mine(self) -> list[dict]:
        res = self.api.get("/invoices")
        assert res.status_code == 200, f"invoices: {res.status_code}"
        return res.json().get("data", [])

    def count(self) -> int:
        return len(self.mine())
