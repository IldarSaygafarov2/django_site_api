from django.contrib import admin
from .models import Subscriber, UserProfile


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass



# TODO: создать страницу subscribers.html
# сделать переход на эту страницу
# users/me/subscribers/