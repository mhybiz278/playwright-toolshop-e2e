"""Catalogue reads over the API, used to assert the UI against the source."""
from services.api_client import ApiClient


class ProductService:
    def __init__(self, api: ApiClient):
        self.api = api

    def page(self, number: int = 1) -> list[dict]:
        res = self.api.get(f"/products?page={number}")
        assert res.status_code == 200, f"products page {number}: {res.status_code}"
        return res.json()["data"]

    def names_on_page(self, number: int = 1) -> list[str]:
        return [p["name"] for p in self.page(number)]

    def first_purchasable(self) -> dict:
        for product in self.page(1):
            if not product.get("is_rental", False):
                return product
        raise AssertionError("no purchasable product on page 1")
