import random
import string
from selenium.webdriver.support.ui import Select
import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    wd.implicitly_wait(5)
    request.addfinalizer(wd.quit)
    return wd


def random_str(str_len):
    return ''.join(random.choice(string.ascii_letters) for x in range(str_len))


def random_digit(digit_count):
    return ''.join(str(random.randint(1,10)) for i in range(digit_count))


def login(driver, email, password):
    driver.find_element_by_css_selector("[name=email]").send_keys(email)
    driver.find_element_by_css_selector("[name=password").send_keys(password)
    driver.find_element_by_css_selector("[name=login]").click()


def logout(driver):
    driver.get(driver.find_elements_by_css_selector("#box-account .content .list-vertical li")[3].find_element_by_tag_name("a").get_attribute("href"))


def test_new_user(driver):
    driver.get("http://localhost/litecart/en/create_account")

    field_values = {
        "firstname": random_str(4), "lastname": random_str(5), "address1": random_str(5), "postcode": "11223",
        "city": "test_city", "email": random_str(5) + "@" + random_str(3) + "." + random_str(3), "phone": "+1" + random_digit(10),
        "password": "root", "confirmed_password": "root"
    }

    for item in field_values.items():
        driver.find_element_by_css_selector("[name="+item[0]+"]").send_keys(item[1])

    select_country = Select(driver.find_element_by_css_selector("[name=country_code]"))
    select_country.select_by_visible_text("United States")

    select_zone = Select(driver.find_element_by_css_selector("select[name=zone_code]"))
    options = select_zone.options
    zone = random.randint(0, len(options) - 1)
    select_zone.select_by_visible_text(select_zone.options[zone].text)

    driver.find_element_by_css_selector("[name=create_account]").click()

    logout(driver)
    login(driver, field_values['email'], field_values['password'])
    logout(driver)
