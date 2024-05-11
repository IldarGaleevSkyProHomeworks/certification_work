# Create your models here.
from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=250,
        verbose_name="Название",
    )

    model = models.CharField(
        max_length=150,
        verbose_name="Модель",
    )

    release_date = models.DateField(
        auto_now=False, verbose_name="Дата выхода продукта на рынок"
    )

    dealers = models.ManyToManyField(
        to="Supplier",
        related_name="products",
        verbose_name="Дилеры",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
