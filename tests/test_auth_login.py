"""Sign-in, including the lockout the application enforces.

Every scenario mints its own account. The lockout is the reason: a negative
test pointed at a shared account leaves it locked at 423, and the next run's
cart, checkout and account suites all fail somewhere unrelated.
"""
import re

from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from models.login_page import LoginPage

scenarios("auth_login.feature")


@given("I have a registered account", target_fixture="account")
def have_account(registered_user) -> dict:
    return registered_user


@when("I sign in with my own password")
def sign_in_valid(page, account):
    LoginPage(page).visit().sign_in(account["email"], account["password"])


@when(parsers.parse('I sign in with the password "{password}"'))
def sign_in_wrong(page, account, password):
    LoginPage(page).visit().sign_in(account["email"], password)


@when(parsers.parse("I sign in with a wrong password {attempts:d} times"))
def sign_in_wrong_repeatedly(auth_service, account, context_state, attempts):
    statuses = [
        auth_service.login(account["email"], "definitely-not-it").status_code
        for _ in range(attempts)
    ]
    context_state["statuses"] = statuses


@then("I am signed in")
def signed_in(page):
    # The application redirects to the account area; asserting on the URL keeps
    # this independent of whatever the dashboard happens to render.
    expect(page).to_have_url(re.compile(r"/account"))


@then("I am not signed in")
def not_signed_in(page):
    expect(page).to_have_url(re.compile(r"/auth/login"))


@then("the account is locked")
def account_locked(auth_service, account, context_state):
    final = auth_service.login(account["email"], account["password"])
    assert final.status_code == 423, (
        f"expected the account to be locked (423) after "
        f"{len(context_state['statuses'])} failures, got {final.status_code}"
    )
