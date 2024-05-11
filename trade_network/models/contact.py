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

    def __str__(self):
        return (
            f"{self.email}, "
            f"{self.country}, "
            f"{self.city}, "
            f"{self.street}, "
            f"{self.house_number}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"pk={self.pk},"
            f"owner={self.owner},"
            f"email={self.email},"
            f"country={self.country},"
            f"city={self.city},"
            f"street={self.street},"
            f"house_number={self.house_number},"
            f")"
        )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
