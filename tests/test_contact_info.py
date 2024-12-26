import time

import pytest
from selenium import webdriver

from pages.cart_page import CartPage
from pages.contact_info_page import ContactInfoPage
from pages.main_page import MainPage
from pages.place_order_page import PlaceOrderPage
from pages.tv_page import TVPage


@pytest.fixture()
def prepare_contact_info_test():
    '''Фикстура до прохождения теста - запускает браузер в режиме "headless",
    открывает главную страницу, проводит авторизацию на сайте,
    открывает страницу категории "Телевизоры", инициализирует экземпляры классов
    TVPage, CartPage, PlaceOrderPage, ContactInfoPage,
    фильтрует страницу телевизоров по бренду и диагонали,
    добавляет в корзину покупок, случайно выбранный с этой страницы телевизор,
    переходит на страницу корзины выбранных для покупки товаров,
    переходит на страницу заполнения данных для доставки покупателю,
    заполняет данными необходимые поля;

    после прохождения теста - переходит на страницу корзины покупок,
    удаляет все выбранные товары из корзины, закрывает браузер'''

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    mp = MainPage(driver)
    mp.start_driver(mp.URL)

    print()
    mp.open_personal_account()
    mp.back_driver()
    print()

    mp.select_category("Телевизоры")
    print()

    tvp = TVPage(driver)
    cp = CartPage(driver)
    plop = PlaceOrderPage(driver)
    cip = ContactInfoPage(driver)

    brand = "LG"
    brand_filter = "Производитель"
    diagonal = "43 inches"
    diagonal_filter = "Диагональ"

    tvp.add_to_cart_random_tv(brand, brand_filter, diagonal, diagonal_filter)
    time.sleep(0.1)
    print()
    mp.come_to_cart()
    print()
    cp.place_order()
    plop.send_place_order()

    yield cip

    print()
    mp.come_to_cart()
    cp.clear_cart()
    time.sleep(1)
    mp.quit_driver()


def test_fill_contact_form(start_finish, prepare_contact_info_test):
    '''Тест проверяет корректность данных для доставки товара покупателю,
    заполненных на предыдущей стадии оформления заказа, проверяет корректность
    заполнения формы контактными данными, корректность url-адреса и заголовков
    финальной страницы, а также делает скриншот финальной страницы'''

    cip = prepare_contact_info_test
    print()

    cip.check_delivery_info()

    cip.send_contact_info()
    print("\nThe purchase of the product was completed SUCCESSFULLY. ALL TESTS ARE GOOD.")
    cip.create_screenshot()
