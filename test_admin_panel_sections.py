import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome('D:\\chromedriver\\chromedriver.exe')
    request.addfinalizer(wd.quit)
    return wd


def authentication(driver):
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()


def follow_links_and_check_title(driver):
    for i in range(len(driver.find_elements_by_id("app-"))):
        driver.find_elements_by_id("app-")[i].click()
        for j in range(len(driver.find_elements_by_id("app-")[i].find_elements_by_tag_name("li"))):
            driver.find_elements_by_id("app-")[i].find_elements_by_tag_name("li")[j].click()
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))


def test_admin_panel_sections(driver):
    authentication(driver)
    follow_links_and_check_title(driver)
