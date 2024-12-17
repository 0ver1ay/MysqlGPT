import mysql.connector

# Настройки подключения к базе данных
db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'my_strongest_password',
    'database': 'shopd_db',
}

# Подключение к базе данных
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# SQL-запрос для получения включенных категорий и всех необходимых полей
# если хотим запустить только с теми категориями, которые включены, то 1, если выключены то 0
# для генерации текстов уместно будет поставить 1 и генерить только для включенных

#SELECT cd.category_id, cd.meta_h1, cd.meta_title, cd.meta_description, cd.meta_keyword, cd.name
#FROM category c
#JOIN category_description cd ON c.category_id = cd.category_id
#JOIN category_description cd ON c.category_id = cd.category_id
#WHERE c.status = 1;

query = """
SELECT cd.category_id, cd.meta_h1, cd.meta_title, cd.meta_description, cd.meta_keyword, cd.name
FROM category c
JOIN category_description cd ON c.category_id = cd.category_id

"""

# Выполнение запроса
cursor.execute(query)
categories = cursor.fetchall()

# Словарь для замены названий
replacements = {
    'Аркана': 'Arkana', 'Дастер': 'Duster', 'Кангу': 'Kangoo', 'Каптур': 'Captur', 'Клио': 'Clio',
    'Колеос': 'Koleos', 'Лагуна': 'Laguna', 'Трафик': 'Trafic', 'Мастер': 'Master', 'Меган': 'Megane', 'Логан': 'Logan', 'Флюенс': 'Fluence',
    'Сандеро': 'Sandero', 'Сценик': 'Scenic', 'Симбол': 'Symbol', 'Ларгус': 'Largus', 'Берлинго': 'Berlingo', 'Партнер': 'Partner',
    'Ситроен': 'Citroen', 'Пежо': 'Peugeot', 'Рено': 'Renault', 'Лада': 'Lada',  'Ниссан': 'Nissan', 'Террано': 'Terrano', 'Альмера': 'Almera'
}
# убрать потом еще " для " в h1 и description
# Функция для очистки и замены текста
def process_text(text):
    if text is None:
        return ""  # Присваиваем пустую строку вместо None
    #text = text.strip()  # Убираем пробелы в начале и в конце
    #for rus, eng in replacements.items():
        #text = text.replace(rus, eng)  # Меняем по словарю слова на английские
    #text = " ".join(text.split())  # Заменяем двойные пробелы на одинарные
    text = text.replace(" для ", " ")
    return text  # Возвращаем обработанный текст


# Обновление записей в базе данных
update_query = """
UPDATE category_description AS cd
JOIN category AS c ON cd.category_id = c.category_id
SET cd.meta_h1 = %s, cd.meta_title = %s, cd.meta_description = %s, cd.meta_keyword = %s, cd.name = %s
WHERE cd.category_id = %s
"""

for category in categories:
    category_id, meta_h1, meta_title, meta_description, meta_keyword, name = category

    # Очистка и обработка текстов
    meta_h1 = process_text(meta_h1 if meta_h1 is not None else "")
    meta_title = process_text(meta_title if meta_title is not None else "")
    meta_description = process_text(meta_description if meta_description is not None else "")
    #meta_keyword = process_text(meta_keyword if meta_keyword is not None else "")
    # name = process_text(name if name is not None else "")

    # Обновление записи
    cursor.execute(update_query, (meta_h1, meta_title, meta_description, meta_keyword, name, category_id))

# Сохранение изменений
connection.commit()

# Закрытие соединения
cursor.close()
connection.close()
