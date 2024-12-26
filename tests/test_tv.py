import time

import pytest
from selenium import webdriver

from pages.main_page import MainPage
from pages.tv_page import TVPage


@pytest.fixture()
def prepare_test():
    '''Фикстура до прохождения теста - запускает браузер, открывает главную страницу,
    открывает страницу категории "Телевизоры",
    после прохождения теста - закрывает браузер'''

    driver = webdriver.Chrome()

    mp = MainPage(driver)
    mp.start_driver(mp.URL)
    mp.select_category("Телевизоры")
    print()

    tvp = TVPage(driver)
    print("Quantity products without filters:", tvp.get_quantity_found_products())

    yield mp, tvp

    time.sleep(5)
    mp.quit_driver()


@pytest.fixture()
def prepare_filter():
    '''Фикстура до прохождения теста - запускает браузер, открывает главную страницу,
    открывает страницу категории "Телевизоры", отфильтровывает телевизоры
    по двум заданным параметрам,
    после прохождения теста - закрывает браузер'''

    driver = webdriver.Chrome()

    mp = MainPage(driver)
    mp.start_driver(mp.URL)
    mp.select_category("Телевизоры")
    print()

    tvp = TVPage(driver)
    print("Quantity products without filters:", tvp.get_quantity_found_products())

    brand = "Hisense"
    filter_type_1 = "Производитель"
    tvp.click_brand_filter_more_button()
    tvp.select_brand_filter(brand)
    tvp.apply_filter(filter_type_1)

    diagonal = "43 inches"
    filter_type_2 = "Диагональ"
    tvp.select_diagonal_filter(diagonal)
    tvp.apply_filter(filter_type_2)

    yield mp, tvp

    mp.quit_driver()


@pytest.mark.tv_brand
# @pytest.mark.parametrize('brand', [input(), input(), "TCL"])
def test_brand_filter(start_finish, prepare_test):
    '''Тест проверяет корректность работы фильтра телевизоров по одному бренду.
    Тест отмечен маркировкой "tv_brand", что позволяет запускать его в группе тестов,
    помеченных такой маркировкой'''

    mp, tvp = prepare_test
    tvp.brand_quantity_list.clear()

    brand = "Hisense"
    negative_brand = "BBK"
    filter_type = "Производитель"

    tvp.click_brand_filter_more_button()
    tvp.select_brand_filter(brand)
    tvp.apply_filter(filter_type)

    quantity_selected_products = tvp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_products)
    tvp.check_sum_selected_products(quantity_selected_products, tvp.brand_quantity_list)

    selected_product_names_list = tvp.get_selected_product_names_list()
    tvp.check_brand_in_product_name(brand, selected_product_names_list, negative_brand)


@pytest.mark.tv_brand
# @pytest.mark.parametrize("brand_indexes", [(0, 1, 2), (3, 4, 5)])
def test_several_brand_filter(start_finish, prepare_test):
    '''Тест проверяет корректность работы фильтра телевизоров по нескольким брендам.
    Тест отмечен маркировкой "tv_brand", что позволяет запускать его в группе тестов,
    помеченных такой маркировкой'''

    mp, tvp = prepare_test
    tvp.brand_quantity_list.clear()

    brand_indexes = (0, 1, 2)
    negative_brand = "BBK"
    filter_type = "Производитель"

    tvp.click_brand_filter_more_button()
    for i in brand_indexes:
        tvp.select_brand_filter(tvp.BRANDS_FOR_TEST[i])
    tvp.apply_filter(filter_type)

    quantity_selected_products = tvp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_products)
    tvp.check_sum_selected_products(quantity_selected_products, tvp.brand_quantity_list)

    selected_product_names_list = tvp.get_selected_product_names_list()
    brand_list = [tvp.BRANDS_FOR_TEST[i] for i in brand_indexes]
    tvp.check_multy_brand_in_product_name(brand_list, selected_product_names_list, negative_brand)


