import pymysql
import html
from bs4 import BeautifulSoup

# Настройки подключения к базе данных
# mysqldump -u root -p renokom_shopd_db category_description > category_description_dump.sql


db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'my_strongest_password',
    'database': 'shopd_db',
}


def remove_styles(html_text):
    # Парсим HTML-код
    soup = BeautifulSoup(html_text, 'html.parser')

    # Удаляем все атрибуты 'style' из всех тегов
    for tag in soup.find_all(True):  # True означает, что выбираются все теги
        if tag.has_attr('style'):
            del tag['style']  # Удаление атрибута style, если он есть

    # Возвращаем модифицированный HTML как строку
    return str(soup)


# Функция для обработки текста
def process_description(description):
    # Проверка, что строка непустая и содержит хотя бы один HTML-тег
    if not description.strip() or '<' not in description:
        return None

    # Парсим HTML-код
    soup = BeautifulSoup(description, 'html.parser')

    # Проверка наличия тегов <style> или <font>
    if not soup.find('style') and not soup.find('font'):
        return None  # Пропускаем запись, если нужные теги отсутствуют

    # Разэкранирование HTML
    unescaped_description = html.unescape(description)

    # Удаление стилей
    cleaned_description = remove_styles(unescaped_description)

    # Экранирование результата обратно
    escaped_description = html.escape(cleaned_description)

    return escaped_description


# Подключение к базе данных
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

try:
    # Извлечение всех записей с полем description
    query = "SELECT category_id, description FROM category_description"
    cursor.execute(query)
    records = cursor.fetchall()

    # Вывод количества извлеченных записей
    print(f"Извлечено записей: {len(records)}")

    # Проход по записям и обработка description
    for record in records:
        category_id, description = record
        new_description = process_description(description)

        # Вывод готового нового текста на консоль, только если он был обработан
        if new_description is not None:
            print(f"Обработка записи category_id={category_id}:\n{description}\n")  # Отладочный вывод
            print(f"Новая версия описания для category_id={category_id}:\n{new_description}\n")

            # Пока закомментируем, чтобы не записалось в базу случайно
            # cursor.execute("UPDATE category_description SET description = %s WHERE category_id = %s", (new_description, category_id))

except pymysql.MySQLError as e:
    print("Ошибка при работе с базой данных:", e)

finally:
    # Закрытие курсора и соединения
    cursor.close()
    connection.close()
