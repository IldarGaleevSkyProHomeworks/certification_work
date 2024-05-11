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

    def __str__(self):
        return f"{self.name} - {self.model}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"name={self.name},"
            f"model={self.model},"
            f"release_date={self.release_date},"
            f")"
        )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
