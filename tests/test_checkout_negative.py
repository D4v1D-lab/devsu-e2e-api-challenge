import os

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def test_checkout_sin_codigo_postal_muestra_error(driver, base_url):
    """Caso negativo: el formulario exige codigo postal antes de continuar."""
    login = LoginPage(driver)
    login.open_login(base_url)
    login.login(
        os.getenv("SAUCE_USERNAME", "standard_user"),
        os.getenv("SAUCE_PASSWORD", "secret_sauce"),
    )

    products = ProductsPage(driver)
    products.add_product_to_cart("sauce-labs-backpack")
    products.open_cart()
    CartPage(driver).proceed_to_checkout()

    mensaje = CheckoutPage(driver).submit_without_postal_code("John", "Doe")

    assert "postal code is required" in mensaje.lower()
    assert "checkout-step-one" in driver.current_url
