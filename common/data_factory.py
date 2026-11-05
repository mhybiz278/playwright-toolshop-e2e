"""Test data is generated, never hard-coded.

Shared fixture accounts create order-dependent tests: one test changes a
password and four others fail somewhere else entirely. Every test that needs an
account mints its own.

The generated values have to be data a real customer could actually submit.
Faker will happily produce "Dr. Anna O'Neill" for a field the application
validates as letters-and-spaces, which fails as a validation error rather than
as the bug the test was written to find.
"""
import random
import string

from faker import Faker

fake = Faker()
PASSWORD = "Playwright#2026"


def _letters_only(value: str) -> str:
    return "".join(c for c in value if c.isalpha() or c == " ").strip()


def new_user(**overrides) -> dict:
    """A registration payload the API will accept."""
    user = {
        "first_name": _letters_only(fake.first_name()),
        "last_name": _letters_only(fake.last_name()),
        # A unique local part keeps parallel CI jobs from colliding on an email.
        "email": f"qa.{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}@example.test",
        "password": PASSWORD,
        "dob": fake.date_of_birth(minimum_age=25, maximum_age=55).isoformat(),
        "street": _letters_only(fake.street_name()),
        "house_number": str(random.randint(1, 999)),
        "city": _letters_only(fake.city()),
        "state": _letters_only(fake.state()),
        "country": "New Zealand",
        "postal_code": str(random.randint(1000, 9999)),
        "phone": "".join(random.choices(string.digits, k=10)),
    }
    user.update(overrides)
    return user
