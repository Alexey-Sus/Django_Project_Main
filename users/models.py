from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # username = models.CharField(max_length=30, blank=True, null=True, verbose_name='Имя пользователя', unique=True)
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    phone_number = models.CharField(max_length=35, verbose_name='Номер телефона', blank=True, null=True,
                                    help_text='Введите номер телефона')

    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Картинка', blank=True, null=True,
                               help_text='Загрузите аватар')

    user_country = models.CharField(max_length=50, verbose_name='Страна вашего проживания',
                                    help_text='Введите название страны')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

