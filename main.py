import telebot
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Конфигурация
TELEGRAM_TOKEN = '7662276274:AAGwQKxLCV2aAM_wGdX8CUHgpd4poa2t7Jg'
NOTES_FILE = "notes.json"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Функции для работы с заметками
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

notes = load_notes()

# Главное меню
def main_menu():
    """Создаёт главное меню с кнопками."""
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Создать заметку", callback_data="add_note"),
        InlineKeyboardButton("Показать заметки", callback_data="list_notes")
    )
    markup.add(
        InlineKeyboardButton("Редактировать заметку", callback_data="edit_note"),
        InlineKeyboardButton("Удалить заметку", callback_data="delete_note")
    )
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я бот для работы с заметками. Выберите действие:",
        reply_markup=main_menu()
    )

# Обработчик кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "add_note":
        bot.send_message(call.message.chat.id, "Введите текст заметки:")
        bot.register_next_step_handler(call.message, add_note_handler)
    elif call.data == "list_notes":
        list_notes(call.message)
    elif call.data == "edit_note":
        bot.send_message(call.message.chat.id, "Введите ID заметки и новый текст в формате:\n<ID> <новый текст>")
        bot.register_next_step_handler(call.message, edit_note_handler)
    elif call.data == "delete_note":
        bot.send_message(call.message.chat.id, "Введите ID заметки для удаления:")
        bot.register_next_step_handler(call.message, delete_note_handler)

# Обработчики действий
def add_note_handler(message):
    """Добавление новой заметки."""
    user_id = str(message.chat.id)
    note_text = message.text

    if not note_text.strip():
        bot.reply_to(message, "Заметка не может быть пустой.")
        return

    user_notes = notes.get(user_id, [])
    note_id = len(user_notes) + 1
    user_notes.append({"id": note_id, "text": note_text})
    notes[user_id] = user_notes
    save_notes(notes)

    bot.reply_to(message, f"Заметка добавлена с ID {note_id}.", reply_markup=main_menu())

def list_notes(message):
    """Просмотр всех заметок."""
    user_id = str(message.chat.id)
    user_notes = notes.get(user_id, [])

    if not user_notes:
        bot.reply_to(message, "У вас пока нет заметок.", reply_markup=main_menu())
        return

    response = "\n".join([f"ID {note['id']}: {note['text']}" for note in user_notes])
    bot.reply_to(message, f"Ваши заметки:\n{response}", reply_markup=main_menu())

def edit_note_handler(message):
    """Редактирование заметки."""
    user_id = str(message.chat.id)
    user_notes = notes.get(user_id, [])
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2 or not parts[0].isdigit():
        bot.reply_to(message, "Используйте формат: <ID> <новый текст>")
        return

    note_id = int(parts[0])
    new_text = parts[1]
    note_found = False

    for note in user_notes:
        if note['id'] == note_id:
            note['text'] = new_text
            note_found = True
            break

    if note_found:
        notes[user_id] = user_notes
        save_notes(notes)
        bot.reply_to(message, f"Заметка с ID {note_id} успешно обновлена.", reply_markup=main_menu())
    else:
        bot.reply_to(message, f"Заметка с ID {note_id} не найдена.", reply_markup=main_menu())

def delete_note_handler(message):
    """Удаление заметки."""
    user_id = str(message.chat.id)
    user_notes = notes.get(user_id, [])

    if not message.text.isdigit():
        bot.reply_to(message, "ID должен быть числом.")
        return

    note_id = int(message.text)
    updated_notes = [note for note in user_notes if note['id'] != note_id]

    if len(updated_notes) == len(user_notes):
        bot.reply_to(message, f"Заметка с ID {note_id} не найдена.", reply_markup=main_menu())
    else:
        notes[user_id] = updated_notes
        save_notes(notes)
        bot.reply_to(message, f"Заметка с ID {note_id} удалена.", reply_markup=main_menu())

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
