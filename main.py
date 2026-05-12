import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x600")

        # Данные
        self.quotes = []          # [{"text": ..., "author": ..., "topic": ...}]
        self.history = []         # [{"text": ..., "author": ..., "topic": ..., "timestamp": ...}]

        self.load_quotes()
        self.load_history()

        # GUI элементы
        self.create_widgets()
        self.update_history_list()

    # ------------------- Загрузка/сохранение -------------------
    def load_quotes(self):
        if os.path.exists("quotes.json"):
            with open("quotes.json", "r", encoding="utf-8") as f:
                self.quotes = json.load(f)
        else:
            # Предопределённые цитаты
            self.quotes = [
                {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "жизнь"},
                {"text": "Будь тем изменением, которое хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "мотивация"},
                {"text": "Я мыслю, следовательно, существую.", "author": "Рене Декарт", "topic": "философия"},
                {"text": "Единственный способ делать великую работу — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "работа"},
                {"text": "Победа не означает быть первым. Победа — это стать лучше, чем ты был раньше.", "author": "Будда", "topic": "саморазвитие"}
            ]
            self.save_quotes()

    def save_quotes(self):
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(self.quotes, f, indent=4, ensure_ascii=False)

    def load_history(self):
        if os.path.exists("history.json"):
            with open("history.json", "r", encoding="utf-8") as f:
                self.history = json.load(f)

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    # ------------------- GUI -------------------
    def create_widgets(self):
        # Рамка для генерации
        frame_gen = ttk.LabelFrame(self.root, text="Генерация цитаты", padding=10)
        frame_gen.pack(fill="x", padx=10, pady=5)

        self.btn_generate = ttk.Button(frame_gen, text="🎲 Сгенерировать цитату", command=self.generate_quote)
        self.btn_generate.pack(pady=5)

        self.lbl_quote = tk.Label(frame_gen, text="", wraplength=650, justify="left", font=("Arial", 10))
        self.lbl_quote.pack(pady=5)

        # Рамка для фильтров
        frame_filter = ttk.LabelFrame(self.root, text="Фильтрация истории", padding=10)
        frame_filter.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_filter, text="Автор:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_author = ttk.Entry(frame_filter, width=20)
        self.entry_author.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_filter, text="Тема:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_topic = ttk.Entry(frame_filter, width=20)
        self.entry_topic.grid(row=0, column=3, padx=5, pady=5)

        self.btn_filter = ttk.Button(frame_filter, text="Применить фильтр", command=self.apply_filter)
        self.btn_filter.grid(row=0, column=4, padx=10, pady=5)

        self.btn_reset = ttk.Button(frame_filter, text="Сбросить", command=self.reset_filter)
        self.btn_reset.grid(row=0, column=5, padx=5, pady=5)

        # История
        frame_history = ttk.LabelFrame(self.root, text="История цитат", padding=10)
        frame_history.pack(fill="both", expand=True, padx=10, pady=5)

        self.history_listbox = tk.Listbox(frame_history, height=15)
        self.history_listbox.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(frame_history, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # Рамка для добавления новой цитаты
        frame_add = ttk.LabelFrame(self.root, text="Добавить новую цитату", padding=10)
        frame_add.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_add, text="Текст:").grid(row=0, column=0, sticky="w")
        self.entry_text = tk.Text(frame_add, height=3, width=50)
        self.entry_text.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_add, text="Автор:").grid(row=1, column=0, sticky="w")
        self.entry_new_author = ttk.Entry(frame_add, width=30)
        self.entry_new_author.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(frame_add, text="Тема:").grid(row=2, column=0, sticky="w")
        self.entry_new_topic = ttk.Entry(frame_add, width=30)
        self.entry_new_topic.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.btn_add = ttk.Button(frame_add, text="➕ Добавить цитату", command=self.add_quote)
        self.btn_add.grid(row=3, column=1, pady=5, sticky="w")

    # ------------------- Основная логика -------------------
    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "Список цитат пуст. Добавьте новые цитаты.")
            return
        quote = random.choice(self.quotes)
        display = f"«{quote['text']}»\n\n— {quote['author']} (тема: {quote['topic']})"
        self.lbl_quote.config(text=display)

        # Сохраняем в историю
        entry = quote.copy()
        entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(entry)
        self.save_history()
        self.update_history_list()

    def add_quote(self):
        text = self.entry_text.get("1.0", tk.END).strip()
        author = self.entry_new_author.get().strip()
        topic = self.entry_new_topic.get().strip()

        # Проверка на пустые строки
        if not text or not author or not topic:
            messagebox.showerror("Ошибка", "Все поля (текст, автор, тема) должны быть заполнены!")
            return

        self.quotes.append({"text": text, "author": author, "topic": topic})
        self.save_quotes()
        messagebox.showinfo("Успех", "Цитата добавлена!")

        # Очистка полей
        self.entry_text.delete("1.0", tk.END)
        self.entry_new_author.delete(0, tk.END)
        self.entry_new_topic.delete(0, tk.END)

    def update_history_list(self, filtered_history=None):
        self.history_listbox.delete(0, tk.END)
        to_show = filtered_history if filtered_history is not None else self.history
        for item in to_show[::-1]:  # новые сверху
            display = f"{item['timestamp']} — {item['author']} ({item['topic']}): {item['text'][:80]}..."
            self.history_listbox.insert(tk.END, display)

    def apply_filter(self):
        author_filter = self.entry_author.get().strip().lower()
        topic_filter = self.entry_topic.get().strip().lower()
        if not author_filter and not topic_filter:
            self.update_history_list()
            return

        filtered = []
        for q in self.history:
            if author_filter and author_filter not in q["author"].lower():
                continue
            if topic_filter and topic_filter not in q["topic"].lower():
                continue
            filtered.append(q)
        self.update_history_list(filtered)

    def reset_filter(self):
        self.entry_author.delete(0, tk.END)
        self.entry_topic.delete(0, tk.END)
        self.update_history_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()
