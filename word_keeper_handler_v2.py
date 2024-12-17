import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob

# Настройка логирования
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING, encoding='utf-8')

# URL для работы
base_url = "https://word-keeper.ru/core"

# Настройки для использования профиля пользователя Chrome
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/0verlay/AppData/Local/Google/Chrome/User Data")
options.add_argument("profile-directory=Profile 1")
options.headless = False  # Отключен headless режим, чтобы видеть UI
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Путь к папке с моделями и путь к стоп-листу
models_folder = 'direct_models'
stoplist_path = 'minusation/stoplist.txt'
downloads_folder = 'E:/WORK/Python/mysql_GPT_fill/parsed'  # Путь к папке загрузок

def login():
    """Функция для входа в систему (без ввода пароля, с использованием cookies)"""
    driver.get(base_url)
    time.sleep(3)

def get_latest_downloaded_file():
    """Функция для получения пути к последнему загруженному файлу в папке загрузок."""
    # Ищем все файлы в папке загрузок с расширением .xlsx (или другое, если необходимо)
    time.sleep(2)
    files = glob.glob(os.path.join(downloads_folder, "*.xlsx"))
    if not files:
        return None

    # Возвращаем файл с максимальным временем последнего изменения
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

def clear_projects():
    """Функция для очистки списка проектов в Word-Keeper"""
    driver.get(base_url)
    time.sleep(0.5)

    # Выбираем все проекты, используя текст "Выделить все"
    select_all_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Выделить все')]"))
    )
    select_all_button.click()
    time.sleep(0.5)

    # Нажимаем кнопку "Удалить", используя текст "Удалить"
    delete_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Удалить')]"))
    )
    delete_button.click()
    time.sleep(0.5)

    # Ожидаем появления модального окна (JavaScript alert) и нажимаем "ОК"
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()  # Нажимаем "ОК" на alert
        print("Модальное окно успешно подтверждено.")
    except Exception as e:
        print("Не удалось найти модальное окно:", e)

    time.sleep(0.3)

    print("Список проектов успешно очищен.")

def save_combined_file(parsed_files, model_folder, original_file_name):
    """Сохраняет объединённый файл для конкретной модели в нужной папке"""

    if parsed_files:
        # Объединяем все файлы в один DataFrame
        combined_df = pd.concat([pd.read_excel(file) for file in parsed_files], ignore_index=True)

        # Создаём папку для готовых файлов, если её ещё нет
        output_dir = os.path.join("E:/WORK/Python/mysql_GPT_fill/Parsing_ready", model_folder)
        os.makedirs(output_dir, exist_ok=True)

        # Сохраняем объединённый файл в нужной папке
        output_file = os.path.join(output_dir, f"ready_{original_file_name}")
        combined_df.to_excel(output_file, index=False)

        print(f"Объединённый файл сохранён: {output_file}")

