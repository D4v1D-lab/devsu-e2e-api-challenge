from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    TITLE = (By.CSS_SELECTOR, ".title")
    INFO_CONTAINER = (By.ID, "checkout_info_container")
    SUMMARY_CONTAINER = (By.ID, "checkout_summary_container")

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.wait.until(EC.visibility_of_element_located(self.INFO_CONTAINER))
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.SUMMARY_CONTAINER))

    def finish_order(self) -> None:
        self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON))
        self.click(self.FINISH_BUTTON)

    def get_summary_item_names(self) -> list[str]:
        return [
            el.text
            for el in self.driver.find_elements(
                By.CSS_SELECTOR, ".cart_item .inventory_item_name"
            )
        ]

    def get_summary_item_total(self) -> float:
        label = self.find((By.CSS_SELECTOR, ".summary_subtotal_label")).text
        return float(label.split("$")[1])
