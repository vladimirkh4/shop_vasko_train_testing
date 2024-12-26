from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base.base_panel import BasePanel


class CartPage(BasePanel):
    '''Класс описыващий страницу корзины выбранных товаров'''

    # Vars:
    URL_PLACE_ORDER = "https://vasko.ru/personal/order/delivery/"

    # Locators:
    USER_NAME = (By.XPATH, "//aside//div[@class='user-line__name']")
    ACCOUNT_CART_QUANTITY = (By.XPATH, "//aside//span[contains(@class, 'js-basket-line')]")
    EXIT_ACCOUNT_BUTTON = (By.XPATH, "(//a[@class='user-menu__link'])[7]")

    PRODUCT_NAME_IN_CART = (By.XPATH, "//div[@class='basket-item__name']")
    PRODUCT_DELIVERY_PRICE = (By.XPATH, "//div[contains(@class, 'show-on-tablet')]//span[contains(text(), 'Доставка')]")
    PRODUCT_PRICE_IN_CART = (By.XPATH, "//div[@class='basket-price']")
    PRODUCT_QUANTITY_FIELD = (By.XPATH, "//input[@name='product-quantity']")
    PRODUCT_QUANTITY_DECREASE = (By.XPATH, "//button[@data-decrease]")
    PRODUCT_QUANTITY_INCREASE = (By.XPATH, "//button[@data-increase]")
    PRODUCT_DELETE_IN_CART = (By.XPATH, "//button[contains(@class, 'js-product-delete')]")

    TOTAL_ORDER_SUM = (By.XPATH, "//span[@class='basket-total__value']")
    TOTAL_PRODUCTS_SUM = (By.XPATH, "(//div[@class='basket-summary']/div)[2]")
    TOTAL_DELIVERY_SUM = (By.XPATH, "(//div[@class='basket-summary']/div)[3]")
    PLACE_ORDER_BUTTON = (By.XPATH, "//a[contains(text(), 'Оформить заказ')]")

    # Initialization class instance
    def __init__(self, driver):
        super().__init__(driver)

    def delivery_calculation(self, string):
        '''Вспомогательный метод по извлечению из строки суммы всех чисел'''

        count = 0
        for elem in string.split():
            if elem.isdigit():
                count += int(elem)
        return count

    # Get methods:
    def get_user_name(self):
        '''Метод возвращающий имя пользователя'''

        elem_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.USER_NAME))
        return elem_name.text.strip(' .')

    def get_number_product_in_cart(self):
        '''Метод возвращающий количество товаров в корзине указанное в разделе
        личный кабинет на странице корзины'''

        elem_number = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.ACCOUNT_CART_QUANTITY))
        return int(elem_number.text)

    def get_product_names_set_in_cart(self):
        '''Метод возвращающий множество наименований товаров в корзине'''

        product_elements = self.driver.find_elements(*self.PRODUCT_NAME_IN_CART)
        return {element.text for element in product_elements}

    def get_product_delivery_prices_list(self):
        '''Метод возвращающий список со значениями цен доставки товаров в корзине'''

        delivery_elements = self.driver.find_elements(*self.PRODUCT_DELIVERY_PRICE)
        return [self.delivery_calculation(element.text) for element in delivery_elements]

    def get_product_prices_set_in_cart(self):
        '''Метод возвращающий множество со значениями цен товаров в корзине'''

        price_elements = self.driver.find_elements(*self.PRODUCT_PRICE_IN_CART)
        price_element = self.driver.find_element(*self.PRODUCT_PRICE_IN_CART)
        return {int(element.text[:-1].replace(' ', '')) for element in price_elements}

    def get_product_delete_button(self):
        '''Метод доступа к кнопке удаляющей товар из корзины'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.PRODUCT_DELETE_IN_CART))

    def get_exit_account_button(self):
        '''Метод доступа к кнопке по выходу из аккунта'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.EXIT_ACCOUNT_BUTTON))

    def get_total_order_sum(self):
        '''Метод возвращающий общую сумму заказа в корзине'''

        elem_sum = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.TOTAL_ORDER_SUM))
        return int(elem_sum.text.replace(' ', ''))

    def get_total_products_sum(self):
        '''Метод возвращающий общую стоимость товаров в корзине'''

        elem_sum = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.TOTAL_PRODUCTS_SUM))
        return int(elem_sum.text.split(': ')[-1][:-1].replace(' ', ''))

    def get_total_delivery_sum(self):
        '''Метод возвращающий общую стоимость  доставки товаров в корзине'''

        elem_sum = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.TOTAL_DELIVERY_SUM))
        return int(elem_sum.text.split(': ')[-1][:-1].replace(' ', ''))

    def get_place_order_button(self):
        '''Метод доступа к кнопке "Оформить заказ"'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.PLACE_ORDER_BUTTON))

    def get_product_quantity_field(self):
        '''Метод доступа к полю количества экземпляров товара одного наименования'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.PRODUCT_QUANTITY_FIELD))

    def get_product_quantity_field_value(self):
        '''Метод возвращающий количество экземпляров товара одного наименования'''

        value = self.get_product_quantity_field().get_attribute('value')
        return int(value)

    def get_product_decrease_button(self):
        '''Метод доступа к кнопке уменьшения количества экземпляров
        товара одного наименования'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.PRODUCT_QUANTITY_DECREASE))

    def get_product_increase_button(self):
        '''Метод доступа к кнопке увеличения количества экземпляров
        товара одного наименования'''
        
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.PRODUCT_QUANTITY_INCREASE))

    # Click and input methods:
    def click_product_delete_button(self):
        '''Метод - нажать кнопку удалить товар из корзины'''

        self.get_product_delete_button().click()
        print("Click button delete product in cart")

    def click_exit_account_button(self):
        '''Метод - нажать кнопку выйти из аккаунта'''

        self.get_exit_account_button().click()
        print("Click exit account button")

    def click_place_order_button(self):
        '''Метод - нажать кнопку "Оформить заказ"'''

        self.get_place_order_button().click()
        print("Click place order button")

    def click_product_decrease_button(self):
        '''Метод - нажать кнопку уменьшить количество экземпляров товара'''

        button = self.get_product_decrease_button()
        button.click()
        print("Click product decrease button")

    def click_product_increase_button(self):
        '''Метод - нажать кнопку увеличить количество экземпляров товара'''

        button = self.get_product_increase_button()
        button.click()
        print("Click product increase button")

    def input_product_quantity_field(self, num):
        '''Метод - заполнить поле количество экземпляров товара'''

        field = self.get_product_quantity_field()
        field.send_keys(Keys.CONTROL + 'a')
        field.send_keys(Keys.DELETE)
        field.send_keys(num)
        field.send_keys(Keys.ENTER)
        print(f"Input {num} in quantity product field")

    # Actions:
    def clear_cart(self):
        '''Метод удаляет из корзины все товары'''

        n = self.get_number_product_in_cart()
        for _ in range(n):
            self.click_product_delete_button()
            self.refresh_driver()

    def place_order(self):
        '''Метод по переходу на следующую страницу оформления заказа
        с проверкой адреса страницы'''

        self.click_place_order_button()
        self.check_url(self.URL_PLACE_ORDER)

    # Check methods:
    def check_user_name(self, fact_user_name, user_name_in_cart):
        '''Метод по сравнению фактического имени пользователя
         с именем указанным в корзине'''

        assert fact_user_name == user_name_in_cart
        print(f"The user name '{fact_user_name}' match to user name in account. The test is GOOD")

    def check_quantity_goods_in_cart(self, selected_goods, goods_in_cart, goods_in_account):
        '''Метод по сравнению количесву фактически выбранных товаров,
        количеству товаров в корзине и количетсву товаров в разделе личный кабинет'''

        assert goods_in_cart == selected_goods and goods_in_account == selected_goods
        print('''The quantity of selected goods is equal to the quantity of goods in the cart
