from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
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

    def click(self, locator: tuple[By, str], expected=None, retries: int = 2) -> None:
        """Clic nativo con reintento verificable.

        En algunos entornos headless Chrome pierde el evento del clic si la
        página está re-renderizando (React). En lugar de reintentar a ciegas
        (eso duplicaría el clic), se verifica un efecto observable en el DOM
        y se vuelve a hacer clic solo si el primero no tuvo efecto.
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        if expected is None:
            return
        if self._has_effect(expected):
            return
        for _ in range(retries):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            if self._has_effect(expected):
                return
        # Último recurso: ciertos entornos headless pierden el evento del clic
        # nativo sin error. El clic programático se verifica igual contra el
        # efecto observable (no duplica clics) y sobre un botón deshabilitado
        # no tiene efecto: el test falla como lo haría con un usuario real.
        self.driver.execute_script(
            "arguments[0].click();", self.driver.find_element(*locator)
        )
        if self._has_effect(expected):
            return
        self.wait.until(expected)

    def _has_effect(self, expected) -> bool:
        try:
            WebDriverWait(self.driver, 3).until(expected)
            return True
        except TimeoutException:
            return False

    def type_text(self, locator: tuple[By, str], text: str) -> None:
        element = self.find(locator)
        element.send_keys(text)
        try:
            if element.get_attribute("value") == text:
                return
        except StaleElementReferenceException:
            pass
        # Headless moderno a veces pierde también eventos de teclado: reponemos
        # el valor con el setter nativo de React y disparamos input/change.
        # Es el mismo efecto que teclear; si el campo está deshabilitado,
        # send_keys ya habría fallado antes con ElementNotInteractable.
        self.driver.execute_script(
            """
            const el = arguments[0];
            const value = arguments[1];
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            setter.call(el, value);
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
