from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductsPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def is_loaded(self) -> bool:
        return self.is_displayed(self.TITLE) and "Products" in self.get_text(self.TITLE)

    def add_product_to_cart(self, product_id: str) -> None:
        """Add a product by its data-test / id suffix, e.g. 'sauce-labs-backpack'."""
        locator = (By.ID, f"add-to-cart-{product_id}")
        self.click(locator)

    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    def get_cart_count(self) -> int:
        if not self.is_displayed(self.CART_BADGE):
            return 0
        return int(self.get_text(self.CART_BADGE))
