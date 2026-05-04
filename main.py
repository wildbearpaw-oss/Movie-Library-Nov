import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Глобальные переменные
data_file = "movies.json"
movies = []
current_filter_genre = ""
current_filter_year = ""

def load_data():
    """Загрузка данных из JSON файла"""
    global movies
    try:
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                movies = json.load(f)
        else:
            movies = []
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {e}")
        movies = []

def save_data():    """Сохранение данных в JSON файл"""
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(movies, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения данных: {e}")

def validate_year(year):    """Проверка корректности года (1900–2026)"""
    try:
        year_num = int(year)
        return 1900 <= year_num <= 2026
    except ValueError:
        return False

def validate_rating(rating):    """Проверка корректности рейтинга (0–10)"""
    try:
        rating_num = float(rating)
        return 0 <= rating_num <= 10
    except ValueError:
        return False

def refresh_table():    """Обновление таблицы с учётом фильтрации"""
    filtered = filter_movies()
    for item in tree.get_children():
        tree.delete(item)
    for movie in filtered:
        tree.insert("", "end", values=(
            movie["title"],
            movie["genre"],
            movie["year"],
            f"{movie['rating']:.1f}"
        ))

def filter_movies():    """Фильтрация фильмов по жанру и году"""
    global current_filter_genre, current_filter_year

    filtered = movies.copy()
# Фильтр по жанру (частичное совпадение, регистронезависимо)
    if current_filter_genre:
        filtered = [m for m in filtered if current_filter_genre.lower() in m["genre"].lower()]

    # Фильтр по году
    if current_filter_year:
        try:
            year_int = int(current_filter_year)
            filtered = [m for m in filtered if m["year"] == year_int]
        except ValueError:
            pass

    return filtered

def add_movie():
    """Добавление нового фильма"""
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    rating = rating_entry.get().strip()

    # Проверка полей
    if not title:
        messagebox.showwarning("Предупреждение", "Введите название фильма!")
        return
    if not genre:
        messagebox.showwarning("Предупреждение", "Введите жанр фильма!")
        return
    if not validate_year(year):
        messagebox.showwarning("Предупреждение", "Год должен быть числом от 1900 до 2026!")
        return
    if not validate_rating(rating):
        messagebox.showwarning("Предупреждение", "Рейтинг должен быть числом от 0 до 10!")
        return

    # Добавление фильма
    movie = {
        "title": title,
        "genre": genre,
        "year": int(year),
        "rating": float(rating)
    }
    movies.append(movie)
    save_data()

    # Очистка полей
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)

    messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")
    refresh_table()

def delete_movie():
    """Удаление выбранного фильма"""
    selected_item = tree.selection()
    if selected_item:
        index = tree.index(selected_item[0])
        deleted_movie = movies.pop(index)
        save_data()
        refresh_table()
        messagebox.showinfo("Успех", f"Фильм '{deleted_movie['title']}' удалён!")
    else:
        messagebox.showwarning("Предупреждение", "Выберите фильм для удаления!")

def apply_genre_filter():
    """Применение фильтра по жанру"""
    global current_filter_genre
    current_filter_genre = genre_filter_entry.get().strip()
    refresh_table()
    status_label.config(text=f"Фильтр по жанру: {current_filter_genre if current_filter_genre else 'Все'}", fg="blue")

def apply_year_filter():
    """Применение фильтра по году"""
    global current_filter_year
    current_filter_year = year_filter_entry.get().strip()
    refresh_table()
    status_label.config(text=f"Фильтр по году: {current_filter_year if current_filter_year else 'Все'}", fg="blue")

def reset_filters():
    """Сброс фильтров"""
    global current_filter_genre, current_filter_year
    current_filter_genre = ""
    current_filter_year = ""
    genre_filter_entry.delete(0, tk.END)
    year_filter_entry.delete(0, tk.END)
    refresh_table()
    status_label.config(text="Фильтры сброшены", fg="blue")

def main():
    global title_entry, genre_entry, year_entry, rating_entry
    global tree, status_label, genre_filter_entry, year_filter_entry

    root = tk.Tk()
    root.title("Movie Library - Личная кинотека")
    root.geometry("900x600")
    root.configure(bg="#f0f0f0")

    # Загрузка данных
    load_data()

    # Фрейм для ввода данных
    input_frame = tk.LabelFrame(root, text="Добавление фильма", bg="#f0f0f0", bd=2, relief="groove")
    input_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(input_frame, text="Название:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    title_entry = tk.Entry(input_frame, width=25)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Жанр:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    genre_entry = tk.Entry(input_frame, width=20)
    genre_entry.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(input_frame, text="Год:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    year_entry = tk.Entry(input_frame, width=15)
    year_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Рейтинг (0-10):", bg="#f0f0f0").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    rating_entry = tk.Entry(input_frame, width=15)
    rating_entry.grid(row=1, column=3, padx=5, pady=5)

    # Кнопка добавления
    add_button = tk.Button(input_frame, text="Добавить фильм", bg="green", fg="white", font=("Arial", 10, "bold"),
                          command=add_movie)
    add_button.grid(row=2, column=0, columnspan=4, pady=10)

    # Фрейм для фильтрации
    filter_frame = tk.LabelFrame(root, text="Фильтрация", bg="#f0f0f0", bd=2, relief="groove")
    filter_frame.pack(fill="x", padx=10, pady=10)


    tk.Label(filter_frame, text="Фильтр по жанру:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    genre_filter_entry = tk.Entry(filter_frame, width=20)
    genre_filter_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(filter_frame, text="Применить", command=apply_genre_filter).grid(row=0, column=2, padx=5)


    tk.Label(filter_frame, text="Фильтр по году:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    year_filter_entry = tk.Entry(filter_frame, width=15)
    year_filter_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(filter_frame, text="Применить", command=apply_year_filter).grid(row=1, column=2, padx=5)

    tk.Button(filter_frame, text="Сбросить фильтры", bg="orange",
              command=reset_filters).grid(row=0, column=3, rowspan=2, padx=20, pady=5)


    # Таблица
    tree_frame = tk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)


    columns = ("Название", "Жанр", "Год", "Рейтинг")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.column("Название", width=250)
    tree.column("Жанр", width=180)
    tree.column("Год", width=80)
    tree.column("Рейтинг", width=80)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Кнопки управления
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(fill="x", padx=10, pady=5)

    delete_button = tk.Button(button_frame, text="Удалить выбранный фильм", bg="red", fg="white",
                          command=delete_movie)
    delete_button.pack(side="left", padx=5)

    # Статус-бар
    status_label = tk.Label(root, text="Готов к работе", relief="sunken", anchor="w", bg="#ffffcc")
    status_label.pack(fill="x", side="bottom", padx=10, pady=5)

    # Инициализация таблицы
    refresh_table()

    root.mainloop()

if __name__ == "__main__":
    main()
