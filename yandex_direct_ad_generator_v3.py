import os
import pandas as pd

# Словарь марок автомобилей
brands_models = {
    "Renault": "Рено",
    "Lada": "Лада"
}

# Словарь моделей автомобилей
models = {
    "Arkana": ("Аркана", "Arkana"),
    "Duster": ("Дастер", "Duster"),
    "Kangoo": ("Кангу", "Kangoo"),
    "Kangoo 2": ("Кангу 2", "Kangoo 2"),
    "Captur": ("Каптур", "Captur"),
    "Clio 2": ("Клио 2", "Clio 2"),
    "Clio": ("Клио", "Clio"),
    "Koleos": ("Колеос", "Koleos"),
    "Laguna 2": ("Лагуна 2", "Laguna 2"),
    "Laguna": ("Лагуна", "Laguna"),
    "Logan": ("Логан", "Logan"),
    "Logan 2": ("Логан 2", "Logan 2"),
    "Fluence": ("Флюенс", "Fluence"),
    "Trafic": ("Трафик", "Trafic"),
    "Master": ("Мастер", "Master"),
    "Master 2": ("Мастер 2", "Master 2"),
    "Megane": ("Меган", "Megane"),
    "Megane 3": ("Меган 3", "Megane 3"),
    "Sandero": ("Сандеро", "Sandero"),
    "Sandero 2": ("Сандеро 2", "Sandero 2"),
    "Scenic": ("Сценик", "Scenic"),
    "Symbol": ("Симбол", "Symbol"),
    "Largus": ("Ларгус", "Largus")
}

models_url_codes = {
    "Arkana": "arkana",
    "Duster": "duster-1",
    "Kangoo": "kangoo-1",
    "Kangoo 2": "kangoo-2",
    "Captur": "captur",
    "Clio 2": "clio-2",
    "Clio": "clio-2",
    "Koleos": "koleos-1",
    "Laguna 2": "laguna-2",
    "Laguna": "laguna-2",
    "Logan": "logan-1",
    "Logan 2": "logan-2",
    "Fluence": "fluence",
    "Trafic": "trafic-2",
    "Master": "master-3",
    "Master 2": "master-2",
    "Megane": "megane-2",
    "Megane 3": "megane-3",
    "Sandero": "sandero-1",
    "Sandero 2": "sandero-2",
    "Scenic": "scenic-2",
    "Symbol": "symbol-1",
    "Largus": "largus"
}

# Путь к шаблону и папке с директориями моделей
template_path = 'all_groups_semantics.xlsx'
models_folder = r'Parsing_ready\direct_models'
sitemap_path = r'sitemap\filtered_sitemap_urls.xlsx'

# Загружаем шаблон
template_df = pd.read_excel(template_path)

# Загружаем URLs из sitemap в список
sitemap_df = pd.read_excel(sitemap_path)
sitemap_urls = sitemap_df.iloc[:, 0].tolist()  # Предполагаем, что все URL в первом столбце

# Создаем пустой DataFrame для объединенных данных
combined_data = pd.DataFrame(columns=['Category', 'Search Query', 'Ad Title', 'Ad Text', 'URL', 'Quick Link Text'])

# Проходим по всем моделям в папке с директориями
for model_folder in os.listdir(models_folder):
    model_path = os.path.join(models_folder, model_folder)

    # Проверяем, что это директория
    if os.path.isdir(model_path):
        # Проходим по всем файлам в директории модели
        for file_name in os.listdir(model_path):
            if file_name.endswith('.xlsx') and file_name.startswith('ready_'):
                file_path = os.path.join(model_path, file_name)

                # Извлекаем модель (из названия папки) и категорию (из названия файла)
                model_name = model_folder
                try:
                    category_name = file_name[6:-5].split('_')[1:]  # Извлекаем все элементы после 'ready_' до '.xlsx'
                    category_name = ' '.join(category_name)  # Объединяем в строку, убирая нижние подчеркивания
                except ValueError:
                    print(f"Предупреждение: Не удалось извлечь категорию из названия файла '{file_name}'. Пропускаем файл.")
                    continue

                print(f"Обрабатываем файл: {file_name} (Модель: {model_name}, Категория: {category_name})")

                # Загружаем данные из файла
                model_data = pd.read_excel(file_path)

                # Фильтруем данные, оставляя только строки с "Запросы без группы" в первом столбце
                filtered_data = model_data[model_data.iloc[:, 0] == "Запросы без группы"]
                print(f"фильтрованные Данные:")
                print(filtered_data.head())  # Вывод первых нескольких строк для проверки

                # Проверяем, есть ли отфильтрованные данные
                if filtered_data.empty:
                    print(f"Предупреждение: Файл '{file_name}' не содержит запросов без группы. Пропускаем файл.")
                    continue  # Пропускаем итерацию, если данных нет

                # Берем только второй столбец (с запросами)
                requests = filtered_data.iloc[:, 1]
                print(f"Запросы из файла {file_name}:")
                print(requests.head())

                # Создаем словарь для отслеживания количества запросов в каждой группе
                group_counters = {}

                # Проходим по запросам
                for search_query in requests:
                    for index, row in template_df.iterrows():
                        group = row.iloc[0]  # Группа из первого столбца
                        url_template = row.iloc[2]  # Шаблон URL из третьего столбца
                        quick_link_text = row.iloc[3]  # Текст для быстрой ссылки из четвертого столбца

                        # Проверяем, если название категории из имени файла соответствует группе
                        if category_name == group:
                            # Определяем бренд и модель
                            brand = brands_models.get("Lada" if model_name == "Largus" else "Renault")
                            english_name, _ = models.get(model_name, (model_name, model_name))
                            ad_title = f"{category_name} для {brand} {english_name}"

                            # Инициализируем счетчик для группы, если его еще нет
                            if group not in group_counters:
                                group_counters[group] = 0

                            # Увеличиваем счетчик для текущей группы
                            group_count = group_counters[group]
                            if group_count >= 199:
                                # Добавляем номер к названию группы, если превышен лимит запросов
                                group_with_suffix = f"{group} {group_count // 199 + 1}"
                            else:
                                group_with_suffix = group

                            # Увеличиваем счетчик после добавления
                            group_counters[group] += 1

                            # Создаем новый DataFrame для добавляемых данных
                            new_row = pd.DataFrame({
                                'Category': [f"{model_name} ({group_with_suffix})"],
                                'Search Query': [search_query],
                                'Ad Title': [ad_title],
                                'URL': [url_template.replace('[placeholder]', models_url_codes[model_name])],
                                'Quick Link Text': [quick_link_text]
                            })

                            # Добавляем данные в общий DataFrame
                            combined_data = pd.concat([combined_data, new_row], ignore_index=True)

# Создаем папку final, если она не существует
output_folder = 'final'
os.makedirs(output_folder, exist_ok=True)

# Сохранение результирующего DataFrame в файл с использованием имени модели
output_file_path = os.path.join(output_folder, f'output_all_models.xlsx')
combined_data.to_excel(output_file_path, index=False)
print(f"Все данные успешно сохранены в '{output_file_path}'.")
