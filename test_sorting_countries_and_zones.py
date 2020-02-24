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
        result.append(row.find_elements_by_tag_name("td")[column_number].text)
    return result


def check_sort(mass_for_check):
    return sorted(mass_for_check) == mass_for_check


def test_check_sorting_countries(driver):
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    authentication(driver)
    rows = driver.find_elements_by_class_name("row")
    countries = get_text(4, rows)
    assert check_sort(countries)


def test_check_zones(driver):
    countries_link = "http://localhost/litecart/admin/?app=countries&doc=countries"
    driver.get(countries_link)
    authentication(driver)

    for i in range(len(driver.find_elements_by_class_name("row"))):
        count_of_zones_for_country = int(driver.find_elements_by_class_name("row")[i].find_elements_by_tag_name("td")[5].text)
        if count_of_zones_for_country > 0:
            country_with_zones = driver.find_elements_by_class_name("row")[i].find_elements_by_tag_name("td")[4]
            link = country_with_zones.find_element_by_tag_name("a").get_attribute("href")

            driver.get(link)

            table_with_zones = driver.find_element_by_id("table-zones")
            rows = table_with_zones.find_elements_by_tag_name("tr")
            zones = get_text(2, rows[1:-1])

            assert check_sort(zones)

            driver.get(countries_link)
