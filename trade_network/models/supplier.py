# Create your models here.
from django.core.validators import MinValueValidator
from django.db import models


class SupplierTypeEnum(models.IntegerChoices):
    MANUFACTURER = (0, "Завод")
    RETAIL_NETWORK = (1, "Розничная сеть")
    INDIVIDUAL_ENTREPRENEUR = (2, "Частный предприниматель")


class Supplier(models.Model):
    MAX_CHAIN_LENGTH = 5

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

    supplier_type = models.IntegerField(
        default=SupplierTypeEnum.MANUFACTURER,
        choices=SupplierTypeEnum.choices,
        verbose_name="Тип поставщика",
    )

    @property
    def hierarchy_level(self) -> int | None:
        """
        returns chain length or None if chain
        greater than MAX_CHAIN_LENGTH or does not end with the MANUFACTURER
        """

        attr_name = '__h_level'
        if hasattr(self, attr_name):
            return getattr(self, attr_name, int | None)

        result = 0
        chain = self
        while chain and chain.supplier_type != SupplierTypeEnum.MANUFACTURER:
            result += 1
            chain = chain.supplier
            if not chain or result > self.MAX_CHAIN_LENGTH:
                result = None
                break

        setattr(self, attr_name, result)
        return result

    hierarchy_level.fget.short_description = "Уровень иерархии"

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"pk={self.pk},"
            f"name={self.name},"
            f"supplier={self.supplier},"
            f"debt={self.debt},"
            f"creation_date_time={self.creation_date_time},"
            f")"
        )

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
