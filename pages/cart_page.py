from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")

    def is_loaded(self) -> bool:
        return self.is_displayed(self.TITLE) and "Your Cart" in self.get_text(self.TITLE)

    def get_item_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def proceed_to_checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)
