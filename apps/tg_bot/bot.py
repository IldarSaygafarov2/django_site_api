from core.settings import BOT_TOKEN
from telebot import TeleBot, types
from django.contrib.auth.models import User
from .models import TelegramBotUser

bot = TeleBot(token=BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    # получить chat_id
    # получить username
    # создать объект в таблицу TelegramBotUser
    # отправить пользователю сообщение, регистрация прошла успешно

    chat_id = message.chat.id

    _, user_id = message.text.split()
    TelegramBotUser.objects.create(
        user_id=int(user_id),
        tg_username=message.chat.username,
        tg_chat_id=chat_id
    )
    bot.send_message(chat_id, f'Вы успешно зарегистрировались')
    bot.send_message(chat_id, '<a href="http://127.0.0.1:8000/users/login/">Войти в аккаунт</a>',
                     parse_mode='HTML')