and equal to the quantity of goods in the account. The test is GOOD.''')

    def check_goods_names(self, selected_goods_names, goods_names_in_cart):
        '''Метод по сравнению наименований фактически выбранных товаров с
        наименованиями товаров в корзине'''

        assert selected_goods_names == goods_names_in_cart
        print("The names of selected goods are match to the names of goods in cart. The test is GOOD.")

    def check_goods_prices(self, selected_goods_prices, goods_prices_in_cart):
        '''Метод по сравнению цен фактически выбранных товаров с
        ценами товаров в корзине'''

        assert selected_goods_prices == goods_prices_in_cart
        print("The prices of selected goods are match to the prices of goods in cart. The test is GOOD.")

    def check_total_goods_sum(self, selected_goods_sum, total_goods_sum):
        '''Метод по сравнению суммы стоимостей товаров в корзине с
        общей стоимостью товаров в корзине'''

        assert selected_goods_sum == total_goods_sum
        print(f"The total sum of goods {total_goods_sum}₽ is calculated correctly. The test is GOOD.")

    def check_total_delivery_sum(self, selected_goods_delivery_sum, total_delivery_goods_sum):
        '''Метод по сравнению суммы стоимостей доставки товаров в корзине с
        общей стоимостью доставки товаров в корзине'''

        assert selected_goods_delivery_sum == total_delivery_goods_sum
        print(f"The total delivery sum of goods {total_delivery_goods_sum}₽ is calculated correctly. The test is GOOD.")

    def check_total_order_sum(self, total_goods_sum, total_delivery_goods_sum, total_order_sum):
        '''Метод по сравнению суммы общей стоимостью товаров в корзине
        и общей стоимостью доставки товаров в корзине с общей стоимостью заказа'''

        assert total_goods_sum + total_delivery_goods_sum == total_order_sum
        print(f"The total order sum {total_order_sum}₽ is calculated correctly. The test is GOOD.")
