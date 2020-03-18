from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class ProductPage:

    def __init__(self, driver):
        self.driver = driver

    def choose_product_size(self):
        select = Select(self.driver.find_element_by_css_selector("[name=options\[Size\]]"))
        select.select_by_visible_text("Small")
        return self

    def add_to_cart(self):
        self.driver.find_element_by_css_selector("[name=add_cart_product]").click()
        return self

    def wait_product_counter_update(self, count):
        WebDriverWait(self.driver, 5).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart a.content .quantity"), str(count + 1)))
        return self

