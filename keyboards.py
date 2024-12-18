from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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
