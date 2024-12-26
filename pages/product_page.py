from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base.base_panel import BasePanel


class ProductPage(BasePanel):
    '''Класс описыващий методы, которые могут применяться
    на всех продуктовых страницах приложения.
    Является родительским классом для всех продуктовых страниц'''

    # Vars:
    CONTROL_SHIFT = 50

    # Locators:
    QUANTITY_FOUND_PRODUCTS = (By.XPATH, "//div[@class='catalog__header']/div/b")

    SELECTED_PRODUCTS_LIST = (By.XPATH, "//div[@class='catalog-list__row']")
    SELECTED_PRODUCT_PRICE = "(//div[@class='catalog-list__price'])["  # first part locator
    SELECTED_PRODUCT_NAME = (By.TAG_NAME, 'h2')
    SELECTED_PRODUCT_NAME_PART = "(//div[@class='catalog-list__row']//h2)["  # first part locator
    SELECTED_PRODUCT_ARTICLE = "(//div[@class='catalog-list__vendor-code'])["  # first part locator
    SELECTED_FILTER_BUTTON_LIST = (By.XPATH, "//aside//div[contains(@class, 'filter__selected_title')]/a")
    SELECTED_FILTER_BUTTON = "(//aside//div[contains(@class, 'filter__selected_title')]/a)["  # first part locator

    SORT_PRICE_BUTTON = (By.XPATH, "//button[@class='catalog-sort__btn']")
    SORT_PRICE_DOWN = (By.XPATH, "//a[contains(@href, 'sort_price1')]")
    SORT_PRICE_UP = (By.XPATH, "//a[contains(@href, 'sort_price2')]")

    PRICE_BORDER_SIGNS = (By.XPATH, "//aside//input[contains(@class, 'irs-hidden-input')]")
    LEFT_PRICE_SLIDER = (By.XPATH, "//aside//span[contains(@class, 'irs-handle') and contains(@class, 'from')]")
    RIGHT_PRICE_SLIDER = (By.XPATH, "//aside//span[contains(@class, 'irs-handle') and contains(@class, 'to')]")
    LEFT_PRICE_FIELD = (By.XPATH, "//aside//input[@name='price_min']")
    RIGHT_PRICE_FIELD = (By.XPATH, "//aside//input[@name='price_max']")

    ADD_TO_CART_BUTTON = "//button[@id='js-BuyProductList"  # first part locator

    # Initialization class instance
    def __init__(self, driver):
        super().__init__(driver)
        self.actions = ActionChains(self.driver)

    # Get methods
    def get_quantity_found_products(self):
        '''Метод возвращающий количество найденных товаров'''

        quantity = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.QUANTITY_FOUND_PRODUCTS))
        return int(quantity.text)

    def get_selected_products_list(self):
        '''Метод возвращающий список элементов товаров на странице'''

        return self.driver.find_elements(*self.SELECTED_PRODUCTS_LIST)

    def get_quantity_product_at_webpage(self):
        '''Метод возвращающий количество товаров на странице'''

        return len(self.get_selected_products_list())

    def get_selected_product_names_list(self):
        '''Метод возвращающий список наименований всех товаров на странице'''

        products_list = self.get_selected_products_list()
        product_names_list = [product.find_element(
            *self.SELECTED_PRODUCT_NAME).text for product in products_list]
        return product_names_list

    def get_selected_product_article(self, num_product):
        '''Метод возвращающий артикул товара'''

        article_elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"{self.SELECTED_PRODUCT_ARTICLE}{num_product}]")))
        return article_elem.text.split(': ')[-1]

    def get_selected_product_name(self, num_product):
        '''Метод возвращающий наименование товара'''

        article_elem = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"{self.SELECTED_PRODUCT_NAME_PART}{num_product}]")))
        return article_elem.text

    def get_selected_filter_buttons_list(self):
        '''Метод возвращающий список элементов кнопок всех примененных фильтров'''

        return self.driver.find_elements(*self.SELECTED_FILTER_BUTTON_LIST)

    def get_quantity_filter_buttons(self):
        '''Метод возвращающий количество примененных фильтров'''

        return len(self.get_selected_filter_buttons_list())

    def get_selected_filter_button(self, num_button):
        '''Метод доступа к кнопке примененного фильтра'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"{self.SELECTED_FILTER_BUTTON}{num_button}]")))

    def get_sort_price_button(self):
        '''Метод доступа к кнопке открывающей меню сортировки'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.SORT_PRICE_BUTTON))

    def get_sort_price_down(self):
        '''Метод доступа к кнопке сортировки товара по цене по убыванию'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.SORT_PRICE_DOWN))

    def get_sort_price_up(self):
        '''Метод доступа к кнопке сортировки товара по цене по возрастанию'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.SORT_PRICE_UP))

    def get_select_product_price(self, num_product):
        '''Метод возвращающий цену товара'''

        elem_price = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, f"{self.SELECTED_PRODUCT_PRICE}{num_product}]")))
        price = int(elem_price.text.split(': ')[-1][:-1].replace(' ', ''))
        return price

    def get_border_price_signs(self):
        '''Метод возвращающий границы максимальной и минимальной цены
        для фильтра товаров по цене'''

        borders_elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.PRICE_BORDER_SIGNS))
        borders = borders_elem.get_attribute('value')
        price_min, price_max = map(int, borders.split(';'))
        return price_min, price_max

    def get_left_price_slider(self):
        '''Метод доступа к левому движку ползунка фильтра товаров по цене'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.LEFT_PRICE_SLIDER))

    def get_right_price_slider(self):
        '''Метод доступа к правому движку ползунка фильтра товаров по цене'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.RIGHT_PRICE_SLIDER))

    def get_left_price_field(self):
        '''Метод доступа к левому полю фильтра товаров по цене'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.LEFT_PRICE_FIELD))

    def get_right_price_field(self):
        '''Метод доступа к правому полю фильтра товаров по цене'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.RIGHT_PRICE_FIELD))

    def get_add_to_cart_button(self, article):
        '''Метод доступа к кнпке добавления товара в корзину'''

        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, f"{self.ADD_TO_CART_BUTTON}{article}']")))

    # Click, move and input methods
    def move_left_price_slider(self, shift):
        '''Метод движения левого движка ползунка фильтра товаров по цене'''

        slider = self.get_left_price_slider()
        self.actions.click_and_hold(slider).move_by_offset(shift, 0).release().perform()

    def move_right_price_slider(self, shift):
        '''Метод движения правого движка ползунка фильтра товаров по цене'''

        slider = self.get_right_price_slider()
        self.actions.click_and_hold(slider).move_by_offset(shift, 0).release().perform()

    def click_selected_filter_button(self, num_button):
        '''Метод нажатия кнопки отмены примененного фильтра'''

        self.get_selected_filter_button(num_button).click()
        print("Click selected filter button")

    def click_sort_price_button(self):
        '''Метод нажатия кнопки открытия меню сортировки товаров'''

        self.get_sort_price_button().click()
        print("Click sort price button")

    def click_sort_price_down(self):
        '''Метод нажатия кнопки сортировки товаров по цене по убыванию'''

        self.get_sort_price_down().click()
        print("Click sort price down button")

    def click_sort_price_up(self):
        '''Метод нажатия кнопки сортировки товаров по цене по возрастанию'''

        self.get_sort_price_up().click()
        print("Click sort price up button")

    def click_add_to_cart_button(self, article):
        '''Метод нажатия кнопки добавления товара в корзину'''

        self.get_add_to_cart_button(article).click()
        print("Click add to cart button")

    def input_left_price_field(self, value):
        '''Метод заполнения левого поля фильтра товаров по цене'''

        price_field = self.get_left_price_field()
        price_field.send_keys(Keys.CONTROL + 'a')
        price_field.send_keys(Keys.DELETE)
        price_field.send_keys(value)
        price_field.send_keys(Keys.RETURN)

    def input_right_price_field(self, value):
        '''Метод заполнения правого поля фильтра товаров по цене'''

        price_field = self.get_right_price_field()
        price_field.send_keys(Keys.CONTROL + 'a')
        price_field.send_keys(Keys.DELETE)
        price_field.send_keys(value)
        price_field.send_keys(Keys.RETURN)

    # Action and check methods
    def sort_price_up(self):
        '''Метод сортировки товаров по цене по возрастанию'''

        self.click_sort_price_button()
        self.click_sort_price_up()

    def sort_price_down(self):
        '''Метод сортировки товаров по цене по убыванию'''

        self.click_sort_price_button()
        self.click_sort_price_down()

    def check_sort_price_up(self):
        '''Метод по проверке сортировки товаров по цене по возрастанию'''

        n = self.get_quantity_product_at_webpage()
        first_elem_price = self.get_select_product_price(1)
        last_elem_price = self.get_select_product_price(n)
        print(f"First product price at page: {first_elem_price}₽")
        print(f"Last product price at page: {last_elem_price}₽")
        assert first_elem_price <= last_elem_price
        print("Selected products sort price ASC. Test GOOD")

    def check_sort_price_down(self):
        '''Метод по проверке сортировки товаров по цене по убыванию'''

        n = self.get_quantity_product_at_webpage()
        first_elem_price = self.get_select_product_price(1)
        last_elem_price = self.get_select_product_price(n)
        print(f"First product price at page: {first_elem_price}₽")
        print(f"Last product price at page: {last_elem_price}₽")
        assert first_elem_price >= last_elem_price
        print("Selected products sort price DESC. Test GOOD")

    def check_sum_selected_products(self, num, lst):
        '''Метод по сравнению количества выбранных примененным фильтром товаров и
        количества товаров указанных на чекбоксах фильтра'''

        assert num == sum(lst)
        print("Sum of selected products is GOOD. Test GOOD")

    def check_brand_in_product_name(self, brand, name_list, negative_brand):
        '''Метод по проверке того, что в названиях товаров, выбранных фильтром по бренду,
        присутствует только тот бренд, который указан в фильтре'''

        assert all(brand in name for name in name_list)
        print(f"All selected products have brand '{brand}' in self name. Positive test is GOOD")
        assert not any(negative_brand in name for name in name_list)
        print(f"Any selected product have not brand '{negative_brand}' in self name. Negative test is GOOD")

    def check_multy_brand_in_product_name(self, brand_list, name_list, negative_brand):
        '''Метод по проверке того, что в названиях товаров, выбранных фильтром по нескольким брендам,
        присутствует только те бренды, которые указаны в фильтре'''

        assert all(sum(brand in name for brand in brand_list) for name in name_list)
        print(f"All selected products have brand from list '{brand_list}' in self name. Positive test is GOOD")
        assert not any(negative_brand in name for name in name_list)
        print(f"Any selected product have not brand '{negative_brand}' in self name. Negative test is GOOD")

    def check_feature_in_selected_products(self,
                                           feature_signs_list,
                                           features_in_selected_products_list,
                                           feature_name,
                                           negative_feature):
        '''Метод по проверке того, что в характеристиках товаров,
        выбранных фильтром по нескольким значениям какой-либо характеристике,
        присутствует только те значения характеристики, которые указаны в фильтре'''

        assert all(feature_selected in feature_signs_list for feature_selected in features_in_selected_products_list)
        print(
            f"All selected products have feature '{feature_name}' from list '{feature_signs_list}'. Positive test is GOOD.")
        assert negative_feature not in features_in_selected_products_list
        print(
            f"Any selected product have not feature '{feature_name}' with sign '{negative_feature}'. Negative test is GOOD.")

    def check_price_sliders(self):
        '''Метод по проверке корректной работы плзунка фильтра товаров по цене'''

        min_price_before_move, max_price_before_move = self.get_border_price_signs()
        print(f"Min price before move slider: {min_price_before_move}₽")
        print(f"Max price before move slider: {max_price_before_move}₽")

        self.move_left_price_slider(self.CONTROL_SHIFT)
        self.move_right_price_slider(-self.CONTROL_SHIFT)

        min_price_after_move, max_price_after_move = self.get_border_price_signs()
        print(f"Min price after move slider: {min_price_after_move}₽")
        print(f"Max price after move slider: {max_price_after_move}₽")

        assert min_price_before_move < min_price_after_move and \
               max_price_before_move > max_price_after_move
        print("The borders of the price values have changed CORRECTLY after move slider. Test Good\n")

        self.move_left_price_slider(-self.CONTROL_SHIFT)
        self.move_right_price_slider(self.CONTROL_SHIFT)

        min_price_after_return, max_price_after_return = self.get_border_price_signs()
        print(f"Min price after return slider: {min_price_after_return}₽")
        print(f"Max price after return slider: {max_price_after_return}₽")

        assert min_price_before_move == min_price_after_return and \
               max_price_before_move == max_price_after_return
        print("The borders of the price values have changed CORRECTLY after return slider. Test Good\n")

    def check_input_price_fields(self, left_value, right_value):
        '''Метод по проверке корректности заполнения полей фильтра товаров по цене'''

        min_price_before_input, max_price_before_input = self.get_border_price_signs()
        print(f"Min price before input price field: {min_price_before_input}₽")
        print(f"Max price before input price field: {max_price_before_input}₽")

        self.input_right_price_field(right_value)
        self.input_left_price_field(left_value)

        min_price_after_input, max_price_after_input = self.get_border_price_signs()
        print(f"Min price after input price field: {min_price_after_input}₽")
        print(f"Max price after input price field: {max_price_after_input}₽")

        assert min_price_after_input == left_value and \
               max_price_after_input == right_value
        print("The borders of the price values have changed CORRECTLY after input price fields. Test Good\n")

    def check_price_filter(self, func_apply_filter):
        '''Метод по проверке корректности цен выбранных товаров фильтром по цене
        на верхней и нижней границе выбранного ценового диапазона'''

        change_dict = {
            0: "100₽ less",
            1: "equal",
            2: "100₽ more"
        }

        self.sort_price_down()
        first_product_price_down = self.get_select_product_price(1)
        down_price_list = [
            first_product_price_down - 100,
            first_product_price_down,
            first_product_price_down + 100
        ]
        print()

        for i in range(len(down_price_list)):
            self.input_right_price_field(down_price_list[i])

            try:
                func_apply_filter("Цена")
            except TimeoutException:
                print("The button 'Применить' doesn't work.")
                print("The UPPER price limit filter doesn't work. The test FAILED!!!\n")
                break

            first_price_i = self.get_select_product_price(1)
            print(f"The price of the most expensive product before apply price filter: {first_product_price_down}")
            print(
                f"The price of the most expensive product after apply price filter with sign '{change_dict[i]}': {first_price_i}")
            if i != 0:
                assert first_price_i == first_product_price_down
                print("The price of the most expensive product has not changed. Test GOOD")
            else:
                assert first_price_i < first_product_price_down
                print("The price of the most expensive product has decreased. Test GOOD")

            price_filter_button_num = self.get_quantity_filter_buttons()
            self.click_selected_filter_button(price_filter_button_num)
            print()

        self.sort_price_up()
        first_product_price_up = self.get_select_product_price(1)
        up_price_list = [
            first_product_price_up - 100,
            first_product_price_up,
            first_product_price_up + 100
        ]
        print()

        for i in range(len(up_price_list)):
            self.input_left_price_field(up_price_list[i])

            try:
                func_apply_filter("Цена")
            except TimeoutException:
                print("The button 'Применить' doesn't work.")
                print("The LOWER price limit filter doesn't work. The test FAILED!!!\n")
                break

            first_price_i = self.get_select_product_price(1)
            print(f"The price of the cheapest product before apply price filter: {first_product_price_up}")
            print(
                f"The price of the cheapest product after apply price filter with sign '{change_dict[i]}': {first_price_i}")
            if i != 2:
                assert first_price_i == first_product_price_up
                print("The price of the cheapest product has not changed. Test GOOD")
            else:
                assert first_price_i > first_product_price_up
                print("The price of the most expensive product has increased. Test GOOD")

            price_filter_button_num = self.get_quantity_filter_buttons()
            self.click_selected_filter_button(price_filter_button_num)
            print()
