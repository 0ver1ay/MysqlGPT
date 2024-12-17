import pymysql
import re
import html
import requests

# Настройки подключения к базе данных
db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'my_strongest_password',
    'database': 'shopd_db',
}

# URL для обращения к Koboldcpp API на локалке
kobold_url = "http://localhost:5001/api/v1/generate"


car_brands = ["Renault", "Peugeot", "Citroen", "Lada", "Nissan"]


# Функция для извлечения частей строки
def parse_meta_h1(text, brands):
    brand_pattern = "|".join(brands)
    match = re.search(rf"(.+?)\s({brand_pattern})\s(.+)", text)
    if match:
        part1 = match.group(1).strip()  # Часть до марки
        brand_model = f"{match.group(2)} {match.group(3)}"  # Марка и модель
        return part1, brand_model
    return None, None


# Подключение к базе данных
connection = pymysql.connect(**db_config)
cursor = connection.cursor()
try:
    # Извлечение всех записей с полями meta_h1 и description_dev
    cursor.execute("SELECT category_id, meta_h1, description_dev FROM category_description")
    records = cursor.fetchall()

    for record in records:
        category_id, meta_h1, description_dev = record

        # Пропуск записи, если description_dev уже содержит данные
        if description_dev.strip():
            continue

        # Разделение meta_h1 на части
        part1, brand_model = parse_meta_h1(meta_h1, car_brands)

        # Если удалось распарсить meta_h1
        if part1 and brand_model:

            prompt = f"""
            Напиши seo-текст для описания одной конкретной категории каталога сайта: {part1} для {brand_model}
            Текст должен состоять из 1 заголовка <h2> и 2 абзацев <p>!
            
            Шаблон:
            <h2>{part1} для {brand_model}</h2>
            <p>[Текст описания функции {part1} в системе {brand_model} -  2 предложения] + Слова о важности {part1} в системе автомобиля, к которой относится запчасть - 2 предложения].</p>
            <p>[Текст о подходе к подбору запасных частей из этой категории - 1 предложение]</p>
            """


            data = {
                "max_context_length": 4096,
                "max_length": 600,
                "prompt": prompt,
                "quiet": True,
                "rep_pen": 1.1,
                "rep_pen_range": 256,
                "rep_pen_slope": 1,
                "temperature": 0.70,
                "tfs": 1,
                "top_a": 0,
                "top_k": 100,
                "top_p": 0.9,
                "typical": 1
            }

            print(f"Генерируем текст для: {part1} для {brand_model}")

            try:

                response = requests.post(kobold_url, json=data, headers={'accept': 'application/json'})
                response.raise_for_status()

                # Получение данных из ответа
                result = response.json()

                generated_text = result.get("text", "").strip()  # Получаем сгенерированный текст из ответа
                print(" ")
                print(generated_text)
                print(" ")
                print(" ")
                print(" ")
                # Если текст корректен, экранируем его и обновляем запись в базе данных
                if generated_text.startswith("<h2>") and generated_text.endswith("</p>"):
                    pass # Раскомментировать, если все ок с качеством текста
                    escaped_text = html.escape(generated_text)  # Экранирование сгенерированного текста
                    # Обновление записи в базе данных
                    cursor.execute("UPDATE category_description SET description_dev = %s WHERE category_id = %s",
                                   (escaped_text, category_id))
                    print(f"Описание для записи с category_id {category_id} обновлено.")

            except requests.RequestException as e:
                print("Произошла ошибка при обращении к Koboldcpp:", e)

    # Подтверждение изменений
    connection.commit()


except pymysql.MySQLError as e:
    print("Ошибка при работе с базой данных:", e)

finally:
    # Закрытие курсора и соединения
    cursor.close()
    connection.close()
