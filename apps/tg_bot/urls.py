from django.urls import path

from . import views

urlpatterns = [
    path('confirmation/', views.show_telegram_redirect_page, name='tg-bot-page')
]

# path('tg-bot', include('apps.tg_bot.urls')