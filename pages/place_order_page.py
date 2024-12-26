from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from base.base_panel import BasePanel


class PlaceOrderPage(BasePanel):
    '''Класс описыващий страницу для заполнения информации,
    необходимой для доставки товара покупателю'''

    # Vars:
    URL_CONTACTS = "https://vasko.ru/personal/order/contacts/"

    PROFILE_NAME = "Артур"
    STREET_NAME = "Лескова"
    BUILDING_NUMBER = "3"
    FLOOR_NUMBER = "5"  # fill it optional
    LIFT = "Лифт грузовой"

    # Locators:
    PROFILE_NAME_FIELD = (By.XPATH, "//input[@id='input-profile-name']")
    STREET_NAME_FIELD = (By.XPATH, "//input[@name='ADDRESS_STREET']")
    BUILDING_NUMBER_FIELD = (By.XPATH, "//input[@name='ADDRESS_HOUSE']")
    FLOOR_NUMBER_FIELD = (By.XPATH, "//input[@name='ADDRESS_FLOOR']")
    LIFT_SELECT = (By.XPATH, "//select[@name='ADDRESS_LIFT']")
    RESUME_BUTTON = (By.XPATH, "//button[contains(@class, 'show-on-tablet')]")

    # Initialization class instance
    def __init__(self, driver):
        super().__init__(driver)

    # Get methods:
    def get_profile_name_field(self):
        '''Метод доступа к полю "Имя профиля"'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.PROFILE_NAME_FIELD))

    def get_street_name_field(self):
        '''Метод доступа к полю "Название улицы"'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.STREET_NAME_FIELD))

    def get_building_number_field(self):
        '''Метод доступа к полю "Номер дома"'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.BUILDING_NUMBER_FIELD))

    def get_floor_number_field(self):
        '''Метод доступа к полю "Номер этажа"'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.FLOOR_NUMBER_FIELD))

    def get_resume_button(self):
        '''Метод доступа к кнопке перехода на следующую страницу оформления заказа'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.RESUME_BUTTON))

    # Click, input and select methods:
    def input_profile_name_field(self):
        '''Метод - ввести имя профиля в поле "Имя профиля"'''

        field = self.get_profile_name_field()
        field.clear()
        field.send_keys(self.PROFILE_NAME)
        print("Input profile name in profile name field")

    def input_street_name_field(self):
        '''Метод - ввести название улицы в поле "название улицы"'''

        field = self.get_street_name_field()
        field.clear()
        field.send_keys(self.STREET_NAME)
        print("Input stree name in street name field")

    def input_building_number_field(self):
        '''Метод - ввести номер дома в поле "Номер дома"'''

        field = self.get_building_number_field()
        field.clear()
        field.send_keys(self.BUILDING_NUMBER)
        print("Input building number in building number field")

    def input_floor_number_field(self):
        '''Метод - ввести номер этажа в поле "Номер этажа"'''

        field = self.get_floor_number_field()
        field.clear()
        field.send_keys(self.FLOOR_NUMBER)
        print("Input floor number in floor number field")

    def select_lift(self):
        '''Метод по выбору типа лифта в доме покупателя'''

        select = Select(WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LIFT_SELECT)))
        select.select_by_visible_text(self.LIFT)

    def click_resume_button(self):
        '''Метод - нажать на кнопку "Продолжить оформление заказа"'''

        self.get_resume_button().click()
        print("Click resume button")

    # Actions:
    def send_place_order(self):
        '''Метод по заполнению 4-х из 4-х обязательных полей и одного не обязательного поля,
        и переходу на следующую страницу оформления заказа с проверкой ее url-адреса'''

        self.input_profile_name_field()
        self.input_street_name_field()
        self.input_building_number_field()
        self.input_floor_number_field()
        self.select_lift()
        self.click_resume_button()
        self.check_url(self.URL_CONTACTS)

    def send_place_order_without_necessary_street_name(self):
        '''Метод по заполнению 3-х из 4-х обязательных полей и одного не обязательного поля,
        и переходу на следующую страницу оформления заказа с проверкой ее url-адреса.
        Не заполняем поле "Название улицы"'''

        self.input_profile_name_field()

        self.input_building_number_field()
        self.input_floor_number_field()
        self.select_lift()
        self.click_resume_button()
        self.check_url(self.URL_CONTACTS)

    def send_place_order_without_optional_floor_number(self):
        '''Метод по заполнению только всех обязательных полей,
        и переходу на следующую страницу оформления заказа с проверкой ее url-адреса.
        Не заполняем опциальное поле "Номер этажа"'''

        self.input_profile_name_field()
        self.input_street_name_field()
        self.input_building_number_field()

        self.select_lift()
        self.click_resume_button()
        self.check_url(self.URL_CONTACTS)
