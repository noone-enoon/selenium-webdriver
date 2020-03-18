from selenium.webdriver.support.wait import WebDriverWait


class CommonPage:

    def __init__(self, driver):
        self.driver = driver

    def is_element_present(self, locator):
        if len(self.driver.find_elements_by_css_selector(locator)) > 0:
            return True
        return False
