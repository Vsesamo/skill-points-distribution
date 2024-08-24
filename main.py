import tkinter as tk
from tkinter import messagebox

def calculate_modifier(value):
    """Рассчитывает модификатор на основе значения."""
    if 0 <= value <= 1:
        return -5
    elif 2 <= value <= 3:
        return -4
    elif 4 <= value <= 5:
        return -3
    elif 6 <= value <= 7:
        return -2
    elif 8 <= value <= 9:
        return -1
    elif 10 <= value <= 11:
        return 0
    elif 12 <= value <= 13:
        return +1
    elif 14 <= value <= 15:
        return +2
    elif 16 <= value <= 17:
        return +3
    elif 18 <= value <= 19:
        return +4
    elif 20 <= value <= 21:
        return +5
    elif 22 <= value <= 23:
        return +6
    elif 24 <= value <= 25:
        return +7
    elif 26 <= value <= 27:
        return +8
    elif 28 <= value <= 29:
        return +9
    elif value == 30:
        return +10


def update_modifier(label, modifier_label):
    """Обновляет модификатор на основе значения."""
    value = int(label.get())
    modifier = calculate_modifier(value)
    modifier_label["text"] = f"Модификатор: {modifier}"


def update_total_points(event, entry, total_label, value_labels):
    """Обновляет общее количество очков на основе введенного значения, с учетом уже выставленных очков."""
    try:
        new_total = int(entry.get())
        used_points = sum(int(lbl.get()) for lbl in value_labels)
        total_label["text"] = str(new_total - used_points)
    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(0, total_label["text"])


def set_value(label, total_label, modifier_label):
    """Устанавливает значение очков в строке вручную, обновляя общий счет и модификатор."""
    try:
        new_value = int(label.get())
        if 0 <= new_value <= 30:
            current_value = int(label.old_value)
            total_points = int(total_label["text"])
            difference = new_value - current_value
            if total_points - difference >= 0:
                total_label["text"] = str(total_points - difference)
                update_modifier(label, modifier_label)
                label.old_value = new_value
            else:
                label.set(current_value)  # Вернуть старое значение, если недостаточно очков
        else:
            label.set(label.old_value)  # Вернуть старое значение, если значение вне диапазона
    except ValueError:
        label.set(label.old_value)  # Вернуть старое значение, если ввод некорректен


def increment(label, total_label, modifier_label):
    """Увеличивает значение на 1, уменьшая общее количество очков."""
    total_points = int(total_label["text"])
    value = int(label.get())
    if total_points > 0 and value < 30:
        label.set(str(value + 1))
        total_label["text"] = str(total_points - 1)
        update_modifier(label, modifier_label)


def decrement(label, total_label, modifier_label):
    """Уменьшает значение на 1, увеличивая общее количество очков."""
    value = int(label.get())
    if value > 0:
        total_points = int(total_label["text"])
        label.set(str(value - 1))
        total_label["text"] = str(total_points + 1)
        update_modifier(label, modifier_label)


def reset_points(label, total_label, modifier_label):
    """Сбрасывает значение очков одной характеристики и возвращает очки в общий пул."""
    value = int(label.get())
    if value > 0:
        total_points = int(total_label["text"])
        total_label["text"] = str(total_points + value)
        label.set("0")
        update_modifier(label, modifier_label)


def reset_all_points(total_label, value_labels, entry):
    """Сбрасывает все значения очков и обновляет общее количество очков."""
    entry_value = int(entry.get())
    total_label["text"] = str(entry_value)
    for i in range(len(value_labels)):
        value_labels[i].set("0")
        update_modifier(value_labels[i], modifier_labels[i])


def copy_to_clipboard(value_labels, modifier_labels):
    """Копирует выставленные очки и модификаторы в буфер обмена."""
    labels = ["Сила", "Атлетика", "Ловкость",
              "Реакция", "Восприятие",
              "Пси - потенциал", "Харизма", "Интеллект"]

    result = []
    for i in range(8):
        value = value_labels[i].get()
        modifier = calculate_modifier(int(value))
        result.append(f"{labels[i]}: {value} ({modifier:+})")

    formatted_result = "\n".join([
        " ".join(result[:3]),  # Сила, Атлетика, Ловкость
        " ".join(result[3:5]),  # Реакция, Восприятие
        " ".join(result[5:8])  # Пси - потенциал, Харизма, Интеллект
    ])

    root.clipboard_clear()
    root.clipboard_append(formatted_result)
    root.update()
    messagebox.showinfo("Скопировано", formatted_result)


root = tk.Tk()
root.title("Распределение очков навыков")
root.geometry("550x400")

# Список подписей для строк
labels = ["Сила:", "Атлетика:", "Ловкость:",
          "Реакция:", "Восприятие:",
          "Пси - потенциал:", "Харизма:", "Интеллект:"]

initial_total_points = 10

top_frame = tk.Frame(root)
top_frame.pack(pady=5, anchor='w')
top_label = tk.Label(top_frame, text="Общее количество очков:", width=20, anchor='w')
top_label.pack(side=tk.LEFT)

entry = tk.Entry(top_frame, width=5)
entry.insert(0, str(initial_total_points))
entry.pack(side=tk.LEFT, padx=5)

top_label_rest = tk.Label(top_frame, text="Очков осталось:", width=13, anchor='w')
top_label_rest.pack(side=tk.LEFT)

total_label = tk.Label(top_frame, text=str(initial_total_points), width=5, anchor='w')
total_label.pack(side=tk.LEFT, padx=5)

reset_all_button = tk.Button(top_frame, text="Сбросить все очки",
                             command=lambda: reset_all_points(total_label, value_labels, entry))
reset_all_button.pack(side=tk.LEFT)

entry.bind("<KeyRelease>", lambda event: update_total_points(event, entry, total_label, value_labels))

value_labels = []
modifier_labels = []

for i in range(8):
    frame = tk.Frame(root)
    frame.pack(pady=5, anchor='w')

    label_text = labels[i]
    label = tk.Label(frame, text=label_text, width=15, anchor='w')
    label.pack(side=tk.LEFT)

    value_var = tk.StringVar()
    value_var.set("0")
    value_var.old_value = "0"

    value_entry = tk.Entry(frame, textvariable=value_var, width=5)
    value_entry.pack(side=tk.LEFT)
    value_labels.append(value_var)

    modifier_label = tk.Label(frame, text="Модификатор: -5", width=15, anchor='w')
    modifier_label.pack(side=tk.LEFT)
    modifier_labels.append(modifier_label)

    value_entry.bind("<FocusOut>",
                     lambda event, lbl=value_var, mod_lbl=modifier_label: set_value(lbl, total_label, mod_lbl))

    plus_button = tk.Button(frame, text="+",
                            command=lambda lbl=value_var, mod_lbl=modifier_label: increment(lbl, total_label, mod_lbl))
    plus_button.pack(side=tk.LEFT, padx=5)

    minus_button = tk.Button(frame, text="-",
                             command=lambda lbl=value_var, mod_lbl=modifier_label: decrement(lbl, total_label, mod_lbl))
    minus_button.pack(side=tk.LEFT, padx=5)

    reset_button = tk.Button(frame, text="Сбросить очки",
                             command=lambda lbl=value_var, mod_lbl=modifier_label: reset_points(lbl, total_label,
                                                                                                mod_lbl))
    reset_button.pack(side=tk.LEFT, padx=5)

copy_button = tk.Button(top_frame, text="Копировать очки навыков",
                        command=lambda: copy_to_clipboard(value_labels, modifier_labels))
copy_button.pack(side=tk.LEFT)

root.mainloop()
#Bebebeb

