import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def authentication(driver):
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()


def open_new_window(driver, old_window):
    all_window = driver.window_handles
    new_window = list(set(all_window)-set(old_window))
    if len(new_window) != 0:
        return new_window[0]


def test_open_link_in_new_windoow(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    authentication(driver)
    first_row = driver.find_elements_by_css_selector(".dataTable .row")[0]
    first_row.find_element_by_css_selector(".fa-pencil").click()

    main_window = driver.current_window_handle
    old_window = driver.window_handles

    for i in range(len(driver.find_elements_by_css_selector("#content tbody [target=_blank]"))):
        driver.find_elements_by_css_selector("#content tbody [target=_blank]")[i].click()
        new_window = WebDriverWait(driver, 10).until(lambda d: open_new_window(d, old_window))
        driver.switch_to_window(new_window)
        driver.close()
        driver.switch_to_window(main_window)
