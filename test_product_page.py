import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL целевой страницы
PRODUCT_URL = "https://vk.com/market/product/fyvaf-225299895-10044406"

# Локаторы (обновлены, учитывая структуру страницы на момент написания)
TITLE_LOCATOR = (By.CSS_SELECTOR, ".market_item_header__name")
PRICE_LOCATOR = (By.CSS_SELECTOR, ".market_item_header__price")
ADD_TO_CART_BUTTON_LOCATOR = (By.CSS_SELECTOR, ".market_item_control__button")  #  Кнопка "Добавить в корзину"
CART_ICON_LOCATOR = (By.CSS_SELECTOR, ".MarketCartLink__link") # Иконка корзины (в верхней панели)
CART_ITEM_TITLE_LOCATOR = (By.CSS_SELECTOR, ".cart_item_title") # Заголовок товара в корзине (после добавления)


class ProductPage:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def open(self):
        self.browser.get(self.url)

    def _wait_for_element(self, locator, timeout=10):
        """Вспомогательная функция для ожидания появления элемента."""
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def get_product_title(self):
        """Получает заголовок товара."""
        element = self._wait_for_element(TITLE_LOCATOR)
        return element.text

    def get_product_price(self):
        """Получает цену товара."""
        element = self._wait_for_element(PRICE_LOCATOR)
        return element.text

    def add_to_cart(self):
        """Добавляет товар в корзину."""
        button = self._wait_for_element(ADD_TO_CART_BUTTON_LOCATOR)
        button.click()


    def open_cart(self):
        """Открывает корзину (переходит по ссылке на иконку корзины)."""
        cart_icon = self._wait_for_element(CART_ICON_LOCATOR)
        cart_icon.click()


    def get_cart_item_title(self):
        """Получает заголовок товара в корзине.  Предполагается, что корзина открыта."""
        element = self._wait_for_element(CART_ITEM_TITLE_LOCATOR)
        return element.text


@pytest.fixture
def product_page(browser):
    """Фикстура для открытия страницы товара."""
    page = ProductPage(browser, PRODUCT_URL)
    page.open()
    return page


def test_product_title(product_page):
    """Проверка заголовка товара."""
    title = product_page.get_product_title()
    assert "фываф" in title, f"Неверный заголовок товара.  Получено: {title}"


def test_product_price(product_page):
    """Проверка цены товара."""
    price = product_page.get_product_price()
    #  Цена может меняться, поэтому более надёжная проверка - наличие "₽" и числовых значений.
    assert "₽" in price and any(char.isdigit() for char in price), f"Неверная цена товара. Получено: {price}"


def test_add_to_cart(product_page):
    """Проверка добавления товара в корзину."""
    product_page.add_to_cart()
    product_page.open_cart()  # Открываем корзину, чтобы проверить наличие товара

    cart_item_title = product_page.get_cart_item_title()
    assert "фываф" in cart_item_title, "Товар не был добавлен в корзину или отображается некорректно."