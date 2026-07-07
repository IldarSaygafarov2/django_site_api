from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='users/profiles/%Y/%m/%d/', null=True)  # users/profiles/2026/05/14/profile.png

    def __str__(self):
        return f'{self.user.username} profile'


class Subscriber(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE,
                                        related_name='subscribers',
                                        verbose_name='Профиль пользователя')
    subscriber = models.ManyToManyField('auth.User', related_name='subscribers')

    def __str__(self):
        return f'{self.user_profile.user.username}'