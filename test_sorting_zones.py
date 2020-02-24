import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome('D:\\chromedriver\\chromedriver.exe')
    request.addfinalizer(wd.quit)
    return wd


def authentication(driver):
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()


def get_text(column_number, rows):
    result = []
    for row in rows:
        result.append((row.find_elements_by_tag_name("td")[column_number]).find_element_by_css_selector("[selected=selected]").text)
    return result


def check_sort(mass_for_check):
    return sorted(mass_for_check) == mass_for_check


def test_check_sorting_zones(driver):
    start_link = "http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones"
    driver.get(start_link)
    authentication(driver)

    for i in range(len(driver.find_element_by_name("geo_zones_form").find_elements_by_class_name("row"))):
        rows = driver.find_element_by_name("geo_zones_form").find_elements_by_class_name("row")
        country_link = rows[i].find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").get_attribute("href")

        driver.get(country_link)

        table_with_zones = driver.find_element_by_id("table-zones")
        rows = table_with_zones.find_elements_by_tag_name("tr")[1:-1]
        zones = get_text(2, rows)
        assert check_sort(zones)

        driver.get(start_link)
