from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base.base_panel import BasePanel


class ContactInfoPage(BasePanel):
    '''Класс описыващий страницу контакной информации
    для доставки купленного товара. В данном проекте это страница,
    на которой завершается процесс покупки товара в интернет-магазине'''

    # Vars:
    URL_CONFIRM = "https://vasko.ru/personal/order/confirm/"

    CONTACT_PERSON = "Артур"
    EMAIL = "arthur@yandex.ru"
    PHONE_NUMBER = "9" * 10

    CHECK_CITY = "Москва"
    CHECK_PROFILE = "Артур"
    CHECK_STREET = "Лескова"
    CHECK_BUILDING = "3"
    CHECK_FLOOR = "5"

    CHECK_STEP = "4"
    CHECK_TITLE = "Подтверждение"

    # Locators:
    CONTACT_PERSON_FIELD = (By.XPATH, "//input[@name='CONTACT_PERSON']")
    EMAIL_FIELD = (By.XPATH, "//input[@name='EMAIL']")
    PHONE_NUMBER_FIELD = (By.XPATH, "//input[@name='CONTACT_PHONE_M']")
    RESUME_BUTTON_INFO = (By.XPATH, "//button[contains(@class, 'show-on-tablet')]")

    INFO_CITY = (By.XPATH, "//div[contains(@class, 'profiles-form__input')]/b")
    INFO_PROFILE = (By.XPATH, "//div[contains(@class, 'profile-form__input')]/b")
    INFO_STREET = (By.XPATH, "(//span[contains(@class, 'text-right')])[1]")
    INFO_BUILDING = (By.XPATH, "(//span[contains(@class, 'text-right')])[2]")
    INFO_FLOOR = (By.XPATH, "(//span[contains(@class, 'text-right')])[5]")

    CHECKOUT_TITLE = (By.XPATH, "(//div[@class='checkout__title'])[3]")

    # Initialization class instance
    def __init__(self, driver):
        super().__init__(driver)

    # Get methods:
    def get_contact_person_field(self):
        '''Метод доступа к полю "Контактное лицо"'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.CONTACT_PERSON_FIELD))

    def get_email_field(self):
        '''Метод доступа к полю "email"'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.EMAIL_FIELD))

    def get_phone_number_field(self):
        '''Метод доступа к полю "Номер телефона"'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.PHONE_NUMBER_FIELD))

    def get_info_city(self):
        '''Метод возвращающий название города введенное
        на предыдущей стадии оформления заказа'''

        elem_city = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.INFO_CITY))
        return elem_city.text

    def get_info_profile(self):
        '''Метод возвращающий название профиля покупателя введенное
        на предыдущей стадии оформления заказа'''

        elem_profile = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.INFO_PROFILE))
        return elem_profile.text

    def get_info_street(self):
        '''Метод возвращающий название улицы введенное
        на предыдущей стадии оформления заказа'''

        elem_street = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.INFO_STREET))
        return elem_street.text

    def get_info_building(self):
        '''Метод возвращающий номер дома введенный
        на предыдущей стадии оформления заказа'''

        elem_building = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.INFO_BUILDING))
        return elem_building.text

    def get_info_floor(self):
        '''Метод возвращающий номер этажа введенный
        на предыдущей стадии оформления заказа'''

        elem_floor = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.INFO_FLOOR))
        return elem_floor.text

    def get_resume_button_info(self):
        '''Метод доступа к кнопке перехода на страницу подтверждения заказа'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.RESUME_BUTTON_INFO))

    def get_checkout_info(self):
        '''Метод возвращающий номер стадии и название заголовка
        на странице подтверждения заказа'''

        elem_title = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.CHECKOUT_TITLE))
        check_elements = elem_title.text.split('\n')
        step = check_elements[0].split()[-1]
        title = check_elements[1].strip()
        return step, title

    # Click and input methods:
    def input_contact_person_field(self):
        '''Метод - ввести имя контакного лица в поле "Контактное лицо"'''

        field = self.get_contact_person_field()
        field.clear()
        field.send_keys(self.CONTACT_PERSON)
        print("Input contact person in contact person field")

    def input_email_field(self):
        '''Метод - ввести email в поле "email"'''

        field = self.get_email_field()
        field.clear()
        field.send_keys(self.EMAIL)
        print("Input email in email field")

    def input_phone_number_field(self):
        '''Метод - ввести номер телефона в поле "Номер телефона"'''

        field = self.get_phone_number_field()
        field.send_keys(self.PHONE_NUMBER)
        print("Input phone number in phone number field")

    def click_resume_button_info(self):
        '''Метод - нажать на кнопку "Продолжить оформление заказа"'''

        self.get_resume_button_info().click()
        print("Click resume button_info")

    # Actions:
    def send_contact_info(self):
        '''Метод по заполнению всех необходимых полей и переходу
        на страницу подтверждения заказа, с проверкой url-адреса, номера стадии
        и заголовка на странице подтверждения заказа'''

        self.input_contact_person_field()
        self.input_email_field()
        self.input_phone_number_field()

        self.click_resume_button_info()

        self.check_url(self.URL_CONFIRM)
        step, title = self.get_checkout_info()
        self.check_word(self.CHECK_STEP, step)
        self.check_word(self.CHECK_TITLE, title)

    def check_delivery_info(self):
        '''Метод по проверке корректности отображения информации
        по доставке товара покупателю, введенной на предыдущей стадии оформления заказа'''

        self.check_word(self.CHECK_CITY, self.get_info_city())
        self.check_word(self.CHECK_PROFILE, self.get_info_profile())
        self.check_word(self.CHECK_STREET, self.get_info_street())
        self.check_word(self.CHECK_BUILDING, self.get_info_building())
        self.check_word(self.CHECK_FLOOR, self.get_info_floor())
        print("All delivery info is CORRECTLY. Five tests are GOOD\n")
