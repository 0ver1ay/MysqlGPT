import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from collections import Counter


current_file_index = 0
files_list = []
folder_path = ""
deleted_words = []  # Список для хранения удалённых слов
rare_words = []
rare_first_words = []

# Словари для исключения
brands_models = {
    "Renault": "Рено",
    "Lada": "Лада"
}

models = {
    "Arkana": "Аркана",
    "Duster": "Дастер",
    "Kangoo": "Кангу",
    "Kangoo 2": "Кангу 2",
    "Captur": "Каптур",
    "Clio 2": "Клио 2",
    "Clio": "Клио",
    "Koleos": "Колеос",
    "Laguna 2": "Лагуна 2",
    "Laguna": "Лагуна",
    "Logan": "Логан",
    "Logan 2": "Логан 2",
    "Fluence": "Флюенс",
    "Trafic": "Трафик",
    "Master": "Мастер",
    "Master 2": "Мастер 2",
    "Megane": "Меган",
    "Megane 3": "Меган 3",
    "Sandero": "Сандеро",
    "Sandero 2": "Сандеро 2",
    "Scenic": "Сценик",
    "Symbol": "Симбол",
    "Largus": "Ларгус"
}

# Функция для выбора файла
def select_folder():
    global files_list, current_file_index, folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        files_list = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
        current_file_index = 0
        if files_list:
            open_file(os.path.join(folder_path, files_list[current_file_index]))

def open_file(filepath):
    global current_file_index
    # Открытие файла и чтение данных
    try:
        df = pd.read_excel(filepath)
        if df.shape[1] < 2:
            messagebox.showerror("Ошибка", "Файл не содержит второго столбца.")
            return

        display_filtered_second_column(df)
        update_rare_words_buttons(df)
        update_rare_first_words_buttons(df)
        update_unique_first_words_buttons(df)
        update_window_title()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")

def delete_rows(substring, button=None):
    global current_file_index, deleted_words

    if not files_list:
        return

    filepath = os.path.join(folder_path, files_list[current_file_index])
    df = pd.read_excel(filepath)

    mask = df.apply(lambda row: row.astype(str).str.contains(substring, case=False, na=False).any(), axis=1)
    to_delete = df[mask]
    deleted_words.extend(to_delete.iloc[:, 1].astype(str).tolist())

    df = df[~mask]
    df.to_excel(filepath, index=False)

    if button:
        button.destroy()

    update_deleted_words_display()
    display_filtered_second_column(df)
    update_rare_first_words_buttons(df)

def update_deleted_words_display():
    deleted_words_display.delete(1.0, tk.END)
    deleted_words_display.insert(tk.END, "\n".join(deleted_words))

def display_filtered_second_column(df):
    filtered_df = df[df.iloc[:, 0].astype(str).str.contains("Запросы без группы", case=False, na=False)]
    second_column = filtered_df.iloc[:, 1].astype(str).tolist()
    second_column_sorted = sorted(second_column, key=lambda x: tuple(x.split()), reverse=True)

    second_column_display.delete("1.0", tk.END)
    second_column_display.insert(tk.END, "\n".join(second_column_sorted))

def update_rare_first_words_buttons(df):
    global rare_first_words

    second_column_content = df.iloc[:, 1].astype(str).tolist()
    first_words = [line.split()[0] for line in second_column_content if line.split()]
    first_word_counter = Counter(first_words)
    rare_first_words = [word for word, count in first_word_counter.items() if count == 1]

    for widget in rare_first_words_display.winfo_children():
        widget.destroy()

    for word in rare_first_words[:20]:
        button = tk.Button(rare_first_words_display, text=word)
        button.configure(command=lambda w=word: delete_rows(substring=w, button=button))
        button.pack(side=tk.TOP, fill=tk.X)

def update_rare_words_buttons(df):
    global rare_words

    second_column_content = df.iloc[:, 1].astype(str).tolist()
    word_counter = Counter(word for line in second_column_content for word in line.split() if len(word) > 1)
    rare_words = [word for word, count in word_counter.items() if count == 1]

    for widget in deleted_words_display.winfo_children():
        widget.destroy()

    for word in rare_words[:20]:
        button = tk.Button(deleted_words_display, text=word)
        button.configure(command=lambda w=word, b=button: delete_rows(substring=w, button=b))
        button.pack(side=tk.TOP, fill=tk.X)

def update_unique_first_words_buttons(df):
    first_words = {line.split()[0] for line in df.iloc[:, 1].astype(str).tolist() if line.split()}
    unique_first_words = sorted(first_words)

    for widget in unique_first_words_display.winfo_children():
        widget.destroy()

    for word in unique_first_words[:20]:
        button = tk.Button(unique_first_words_display, text=word)
        button.configure(command=lambda w=word: delete_rows(substring=w, button=button))
        button.pack(side=tk.TOP, fill=tk.X)

def update_window_title():
    if files_list and folder_path:
        current_file = files_list[current_file_index]
        root.title(f"Обработка Excel файлов - {current_file}")
    else:
        root.title("Обработка Excel файлов")

def next_file():
    global current_file_index
    if current_file_index < len(files_list) - 1:
        current_file_index += 1
        open_file(os.path.join(folder_path, files_list[current_file_index]))

def previous_file():
    global current_file_index
    if current_file_index > 0:
        current_file_index -= 1
        open_file(os.path.join(folder_path, files_list[current_file_index]))

root = tk.Tk()
root.title("Обработка Excel файлов")
root.geometry("976x1080")
root.minsize(976, 1080)

frame_left = tk.Frame(root, width=400)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH)

frame_buttons = tk.Frame(root, width=192)
frame_buttons.pack(side=tk.LEFT, fill=tk.BOTH)

substring_entry = tk.Entry(frame_buttons, width=20)
substring_entry.pack(fill=tk.X)
substring_entry.insert(0, "Введите подстроку")

delete_by_substring_button = tk.Button(
    frame_buttons,
    text="",
    command=lambda: delete_rows(substring_entry.get())
)
delete_by_substring_button.pack(fill=tk.X)

frame_right = tk.Frame(root, width=192)
frame_right.pack(side=tk.LEFT, fill=tk.BOTH)

rare_first_words_display = tk.Frame(root, width=192)
rare_first_words_display.pack(expand=True, fill=tk.BOTH)

unique_first_words_display = tk.Frame(root, width=192)
unique_first_words_display.pack(expand=True, fill=tk.BOTH)

second_column_display = scrolledtext.ScrolledText(frame_left, wrap=tk.WORD)
second_column_display.pack(expand=True, fill=tk.BOTH)

deleted_words_display = scrolledtext.ScrolledText(frame_right, wrap=tk.WORD)
deleted_words_display.pack(expand=True, fill=tk.BOTH)

select_file_button = tk.Button(frame_buttons, text="Выбрать папку", command=select_folder)
select_file_button.pack(fill=tk.X)

previous_file_button = tk.Button(frame_buttons, text="Предыдущий файл", command=previous_file)
previous_file_button.pack(fill=tk.X)

next_file_button = tk.Button(frame_buttons, text="Следующий файл", command=next_file)
next_file_button.pack(fill=tk.X)

root.mainloop()
