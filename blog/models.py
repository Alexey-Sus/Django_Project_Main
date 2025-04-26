from datetime import datetime
from django.db import models


class Article(models.Model):

    title = models.CharField(
        max_length=80, verbose_name='Название статьи', help_text='Введите название статьи'
    )

    short_descr = models.CharField(max_length=200, verbose_name='Краткое содержание статьи, до 200 симвл.',
        help_text='Введите краткое содержание статьи')

    content = models.TextField(max_length=8000, verbose_name='Содержимое статьи', help_text='Напишите сюда '
                                                                     'свою статью')

    preview = models.ImageField(upload_to='images/', verbose_name='Превью изображения')

    created_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateField(auto_now=True)

    is_published = models.BooleanField(
        verbose_name='Признак публикации',
        default=False
    )

    number_of_views = models.IntegerField()


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'Статья "{self.title}" от {self.created_at}'