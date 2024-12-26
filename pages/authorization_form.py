from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base.base_class import Base


class AuthorizationForm(Base):
    '''Класс описыващий форму для авторизации в интернет-магазине'''

    # Vars:
    LOGIN = "Arthur223"
    PASSWORD = "E9X4vp6uHn"

    # Locators:
    LOGIN_FIELD = (By.XPATH, "//input[@id='loginInput']")
    PASSWORD_FIELD = (By.XPATH, "//input[@id='passwordInput']")
    REMEMBER_CHECKBOX = (By.XPATH, "//span[@class='checkbox__box']")
    AUTHORIZE_BUTTON = (By.XPATH, "//button[@name='Login']")

    # Initialization class instance
    def __init__(self, driver):
        super().__init__(driver)

    # Get methods:
    def get_login_field(self):
        '''Метод доступа к полю логина'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.LOGIN_FIELD))

    def get_password_field(self):
        '''Метод доступа к полю пароля'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.PASSWORD_FIELD))

    def get_remember_checkbox(self):
        '''Метод доступа к чекбоксу для отключения запоминания
         логина и пароля на данном компьютере'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.REMEMBER_CHECKBOX))

    def get_authorize_button(self):
        '''Метод доступа к кнопке "Авторизоваться"'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.AUTHORIZE_BUTTON))

    # Click and input methods:
    def input_login_field(self):
        '''Метод - заполнение поля логина'''

        self.get_login_field().send_keys(self.LOGIN)
        print("Input login in login field")

    def input_password_field(self):
        '''Метод - заполнение поля пароля'''

        self.get_password_field().send_keys(self.PASSWORD)
        print("Input password in password field")

    def click_remember_checkbox(self):
        '''Метод - отключение запоминания логина и пароля на данном компьютере'''

        self.get_remember_checkbox().click()
        print("Unclick remember checkbox")

    def click_authorize_button(self):
        '''Метод - нажатие кнопки "Авторизоваться"'''

        self.get_authorize_button().click()
        print("Click authorize button")

    # Actions:
    def send_authorization_form(self):
        '''Метод по выполнению всех действий по авторизации на сайте'''

        self.input_login_field()
        self.input_password_field()
        self.click_remember_checkbox()
        self.click_authorize_button()
