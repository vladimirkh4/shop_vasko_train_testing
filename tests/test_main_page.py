import time

import pytest
from selenium import webdriver

from pages.main_page import MainPage


@pytest.fixture()
def open_main_page():
    '''Фикстура до прохождения теста - запускает браузер, открывает главную страницу,
    после прохождения теста - закрывает браузер'''

    driver = webdriver.Chrome()

    mp = MainPage(driver)
    mp.start_driver(mp.URL)

    yield mp

    mp.quit_driver()


def test_select_several_categories(start_finish, open_main_page):
    '''Тест проверяет корректность открытия страниц всех категорий товаров или услуг,
    находящихся на главной странице, поочередно'''

    mp = open_main_page
    mp.several_category_select()


def test_select_all_base_category_group(start_finish, open_main_page):
    '''Тест проверяет корректность открытия страниц
    всех базовых категорий товаров, поочередно'''

    mp = open_main_page
    mp.select_all_base_category_group()


def test_search_products_by_articles(start_finish, open_main_page):
    '''Тест проверяет корректность выбора нескольких товаров по артикулам, поочередно'''

    mp = open_main_page
    mp.select_several_product_by_article()


def test_open_personal_account(start_finish, open_main_page):
    '''Тест проверяет корректность открытия страницы личного кабинета пользователя,
    если пользователь не зарегистрирован. Также тест проверяет корректность
    авторизации пользователя на сайте интернет-магазина'''

    mp = open_main_page
    mp.open_personal_account()
    time.sleep(2)


def test_open_personal_account_double(start_finish, open_main_page):
    '''Тест проверяет корректность открытия страницы личного кабинета пользователя
    два раза: до регистрации пользователя и после регистрации пользователя'''

    mp = open_main_page
    mp.open_personal_account()
    mp.back_driver()
    time.sleep(2)
    mp.open_personal_account()
    time.sleep(2)
