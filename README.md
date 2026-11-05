# Toolshop E2E — Playwright + Python

An end-to-end suite for the open-source [Practice Software Testing "Toolshop"](https://github.com/testsmith-io/practice-software-testing)
demo shop, written in **Python 3.12 / pytest-bdd / Playwright**.

This is the same application as my [Cypress suite](https://github.com/mhybiz278/cypress-toolshop-e2e),
tested again in a different stack on purpose. Running both against one app is
the only honest way to compare them: the variable is the framework, not the
system under test.

**→ [What the two frameworks actually do differently](docs/CYPRESS-VS-PLAYWRIGHT.md)** —
written from a real bug, not from the marketing pages.

## Running it

```bash
pipenv install && pipenv shell
playwright install chromium

BASE_URL=https://practicesoftwaretesting.com \
API_URL=https://api.practicesoftwaretesting.com \
pytest
```

Point it at any environment with those two variables — that is how the CI jobs
target dev and staging without a code change. There are **no credentials in this
repository**: every test that needs an account creates its own over the API.

Useful subsets:

```bash
pytest -m smoke          # the pre-merge gate
pytest -m catalogue      # one area
pytest --headed          # watch it drive
```

## How it is put together

```
common/       config and the Faker data factory
services/     API layer — httpx. Sets up state; never knows about the DOM
models/       Page objects. Return locators; never assert business rules
features/     Gherkin. The scenario a non-engineer can read
tests/        Step definitions — the glue, and where assertions live
```

Four layers, each with one job — the same separation as the Cypress suite, so
the comparison is about the tools rather than about two different designs.

| Layer | Responsibility | Never does |
|---|---|---|
| Feature | States intent in business language | Mention a selector |
| Step definition | Asserts the business outcome | Know how a screen is built |
| Page object | Drives one screen, returns locators | Assert business rules |
| Service | Sets up state over HTTP | Touch the DOM |

## What is covered

| Area | Scenarios | Notable |
|---|---:|---|
| Catalogue search | 3 | Case-insensitivity, empty-result handling |
| Catalogue pagination | 3 | **No product repeated across a page boundary** |
| Sign in | 3 | **Account lockout after three failures (423)** |
| Catalogue API contract | 3 | Pagination envelope, product schema, negative-price guard |

Two of these exist because they catch things a UI assertion cannot see:

- **Page-boundary duplication** — off-by-one errors in offset/limit show up as
  one record repeated across two pages, never as an obvious failure.
- **Account lockout** — three wrong passwords lock a customer out with `423`.
  Worth asserting deliberately, and worth knowing about before it takes an
  entire suite down by accident. It is why every scenario mints its own account.

## Still to port

Cart, checkout (all five payment methods, and order creation verified over the
API), account and the accessibility gate. Those exist in the Cypress suite; the
page objects here are built to take them.
