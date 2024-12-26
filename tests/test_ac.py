import time

import pytest
from selenium import webdriver

from pages.ac_page import ACPage
from pages.main_page import MainPage


@pytest.fixture()
def prepare_test():
    '''Фикстура до прохождения теста - запускает браузер, открывает главную страницу,
    открывает страницу категории "Кондиционеры",
    после прохождения теста - закрывает браузер'''

    driver = webdriver.Chrome()

    mp = MainPage(driver)
    mp.start_driver(mp.URL)
    mp.select_category("Климатическая техника")

    acp = ACPage(driver)
    acp.select_ac_category()
    print()
    print("Quantity products without filters:", acp.get_quantity_found_products())

    yield mp, acp

    time.sleep(1)
    mp.quit_driver()


@pytest.fixture()
def prepare_filter():
    '''Фикстура до прохождения теста - запускает браузер, открывает главную страницу,
    открывает страницу категории "Кондиционеры", отфильтровывает кондиционеры
    по двум заданным параметрам,
    после прохождения теста - закрывает браузер'''

    driver = webdriver.Chrome()

    mp = MainPage(driver)
    mp.start_driver(mp.URL)
    mp.select_category("Климатическая техника")

    acp = ACPage(driver)
    acp.select_ac_category()
    print()
    print("Quantity products without filters:", acp.get_quantity_found_products())

    brands = ["Ballu", "Electrolux"]
    brand_filter = "Производитель"
    plant_names = ["Midea", "Hisense"]
    plant_filter = "Завод-изготовитель"

    acp.more_filter(brand_filter)
    for brand in brands:
        acp.select_brand_filter(brand)
    acp.apply_filter(brand_filter)
    print()

    acp.more_filter(plant_filter)
    for plant_name in plant_names:
        acp.select_plant_name_filter(plant_name)
    acp.apply_filter(plant_filter)
    print()

    yield mp, acp

    mp.quit_driver()


@pytest.mark.parametrize('brand', ["Ballu", "Electrolux", "Hisense"])
def test_brand_filter(start_finish, prepare_test, brand):
    '''Тест проверяет корректность работы фильтра кондиционеров по одному бренду.
    В тесте предусмотрена передача названий брендов в виде списка параметров,
    т.е. можно поочередно протестировать несколько брендов'''

    mp, acp = prepare_test
    acp.brand_quantity_list.clear()

    # brand = "Ballu"
    negative_brand = "AUX"
    filter_type = "Производитель"

    acp.more_filter(filter_type)
    acp.select_brand_filter(brand)
    acp.apply_filter(filter_type)

    quantity_selected_products = acp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_products)
    acp.check_sum_selected_products(quantity_selected_products, acp.brand_quantity_list)

    selected_product_names_list = acp.get_selected_product_names_list()
    acp.check_brand_in_product_name(brand, selected_product_names_list, negative_brand)


@pytest.mark.parametrize("brand_indexes", [(0, 1, 2), (3, 4, 5)])
def test_several_brand_filter(start_finish, prepare_test, brand_indexes):
    '''Тест проверяет корректность работы фильтра кондиционеров по нескольким брендам.
    В тесте предусмотрена передача брендов в виде списка кортежей параметров,
    т.е. можно поочередно протестировать несколько комплектов брендов'''

    mp, acp = prepare_test
    acp.brand_quantity_list.clear()

    # brand_indexes = (0, 1, 2)
    negative_brand = "AUX"
    filter_type = "Производитель"

    acp.more_filter(filter_type)
    for i in brand_indexes:
        acp.select_brand_filter(acp.BRANDS_FOR_TEST[i])
    acp.apply_filter(filter_type)

    quantity_selected_products = acp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_products)
    acp.check_sum_selected_products(quantity_selected_products, acp.brand_quantity_list)

    selected_product_names_list = acp.get_selected_product_names_list()
    brand_list = [acp.BRANDS_FOR_TEST[i] for i in brand_indexes]
    acp.check_multy_brand_in_product_name(brand_list, selected_product_names_list, negative_brand)


