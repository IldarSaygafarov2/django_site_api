from django.core.management.base import BaseCommand

from apps.tg_bot.bot import bot


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('bot started')
        bot.infinity_polling()
        print('bot stopped')