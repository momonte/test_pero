import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL целевой страницы (главная страница сообщества)
COMMUNITY_URL = "https://vk.com/club225299895"


COMMUNITY_NAME_LOCATOR = (By.CSS_SELECTOR, ".group_name")  # Название сообщества
SUBSCRIBE_BUTTON_LOCATOR = (By.CSS_SELECTOR, ".group_join_button") # Кнопка "Подписаться" или "Вы подписаны"
POST_TEXT_LOCATOR = (By.CSS_SELECTOR, ".post_text")  # Локатор для текста поста (пример)



class CommunityPage:
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

    def get_community_name(self):
        """Получает название сообщества."""
        element = self._wait_for_element(COMMUNITY_NAME_LOCATOR)
        return element.text

    def is_subscribe_button_present(self):
        """Проверяет наличие кнопки "Подписаться" (или аналога)."""
        try:
            self._wait_for_element(SUBSCRIBE_BUTTON_LOCATOR, timeout=2) # Уменьшаем timeout, чтобы не ждать долго, если кнопки нет
            return True
        except:
            return False

    def get_first_post_text(self):
        """Получает текст первого поста (если есть)."""
        try:
            element = self._wait_for_element(POST_TEXT_LOCATOR, timeout=5)  # Уменьшаем timeout для более быстрой проверки
            return element.text
        except:
            return None # Если постов нет, вернем None

    


@pytest.fixture
def community_page(browser):
    """Фикстура для открытия страницы сообщества."""
    page = CommunityPage(browser, COMMUNITY_URL)
    page.open()
    return page


def test_community_name(community_page):
    """Проверка названия сообщества."""
    name = community_page.get_community_name()
    assert "Test public for test" in name, f"Неверное название сообщества. Получено: {name}"


def test_subscribe_button_visibility(community_page):
    """Проверка отображения кнопки "Подписаться" (или аналога)."""
    is_present = community_page.is_subscribe_button_present()
    assert is_present, "Кнопка 'Подписаться' не найдена." #  Или проверьте другой статус (например, "Вы подписаны")

def test_first_post_text(community_page):
    """Проверка текста первого поста (простая проверка)."""
    post_text = community_page.get_first_post_text()
    if post_text:
        assert len(post_text) > 10, "Текст первого поста слишком короткий." #  Проверка минимальной длины текста
    else:
        print("В сообществе нет постов.")
        