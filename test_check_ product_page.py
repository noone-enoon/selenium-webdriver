import pytest
from selenium import webdriver
import re


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
  #  wd = webdriver.Firefox()
  #  wd = webdriver.Ie(capabilities={"requireWindowFocus": True})
    request.addfinalizer(wd.quit)
    return wd


#a
def test_match_text_on_the_main_page_and_product_page(driver):
    driver.get("http://localhost/litecart/en/")

    main_page_text = driver.find_element_by_css_selector("#box-campaigns .product .name").text
    product_page_link = driver.find_element_by_css_selector("#box-campaigns .product a").get_attribute("href")

    driver.get(product_page_link)
    
    product_page_text = driver.find_element_by_css_selector("#box-product .title").text
    assert main_page_text == product_page_text


#б_regular
def test_match_regular_price_on_the_main_page_and_product_page(driver):
    driver.get("http://localhost/litecart/en/")

    main_page_regular_price = driver.find_element_by_css_selector("#box-campaigns .price-wrapper .regular-price").text
    product_page_regular_price = driver.find_element_by_css_selector(".price-wrapper .regular-price").text

    assert main_page_regular_price == product_page_regular_price


#б_campaign
def test_match_campaign_price_on_the_main_page_and_product_page(driver):
    driver.get("http://localhost/litecart/en/")

    main_page_campaign_price = driver.find_element_by_css_selector("#box-campaigns .price-wrapper .campaign-price").text
    product_page_campaign_price = driver.find_element_by_css_selector(".price-wrapper .campaign-price").text

    assert main_page_campaign_price == product_page_campaign_price


#в
def test_check_color_and_strikeout_font_regular_price(driver):
    driver.get("http://localhost/litecart/en/")

    main_page_color_regular_price = driver.find_element_by_css_selector("#box-campaigns .price-wrapper .regular-price").value_of_css_property("color")
    rgb = re.search("\d+, \d+, \d+", main_page_color_regular_price).group().split(', ')
    assert int(rgb[0]) == int(rgb[1]) == int(rgb[2])

    main_page_strikeout_font_regular_price = driver.find_element_by_css_selector("#box-campaigns .price-wrapper .regular-price").value_of_css_property("text-decoration-line")
    main_page_strikeout_font_regular_price_ie = driver.find_element_by_css_selector("#box-campaigns .price-wrapper .regular-price").value_of_css_property("text-decoration")
    assert main_page_strikeout_font_regular_price == "line-through" or main_page_strikeout_font_regular_price_ie == "line-through"

    product_page_link = driver.find_element_by_css_selector("#box-campaigns .product a").get_attribute("href")
    driver.get(product_page_link)

    product_page_color_regular_price = driver.find_element_by_css_selector(".price-wrapper .regular-price").value_of_css_property("color")
    rgb = re.search("\d+, \d+, \d+", product_page_color_regular_price).group().split(', ')
    assert int(rgb[0]) == int(rgb[1]) == int(rgb[2])

    product_page_strikeout_font_regular_price = driver.find_element_by_css_selector(".price-wrapper .regular-price").value_of_css_property("text-decoration-line")
    product_page_strikeout_font_regular_price_ie = driver.find_element_by_css_selector(".price-wrapper .regular-price").value_of_css_property("text-decoration")
    assert product_page_strikeout_font_regular_price == "line-through" or product_page_strikeout_font_regular_price_ie == "line-through"


#г
def test_check_color_and_fat_type_campaign_price(driver):
    driver.get("http://localhost/litecart/en/")

    main_page_color_campaign_price = driver.find_element_by_css_selector("#box-campaigns .price-wrapper .campaign-price").value_of_css_property("color")
    rgb = re.search("\d+, \d+, \d+", main_page_color_campaign_price).group().split(', ')
    assert int(rgb[1]) == 0 and int(rgb[2]) == 0

    main_page_fat_type_campaign_price = driver.find_element_by_css_selector("#box-campaigns .price-wrapper .campaign-price").value_of_css_property("font-weight")
    assert int(main_page_fat_type_campaign_price) >= 700

    product_page_link = driver.find_element_by_css_selector("#box-campaigns .product a").get_attribute("href")
    driver.get(product_page_link)

    product_page_color_campaign_price = driver.find_element_by_css_selector(".price-wrapper .campaign-price").value_of_css_property("color")
    rgb = re.search("\d+, \d+, \d+", product_page_color_campaign_price).group().split(', ')
    assert int(rgb[1]) == 0 and int(rgb[2]) == 0

    product_page_fat_type_campaign_price = driver.find_element_by_css_selector(".price-wrapper .campaign-price").value_of_css_property("font-weight")
    assert int(product_page_fat_type_campaign_price) >= 700


#д
def test_check_size(driver):
    driver.get("http://localhost/litecart/en/")

    main_page_regular_price_size = driver.find_element_by_css_selector("#box-campaigns .price-wrapper .regular-price").value_of_css_property("font-size")
    main_page_campaign_price_size = driver.find_element_by_css_selector("#box-campaigns .price-wrapper .campaign-price").value_of_css_property("font-size")

    main_page_regular_price_size_float = re.search("\d+\.?\d*", main_page_regular_price_size).group()
    main_page_campaign_price_size_float = re.search("\d+\.?\d*", main_page_campaign_price_size).group()

    assert float(main_page_regular_price_size_float) < float(main_page_campaign_price_size_float)

    product_page_link = driver.find_element_by_css_selector("#box-campaigns .product a").get_attribute("href")
    driver.get(product_page_link)

    product_page_regular_price_size = driver.find_element_by_css_selector(".price-wrapper .regular-price").value_of_css_property("font-size")
    product_page_campaign_price_size = driver.find_element_by_css_selector(".price-wrapper .campaign-price").value_of_css_property("font-size")

    product_page_regular_price_size_float = re.search("\d+\.?\d*", product_page_regular_price_size).group()
    product_page_campaign_price_size_float = re.search("\d+\.?\d*", product_page_campaign_price_size).group()

    assert float(product_page_regular_price_size_float) < int(product_page_campaign_price_size_float)
