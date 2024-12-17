import pandas as pd
import os

# Создание словаря марок и моделей
brands_models = {
    "Renault": "Рено",
    "Lada": "Лада"
}

models = {
    #"Arkana": "Аркана",
    #"Duster": "Дастер",
    #"Kangoo": "Кангу",
    #"Kangoo 2": "Кангу 2",
    #"Captur": "Каптур",
    #"Clio 2": "Клио 2",
    "Clio": "Клио",
    #"Koleos": "Колеос",
    #"Laguna 2": "Лагуна 2",
    "Laguna": "Лагуна",
    #"Logan": "Логан",
    #"Logan 2": "Логан 2",
    #"Fluence": "Флюенс",
    #"Trafic": "Трафик",
    #"Master": "Мастер",
    #"Master 2": "Мастер 2",
    #"Megane": "Меган",
    #"Megane 3": "Меган 3",
    #"Sandero": "Сандеро",
    #"Sandero 2": "Сандеро 2",
    #"Scenic": "Сценик",
    #"Symbol": "Симбол",
    #"Largus": "Ларгус"  # Исправлено название марки
}

# Путь к исходному файлу и папке для сохранения выходных файлов
source_file_path = 'all_groups_semantics.xlsx'
output_folder = 'direct_models'  # Измените путь на относительный
os.makedirs(output_folder, exist_ok=True)

# Чтение данных из исходного файла
xls_data = pd.ExcelFile(source_file_path)
sheet1_data = xls_data.parse('Лист1')  # Используем первый лист с данными

# Функция для генерации запросов на основе группы и маркеров
def generate_queries(base_query, model_en, model_ru, brand_en=None, brand_ru=None):
    return [
        f"{base_query} {brand_en} {model_en}" if brand_en else f"{base_query} {model_en}",
        f"{base_query} {model_en}",
        f"{base_query} {brand_ru} {model_ru}" if brand_ru else f"{base_query} {model_ru}",
        f"{base_query} {model_ru}"
    ]

# Процесс обработки данных для каждой модели
for model_en, model_ru in models.items():
    model_data = []

    # Определяем марку (бренд) для модели
    brand_en = "Renault" if model_en != "Largus" else "Lada"
    brand_ru = "Рено" if model_en != "Largus" else "Лада"

    # Обработка групп и маркерных запросов из исходного файла
    for index, row in sheet1_data.iterrows():
        group_name = row.iloc[0]  # Название группы
        base_queries = str(row.iloc[1]).split("\n")  # Список маркерных запросов

        # Генерация запросов для каждого маркерного запроса
        for base_query in base_queries:
            generated_queries = generate_queries(base_query, model_en, model_ru, brand_en, brand_ru)

            # Добавляем данные в общий список
            for generated_query in generated_queries:
                model_data.append({
                    "Группа": group_name,
                    "Маркерный запрос": base_query,
                    "Сгенерированные запросы": generated_query
                })

    # Создаем DataFrame для текущей модели
    model_df = pd.DataFrame(model_data)


    # Удаление пустых строк во втором столбце и лишних строк
    # v2
    model_df = model_df[model_df['Маркерный запрос'].notna() & (model_df['Маркерный запрос'].str.strip() != '')]  # Удаляем пустые строки
    model_df = model_df[~model_df['Сгенерированные запросы'].isin(models.values())]  # Удаляем строки с только маркой или моделью
    # v1
    # model_df = model_df[model_df['Маркерный запрос'].notna() & (model_df['Маркерный запрос'] != '')]  # Удаляем пустые строки
    # model_df = model_df[~model_df['Сгенерированные запросы'].isin(models.values())]  # Удаляем строки с только маркой или моделью

    # Удаление дубликатов
    model_df.drop_duplicates(inplace=True)

    # Удаление двойных пробелов в каждой ячейке
    model_df = model_df.apply(lambda x: x.str.replace(' +', ' ', regex=True) if x.dtype == "object" else x)

    # Создаем отдельную папку для текущей модели
    model_output_folder = os.path.join(output_folder, model_en)
    os.makedirs(model_output_folder, exist_ok=True)

    # Разделение на файлы по группам
    for group_name, group_data in model_df.groupby('Группа'):
        group_file_name = f"{model_en}_{group_name.replace(' ', '_')}.xlsx"  # Создаем имя файла
        group_file_path = os.path.join(model_output_folder, group_file_name)  # Полный путь к файлу
        group_data.to_excel(group_file_path, index=False)  # Сохраняем файл

print("Файлы успешно сохранены для каждой модели и разбиты по группам!")