def parse_wordstat_group(group_data, original_file_name, model_folder):
    """Функция для отправки запросов из группы в Word-Keeper"""
    driver.find_element(By.CSS_SELECTOR, "a.btnMenu[href='/core/parseword']").click()
    time.sleep(2)

    parsed_files = []

    for i in range(0, len(group_data), 50):
        sub_group = group_data[i:i + 50]

        # Вставляем подгруппу запросов в поле
        textarea = driver.find_element(By.CSS_SELECTOR, "textarea[name='core_zapros[]'].zapros")
        textarea.clear()

        for query in sub_group:
            textarea.send_keys(query + "\n")

        # Устанавливаем регион "Москва и область"
        region_button = driver.find_element(By.CSS_SELECTOR, "span.rtips[data-name='Москва и область']")
        region_button.click()
        time.sleep(1)

        # Вставляем частотность запроса (2)
        frequency_input = driver.find_element(By.CSS_SELECTOR, "input.core_freqzapros")
        frequency_input.clear()
        frequency_input.send_keys("2")
        time.sleep(1)

        # Устанавливаем лимит (5000)# пока что Устанавливаем лимит (2000) # потом вернуть 5000 после отладки
        #limit_button = driver.find_element(By.XPATH, "//span[@class='wtips' and text()='2000']")
        #limit_button.click()
        #time.sleep(1)
        limit_field = driver.find_element(By.CSS_SELECTOR, "input.core_cntzapros[name='core_cntzapros']")
        limit_field.clear()  # Очистка поля, если в нем уже есть значение
        limit_field.send_keys("5000")
        time.sleep(1)



        # Загружаем и вставляем стоп-лист
        with open(stoplist_path, 'r', encoding='utf-8') as f:
            stoplist_text = f.read()

        stoplist_textarea = driver.find_element(By.CSS_SELECTOR,
                                                "textarea[name='core_stoplist_text'].core_stoplist_text.words")
        stoplist_textarea.clear()
        stoplist_textarea.send_keys(stoplist_text)
        time.sleep(1)

        # Нажимаем кнопку "Создать задание"
        submit_button = driver.find_element(By.CSS_SELECTOR, "submit.btn-1.new_task")
        submit_button.click()

        # Ожидаем, пока на странице не появится ссылка с текстом "Перейти в проект"
        try:
            project_link = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//a[text()='Перейти в проект']"))
            )
            project_link.click()  # Переходим в проект
            print("Перешли в проект")
            time.sleep(1)
        except TimeoutException:
            print("Не удалось найти ссылку 'Перейти в проект' в течение 30 секунд, повторяем")
            try:
                submit_button.click()
                time.sleep(1)
                project_link = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//a[text()='Перейти в проект']"))
                )
                project_link.click()  # Переходим в проект
                print("Перешли в проект")
                time.sleep(1)
            except TimeoutException:
                print("Не удалось найти ссылку 'Перейти в проект' во второй раз, aborting")
        process_project()

        # Получаем путь к последнему загруженному файлу
        downloaded_file = get_latest_downloaded_file()
        if downloaded_file:
            parsed_files.append(downloaded_file)
            print(f"Загруженный файл: {downloaded_file}")
        else:
            print("Не удалось найти загруженный файл.")

        save_combined_file(parsed_files, model_folder, original_file_name)

        # Объединяем загруженные файлы
        #if parsed_files:
            #combined_df = pd.concat([pd.read_excel(file) for file in parsed_files], ignore_index=True)

            # Сохраняем объединенный файл в папке модели с отметкой группы
            #output_file = os.path.join(model_folder, f"ready_{original_file_name}")
            #combined_df.to_excel(output_file, index=False)

            #print(f"Объединенный файл сохранен: {output_file}")

    # Очищаем проекты после обработки группы
    print("clear_projects()")
    clear_projects()

def save_combined_file(parsed_files, model_folder, original_file_name):
    """Сохраняет объединённый файл для конкретной модели в нужной папке"""

    if parsed_files:
        # Объединяем все файлы в один DataFrame
        combined_df = pd.concat([pd.read_excel(file) for file in parsed_files], ignore_index=True)

        # Создаём папку для готовых файлов, если её ещё нет
        output_dir = os.path.join("E:/WORK/Python/mysql_GPT_fill/Parsing_ready", model_folder)
        os.makedirs(output_dir, exist_ok=True)

        # Сохраняем объединённый файл в нужной папке
        output_file = os.path.join(output_dir, f"ready_{original_file_name}")
        combined_df.to_excel(output_file, index=False)

        print(f"Объединённый файл сохранён: {output_file}")

