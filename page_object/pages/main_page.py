from selenium.webdriver.support.wait import WebDriverWait


class MainPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_first_element(self):
        self.driver.get(self.driver.find_elements_by_css_selector(".content .products a")[0].get_attribute("href"))
        return self

    def open_main_page(self):
        self.driver.get("http://localhost/litecart/en/")
        return self