@pytest.mark.tv_size
def test_diagonal_filter(start_finish, prepare_test):
    '''Тест проверяет корректность работы фильтра телевизоров
    по одному размеру диагонали.
    Тест отмечен маркировкой "tv_size", что позволяет запускать его в группе тестов,
    помеченных такой маркировкой'''

    mp, tvp = prepare_test
    tvp.diagonal_quantity_list.clear()

    diagonal = "55 inches"
    filter_type = "Диагональ"

    tvp.select_diagonal_filter(diagonal)
    tvp.apply_filter(filter_type)

    quantity_selected_products = tvp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_products)
    tvp.check_sum_selected_products(quantity_selected_products, tvp.diagonal_quantity_list)


@pytest.mark.tv_size
def test_several_diagonal_filter(start_finish, prepare_test):
    '''Тест проверяет корректность работы фильтра телевизоров
    по нескольким размерам диагонали.
    Тест отмечен маркировкой "tv_size", что позволяет запускать его в группе тестов,
    помеченных такой маркировкой'''

    mp, tvp = prepare_test
    tvp.diagonal_quantity_list.clear()

    diagonals = ["43 inches", "55 inches"]
    diagonal_negative = "32"
    filter_type = "Диагональ"

    for diagonal in diagonals:
        tvp.select_diagonal_filter(diagonal)
    tvp.apply_filter(filter_type)

    quantity_selected_products = tvp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_products)
    tvp.check_sum_selected_products(quantity_selected_products, tvp.diagonal_quantity_list)

    diagonal_signs = [diagonal.split()[0] for diagonal in diagonals]
    diagonals_from_selected_products = tvp.get_selected_product_diagonals_list()
    tvp.check_feature_in_selected_products(diagonal_signs,
                                           diagonals_from_selected_products,
                                           filter_type,
                                           diagonal_negative)


# @pytest.mark.parametrize("brand_indexes", [(0, 1), (3, 4)])
def test_several_brand_and_diagonal_filter(start_finish, prepare_test):
    '''Тест сначала проверяет корректность работы фильтра телевизоров
    по нескольким брендам.
    Затем проверяет корректность работы фильтра телевизоров
    по нескольким размерам диагонали'''

    mp, tvp = prepare_test
    tvp.brand_quantity_list.clear()
    tvp.diagonal_quantity_list.clear()

    brand_indexes = (0, 1)
    negative_brand = "BBK"
    diagonals = ["43 inches", "55 inches"]
    diagonal_negative = "32"
    feature_name = "Диагональ"
    filter_brand = tvp.APPLY_FILTERS_LIST[1]
    filter_diagonal = tvp.APPLY_FILTERS_LIST[2]

    tvp.click_brand_filter_more_button()
    for i in brand_indexes:
        tvp.select_brand_filter(tvp.BRANDS_FOR_TEST[i])
    tvp.apply_filter(filter_brand)

    quantity_selected_brand_products = tvp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_brand_products)
    tvp.check_sum_selected_products(quantity_selected_brand_products, tvp.brand_quantity_list)
    print()

    for diagonal in diagonals:
        tvp.select_diagonal_filter(diagonal)
    tvp.apply_filter(filter_diagonal)

    quantity_selected_diagonal_products = tvp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_diagonal_products)
    tvp.check_sum_selected_products(quantity_selected_diagonal_products, tvp.diagonal_quantity_list)

    selected_product_names_list = tvp.get_selected_product_names_list()
    brand_list = [tvp.BRANDS_FOR_TEST[i] for i in brand_indexes]
    tvp.check_multy_brand_in_product_name(brand_list,
                                          selected_product_names_list,
                                          negative_brand)

    diagonal_signs = [diagonal.split()[0] for diagonal in diagonals]
    diagonals_from_selected_products = tvp.get_selected_product_diagonals_list()
    tvp.check_feature_in_selected_products(diagonal_signs,
                                           diagonals_from_selected_products,
                                           feature_name,
                                           diagonal_negative)


