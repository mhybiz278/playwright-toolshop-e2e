"""The catalogue listing."""
from playwright.sync_api import Locator

from models.base_page import BasePage


class ProductListPage(BasePage):
    path = "/"

    @property
    def products(self) -> Locator:
        """A product card is the anchor whose hook is `product-{id}`.

        Restricting to `a` matters: `product-name` and `product-price` share the
        same prefix, so a bare prefix match counts three elements per product
        and every length assertion in the catalogue tests is quietly wrong.
        """
        return self.page.locator('a[data-test^="product-"]')

    @property
    def product_names(self) -> Locator:
        """A *locator*, not a list.

        This is the whole difference from the Cypress suite. A locator is
        re-queried every time an assertion reads it, so `expect(...)` retries
        against the live DOM. Returning `locator.all_text_contents()` here would
        snapshot the page once and compare a stale list — which is exactly the
        bug that made the Cypress pagination tests report a defect that was not
        there.
        """
        return self.el("product-name")

    def names_now(self) -> list[str]:
        """A deliberate snapshot, for when a test needs to compare two states."""
        return [t.strip() for t in self.product_names.all_text_contents()]

    def search(self, term: str) -> "ProductListPage":
        self.fill_field("search-query", term)
        self.click_hook("search-submit")
        # The listing stamps a state container whose `data-test` value *is* the
        # current state. Waiting on that is a real signal from the application
        # rather than a sleep.
        self.el("search_completed").wait_for(state="attached")
        return self

    def next_page(self) -> "ProductListPage":
        self.page.get_by_label("Next").click()
        return self

    def previous_page(self) -> "ProductListPage":
        self.page.get_by_label("Previous").click()
        return self
