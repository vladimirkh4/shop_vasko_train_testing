import random
import time

import pytest
from selenium import webdriver

from pages.ac_page import ACPage
from pages.cart_page import CartPage
from pages.main_page import MainPage
from pages.tv_page import TVPage


@pytest.fixture()
def prepare_cart_test():
    '''Фикстура до прохождения теста - запускает браузер, открывает главную страницу,
    проводит авторизацию на сайте, открывает страницу категории "Телевизоры",
    инициализирует экземпляр класса TVPage и инициализирует экземпляр класса CartPage;
    после прохождения теста - удаляет все выбранные товары из корзины,
    закрывает браузер'''

    driver = webdriver.Chrome()

    mp = MainPage(driver)
    mp.start_driver(mp.URL)

    mp.open_personal_account()
    mp.back_driver()

    mp.select_category("Телевизоры")
    print()

    tvp = TVPage(driver)
    cp = CartPage(driver)

    yield mp, tvp, cp

    print()
    cp.clear_cart()
    time.sleep(1)
    mp.quit_driver()


def test_tv_in_cart(start_finish, prepare_cart_test):
    '''Тест проверяет корректность добавления телевизора в корзину покупок,
    случайно выбранного со страницы категории "Телевизоры",
    отфильтрованной по заданному бренду и заданному размеру диагонали.
    Тест также проверяет соответствие всех основных характеристик телевизора,
    находящегося в корзине покупок, характеристикам фактически выбранного телевизора
    на сайте интернет-магазина'''

    mp, tvp, cp = prepare_cart_test
    mp.come_to_cart()

    brand = "LG"
    brand_filter = "Производитель"
    diagonal = "43 inches"
    diagonal_filter = "Диагональ"

    tv_article, tv_name, tv_price = tvp.add_to_cart_random_tv(brand, brand_filter, diagonal, diagonal_filter)
    time.sleep(0.1)

    mp.come_to_cart()

    user_name = cp.get_user_name()
    number_goods_in_account = cp.get_number_product_in_cart()
    goods_names_set_in_cart = cp.get_product_names_set_in_cart()
    goods_prices_set_in_cart = cp.get_product_prices_set_in_cart()
    goods_delivery_prices_list = cp.get_product_delivery_prices_list()
    total_goods_sum = cp.get_total_products_sum()
    total_delivery_sum = cp.get_total_delivery_sum()
    total_order_sum = cp.get_total_order_sum()

    print()
    cp.check_user_name("Артур", user_name)
    cp.check_quantity_goods_in_cart(1, len(goods_names_set_in_cart), number_goods_in_account)
    cp.check_goods_names({tv_name}, goods_names_set_in_cart)
    cp.check_goods_prices({tv_price}, goods_prices_set_in_cart)
    cp.check_total_goods_sum(sum(goods_prices_set_in_cart), total_goods_sum)
    cp.check_total_delivery_sum(sum(goods_delivery_prices_list), total_delivery_sum)
    cp.check_total_order_sum(total_goods_sum, total_delivery_sum, total_order_sum)
    print()

    cp.place_order()
    mp.back_driver()


def test_tv_and_ac_in_cart(start_finish, prepare_cart_test):
    '''Тест проверяет корректность добавления двух товаров в корзину покупок:
    телевизора, случайно выбранного со страницы категории "Телевизоры",
    отфильтрованной по заданному бренду и заданному размеру диагонали;
    кондиционера, случайно выбранного со страницы категории "Кондиционеры",
    отфильтрованной по заданному бренду и заданному заводу-изготовителю.
    Тест также проверяет соответствие всех основных характеристик товаров,
    находящихся в корзине покупок, характеристикам фактически выбранных товаров
    на сайте интернет-магазина'''

    mp, tvp, cp = prepare_cart_test
    mp.come_to_cart()

    brand = "LG"
    brand_filter = "Производитель"
    diagonal = "43 inches"
    diagonal_filter = "Диагональ"
    tv_article, tv_name, tv_price = tvp.add_to_cart_random_tv(brand, brand_filter, diagonal, diagonal_filter)
    print()

    mp.select_base_category_group("Климатическая техника")
    acp = ACPage(mp.driver)
    acp.select_ac_category()
    print()

    brand = "Ballu"
    brand_filter = "Производитель"
    plant = "Midea"
    plant_filter = "Завод-изготовитель"
    ac_article, ac_name, ac_price = acp.add_to_cart_random_ac(brand, brand_filter, plant, plant_filter)
    time.sleep(0.1)

    mp.come_to_cart()

    user_name = cp.get_user_name()
    number_goods_in_account = cp.get_number_product_in_cart()
    goods_names_set_in_cart = cp.get_product_names_set_in_cart()
    goods_prices_set_in_cart = cp.get_product_prices_set_in_cart()
    goods_delivery_prices_list = cp.get_product_delivery_prices_list()
    total_goods_sum = cp.get_total_products_sum()
    total_delivery_sum = cp.get_total_delivery_sum()
    total_order_sum = cp.get_total_order_sum()

    print()
    cp.check_user_name("Артур", user_name)
    cp.check_quantity_goods_in_cart(2, len(goods_names_set_in_cart), number_goods_in_account)
    cp.check_goods_names({tv_name, ac_name}, goods_names_set_in_cart)
    cp.check_goods_prices({tv_price, ac_price}, goods_prices_set_in_cart)
    cp.check_total_goods_sum(sum(goods_prices_set_in_cart), total_goods_sum)
    cp.check_total_delivery_sum(sum(goods_delivery_prices_list), total_delivery_sum)
    cp.check_total_order_sum(total_goods_sum, total_delivery_sum, total_order_sum)
    print()

    cp.place_order()
    mp.back_driver()


