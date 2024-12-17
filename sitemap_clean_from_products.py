import pandas as pd
import re

# Загрузка файла с отсортированными ссылками
input_file = 'sitemap/combined_sorted_sitemap.xlsx'
df = pd.read_excel(input_file)

# Фильтрация строк: строки с двумя или более цифрами подряд перемещаем в другой DataFrame
pattern = r'\d{2,}'
filtered_links = df[~df['Links'].str.contains(pattern, regex=True)]
removed_links = df[df['Links'].str.contains(pattern, regex=True)]

# Сохранение отфильтрованных ссылок в новый файл
filtered_links.to_excel('sitemap/filtered_sitemap.xlsx', index=False)

# Сохранение удаленных строк в отдельный файл
removed_links.to_excel('sitemap/removed_links.xlsx', index=False)

print("Файлы успешно созданы: filtered_sitemap.xlsx и removed_links.xlsx")
