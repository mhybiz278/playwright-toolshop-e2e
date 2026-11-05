"""Thin HTTP client for the application's REST API.

Tests set up and tear down state here rather than through the UI. A checkout
test is about checkout: driving the registration form first makes it slower and
couples it to an unrelated screen, so when auth breaks, twelve tests fail and
none of them says why.
"""
import httpx

from common.config import API_URL


class ApiClient:
    def __init__(self, base_url: str = API_URL):
        self._client = httpx.Client(base_url=base_url, timeout=30.0)
        self._token: str | None = None

    def set_token(self, token: str) -> None:
        self._token = token

    @property
    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self._token}"} if self._token else {}

    def get(self, path: str, **kwargs) -> httpx.Response:
        return self._client.get(path, headers=self._headers, **kwargs)

    def post(self, path: str, json: dict | None = None, **kwargs) -> httpx.Response:
        return self._client.post(path, json=json, headers=self._headers, **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        return self._client.delete(path, headers=self._headers, **kwargs)

    def close(self) -> None:
        self._client.close()
