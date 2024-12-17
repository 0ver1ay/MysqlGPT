import time

from selenium import webdriver

import logging

# Настройка логирования
logging.basicConfig(filename='app.log',  # Имя файла лога
                    filemode='a',  # Режим открытия файла, 'a' означает дозапись
                    format='%(name)s - %(levelname)s - %(message)s',  # Формат сообщения
                    level=logging.WARNING,  # Уровень логирования
                    encoding='utf-8')  # Кодировка

# Параметры для входа в систему
base_url = "https://word-keeper.ru/dashboard"
username = "my_email@gmail.com"
password = "my_password"


# Настройки для использования профиля пользователя Chrome
options = webdriver.ChromeOptions()

# Прячемся от капч
options.add_argument("--disable-blink-features=AutomationControlled")  # Скрываем Webdriver, чтобы не проходить капчу
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
# Открывает Chrome с текущими настройками профиля, чтобы не вводить капчи
options.add_argument("user-data-dir=C:/Users/0verlay/AppData/Local/Google/Chrome/User Data")  # Путь к профилю
options.add_argument("profile-directory=Profile 1")  # Имя профиля

options.headless = False
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Если остались какие-то открытые вкладки, закроет их
# Сохранение идентификатора первой вкладки
first_tab = driver.window_handles[0]
# Закрытие всех вкладок, кроме первой
for handle in driver.window_handles:
    if handle != first_tab:
        driver.switch_to.window(handle)
        driver.close()
# Переключение обратно на первую вкладку
driver.switch_to.window(first_tab)


# __________________________________________________

def setup_old_driver():
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()  # Добавляем эту строку для открытия браузера на полный экран

def login():
    """ Функция для входа в админ-панель Word-Keeper. """
    try:
        pass
    except Exception as e:
        print(f"Ошибка входа: {e}")
        return None



def main():
    login()
    time.sleep(100)
