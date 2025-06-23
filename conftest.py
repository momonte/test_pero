import pytest
from selenium import webdriver

@pytest.fixture(scope="function")  # scope="function" - драйвер будет пересоздаваться для каждого теста
def browser():
    driver = webdriver.Chrome()  # Или другой браузер: Firefox(), Edge() и т.д.  Убедитесь, что у вас установлен соответствующий драйвер!
    yield driver
    driver.quit() # Закрываем браузер после каждого теста