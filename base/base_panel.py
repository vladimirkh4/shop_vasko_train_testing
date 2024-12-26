import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base.base_class import Base
from pages.authorization_form import AuthorizationForm


class BasePanel(Base):
    '''Класс описывающий элементы,
    которые доступны с любой страницы вебприложения.
    Является родительским, для всех остальных классов, описывающих страницы'''

    # Vars:
    URL_PERSONAL = "https://vasko.ru/personal/"
    URL_CART = "https://vasko.ru/personal/cart/"

    ARTICLES_FOR_TEST = [
        "1775055",
        "2301661",
        "2301372"
    ]
    CATEGORIES = {
        "Товары для кухни": "Бытовая техника для кухни",
        "Товары для дома": "Бытовая техника для дома",
        "Климатическая техника": "Климатическая техника",
        "Телевизоры": "Телевизоры",
        "Товары для дачи": "Товары для дачи",
    }

    # Locators:
    AUTHORIZATION_BUTTON = (By.XPATH, "//a[@id='loginBtn']")
    PERSONAL_BUTTON = (By.XPATH, "//a[@id='userPreviewBtn']")
    PERSONAL_ACCOUNT_BUTTON = (
        By.XPATH, "//div[@class='user-preview__menu']//a[contains(text(), 'Личный кабинет')]"
    )
    CART_BUTTON = (By.XPATH, "//span[@class='basket-line__text']")
    CART_QUANTITY = (By.XPATH, "//span[@id='js-basket-line']")
    CART_CONTENT = (By.XPATH, "//div[@class='basket-preview-item']")
    CART_EMPTY = (By.XPATH, "//div[@class='basket-content__empty']")
    CART_TOTAL_PRICE = (By.XPATH, "//span[@class='basket-content__total-price']")
    COME_TO_CART_BUTTON = (By.XPATH, "//div[@class='basket-content']//a[contains(@class, 'btn')]")

    SEARCH_BUTTON = (By.XPATH, "//span//button[contains(@class, 'header-search-form__btn')]")
    SEARCH_FIELD = (By.XPATH, "//input[@id='headerSearchInput']")
    ARTICLE_SELECT = (By.XPATH, "//div[@class='catalog-tile__vendor-code']")

    BASE_CATEGORY_BUTTON = "//a[@title='"  # first part locator
    CATEGORY_HEADER = (By.TAG_NAME, "h1")

    # Initialization class instance
    def __init__(self, driver):
        super().__init__(driver)
        self.actions = ActionChains(self.driver)

    # Get methods:
    def get_authorization_button(self):
        '''Метод доступа к кнопке авторизации'''

        return WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(
            self.AUTHORIZATION_BUTTON))

    def get_personal_button(self):
        '''Метод доступа к кнопке меню личного кабинета'''

        button_list = self.driver.find_elements(*self.PERSONAL_BUTTON)
        if len(button_list) > 0:
            return button_list[0]
        time.sleep(2)
        button_list = self.driver.find_elements(*self.PERSONAL_BUTTON)
        if len(button_list) > 0:
            return button_list[0]
        print("You are not logged in. At first logged in")
        return False

    def get_personal_account_button(self):
        '''Метод доступа к кнопке личного кабинета'''

        return WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(
            self.PERSONAL_ACCOUNT_BUTTON))

    def get_cart_button(self):
        '''Метод доступа к кнопке корзины'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.CART_BUTTON))

    def get_num_in_button_cart(self):
        '''Метод возвращающий  число товаров в корзине,
        которое указано на кнопке корзины'''

        num = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.CART_QUANTITY))
        return int(num.text)

    def get_cart_empty_text(self):
        '''Метод возвращающий сообщение, выпадающее при нажатии кнопки корзины,
        если корзина пустая'''

        elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.CART_EMPTY))
        return elem.text

    def get_quantity_product_in_cart(self):
        '''Метод возвращащий длину списка товаров в корзине,
        который выпадает при нажатии кнопки корзины'''

        products = self.driver.find_elements(*self.CART_CONTENT)
        if len(products) == 0:
            time.sleep(2)
            products = self.driver.find_elements(*self.CART_CONTENT)
            return len(products)
        return len(products)

    def get_total_price_in_cart(self):
        '''Метод возвращающий общую стоимость товаров в корзине,
        не входя в корзину'''

        price = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.CART_TOTAL_PRICE))
        return int(price.text[:-1].replace(' ', ''))

    def get_come_to_cart_button(self):
        '''Метод доступа к кнопке перехода в корзину'''

        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            self.COME_TO_CART_BUTTON))

    def get_search_button(self):
        '''Метод доступа к кнопке поиска товаров по названию или артиклу'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.SEARCH_BUTTON))

    def get_search_field(self):
        '''Метод доступа к полю поиска товаров по названию или артиклу'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.SEARCH_FIELD))

    def get_article_select(self):
        '''Метод возвращающий значение артикла на странице найденного товара'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.ARTICLE_SELECT))

    def get_base_category_button(self, category_group):
        '''Метод доступа к кнопкам базовых(закрепленных) категорий товаров'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"{self.BASE_CATEGORY_BUTTON}{category_group}']")))

    def get_category_header(self):
        '''Метод возвращающий заголовок категории товаров на странице выбранной категории'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            self.CATEGORY_HEADER))

    # Click and input methods:
    def click_authorization_button(self):
        '''Метод - вход на страницу авторизации'''

        self.get_authorization_button().click()
        print("Click authorization form")

    def click_personal_button(self):
        '''Метод - вход в меню личного кабинета'''

        button = self.get_personal_button()
        if button:
            button.click()
            print("Click personal button")
            return True
        return False

    def click_personal_account_button(self):
        '''Метод - вход в личный кабинет'''

        self.get_personal_account_button().click()
        print("Click personal account button")

    def click_cart_button(self):
        '''Метод - вход в меню перехода в корзину'''

        self.get_cart_button().click()
        print("Click cart button")

    def click_search_button(self):
        '''Метод - нажатие кнопки "Поиск" '''

        self.get_search_button().click()
        print("Click search button")

    def input_search_field(self, string):
        '''Метод - заполнение поля "Поиск"'''

        search_field = self.get_search_field()
        search_field.send_keys(string)
        print("Input text in search field")

    def clear_search_field(self):
        '''Метод - очистка поля "Поиск"'''

        self.get_search_field().clear()

    def click_base_category_button(self, category_group):
        '''Метод - выбор базовой категории товаров'''

        self.return_up_driver()
        self.get_base_category_button(category_group).click()
        print(f"Click base category group button: {category_group}")

    def click_come_to_cart_button(self):
        '''Метод - переход в корзину'''

        self.get_come_to_cart_button().click()
        print("Click come to cart button")

    # Action methods:
    def authorization(self):
        '''Метод - заполнение формы авторизации'''

        self.click_authorization_button()
        af = AuthorizationForm(self.driver)
        af.send_authorization_form()

    def open_personal_account(self):
        '''Метод открывает личный кабинет,
        в случае, если пользователь не авторизован,
        автоматически проводится его авторизация'''

        if self.click_personal_button():
            self.click_personal_account_button()
        else:
            self.authorization()
            self.click_personal_button()
            self.click_personal_account_button()

        self.get_current_url()
        self.check_url(self.URL_PERSONAL)

    def select_product_by_article(self, article):
        '''Метод по поиску и выбору товара по артиклу
        с проверкой url-адреса и артикла товара на странице выбранного товара'''

        self.clear_search_field()
        self.input_search_field(article)
        self.click_search_button()

        url_article = f"https://vasko.ru/search/?q={article}"
        self.get_current_url()
        self.check_url(url_article)

        article_select = self.get_article_select()
        article_control = article_select.text.split(': ')[-1]
        self.check_word(article, article_control)

    def select_several_product_by_article(self):
        '''Метод по выбору нескольких товаров по артиклу, поочередно'''

        for article in self.ARTICLES_FOR_TEST:
            self.select_product_by_article(article)
            self.driver.back()
            print()

    def select_base_category_group(self, group_name):
        '''Метод по выбору базовой категории товаров,
        с проверкой заголовка категории на странице выбранной категории'''

        self.click_base_category_button(group_name)

        header_control = self.get_category_header().text
        self.check_word(self.CATEGORIES[group_name], header_control)

    def select_all_base_category_group(self):
        '''Метод по выбору всех базовых категорий товаров, поочередно'''

        for group_name in self.CATEGORIES:
            self.select_base_category_group(group_name)
            print()

    def come_to_cart(self):
        '''Метод по переходу в корзину выбранных товаров. если корзина не пустая.
        Метод, также возвращает значения количества товаров в корзине и
        общую стоимость товаров в корзине, указанных в меню корзины'''

        if self.get_num_in_button_cart():
            self.click_cart_button()
            quantity_product_in_cart = self.get_quantity_product_in_cart()
            print(f"Quantity_product_in_cart: {quantity_product_in_cart}")
            total_price_in_cart = self.get_total_price_in_cart()
            print(f"Total price of products in cart: {total_price_in_cart}₽")
            self.click_come_to_cart_button()
            self.check_url(self.URL_CART)
            return quantity_product_in_cart, total_price_in_cart
        else:
            self.click_cart_button()
            print(f"{self.get_cart_empty_text()}. Going to the shopping cart is not possible\n")

    def check_quantity_product_in_cart(self, selected_products, products_in_cart):
        '''Метод сравнивает количество выбранных товаров по факту и
        количество товаров указанных в меню корзины'''

        assert selected_products == products_in_cart
        print("The quantity of selected products is equal to the quantity of products in the cart. The test is GOOD")

    def check_price_product_in_cart(self, selected_price, price_in_cart):
        '''Метод сравнивает общую стоимость выбранных товаров по факту и
        общую стоимость товаров указанную в меню корзины'''

        assert selected_price == price_in_cart
        print(
            "The total price of selected products is equal to the total price of products in the cart. The test is GOOD")
