import os

from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def test_login_with_invalid_credentials_shows_error(driver, base_url):
    login_page = LoginPage(driver)
    login_page.open_login(base_url)
    login_page.login("invalid_user", "wrong_password")

    assert login_page.is_error_displayed()
    error = login_page.get_error_message().lower()
    assert "username and password do not match" in error or "epic sadface" in error


def test_login_with_valid_credentials(driver, base_url):
    username = os.getenv("SAUCE_USERNAME", "standard_user")
    password = os.getenv("SAUCE_PASSWORD", "secret_sauce")

    login_page = LoginPage(driver)
    login_page.open_login(base_url)
    login_page.login(username, password)

    products_page = ProductsPage(driver)
    assert products_page.is_loaded()
