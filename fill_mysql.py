import pymysql
import glob

# Настройки подключения к базе данных
db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'my_strongest_password',
    'database': 'shopd_db',
}

# Подключение к базе данных
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# Временно отключаем проверки уникальности, иначе не заработает
cursor.execute("SET UNIQUE_CHECKS=0;")

# Импорт файлов
for filename in glob.glob("E:/WORK/Python/mysql_GPT_fill/database dump/*.sql"):
    with open(filename, 'r', encoding='utf-8') as file:
        sql_script = file.read()
        try:
            cursor.execute(sql_script)
            connection.commit()
            print(f"Файл {filename} успешно загружен.")
        except pymysql.MySQLError as e:
            print(f"Ошибка при загрузке файла {filename}: {e}")

# Включаем проверки уникальности обратно
cursor.execute("SET UNIQUE_CHECKS=1;")

# Закрываем соединение
cursor.close()
connection.close()
