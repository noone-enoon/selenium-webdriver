from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def is_element_present(driver, locator):
    if len(driver.find_elements_by_css_selector(locator)) > 0:
        return True
    return False


def add_to_cart(driver, count):
    first_product = driver.find_elements_by_css_selector(".content .products a")[0].get_attribute("href")
    driver.get(first_product)

    if is_element_present(driver, "[name=options\[Size\]]") == True:
        select = Select(driver.find_element_by_css_selector("[name=options\[Size\]]"))
        select.select_by_visible_text("Small")

    driver.find_element_by_css_selector("[name=add_cart_product]").click()
    WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart a.content .quantity"), str(count+1)))


def test_add_product_to_cart(driver):
    driver.get("http://localhost/litecart/en/")

    for i in range(3):
        add_to_cart(driver, i)
        driver.get("http://localhost/litecart/en/")

    #открытие корзины
    driver.get(driver.find_element_by_css_selector("#cart a.link").get_attribute("href"))

    if is_element_present(driver, "ul.shortcuts li.shortcut") == False:        #если 3 раза была добавлена одна и та же уточка
        driver.find_element_by_css_selector("[name=remove_cart_item]").click()
        products = driver.find_elements_by_css_selector(".dataTable tr")
        WebDriverWait(driver, 10).until(EC.staleness_of(products[1]))

    else:
        for i in range(len(driver.find_elements_by_css_selector("ul.shortcuts li.shortcut"))-1):
            driver.find_element_by_css_selector("ul.shortcuts li.shortcut").click()
            driver.find_element_by_css_selector("[name=remove_cart_item]").click()
            products = driver.find_elements_by_css_selector(".dataTable tr")
            WebDriverWait(driver, 10).until(EC.staleness_of(products[1]))

        driver.find_element_by_css_selector("[name=remove_cart_item]").click()
        products = driver.find_elements_by_css_selector(".dataTable tr")
        WebDriverWait(driver, 10).until(EC.staleness_of(products[1]))
