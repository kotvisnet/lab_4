from telebot import TeleBot
from config import TELEGRAM_TOKEN
from Handler import register_handlers

# Инициализация бота
bot = TeleBot(TELEGRAM_TOKEN)

# Регистрация обработчиков
register_handlers(bot)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()