def test_diagonal_and_brand_filter(start_finish, prepare_test):
    '''Тест сначала проверяет корректность работы фильтра телевизоров
    по одному размеру диагонали.
    Затем проверяет корректность работы фильтра телевизоров по одному бренду'''

    mp, tvp = prepare_test
    tvp.brand_quantity_list.clear()
    tvp.diagonal_quantity_list.clear()

    brand_indexes = (1,)
    negative_brand = "BBK"
    diagonals = ["55 inches"]
    diagonal_negative = "32"
    feature_name = "Диагональ"
    filter_brand = tvp.APPLY_FILTERS_LIST[1]
    filter_diagonal = tvp.APPLY_FILTERS_LIST[2]

    for diagonal in diagonals:
        tvp.select_diagonal_filter(diagonal)
    tvp.apply_filter(filter_diagonal)

    quantity_selected_diagonal_products = tvp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_diagonal_products)
    tvp.check_sum_selected_products(quantity_selected_diagonal_products, tvp.diagonal_quantity_list)

    tvp.click_brand_filter_more_button()
    for i in brand_indexes:
        tvp.select_brand_filter(tvp.BRANDS_FOR_TEST[i])
    tvp.apply_filter(filter_brand)

    quantity_selected_brand_products = tvp.get_quantity_found_products()
    print("Quantity selected products:", quantity_selected_brand_products)
    tvp.check_sum_selected_products(quantity_selected_brand_products, tvp.brand_quantity_list)
    print()

    selected_product_names_list = tvp.get_selected_product_names_list()
    brand_list = [tvp.BRANDS_FOR_TEST[i] for i in brand_indexes]
    tvp.check_multy_brand_in_product_name(brand_list,
                                          selected_product_names_list,
                                          negative_brand)

    diagonal_signs = [diagonal.split()[0] for diagonal in diagonals]
    diagonals_from_selected_products = tvp.get_selected_product_diagonals_list()
    tvp.check_feature_in_selected_products(diagonal_signs,
                                           diagonals_from_selected_products,
                                           feature_name,
                                           diagonal_negative)


def test_sort_price_without_filter(start_finish, prepare_test):
    '''Тест проверяет корректность работы сортировки телевизоров по цене
    на странице без применения фильтров'''

    mp, tvp = prepare_test

    tvp.sort_price_up()
    tvp.check_sort_price_up()
    print()
    tvp.sort_price_down()
    tvp.check_sort_price_down()


def test_sort_price_with_filters(start_finish, prepare_filter):
    '''Тест проверяет корректность работы сортировки телевизоров по цене
    на странице с применением фильтров'''

    mp, tvp = prepare_filter

    tvp.sort_price_up()
    tvp.check_sort_price_up()
    print()
    tvp.sort_price_down()
    tvp.check_sort_price_down()


def test_prise_slider_without_filters(start_finish, prepare_test):
    '''Тест проверяет корректность работы ползунка фильтра телевизоров по цене
    на странице без применения фильтров'''

    mp, tvp = prepare_test
    tvp.check_price_sliders()


def test_prise_slider_with_filters(start_finish, prepare_filter):
    '''Тест проверяет корректность работы ползунка фильтра телевизоров по цене
    на странице с применением фильтров'''

    mp, tvp = prepare_filter
    tvp.check_price_sliders()


def test_input_prise_fields(start_finish, prepare_test):
    '''Тест проверяет корректность заполнения поля фильтра телевизоров по цене'''

    mp, tvp = prepare_test

    min_price = 30000
    max_price = 60000
    tvp.check_input_price_fields(min_price, max_price)


def test_price_filter_apply(start_finish, prepare_test):
    '''Тест проверяет корректность работы фильтра телевизоров по цене
    на верхней и нижней границах ценового диапазона
    на странице с применением фильтров'''

    mp, tvp = prepare_test

    brand = "Hisense"
    filter_type_1 = "Производитель"
    tvp.click_brand_filter_more_button()
    tvp.select_brand_filter(brand)
    tvp.apply_filter(filter_type_1)
    print()

    tvp.check_price_filter(tvp.apply_filter)
