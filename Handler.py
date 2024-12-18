from telebot import types
from notes import add_note, get_user_notes, edit_note, delete_note
from keyboards import main_menu

# Хранение ID старых сообщений для удаления
user_messages = {}


def delete_old_message(bot, chat_id):
    """Удаляет предыдущее сообщение пользователя, если оно существует."""
    if chat_id in user_messages:
        try:
            bot.delete_message(chat_id, user_messages[chat_id])
        except Exception:
            pass  # Если сообщение уже удалено, игнорируем ошибку


def register_handlers(bot):
    """Регистрация обработчиков команд и кнопок."""

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        delete_old_message(bot, message.chat.id)  # Удаляем старое сообщение
        sent_message = bot.send_message(
            message.chat.id,
            "Привет! Я бот для работы с заметками. Выберите действие:",
            reply_markup=main_menu()
        )
        user_messages[message.chat.id] = sent_message.message_id

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        delete_old_message(bot, call.message.chat.id)  # Удаляем старое сообщение
        if call.data == "add_note":
            sent_message = bot.send_message(call.message.chat.id, "Введите текст заметки:")
            user_messages[call.message.chat.id] = sent_message.message_id
            bot.register_next_step_handler(sent_message, add_note_handler)
        elif call.data == "list_notes":
            list_notes(call.message)
        elif call.data == "edit_note":
            sent_message = bot.send_message(call.message.chat.id,
                                            "Введите ID заметки и новый текст в формате:\n<ID> <новый текст>")
            user_messages[call.message.chat.id] = sent_message.message_id
            bot.register_next_step_handler(sent_message, edit_note_handler)
        elif call.data == "delete_note":
            sent_message = bot.send_message(call.message.chat.id, "Введите ID заметки для удаления:")
            user_messages[call.message.chat.id] = sent_message.message_id
            bot.register_next_step_handler(sent_message, delete_note_handler)

    def add_note_handler(message):
        """Добавление новой заметки."""
        delete_old_message(bot, message.chat.id)  # Удаляем старое сообщение
        note_text = message.text
        if not note_text.strip():
            sent_message = bot.reply_to(message, "Заметка не может быть пустой.")
            user_messages[message.chat.id] = sent_message.message_id
            return

        add_note(message.chat.id, note_text)
        sent_message = bot.reply_to(message, "Заметка добавлена.", reply_markup=main_menu())
        user_messages[message.chat.id] = sent_message.message_id

    def list_notes(message):
        """Просмотр всех заметок."""
        delete_old_message(bot, message.chat.id)  # Удаляем старое сообщение
        user_notes = get_user_notes(message.chat.id)
        if not user_notes:
            sent_message = bot.send_message(message.chat.id, "У вас пока нет заметок.", reply_markup=main_menu())
            user_messages[message.chat.id] = sent_message.message_id
            return

        response = "\n".join([f"ID {note['id']}: {note['text']}" for note in user_notes])
        sent_message = bot.send_message(message.chat.id, f"Ваши заметки:\n{response}", reply_markup=main_menu())
        user_messages[message.chat.id] = sent_message.message_id

    def edit_note_handler(message):
        """Редактирование заметки."""
        delete_old_message(bot, message.chat.id)  # Удаляем старое сообщение
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2 or not parts[0].isdigit():
            sent_message = bot.reply_to(message, "Используйте формат: <ID> <новый текст>")
            user_messages[message.chat.id] = sent_message.message_id
            return

        note_id = int(parts[0])
        new_text = parts[1]
        if edit_note(message.chat.id, note_id, new_text):
            sent_message = bot.reply_to(message, "Заметка успешно обновлена.", reply_markup=main_menu())
        else:
            sent_message = bot.reply_to(message, "Заметка с таким ID не найдена.", reply_markup=main_menu())
        user_messages[message.chat.id] = sent_message.message_id

    def delete_note_handler(message):
        """Удаление заметки."""
        delete_old_message(bot, message.chat.id)  # Удаляем старое сообщение
        if not message.text.isdigit():
            sent_message = bot.reply_to(message, "ID должен быть числом.")
            user_messages[message.chat.id] = sent_message.message_id
            return

        note_id = int(message.text)
        if delete_note(message.chat.id, note_id):
            sent_message = bot.reply_to(message, "Заметка удалена.", reply_markup=main_menu())
        else:
            sent_message = bot.reply_to(message, "Заметка с таким ID не найдена.", reply_markup=main_menu())
        user_messages[message.chat.id] = sent_message.message_id
