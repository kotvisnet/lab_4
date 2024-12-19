from telebot import TeleBot
from config import TELEGRAM_TOKEN
from Handler import register_handlers

bot = TeleBot(TELEGRAM_TOKEN)

register_handlers(bot)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()