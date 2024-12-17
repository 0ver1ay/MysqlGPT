import os
import pandas as pd
import re


input_file = 'sitemap/filtered_sitemap.xlsx'
df = pd.read_excel(input_file)

output_folder = 'sitemap/models_links'
os.makedirs(output_folder, exist_ok=True)

# Регулярное выражение для извлечения модели после пути
pattern = r'https://renokom\.ru/katalog/renault/([^/]+)'

# Группировка ссылок по моделям
model_links = {}

for link in df['Links']:
    match = re.search(pattern, link)
    if match:
        model = match.group(1)
        # Добавляем ссылку к списку для этой модели
        model_links.setdefault(model, []).append(link)

# Сохранение ссылок для каждой модели в отдельные файлы в соответствующих папках
for model, links in model_links.items():
    # Создаем папку для модели, если она не существует
    model_folder = os.path.join(output_folder, model)
    os.makedirs(model_folder, exist_ok=True)
    # Сохраняем ссылки в файл xlsx
    model_df = pd.DataFrame(links, columns=['Links'])
    model_df.to_excel(os.path.join(model_folder, f'{model}_links.xlsx'), index=False)

print("Файлы успешно созданы в папке 'models_links'")
