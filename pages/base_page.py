from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class BasePage:
    """Shared Selenium helpers for all page objects."""

    DEFAULT_TIMEOUT = 15

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def find(self, locator: tuple[By, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: tuple[By, str]) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        # JS click: cart link has no href; native click does not navigate in headless
        self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator: tuple[By, str], text: str) -> None:
        element = self.find(locator)
        # React-controlled inputs: set native value so state updates
        self.driver.execute_script(
            """
            const el = arguments[0];
            const value = arguments[1];
            const proto = window.HTMLInputElement.prototype;
            const desc = Object.getOwnPropertyDescriptor(proto, 'value');
            desc.set.call(el, value);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            text,
        )

    def get_text(self, locator: tuple[By, str]) -> str:
        return self.find(locator).text

    def is_displayed(self, locator: tuple[By, str]) -> bool:
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False