def test_plant_name_filter(start_finish, prepare_test):
    '''Тест проверяет корректность работы фильтра кондиционеров по
    одному наименованию завода-изготовителя'''

    mp, acp = prepare_test
    acp.plant_quantity_list.clear()

    plant_names = ["Midea", "Hisense"]
    plant_name_negative = ["AUX"]
    filter_type = "Завод-изготовитель"

    acp.more_filter(filter_type)
    for plant_name in plant_names:
        acp.select_plant_name_filter(plant_name)
    acp.apply_filter(filter_type)

    quantity_selected_products = acp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_products)
    acp.check_sum_selected_products(quantity_selected_products, acp.plant_quantity_list)

    plants_from_selected_products = acp.get_selected_product_plants_list()
    acp.check_feature_in_selected_products(plant_names,
                                           plants_from_selected_products,
                                           filter_type,
                                           plant_name_negative)


def test_brands_and_plant_names_filter(start_finish, prepare_test):
    '''Тест проверяет корректность работы фильтра кондиционеров по
    нескольким наименованиям завода-изготовителя'''

    mp, acp = prepare_test
    acp.brand_quantity_list.clear()
    acp.plant_quantity_list.clear()

    brands = ["Ballu", "Electrolux"]
    negative_brand = "Centek"
    brand_filter = "Производитель"

    plant_names = ["Midea", "Hisense"]
    plant_name_negative = ["AUX"]
    plant_filter = "Завод-изготовитель"

    acp.more_filter(brand_filter)
    for brand in brands:
        acp.select_brand_filter(brand)
    acp.apply_filter(brand_filter)

    quantity_selected_products = acp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_products)
    acp.check_sum_selected_products(quantity_selected_products, acp.brand_quantity_list)
    print()

    acp.more_filter(plant_filter)
    for plant_name in plant_names:
        acp.select_plant_name_filter(plant_name)
    acp.apply_filter(plant_filter)

    quantity_selected_products = acp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_products)
    acp.check_sum_selected_products(quantity_selected_products, acp.plant_quantity_list)
    print()

    selected_product_names_list = acp.get_selected_product_names_list()
    acp.check_multy_brand_in_product_name(brands, selected_product_names_list, negative_brand)

    plants_from_selected_products = acp.get_selected_product_plants_list()
    acp.check_feature_in_selected_products(plant_names,
                                           plants_from_selected_products,
                                           plant_filter,
                                           plant_name_negative)


def test_sort_price_without_filter(start_finish, prepare_test):
    '''Тест проверяет корректность работы сортировки кондиционеров по цене
    на странице без применения фильтров'''

    mp, acp = prepare_test

    acp.sort_price_up()
    acp.check_sort_price_up()
    print()
    acp.sort_price_down()
    acp.check_sort_price_down()


def test_sort_price_with_filters(start_finish, prepare_filter):
    '''Тест проверяет корректность работы сортировки кондиционеров по цене
    на странице с применением фильтров'''

    mp, acp = prepare_filter

    acp.sort_price_up()
    acp.check_sort_price_up()
    print()
    acp.sort_price_down()
    acp.check_sort_price_down()


def test_prise_slider_without_filters(start_finish, prepare_test):
    '''Тест проверяет корректность работы ползунка фильтра кондиционеров по цене
    на странице без применения фильтров'''

    mp, acp = prepare_test
    acp.check_price_sliders()


def test_prise_slider_with_filters(start_finish, prepare_filter):
    '''Тест проверяет корректность работы ползунка фильтра кондиционеров по цене
    на странице с применением фильтров'''

    mp, acp = prepare_filter
    acp.check_price_sliders()


def test_input_prise_fields(start_finish, prepare_test):
    '''Тест проверяет корректность заполнения поля фильтра кондиционеров по цене'''

    mp, acp = prepare_test

    min_price = 30000
    max_price = 50000
    acp.check_input_price_fields(min_price, max_price)


def test_price_filter_apply(start_finish, prepare_filter):
    '''Тест проверяет корректность работы фильтра кондиционеров по цене
    на верхней и нижней границах ценового диапазона
    на странице с применением фильтров'''

    mp, acp = prepare_filter
    acp.check_price_filter(acp.apply_filter)
