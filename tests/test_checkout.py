import os

from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def test_happy_path_checkout(driver, base_url):
    username = os.getenv("SAUCE_USERNAME", "standard_user")
    password = os.getenv("SAUCE_PASSWORD", "secret_sauce")

    login_page = LoginPage(driver)
    login_page.open_login(base_url)
    login_page.login(username, password)

    products = ProductsPage(driver)
    assert products.is_loaded()
    products.add_product_to_cart("sauce-labs-backpack")
    products.add_product_to_cart("sauce-labs-bike-light")
    assert products.get_cart_count() == 2
    products.open_cart()

    expected_items = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]

    cart = CartPage(driver)
    assert cart.is_loaded()
    assert cart.get_item_count() == 2
    assert cart.get_item_names() == expected_items
    cart.proceed_to_checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_information(
        first_name=os.getenv("CHECKOUT_FIRST_NAME", "John"),
        last_name=os.getenv("CHECKOUT_LAST_NAME", "Doe"),
        postal_code=os.getenv("CHECKOUT_POSTAL_CODE", "12345"),
    )

    # El resumen muestra los mismos productos y el subtotal correcto (29.99 + 9.99)
    assert checkout.get_summary_item_names() == expected_items
    assert checkout.get_summary_item_total() == 29.99 + 9.99
    checkout.finish_order()

    complete = CheckoutCompletePage(driver)
    assert complete.is_order_complete()
