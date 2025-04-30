from django.db import models

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def __str__(self):
        return self.name