def test_increase_decrease_buttons(start_finish, prepare_cart_test):
    '''Тест проверяет корректность увеличения и уменьшения количества
    экземпляров выбранного товара, находящегося в корзине, при помощи кнопок'''

    mp, tvp, cp = prepare_cart_test

    brand = "LG"
    brand_filter = "Производитель"
    diagonal = "43 inches"
    diagonal_filter = "Диагональ"

    tvp.add_to_cart_random_tv(brand, brand_filter, diagonal, diagonal_filter)
    time.sleep(0.1)

    mp.come_to_cart()

    total_goods_sum_before_increase = cp.get_total_products_sum()
    total_delivery_sum_before_increase = cp.get_total_delivery_sum()
    counter_before_increase = cp.get_product_quantity_field_value()

    assert counter_before_increase == 1
    print(f"\nThe counter of product before increase equal {counter_before_increase}. The test is GOOD.")

    n_click = random.randint(1, 5)
    for _ in range(n_click):
        cp.click_product_increase_button()
        time.sleep(2)

    total_goods_sum_after_increase = cp.get_total_products_sum()
    total_delivery_sum_after_increase = cp.get_total_delivery_sum()
    counter_after_increase = cp.get_product_quantity_field_value()

    assert total_goods_sum_after_increase == total_goods_sum_before_increase * (n_click + 1)
    print(
        f"\nThe total sum of goods after increase {total_goods_sum_after_increase}₽ is calculated correctly. The test is GOOD.")
    assert total_delivery_sum_after_increase > total_delivery_sum_before_increase
    print("The total delivery sum of goods is increased. The test is GOOD.")
    assert counter_after_increase == counter_before_increase + n_click
    print(f"The sign of the counter product after increase {counter_after_increase} is correct. The test is GOOD.")
    print("The 'increase' button is working correctly. The test is GOOD.\n")

    for _ in range(n_click):
        cp.click_product_decrease_button()
        time.sleep(2)

    total_goods_sum_after_decrease = cp.get_total_products_sum()
    total_delivery_sum_after_decrease = cp.get_total_delivery_sum()
    counter_after_decrease = cp.get_product_quantity_field_value()

    assert total_goods_sum_after_decrease == total_goods_sum_before_increase
    print(
        f"\nThe total sum of goods after decrease returned to its original value: {total_goods_sum_after_decrease}₽. The test is GOOD.")
    assert total_delivery_sum_after_decrease == total_delivery_sum_before_increase
    print(
        f"The total delivery sum of goods after decrease returned to its original value: {total_delivery_sum_after_decrease}₽. The test is GOOD.")
    assert counter_after_decrease == counter_before_increase
    print(f"The sign of the counter product after decrease {counter_after_increase} is correct. The test is GOOD.")
    print("The 'decrease' button is working correctly. The test is GOOD.\n")


def test_increase_decrease_field(start_finish, prepare_cart_test):
    '''Тест проверяет корректность увеличения и уменьшения количества
    экземпляров выбранного товара, находящегося в корзине,
    при помощи заполнения специального поля'''

    mp, tvp, cp = prepare_cart_test

    brand = "LG"
    brand_filter = "Производитель"
    diagonal = "43 inches"
    diagonal_filter = "Диагональ"

    tvp.add_to_cart_random_tv(brand, brand_filter, diagonal, diagonal_filter)
    time.sleep(0.1)

    mp.come_to_cart()

    total_goods_sum_before_increase = cp.get_total_products_sum()
    total_delivery_sum_before_increase = cp.get_total_delivery_sum()
    counter_before_increase = cp.get_product_quantity_field_value()

    assert counter_before_increase == 1
    print(f"\nThe counter of product before increase equal {counter_before_increase}. The test is GOOD.")

    n_increase = random.randint(1, 10)
    cp.input_product_quantity_field(n_increase)
    time.sleep(2)

    total_goods_sum_after_increase = cp.get_total_products_sum()
    total_delivery_sum_after_increase = cp.get_total_delivery_sum()
    counter_after_increase = cp.get_product_quantity_field_value()

    assert total_goods_sum_after_increase == total_goods_sum_before_increase * n_increase
    print(
        f"\nThe total sum of goods after increase {total_goods_sum_after_increase}₽ is calculated correctly. The test is GOOD.")
    assert total_delivery_sum_after_increase > total_delivery_sum_before_increase
    print("The total delivery sum of goods is increased. The test is GOOD.")
    assert counter_after_increase == n_increase
    print(f"The sign of the counter product after increase {counter_after_increase} is correct. The test is GOOD.")
    print("The 'input quantity' field is working correctly. The test is GOOD.\n")

    cp.input_product_quantity_field(1)
    time.sleep(2)

    total_goods_sum_after_decrease = cp.get_total_products_sum()
    total_delivery_sum_after_decrease = cp.get_total_delivery_sum()
    counter_after_decrease = cp.get_product_quantity_field_value()

    assert total_goods_sum_after_decrease == total_goods_sum_before_increase
    print(
        f"\nThe total sum of goods after decrease returned to its original value: {total_goods_sum_after_decrease}₽. The test is GOOD.")
    assert total_delivery_sum_after_decrease == total_delivery_sum_before_increase
    print(
        f"The total delivery sum of goods after decrease returned to its original value: {total_delivery_sum_after_decrease}₽. The test is GOOD.")
    assert counter_after_decrease == counter_before_increase
    print(f"The sign of the counter product after decrease {counter_after_increase} is correct. The test is GOOD.")
    print("The 'input quantity' field is working correctly. The test is GOOD.\n")
