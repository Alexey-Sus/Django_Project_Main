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
        max_length=80, verbose_name="Товар", help_text="Введите название товара"
    )
    description = models.CharField(
        max_length=150,
        verbose_name="Описание товара",
        help_text="Введите описание товара",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="catalog/photos",
        blank=True,
        null=True,
        help_text="Загрузите фото товара",
    )
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL,
        max_length=50, verbose_name="Категория", help_text="Укажите категорию товара", related_name='products', null=True,
                                 blank=True
    )
    purchase_price = models.FloatField(
        verbose_name="Цена товара", help_text="Введите цену товара товара"
    )
    created_at = models.DateField(
        auto_now=True,
        verbose_name="Дата создания", help_text="Укажите дату создания товара"
    )
    updated_at = models.DateField(
        auto_now=True,
        verbose_name="Дата изменения",
        help_text="Укажите дату создания товара",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def __str__(self):
        return self.name
