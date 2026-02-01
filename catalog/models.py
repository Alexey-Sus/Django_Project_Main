from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=80, verbose_name="Название категории", help_text="Введите название категории"
    )
    description = models.CharField(
        max_length=150,
        verbose_name="Описание",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(
        max_length=80, verbose_name="Продукт"
    )
    description = models.CharField(
        max_length=150,
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="catalog/photos",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL,
        max_length=50, verbose_name="Категория продукта", related_name='products', null=True,
                                 blank=True
    )
    purchase_price = models.FloatField(
        verbose_name="Цена"
    )
    created_at = models.DateField(
        auto_now=True,
        verbose_name="Дата создания", help_text="Укажите дату создания товара"
    )
    updated_at = models.DateField(
        auto_now=True,
        verbose_name="Дата изменения",
        help_text="Укажите дату создания товара"
    )

    is_published = models.BooleanField(default=True, verbose_name='Показывать')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]
        permissions = [('can_unpublish_product', 'Is allowed to unpublish products'),
                       ('can_delete_product', 'Is allowed to delete products'),]

    def __str__(self):
        return self.name
