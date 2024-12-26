from random import randint

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.product_page import ProductPage


class ACPage(ProductPage):
    '''Класс описыващий страницу товаров категории "Кондиционеры"'''

    # Vars:
    URL_AC_PAGE = "https://vasko.ru/to_catalog/action_categDesc/id_371/"
    CATEGORY_NAME = "Кондиционеры"
    APPLY_FILTERS_LIST = [
        "Цена",
        "Производитель",
        "Площадь помещения",
        "Фильтр",
        "Дополнительные функции",
        "Завод-изготовитель"
    ]
    MORE_FILTERS_LIST = [
        "Производитель",
        "Площадь помещения",
        "Завод-изготовитель"
    ]
    SIMPLE_FILTERS_LIST = [
        "Инверторное управление мощностью",
        "Мощность кондиционера, BTU",
        "Плазменный фильтр"
    ]
    BRANDS_FOR_TEST = [
        "Ballu",
        "Centek",
        "Dantex",
        "Electrolux",
        "Hisense",
        "RoyalClima",
        "Zanussi"
    ]
    PLANT_CODE_DICT = {
        "Gree": "138296",
        "Midea": "138298",
        "Hisense": "138297",
        "AUX": "138299",
        "TCL": "138301",
        "Changhong": "138302",
        "MBO": "138307",
        "Haier": "138300",
        "Китай (неизвестен)": "138309",
    }

    # Locators:
    CATEGORY_SELECT = "//h2[@class='catalog-sections__title']/a[contains(text(), "  # first part locator
    CATEGORY_HEADER = (By.TAG_NAME, "h1")
    FILTER_MORE_BUTTON = "(//aside//a[contains(@class, 'filter__more')])["  # first part locator

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
        self.plant_quantity_list = []

    # Get methods:
    def get_filter_more_button(self, more_num):
        '''Метод доступа к кнопке открывающей скрытые чекбоксы различных фильтров'''

        try:
            return WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(
                (By.XPATH, f"{self.FILTER_MORE_BUTTON}{more_num}]")))
        except TimeoutException:
            print("There are no hidden checkboxes")

    def get_ac_category_select(self):
        '''Метод доступа к кнопке открытия категории "Кондиционеры"'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"{self.CATEGORY_SELECT}'{self.CATEGORY_NAME}')]")))

    def get_category_header(self):
        '''Метод возвращает заголовок категории товаров'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.CATEGORY_HEADER))

    def get_apply_button(self, apply_num):
        '''Метод достапа к кнопке "Применить" различных фильтров'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"{self.APPLY_BUTTON}{apply_num}]")))

    def get_apply_button_num(self, filter_name):
        '''Метод возвращающий номер кнопки "Применить".
        Номер меняется динамически в зависмости от количества выбранных фильтров'''

        filter_selected_list = self.driver.find_elements(*self.FILTERS_SELECTED_LIST)
        filter_names_set = {filt.text[:-1] for filt in filter_selected_list}
        index = self.APPLY_FILTERS_LIST.index(filter_name)
        diff = len(filter_names_set & set(self.APPLY_FILTERS_LIST[:index]))
        return index - diff + 1

    def get_more_filter_button_num(self, filter_name):
        '''Метод возвращающий номер кнопки открывающей скрытые чебоксы.
        Номер меняется динамически в зависмости от количества выбранных фильтров'''

        filter_selected_list = self.driver.find_elements(*self.FILTERS_SELECTED_LIST)
        filter_names_set = {filt.text[:-1] for filt in filter_selected_list}
        index = self.MORE_FILTERS_LIST.index(filter_name)
        diff = len(filter_names_set & set(self.MORE_FILTERS_LIST[:index]))
        return index - diff + 1

    def get_checkbox_parent(self, value):
        '''Метод возвращающий родительский элемент чекбокса фильтра'''

        child = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, f"{self.FILTER_CHECKBOX_CHILD}'{value}']")))
        return child.find_element(*self.PARENT)

    def get_filter_quantity(self, parent_element):
        '''Метод возвращающий количество товаров выбранных фильтром'''

        elem = parent_element.find_element(*self.FILTER_QUANTITY)
        filter_quantity = int(elem.text.split()[-1][1:-1])
        return filter_quantity

    def get_filter_checkbox(self, parent_element):
        '''Метод доступа к чекбоксу фильтра'''

        return parent_element.find_element(*self.FILTER_CHECKBOX)

    def get_selected_products_features_list(self):
        '''Метод возвращающий список словарей с характеристиками тоаваров
        для всех товаров на странице'''

        return self.driver.find_elements(*self.SELECTED_PRODUCTS_FEATURES_LIST)

    def get_selected_product_plants_list(self):
        '''Метод возвращающий список со значениями характеристики "Завод-изготовитель"
        для всех товаров на странице'''

        product_dicts_list = []
        for products_feature in self.get_selected_products_features_list():
            dt = dict(feature.split(f' {chr(8211)} ') for feature in products_feature.text.split('; '))
            product_dicts_list.append(dt)
        plant_list = [dt["Завод-изготовитель"] for dt in product_dicts_list]
        return plant_list

    # Click and input methods
    def click_ac_category_select(self):
        '''Метод - нажатие кнопки выбора категории "Кондиционеры"'''

        self.get_ac_category_select().click()
        print(f"Click category: '{self.CATEGORY_NAME}'")

    def click_filter_more_button(self, button_num):
        '''Метод - нажатие кнопки открывающей скрытые чекбоксы'''

        button = self.get_filter_more_button(button_num)
        if button:
            button.click()
            print("Click brand filter more button")

    def click_apply_button(self, apply_num):
        '''Метод - нажатие кнопки "Применить"'''

        self.get_apply_button(apply_num).click()
        print("Click apply button")

    def click_filter_checkbox(self, parent_element):
        '''Метод - установка галочки в чекбокс фильтра'''

        self.get_filter_checkbox(parent_element).click()
        print("Click filter checkbox")

    # Action methods
    def select_ac_category(self):
        '''Метод по выбору категории "Кондиционеры", с проверкой
        заголовка категории на странице выбранной категории и url-адреса'''

        self.click_ac_category_select()

        self.get_current_url()
        self.check_url(self.URL_AC_PAGE)

        header_control = self.get_category_header().text
        self.check_word(self.CATEGORY_NAME, header_control)

    def apply_filter(self, filter_name):
        '''Метод выбирает и нажимает нужную кнопку "Применить"'''

        apply_button_num = self.get_apply_button_num(filter_name)
        self.click_apply_button(apply_button_num)

    def more_filter(self, filter_name):
        '''Метод выбирает и нажимает нужную кнопку по открытию скрытых чекбоксов'''

        more_filter_button_num = self.get_more_filter_button_num(filter_name)
        self.click_filter_more_button(more_filter_button_num)

    def select_brand_filter(self, brand):
        '''Метод выбирает чекбокс фильтра по бренду кондиционера'''

        parent_elem = self.get_checkbox_parent(brand)
        quantity = self.get_filter_quantity(parent_elem)
        print(f"Quantity products which selected filter - '{brand}':", quantity)
        self.brand_quantity_list.append(quantity)
        self.click_filter_checkbox(parent_elem)

    def select_plant_name_filter(self, plant_name):
        '''Метод выбирает чекбокс фильтра по заводу-изготовителю кондиционера'''

        parent_elem = self.get_checkbox_parent(self.PLANT_CODE_DICT[plant_name])
        quantity = self.get_filter_quantity(parent_elem)
        print(f"Quantity products which selected filter plant name - '{plant_name}':", quantity)
        self.plant_quantity_list.append(quantity)
        self.click_filter_checkbox(parent_elem)

    def add_to_cart_random_ac(self, brand, brand_filter, plant, plant_filter):
        '''Метод добавляет в корзину, случайно выбранный товар, со страницы
        категории "Кондиционеры", отфильтрованной по бренду кондиционера и
        по заводу-изготовителю кондиционера, а также возвращает
        артикул кондиционера, наименование кондиционера и стоимость кондиционера'''

        self.more_filter(brand_filter)
        self.select_brand_filter(brand)
        self.apply_filter(brand_filter)

        self.more_filter(plant_filter)
        self.select_plant_name_filter(plant)
        self.apply_filter(plant_filter)

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
