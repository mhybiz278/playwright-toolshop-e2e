from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from models.product_list_page import ProductListPage

scenarios("catalogue_search.feature")


@given("the shop is open", target_fixture="catalogue")
def open_shop(page) -> ProductListPage:
    catalogue = ProductListPage(page)
    catalogue.visit()
    expect(catalogue.products.first).to_be_visible()
    return catalogue


@when(parsers.parse('I search for "{term}"'))
def search_for(catalogue, context_state, term):
    catalogue.search(term)
    context_state["term"] = term


@then(parsers.parse('every result mentions "{term}"'))
def every_result_mentions(catalogue, term):
    names = catalogue.names_now()
    assert names, "the search returned nothing to check"
    unrelated = [n for n in names if term.lower() not in n.lower()]
    assert not unrelated, f"results that do not mention {term!r}: {unrelated}"


@then("at least one product is listed")
def at_least_one(catalogue):
    expect(catalogue.product_names.first).to_be_visible()


@then("no products are listed")
def none_listed(catalogue):
    expect(catalogue.product_names).to_have_count(0)
