import pytest


def test_add_to_cart(app):
    app.main_page.open_main_page()

    for i in range(3):
        app.add_first_product_to_cart(i)
        app.main_page.open_main_page()

    app.cart_page.open_cart_page()

    if app.products_are_different() == False:
        app.del_from_cart()

    else:
        for i in range(app.cart_page.number_different_products_in_cart() - 1):
            app.cart_page.click_on_product_thumbnail()
            app.del_from_cart()

        app.del_from_cart()
