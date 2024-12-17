import pandas as pd


all_groups_semantics_path = 'all_groups_semantics.xlsx'

try:
    all_groups_semantics_df = pd.read_excel(all_groups_semantics_path)
    print("Содержимое файла all_groups_semantics.xlsx:")
    print(all_groups_semantics_df.head())  # Выводим первые 5 строк для проверки
except Exception as e:
    print(f"Ошибка при загрузке файла: {e}")
