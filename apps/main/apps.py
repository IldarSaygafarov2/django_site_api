from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main'  # путь до папки приложения, относительно проекта
    verbose_name = 'Основной сайт'  # название приложения на русском языке
