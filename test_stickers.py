import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome('D:\\chromedriver\\chromedriver.exe')
    request.addfinalizer(wd.quit)
    return wd


def check_existence_and_uniqueness_of_sticker(search_context, *args):
    return len(search_context.find_elements(*args)) == 1


def test_check_for_stickers(driver):
    driver.get("http://localhost/litecart/en/")
    products = driver.find_elements_by_class_name("product")

    for product in products:
        assert check_existence_and_uniqueness_of_sticker(product, By.CLASS_NAME, "sticker")
