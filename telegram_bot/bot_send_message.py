from telebot import TeleBot

from DRF_Library import settings

BOT_TOKEN = settings.TG_BOT_TOKEN
CHAT_ID = settings.TG_CHAT_ID

bot = TeleBot(BOT_TOKEN)


def send_telegram_message_when_borrowing(message):
    """This function is not in bot.py because of big time amount
    of loading django server when importing
    from bot.py cause importing bot.polling()"""
    bot.send_message(CHAT_ID, message)
