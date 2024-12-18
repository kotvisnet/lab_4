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

# Хранение ID старых сообщений для удаления
user_messages = {}

def delete_old_message(chat_id):
    """Удаляет предыдущее сообщение пользователя, если оно существует."""
    if chat_id in user_messages:
        try:
            bot.delete_message(chat_id, user_messages[chat_id])
        except Exception:
            pass  # Если сообщение уже удалено, игнорируем ошибку
