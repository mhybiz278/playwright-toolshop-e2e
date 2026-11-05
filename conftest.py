"""Shared fixtures.

Every fixture that creates state is function-scoped and mints its own data.
The application locks a customer out after three failed sign-ins, so a single
negative auth test pointed at a shared account leaves it locked and takes the
cart, checkout and account suites down on the next run — nowhere near the test
that caused it.
"""
import pytest

from common.data_factory import new_user
from services.api_client import ApiClient
from services.auth_service import AuthService
from services.order_service import OrderService
from services.product_service import ProductService


@pytest.fixture
def api():
    client = ApiClient()
    yield client
    client.close()


@pytest.fixture
def auth_service(api) -> AuthService:
    return AuthService(api)


@pytest.fixture
def product_service(api) -> ProductService:
    return ProductService(api)


@pytest.fixture
def order_service(api) -> OrderService:
    return OrderService(api)


@pytest.fixture
def registered_user(auth_service) -> dict:
    """A brand-new account, created over the API."""
    user = new_user()
    res = auth_service.register(user)
    assert res.status_code in (200, 201), f"registration failed: {res.status_code} {res.text[:200]}"
    return user


@pytest.fixture
def context_state() -> dict:
    """A scratchpad for passing values between BDD steps."""
    return {}
