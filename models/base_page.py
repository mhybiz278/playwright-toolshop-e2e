"""Shared behaviour for every page object.

Page objects expose intent ("search for", "add the first product to the cart")
and return locators. They do not assert business rules — those belong in the
step definitions, where a failure message points at the scenario's intent
rather than at framework internals.

Test hooks are `data-test` attributes. The attribute name lives here only, so
if the convention ever changes it is a one-line edit.
"""
from playwright.sync_api import Locator, Page

from common.config import BASE_URL

ATTR = "data-test"


def by_test(value: str) -> str:
    return f'[{ATTR}="{value}"]'


def by_test_starts_with(prefix: str) -> str:
    return f'[{ATTR}^="{prefix}"]'


class BasePage:
    path = "/"

    def __init__(self, page: Page):
        self.page = page

    def visit(self, path: str | None = None) -> "BasePage":
        self.page.goto(f"{BASE_URL}{path or self.path}")
        return self

    def el(self, hook: str) -> Locator:
        return self.page.locator(by_test(hook))

    def els_starting_with(self, prefix: str) -> Locator:
        return self.page.locator(by_test_starts_with(prefix))

    def fill_field(self, hook: str, value: str) -> "BasePage":
        self.el(hook).fill(value)
        return self

    def click_hook(self, hook: str) -> "BasePage":
        self.el(hook).click()
        return self