def process_model_files():
    """Функция для обработки файлов каждой модели"""
    for model_folder in os.listdir(models_folder):
        model_path = os.path.join(models_folder, model_folder)

        if os.path.isdir(model_path):  # Проверка, что это папка модели
            for file in os.listdir(model_path):
                if file.endswith('.xlsx'):
                    file_path = os.path.join(model_path, file)

                    # Ожидание, пока файл полностью сохранится
                    while not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
                        time.sleep(1)  # Ждём 1 секунду, если файл ещё не готов

                    try:
                        model_data = pd.read_excel(file_path)

                        for group_name, group_df in model_data.groupby('Группа'):
                            group_queries = group_df['Сгенерированные запросы'].dropna().tolist()
                            parse_wordstat_group(group_queries, file, model_path)

                    except Exception as e:
                        logging.warning(f"Ошибка обработки файла {file}: {e}")

def process_project():
    """Функция для обработки проекта после парсинга"""

      # Ждем 4 секунды
    print("Ждем 15 сек, пока проект сформируется")
    time.sleep(15)

    # Ожидаем появления хотя бы одного элемента с заданным классом и атрибутами
    print("Ожидаем появления хотя бы одного элемента <tr class='act tblw-1'>")
    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.act.tblw-1[data-idword='1'][data-group_id='0']"))
        )
        print("Элемент найден, продолжаем работу.")
    except Exception as e:
        print("Не удалось дождаться появления элемента:", e)
        return  # Выходим из функции, если элемент не найден


    print("Открываем модальные инструменты")

    # Открываем модальные инструменты
    tools_buttons = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-modal='modal_average_parsing']"))
    )

    # Ищем элемент с текстом "Инструменты"
    tools_button = next((btn for btn in tools_buttons if "Инструменты" in btn.text), None)

    if tools_button:
        tools_button.click()
        print("Модальные инструменты открыты.")
    else:
        print("Ошибка: элемент с текстом 'Инструменты' не найден.")
    time.sleep(1)
    print("Ждем и выбираем 'Чистка фраз по частоте'")
    # Ждем и выбираем "Чистка фраз по частоте"
    clear_by_frequency_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.bl_listname"))
    )

    if "Чистка фраз по частоте" in clear_by_frequency_button.text:
        clear_by_frequency_button.click()
    else:
        print("Ошибка: текст кнопки не соответствует 'Чистка фраз по частоте'.")

    print("Ждем и запускаем обработку")
    # Ждем и запускаем обработку
    start_processing_buttons = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "submit.btn_clearbyfreq.btn-1"))
    )

    # Ищем элемент с текстом "Запустить обработку"
    start_processing_button = next((btn for btn in start_processing_buttons if "Запустить обработку" in btn.text), None)

    if start_processing_button:
        start_processing_button.click()
    else:
        print("Ошибка: элемент с текстом 'Запустить обработку' не найден.")

    print("Закрываем модальное окно")
    # Закрываем модальное окно
    close_buttons = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.closeModal"))
    )

    # Ищем элемент с текстом "Закрыть"
    close_button = next((btn for btn in close_buttons if "Закрыть" in btn.text), None)

    if close_button:
        close_button.click()
    else:
        print("Ошибка: элемент с текстом 'Закрыть' не найден.")

    print("Переходим к выгрузке")
    # Переходим к выгрузке
    export_buttons = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.btn_popup"))
    )

    # Ищем элемент с текстом "Выгрузка"
    export_button = next((btn for btn in export_buttons if "Выгрузка" in btn.text), None)

    if export_button:
        export_button.click()
        time.sleep(0.5)
    else:
        print("Ошибка: элемент с текстом 'Выгрузка' не найден.")

    print("Ожидаем появления ссылки с содержимым XLS")
    # Ожидаем появления ссылки с содержимым XLS
    download_link = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'type=xls') and text()='XLS']"))
    )
    time.sleep(0.5)
    if download_link:
        download_link.click()
        print("Файл XLS успешно загружен.")
    else:
        print("Ошибка: ссылка с содержимым 'XLS' не найдена.")

def main():
    login()
    process_model_files()
    print("Запросы отправлены и результаты сохранены!")

if __name__ == "__main__":
    main()
