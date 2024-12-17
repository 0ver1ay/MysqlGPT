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

# SQL-запрос для получения включенных категорий и их meta_h1
query = """
SELECT cd.category_id, cd.meta_h1
FROM category c
JOIN category_description cd ON c.category_id = cd.category_id
WHERE c.status = 1 
  AND (cd.meta_h1 LIKE '%Аркана%' 
       OR cd.meta_h1 LIKE '%Дастер%' 
       OR cd.meta_h1 LIKE '%Кангу%' 
       OR cd.meta_h1 LIKE '%Каптур%'
       OR cd.meta_h1 LIKE '%Клио%'
       OR cd.meta_h1 LIKE '%Колеос%'
       OR cd.meta_h1 LIKE '%Лагуна%'
       OR cd.meta_h1 LIKE '%Трафик%'
       OR cd.meta_h1 LIKE '%Мастер%'
       OR cd.meta_h1 LIKE '%Меган%'
       OR cd.meta_h1 LIKE '%Сандеро%'
       OR cd.meta_h1 LIKE '%Сценик%'
       OR cd.meta_h1 LIKE '%Симбол%'
       OR cd.meta_h1 LIKE '%Ларгус%');
"""


cursor.execute(query)

# Получение результатов
categories = cursor.fetchall()

# Запись результата в файл
with open('categories_meta_h1.txt', 'w', encoding='utf-8') as file:
    for category in categories:
        category_id, meta_h1 = category
        print(f"{meta_h1}")  # Вывод в консоль (опционально)

        # Запись в файл
        file.write(f"{meta_h1}\n")

# Закрытие соединения
cursor.close()
connection.close()
