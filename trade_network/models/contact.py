# Create your models here.
from django.db import models


class Contact(models.Model):
    owner = models.ForeignKey(
        to="Supplier",
        related_name="contacts",
        on_delete=models.CASCADE,
        verbose_name="Контакт",
    )

    email = models.EmailField()

    country = models.CharField(
        max_length=150,
        verbose_name="Страна",
    )

    city = models.CharField(
        max_length=150,
        verbose_name="Город",
    )

    street = models.CharField(
        max_length=150,
        verbose_name="Улица",
    )

    house_number = models.CharField(
        max_length=10,
        verbose_name="Номер дома",
    )
