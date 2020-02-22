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


def category_selection(driver, category):
    product_list = driver.find_element_by_id(category).find_elements_by_tag_name("li")
    for item in product_list:
        assert check_existence_and_uniqueness_of_sticker(item, By.CLASS_NAME, "sticker")


def test_check_for_stickers(driver):
    driver.get("http://localhost/litecart/en/")

    category_list = ["box-most-popular", "box-latest-products", "box-campaigns"]

    for category in category_list:
        category_selection(driver, category)
