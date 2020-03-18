from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:

    def __init__(self, driver):
        self.driver = driver

    def open_cart_page(self):
        self.driver.get(self.driver.find_element_by_css_selector("#cart a.link").get_attribute("href"))
        return self

    def del_product(self):
        self.driver.find_element_by_css_selector("[name=remove_cart_item]").click()
        return self

    def wait_refresh_table(self):
        products = self.driver.find_elements_by_css_selector(".dataTable tr")
        WebDriverWait(self.driver, 10).until(EC.staleness_of(products[1]))
        return self

    def number_different_products_in_cart(self):
        return(len(self.driver.find_elements_by_css_selector("ul.shortcuts li.shortcut")))

    def click_on_product_thumbnail(self):
        self.driver.find_element_by_css_selector("ul.shortcuts li.shortcut").click()
        return self
