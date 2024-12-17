import pymysql


db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'my_strongest_password',
    'database': 'shopd_db',
}


connection = pymysql.connect(**db_config)
cursor = connection.cursor()

try:
    # Извлечение всех записей, где description равно "&lt;/p&gt;"
    select_query = """
        SELECT category_id, description 
        FROM category_description 
        WHERE description = '&lt;/p&gt;';
    """
    cursor.execute(select_query)
    records = cursor.fetchall()

    # Вывод подходящих записей на консоль перед их очисткой
    if records:
        print("Записи для очистки:")
        for record in records:
            category_id, description = record
            print(f"Category ID: {category_id}, Description: {description}")
    else:
        print("Нет записей для очистки.")

    # Очистка полей description, если они содержат только "&lt;/p&gt;"
    update_query = """
        UPDATE category_description 
        SET description = '' 
        WHERE description = '&lt;/p&gt;';
    """
    cursor.execute(update_query)
    connection.commit()  # Подтверждение изменений в базе данных
    print("Очистка завершена.")

except pymysql.MySQLError as e:
    print("Ошибка при выполнении операции:", e)

finally:
    cursor.close()
    connection.close()
