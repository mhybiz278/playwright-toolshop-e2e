# Cypress and Playwright, on the same application

I built the [Cypress suite](https://github.com/mhybiz278/cypress-toolshop-e2e)
first and this one second, against the same shop. What follows is what actually
differed in practice — not a feature table.

## The difference that mattered: how each one retries

The Cypress suite passed for months against a local Docker stack. Pointed at a
remote instance, six tests failed. Three of them claimed the shop's pagination
was broken — showing the same nine products on page one and page two.

The shop was fine. The tests were reading a stale page.

```js
// Cypress — productNames() ends in .then()
productNames() {
  return this.el('product-name').then(($els) => Cypress._.map($els, e => e.innerText.trim()));
}

productListPage.nextPage();              // waits for the products *response*
productListPage.productNames().should((names) => { ... });   // too late
```

`.then()` is not retryable. It snapshots the DOM once — at the moment the HTTP
response lands, before Angular has re-rendered — and the `.should()` chained
after it re-runs the assertion against that frozen array, never re-querying the
page. On localhost the render happens in the same tick and the race is never
lost. Add real latency and it is lost almost every time.

The fix was to build the assertion on `.should()` against a live query:

```js
shouldHaveProductNames(assertFn) {
  this.el('product-name').should(($els) => {        // re-queries each attempt
    assertFn(Cypress._.map($els, (e) => e.innerText.trim()));
  });
}
```

In Playwright that bug is difficult to write in the first place:

```python
@property
def product_names(self) -> Locator:
    return self.el("product-name")      # a locator, not a value

expect(catalogue.product_names).not_to_have_text(first_page)
```

A locator is a *query*, not a result. `expect()` re-runs it until the assertion
holds or the timeout expires. "The list has changed" is a condition the
assertion waits for, rather than a race the test has to win.

**This is the honest version of "Playwright has auto-waiting."** Cypress retries
too — but only through `.should()`, and it is easy to step outside that without
noticing. Playwright makes the retrying path the default one.

## Where each one is better

**Playwright**

- The retry model above removes a whole class of flake by construction.
- Real browsers, three engines, and parallelism that works without extra setup.
- Python means the suite lives in the same language as the team's other tooling —
  for a team already on pytest, that matters more than any feature.
- `pytest-bdd` gives Gherkin that a product owner can read and amend.

**Cypress**

- The time-travel debugger is still the best in the field. Stepping back through
  a failed run and seeing the DOM at each command finds a cause faster than
  reading a trace.
- One tool, one config, batteries included. Playwright wanted a deliberate
  decision about runner, BDD layer and HTTP client before the first test ran.
- `cy.intercept` reads more naturally than route interception when a test is
  *about* the network.

## What did not differ

Everything that actually decides whether a suite survives contact with a team:

- Setting up state over the API and asserting through the UI.
- Giving every test its own account, because this app locks a customer out
  after three failed sign-ins.
- Generating data the application will accept, rather than whatever Faker
  produces by default.
- Keeping assertions in the tests and selectors in the page objects.
- Not asserting on a value you just changed.

The architecture of both suites is the same, and that is the point. The
framework was the smaller decision.
