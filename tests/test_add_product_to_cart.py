import pytest
import time

from selenium import webdriver
from pages.ac_page import ACPage
from pages.tv_page import TVPage
from pages.main_page import MainPage
from tests.test_tv import prepare_test as tv_prepare_test
from tests.test_ac import prepare_test as ac_prepare_test


@pytest.fixture()
def prepare_double_test():
    '''Фикстура до прохождения теста - запускает браузер, открывает главную страницу,
    открывает страницу категории "Телевизоры", инициализирует экземпляр класса TVPage
    и инициализирует экземпляр класса ACPage
    после прохождения теста - закрывает браузер'''

    driver = webdriver.Chrome()

    mp = MainPage(driver)
    mp.start_driver(mp.URL)

    mp.select_category("Телевизоры")
    print()

    tvp = TVPage(driver)
    acp = ACPage(driver)

    yield mp, tvp, acp

    mp.quit_driver()


def test_add_tv_to_cart(start_finish, tv_prepare_test):
    '''Тест проверяет корректность добавления телевизора в корзину покупок,
    случайно выбранного со страницы категории "Телевизоры",
    отфильтрованной по заданному бренду и заданному размеру диагонали'''

    mp, tvp = tv_prepare_test
    mp.come_to_cart()

    brand = "LG"
    brand_filter = "Производитель"
    diagonal = "43 inches"
    diagonal_filter = "Диагональ"

    tv_article, tv_name, tv_price = tvp.add_to_cart_random_tv(brand, brand_filter, diagonal, diagonal_filter)
    time.sleep(0.5)

    quantity_product_in_cart, total_price_in_cart = mp.come_to_cart()
    mp.check_quantity_product_in_cart(1, quantity_product_in_cart)
    mp.check_price_product_in_cart(tv_price, total_price_in_cart)


def test_add_ac_to_cart(start_finish, ac_prepare_test):
    '''Тест проверяет корректность добавления кондиционера в корзину покупок,
    случайно выбранного со страницы категории "Кондиционеры",
    отфильтрованной по заданному бренду и заданному заводу-изготовителю'''

    mp, acp = ac_prepare_test
    mp.come_to_cart()

    brand = "Ballu"
    brand_filter = "Производитель"
    plant = "Midea"
    plant_filter = "Завод-изготовитель"
    ac_article, ac_name, ac_price = acp.add_to_cart_random_ac(brand, brand_filter, plant, plant_filter)
    time.sleep(0.5)

    quantity_product_in_cart, total_price_in_cart = mp.come_to_cart()
    mp.check_quantity_product_in_cart(1, quantity_product_in_cart)
    mp.check_price_product_in_cart(ac_price, total_price_in_cart)


def test_add_tv_and_ac_to_cart(start_finish, prepare_double_test):
    '''Тест проверяет корректность добавления двух товаров в корзину покупок:
    телевизора, случайно выбранного со страницы категории "Телевизоры",
    отфильтрованной по заданному бренду и заданному размеру диагонали;
    кондиционера, случайно выбранного со страницы категории "Кондиционеры",
    отфильтрованной по заданному бренду и заданному заводу-изготовителю'''

    mp, tvp, acp = prepare_double_test
    mp.come_to_cart()

    brand = "LG"
    brand_filter = "Производитель"
    diagonal = "43 inches"
    diagonal_filter = "Диагональ"
    tv_article, tv_name, tv_price = tvp.add_to_cart_random_tv(brand, brand_filter, diagonal, diagonal_filter)
    print()

    mp.select_base_category_group("Климатическая техника")
    acp.select_ac_category()
    print()

    brand = "Ballu"
    brand_filter = "Производитель"
    plant = "Midea"
    plant_filter = "Завод-изготовитель"
    ac_article, ac_name, ac_price = acp.add_to_cart_random_ac(brand, brand_filter, plant, plant_filter)
    time.sleep(0.5)

    quantity_product_in_cart, total_price_in_cart = mp.come_to_cart()
    mp.check_quantity_product_in_cart(2, quantity_product_in_cart)
    mp.check_price_product_in_cart(tv_price + ac_price, total_price_in_cart)
