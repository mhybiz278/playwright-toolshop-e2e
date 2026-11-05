"""Pagination, written the way Playwright wants it.

The equivalent Cypress tests failed against a remote environment because they
took a snapshot of the product names the moment the products *response*
arrived — before Angular had re-rendered — and then asserted against that
frozen list. Here `product_names` is a locator, and `expect()` re-queries it on
every attempt, so "the list has changed" is a condition the assertion waits
for rather than a race the test has to win.
"""
from playwright.sync_api import expect
from pytest_bdd import given, scenarios, then, when

from models.product_list_page import ProductListPage

scenarios("catalogue_pagination.feature")


@given("the shop is open", target_fixture="catalogue")
def open_shop(page, context_state) -> ProductListPage:
    catalogue = ProductListPage(page)
    catalogue.visit()
    expect(catalogue.products.first).to_be_visible()
    context_state["first_page"] = catalogue.names_now()
    return catalogue


@when("I go to the next page")
def go_next(catalogue, context_state):
    catalogue.next_page()
    # Wait for the list to actually change before anything reads it.
    expect(catalogue.product_names).not_to_have_text(context_state["first_page"])


@when("I go back to the previous page")
def go_back(catalogue):
    catalogue.previous_page()


@then("the products are not the ones from the first page")
def different_products(catalogue, context_state):
    expect(catalogue.product_names).not_to_have_text(context_state["first_page"])


@then("the products are the ones from the first page")
def same_products(catalogue, context_state):
    expect(catalogue.product_names).to_have_text(context_state["first_page"])


@then("no product from the first page is listed again")
def no_overlap(catalogue, context_state):
    second_page = catalogue.names_now()
    overlap = [n for n in second_page if n in context_state["first_page"]]
    assert not overlap, f"products duplicated across pages: {overlap}"
