import random
import string
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(5)
    request.addfinalizer(wd.quit)
    return wd


def random_str(str_len):
    return ''.join(random.choice(string.ascii_letters) for x in range(str_len))


def login(driver):
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()


def general(driver, name, code, path):
    #status
    driver.find_elements_by_css_selector("[name=status]")[0].click()
    #name
    driver.find_element_by_css_selector("[name=name\[en\]]").send_keys(name)
    #code
    driver.find_element_by_css_selector("[name=code]").send_keys(code)
    #categories
    driver.find_element_by_css_selector("[data-name=Root]").click()
    driver.find_element_by_css_selector("[data-name^=Rubber]").click()
    #gender
    driver.find_element_by_css_selector("input[name=product_groups\[\]][value='1-3']").click()
    #quantity
    driver.find_element_by_css_selector("[name=quantity]").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    driver.find_element_by_css_selector("[name=quantity]").send_keys("2")
    #date
    driver.find_element_by_css_selector("[name=date_valid_from]").send_keys(Keys.HOME + "11.02.2020")
    driver.find_element_by_css_selector("[name=date_valid_to]").send_keys(Keys.HOME + "21.02.2020")
    #image
    driver.find_element_by_css_selector("[name=new_images\[\]]")
    driver.find_element_by_css_selector("[name=new_images\[\]]").send_keys(path)
    print("a")


def information(driver, **kwargs):
    #manufacturer_id
    select = Select(driver.find_element_by_css_selector("[name=manufacturer_id]"))
    select.select_by_visible_text("ACME Corp.")
    #keywords
    driver.find_element_by_css_selector("[name=keywords]").send_keys(kwargs['field_keywords'])
    #short description
    driver.find_element_by_css_selector("[name=short_description\[en\]]").send_keys(kwargs['field_short_descr'])
    #description
    driver.find_element_by_css_selector(".trumbowyg-editor").send_keys(kwargs['field_description'])
    #head_title
    driver.find_element_by_css_selector("[name=head_title\[en\]]").send_keys(kwargs['field_head_title'])
    driver.find_element_by_css_selector("[name=meta_description\[en\]]").send_keys(kwargs['field_meta_description'])


def price(driver):
    #purchase price
    driver.find_element_by_css_selector("[name=purchase_price]").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    driver.find_element_by_css_selector("[name=purchase_price]").send_keys("10")
    select = Select(driver.find_element_by_css_selector("[name=purchase_price_currency_code]"))
    select.select_by_visible_text("Euros")
    #price incl. tax
    driver.find_element_by_css_selector("[name=gross_prices\[USD\]]").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    driver.find_element_by_css_selector("[name=gross_prices\[USD\]]").send_keys("10")
    driver.find_element_by_css_selector("[name=gross_prices\[EUR\]]").send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    driver.find_element_by_css_selector("[name=gross_prices\[EUR\]]").send_keys("10")


def check_new_product(driver, name):
    mass_a = driver.find_elements_by_css_selector(".dataTable a")
    for item in mass_a:
        if item.text == name:
            return 0


def test_add_product(driver):
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog")
    login(driver)

    absolute_path = os.path.abspath("./duck.jpg")

    field_values = {
        "field_name": random_str(4), "field_code": random_str(5), "path": absolute_path,
        "field_keywords": random_str(3), "field_short_descr": random_str(3), "field_head_title": random_str(3),
        "field_meta_description": random_str(3), "field_description": random_str(3)
    }

    driver.find_elements_by_css_selector("#content div")[3].find_elements_by_css_selector("a")[1].click()#нажатие на кнопку добавления элемента
    general(driver, field_values['field_name'], field_values['field_code'], field_values['path'])
    driver.find_elements_by_css_selector(".index li")[1].click()#переход на вкладку information
    information(driver, **field_values)
    driver.find_elements_by_css_selector(".index li")[3].click()
    price(driver)
    driver.find_element_by_css_selector("[name=save]").click()
    check_new_product(driver, field_values["field_name"])
