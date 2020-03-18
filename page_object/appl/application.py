from selenium import webdriver
from page_object.pages.cart_page import CartPage
from page_object.pages.common_page import CommonPage
from page_object.pages.main_page import MainPage
from page_object.pages.product_page import ProductPage


class Application:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.cart_page = CartPage(self.driver)
        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.common_page = CommonPage(self.driver)

    def quit(self):
        self.driver.quit()

    def add_first_product_to_cart(self, count):
        self.main_page.open_first_element()
        if self.check_different_sizes() == True:
            self.product_page.choose_product_size()
        self.product_page.add_to_cart()
        self.product_page.wait_product_counter_update(count)

    def products_are_different(self):
        return(self.common_page.is_element_present("ul.shortcuts li.shortcut"))

    def check_different_sizes(self):
        return(self.common_page.is_element_present("[name=options\[Size\]]"))

    def del_from_cart(self):
        self.cart_page.del_product()
        self.cart_page.wait_refresh_table()

