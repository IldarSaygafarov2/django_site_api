from django.db import models


class TelegramBotUser(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    tg_username = models.CharField(max_length=100, unique=True, verbose_name='Имя пользователя в тг')
    tg_chat_id = models.BigIntegerField(unique=True, verbose_name='ID пользователя в тг')

    def __str__(self):
        return f'{self.user.first_name}: {self.tg_username}: {self.tg_chat_id}'

    class Meta:
        verbose_name = 'Аккаунт пользователя в ТГ'
        verbose_name_plural = 'Аккаунты пользователей в ТГ'
