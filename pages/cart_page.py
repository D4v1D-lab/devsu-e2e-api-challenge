from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, ".title")
    CART_CONTENT = (By.ID, "cart_contents_container")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")

    def is_loaded(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self.CART_CONTENT))
            return "Your Cart" in self.find(self.TITLE).text
        except Exception:
            return False

    def get_item_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def proceed_to_checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)
