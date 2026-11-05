from pytest_bdd import scenarios, then, when

scenarios("api_catalogue.feature")


@when("I request page 1 of the products")
def request_page_one(api, context_state):
    context_state["response"] = api.get("/products?page=1")


@then("the response carries a pagination envelope")
def pagination_envelope(context_state):
    res = context_state["response"]
    assert res.status_code == 200, res.status_code
    body = res.json()
    for key in ("data", "current_page", "total"):
        assert key in body, f"missing {key!r} from the pagination envelope"
    assert isinstance(body["data"], list) and body["data"], "page 1 returned no products"


@then("every product has an id, a name and a price")
def product_schema(context_state):
    for product in context_state["response"].json()["data"]:
        for key in ("id", "name", "price"):
            assert key in product, f"{product.get('name', product)} is missing {key!r}"


@then("every product costs more than zero")
def positive_prices(context_state):
    bad = [p["name"] for p in context_state["response"].json()["data"] if float(p["price"]) <= 0]
    assert not bad, f"products priced at or below zero: {bad}"
