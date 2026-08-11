from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")
    COMPLETE_TEXT = (By.CSS_SELECTOR, ".complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    COMPLETE_CONTAINER = (By.ID, "checkout_complete_container")

    def get_complete_header(self) -> str:
        self.wait.until(EC.visibility_of_element_located(self.COMPLETE_CONTAINER))
        return self.get_text(self.COMPLETE_HEADER)

    def is_order_complete(self) -> bool:
        header = self.get_complete_header().upper()
        return "THANK YOU FOR YOUR ORDER" in header
