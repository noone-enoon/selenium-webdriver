import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def authentication(driver):
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()


def check_log(driver):
    assert len(driver.get_log("browser")) == 0


def test_check_log(driver):
    main_page = "http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1"
    driver.get(main_page)
    authentication(driver)
    for i in range(len(driver.find_elements_by_css_selector(".dataTable .row"))-4):
        row = driver.find_elements_by_css_selector(".dataTable .row")
        product = row[i+3].find_elements_by_css_selector("td")[2]
        product.find_element_by_css_selector("a").click()

        driver.get(main_page)
        check_log(driver)
