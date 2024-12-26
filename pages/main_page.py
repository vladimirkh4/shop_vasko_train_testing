from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base.base_panel import BasePanel


class MainPage(BasePanel):
    '''Класс описыващий главную страницу приложения'''

    # Vars:
    URL = "https://vasko.ru/"
    URL_CATEGORY_PATH = "https://vasko.ru/to_catalog/action_categDesc/"
    CATEGORY_DICT = {
        "Распродажа": f"{URL}promo_sale/",
        "Бытовая техника для кухни": f"{URL_CATEGORY_PATH}id_1004/",
        "Бытовая техника для дома": f"{URL_CATEGORY_PATH}id_53/",
        "Мелкая кухонная техника": f"{URL_CATEGORY_PATH}id_307/",
        "Телевизоры": f"{URL_CATEGORY_PATH}id_508/",
        "Климатическая техника": f"{URL_CATEGORY_PATH}id_364/",
        "Товары для дачи": f"{URL_CATEGORY_PATH}id_787/",
        "Товары для автомобиля": f"{URL_CATEGORY_PATH}id_385/",
        "Услуги": f"{URL_CATEGORY_PATH}id_2791/",
        "Товары эконом-класса": f"{URL_CATEGORY_PATH}id_420/",
    }

    # Locators:
    CATEGORY_SELECT = "//h2[@class='catalog-sections__title']/a[contains(text(), "  # first part locator

    # Initialization class instance
    def __init__(self, driver):
        super().__init__(driver)

    # Get methods:
    def get_category_select(self, category_name):
        '''Метод доступа к кнопкам открытия страницы категории товаров или услуг'''

        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f"{self.CATEGORY_SELECT}'{category_name}')]")))

    # Click and input methods:
    def click_category_select(self, category_name):
        '''Метод - нажатие на кнопку открытия страницы категории товаров или услуг'''

        self.get_category_select(category_name).click()
        print(f"Click category: '{category_name}'")

    # Action methods:
    def select_category(self, category_name):
        '''Метод по выбору(переходу на страницу) категории товаров или услуг, с проверкой
        заголовка категории на странице выбранной категории и ее url-адреса'''

        self.click_category_select(category_name)

        category_url = self.CATEGORY_DICT[category_name]
        self.get_current_url()
        self.check_url(category_url)

        header_control = self.get_category_header().text
        self.check_word(category_name, header_control)

    def several_category_select(self):
        '''Метод по переходу на страницы всех категорий товаров или услуг,
         присутствующих на главной странице, поочередно и с соответсвующей проверкой'''

        for category in self.CATEGORY_DICT:
            self.select_category(category)
            self.back_driver()
            print()
