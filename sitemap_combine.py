import os
import pandas as pd
import xml.etree.ElementTree as ET

# Путь к папке с XML файлами sitemap
sitemap_folder = 'sitemap'

# Список для хранения всех ссылок
all_links = []

# Чтение всех файлов sitemap в папке
for file_name in os.listdir(sitemap_folder):
    if file_name.endswith('.xml'):
        file_path = os.path.join(sitemap_folder, file_name)
        # Парсинг XML файла
        tree = ET.parse(file_path)
        root = tree.getroot()
        # Извлечение всех ссылок (ссылки находятся в тегах <loc>)
        for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            all_links.append(url.text)

# Удаление дубликатов и сортировка ссылок
unique_sorted_links = sorted(set(all_links))

# Создание DataFrame для вывода
output_df = pd.DataFrame(unique_sorted_links, columns=['Links'])

# Сохранение в новый файл xlsx
output_df.to_excel('sitemap/combined_sorted_sitemap.xlsx', index=False)

print("Файл успешно создан: combined_sorted_sitemap.xlsx")
