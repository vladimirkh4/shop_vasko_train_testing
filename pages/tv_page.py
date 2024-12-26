from random import randint

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.product_page import ProductPage


class TVPage(ProductPage):
    '''Класс описыващий страницу товаров категории "Телевизоры"'''

    # Vars:
    CATEGORY_NAME = "Телевизоры"
    APPLY_FILTERS_LIST = [
        "Цена",
        "Производитель",
        "Диагональ",
        "Разрешение HD",
        "Цвет рамки",
    ]
    SIMPLE_FILTERS_LIST = [
        "WI-FI",
        "Smart TV",
    ]
    BRANDS_FOR_TEST = [
        "Hisense",
        "LG",
        "Philips",
        "Samsung",
        "Sony",
        "TCL",
        "XIAOMI"
    ]
    DIAGONAL_CODE_DICT = {
        "24 inches": "60930",
        "32 inches": "60934",
        "40 inches": "60936",
        "42 inches": "60937",
        "43 inches": "134294",
        "50 inches": "60940",
        "55 inches": "60942",
        "65 inches": "110601",
        "75 inches": "121394"
    }

    # Locators:
    BRAND_FILTER_MORE_BUTTON = (By.XPATH, "//aside//a[contains(@class, 'filter__more')]")

    FILTER_CHECKBOX_CHILD = "//aside//input[@value="  # first part locator
    PARENT = (By.XPATH, '..')
    FILTER_CHECKBOX = (By.TAG_NAME, 'span')
    FILTER_QUANTITY = (By.TAG_NAME, 'a')

    FILTERS_SELECTED_LIST = (By.XPATH, "//aside//div[contains(@class, 'filter__selected_title')]")
    APPLY_BUTTON = "(//aside//button[contains(text(), 'Применить')])["  # first part locator

    SELECTED_PRODUCTS_FEATURES_LIST = (By.XPATH, "//div[@class='catalog-list__props']")

    # Initialization class instance
    def __init__(self, driver):
        super().__init__(driver)
        self.brand_quantity_list = []
        self.diagonal_quantity_list = []

    # Get methods:
    def get_brand_filter_more_button(self):
        '''Метод доступа к кнопке, открывающей скрытые чекбоксы
        фильтра товаров по бренду'''

        try:
            return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                self.BRAND_FILTER_MORE_BUTTON))
        except TimeoutException:
            print("There are no hidden checkboxes")

    def get_checkbox_parent(self, value):
        '''Метод возвращающий родительский элемент чекбокса фильтра'''

        child = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, f"{self.FILTER_CHECKBOX_CHILD}'{value}']")))
        return child.find_element(*self.PARENT)

    def get_filter_checkbox(self, parent_element):
        '''Метод доступа к чекбоксу фильтра'''

        return parent_element.find_element(*self.FILTER_CHECKBOX)

    def get_filter_quantity(self, parent_element):
        '''Метод возвращающий количество товаров выбранных фильтром'''

        elem = parent_element.find_element(*self.FILTER_QUANTITY)
        filter_quantity = int(elem.text.split()[-1][1:-1])
        return filter_quantity

    def get_apply_button_num(self, filter_name):
        '''Метод возвращающий номер кнопки "Применить".
        Номер меняется динамически в зависмости от количества выбранных фильтров'''

        filter_selected_list = self.driver.find_elements(*self.FILTERS_SELECTED_LIST)
        filter_names_set = {filt.text[:-1] for filt in filter_selected_list}
        index = self.APPLY_FILTERS_LIST.index(filter_name)
        diff = len(filter_names_set & set(self.APPLY_FILTERS_LIST[:index]))
        return index - diff + 1

    def get_apply_button(self, apply_num):
        '''Метод достапа к кнопке "Применить" различных фильтров'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"{self.APPLY_BUTTON}{apply_num}]")))

    def get_selected_products_features_list(self):
        '''Метод возвращающий список словарей с характеристиками тоаваров
        для всех товаров на странице'''

        return self.driver.find_elements(*self.SELECTED_PRODUCTS_FEATURES_LIST)

    def get_selected_product_diagonals_list(self):
        '''Метод возвращающий список со значениями характеристики "Диагональ"
        для всех товаров на странице'''

        product_dicts_list = []
        for products_feature in self.get_selected_products_features_list():
            dt = dict(feature.split(f' {chr(8211)} ') for feature in products_feature.text.split('; '))
            product_dicts_list.append(dt)
        diagonal_list = [dt["Диагональ"].split()[0] for dt in product_dicts_list]
        return diagonal_list

    # Click and input methods
    def click_brand_filter_more_button(self):
        '''Метод - нажатие кнопки открывающей скрытые чекбоксы
        фильтра товаров по бренду'''

        button = self.get_brand_filter_more_button()
        if button:
            button.click()
            print("Click brand filter more button")

    def click_filter_checkbox(self, parent_element):
        '''Метод - установка галочки в чекбокс фильтра'''

        self.get_filter_checkbox(parent_element).click()
        print("Click filter checkbox")

    def click_apply_button(self, apply_num):
        '''Метод - нажатие кнопки "Применить"'''

        self.get_apply_button(apply_num).click()
        print("Click apply button")

    # Action methods:
    def select_brand_filter(self, brand):
        '''Метод выбирает чекбокс фильтра по бренду телевизора'''

        parent_elem = self.get_checkbox_parent(brand)
        quantity = self.get_filter_quantity(parent_elem)
        print(f"Quantity products which selected filter - '{brand}':", quantity)
        self.brand_quantity_list.append(quantity)
        self.click_filter_checkbox(parent_elem)

    def select_diagonal_filter(self, diagonal):
        '''Метод выбирает чекбокс фильтра по диагонали телевизора'''

        parent_elem = self.get_checkbox_parent(self.DIAGONAL_CODE_DICT[diagonal])
        quantity = self.get_filter_quantity(parent_elem)
        print(f"Quantity products which selected filter - '{diagonal}':", quantity)
        self.diagonal_quantity_list.append(quantity)
        self.click_filter_checkbox(parent_elem)

    def apply_filter(self, filter_name):
        '''Метод выбирает и нажимает нужную кнопку "Применить"'''

        apply_button_num = self.get_apply_button_num(filter_name)
        self.click_apply_button(apply_button_num)

    def add_to_cart_random_tv(self, brand, brand_filter, diagonal, diagonal_filter):
        '''Метод добавляет в корзину, случайно выбранный товар, со страницы
        категории "Телевизоры", отфильтрованной по бренду телевизора и
        по диагонали телевизора, а также возвращает артикул телевизора,
        наименование телевизора и стоимость телевизора'''

        self.click_brand_filter_more_button()
        self.select_brand_filter(brand)
        self.apply_filter(brand_filter)

        self.select_diagonal_filter(diagonal)
        self.apply_filter(diagonal_filter)

        self.click_sort_price_button()
        self.click_sort_price_down()
        print()

        quantity_selected_products = self.get_quantity_product_at_webpage()
        product_num = randint(1, quantity_selected_products)
        print(f"The number product on the page: {product_num}")
        product_article = self.get_selected_product_article(product_num)
        print(f"The article of the selected product: {product_article}")
        product_name = self.get_selected_product_name(product_num)
        print(f"The name of the selected product: {product_name}")
        product_price = self.get_select_product_price(product_num)
        print(f"The price of the selected product: {product_price}₽")

        self.click_add_to_cart_button(product_article)

        return product_article, product_name, product_price
