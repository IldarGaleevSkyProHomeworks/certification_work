# Create your models here.
from django.core.validators import MinValueValidator
from django.db import models


class Supplier(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название",
    )

    supplier = models.ForeignKey(
        to="Supplier",
        null=True,
        blank=True,
        related_name="dealers",
        on_delete=models.SET_NULL,
        verbose_name="Поставщик",
    )

    debt = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
        ],
        verbose_name="Задолженость (копеек)",
    )

    creation_date_time = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата создания",
    )
