import time

import pytest
from selenium import webdriver

from pages.cart_page import CartPage
from pages.main_page import MainPage
from pages.place_order_page import PlaceOrderPage
from pages.tv_page import TVPage


@pytest.fixture()
def prepare_order_place_test():
    '''Фикстура до прохождения теста - запускает браузер, открывает главную страницу,
    проводит авторизацию на сайте, открывает страницу категории "Телевизоры",
    инициализирует экземпляры классов TVPage, CartPage, PlaceOrderPage,
    фильтрует страницу телевизоров по бренду и размеру диагонали,
    добавляет в корзину покупок, случайно выбранный с этой страницы телевизор,
    переходит на страницу корзины выбранных для покупки товаров,
    переходит на страницу заполнения данных для доставки покупателю;

    после прохождения теста - переходит на страницу корзины покупок,
    удаляет все выбранные товары из корзины, закрывает браузер'''

    driver = webdriver.Chrome()

    mp = MainPage(driver)
    mp.start_driver(mp.URL)

    mp.open_personal_account()
    mp.back_driver()

    mp.select_category("Телевизоры")
    print()

    tvp = TVPage(driver)
    cp = CartPage(driver)
    plop = PlaceOrderPage(driver)

    brand = "LG"
    brand_filter = "Производитель"
    diagonal = "43 inches"
    diagonal_filter = "Диагональ"

    tvp.add_to_cart_random_tv(brand, brand_filter, diagonal, diagonal_filter)
    time.sleep(0.1)
    mp.come_to_cart()
    cp.place_order()

    yield plop

    print()
    mp.come_to_cart()
    cp.clear_cart()
    time.sleep(1)
    mp.quit_driver()


def test_fill_order_form(start_finish, prepare_order_place_test):
    '''Тест проверяет корректность заполнения всех обязательных полей
    и одного необязательного поля на странице с информацией
    для доставки купленного товара покупателю. Позитивный тест'''

    plop = prepare_order_place_test
    print()
    plop.send_place_order()
    print("The order form is filled out correctly. The test fill order form is GOOD.")


def test_fill_order_form_without_necessary_param(start_finish, prepare_order_place_test):
    '''Тест проверяет корректность заполнения всех, КРОМЕ ОДНОГО, обязательных полей
    и одного необязательного поля на странице с информацией
    для доставки купленного товара покупателю. Негативный тест'''

    plop = prepare_order_place_test
    print()
    try:
        plop.send_place_order_without_necessary_street_name()
        print("The necessary field 'STREET' isn't filled out. The negative test fill order form is BAD.\n")
    except AssertionError:
        print("The necessary field 'STREET' isn't filled out. The negative test fill order form is GOOD.\n")
        plop.input_street_name_field()
        plop.click_resume_button()
        plop.check_url(plop.URL_CONTACTS)
        print("Now the necessary field 'STREET' is filled out. The test fill order form is GOOD.\n")


def test_fill_order_form_without_optional_param(start_finish, prepare_order_place_test):
    '''Тест проверяет корректность заполнения ТОЛЬКО всех обязательных полей
    на странице с информацией для доставки купленного товара покупателю. Позитивный тест'''

    plop = prepare_order_place_test
    print()
    plop.send_place_order_without_optional_floor_number()
    print("The order form is filled out correctly. The test fill order form is GOOD.")
