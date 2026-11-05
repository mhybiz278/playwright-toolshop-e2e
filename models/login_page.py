"""Sign in."""
from models.base_page import BasePage


class LoginPage(BasePage):
    path = "/auth/login"

    def sign_in(self, email: str, password: str) -> "LoginPage":
        self.fill_field("email", email)
        self.fill_field("password", password)
        self.click_hook("login-submit")
        return self

    @property
    def error(self):
        return self.el("login-error")
