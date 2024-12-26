from datetime import datetime


class Base:
    '''Базовый класс с базвыми методами,
    которые могут применяться на всех страницах интернет-магазина'''

    def __init__(self, driver):
        self.driver = driver

    def start_driver(self, url):
        '''Метод, запускающий браузер и окрывающий страницу приложения'''

        self.driver.get(url)
        self.driver.maximize_window()

    def quit_driver(self):
        '''Метод, закрывающий все окна браузера'''

        self.driver.quit()

    def back_driver(self):
        '''Метод, возвращющий браузер на предыдущую страницу'''

        self.driver.back()

    def refresh_driver(self):
        '''Метод обновляющий страницу'''

        self.driver.refresh()

    def return_up_driver(self):
        '''Метод, который скроллит страницу в самое начало'''

        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_current_url(self):
        '''Метод, который выводит url текущей страницы'''

        get_url = self.driver.current_url
        print(f"Url текущей страницы: {get_url}")

    def check_word(self, search_word, control_word):
        '''Метод по проверке контрольного слова на открывшейся странице'''

        assert search_word == control_word
        print(f"Control word='{control_word}' is find. Test GOOD")

    def check_url(self, result):
        '''Метод проверяет url текущей страницы'''

        get_url = self.driver.current_url
        assert get_url == result
        print("URL page is GOOD. Test GOOD")

    def create_screenshot(self):
        '''Метод создающий скриншот страницы'''

        uniq_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        name_screen = f'screenshot_{uniq_time}.png'
        self.driver.save_screenshot(fr"..\screens\{name_screen}")
