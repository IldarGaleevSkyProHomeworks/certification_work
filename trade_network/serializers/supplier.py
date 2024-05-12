from rest_framework import serializers, fields, status
from rest_framework.exceptions import ValidationError

from trade_network.models import Supplier, Product, Contact
from .contact import ContactSerializer, EditContactSerializer
from .product import ProductSerializer


class NestedSupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id',
            'name',
        ]


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    supplier = NestedSupplierSerializer()

    class Meta:
        model = Supplier
        fields = (
            'id',
            'name',
            'supplier',
            'debt',
            'creation_date_time',
            'supplier_type',
            'hierarchy_level',
        )

        read_only_fields = (
            'debt',
            'creation_date_time',
            'hierarchy_level',
        )


class DetailSupplierSerializer(SupplierSerializer):
    products = ProductSerializer(
        source='products.all',
        many=True,
        read_only=True,
    )

    contacts = ContactSerializer(
        source='contacts.all',
        many=True,
        read_only=False,
    )

    class Meta(SupplierSerializer.Meta):
        fields = SupplierSerializer.Meta.fields + (
            'products',
            'contacts',
        )


class EditSupplierSerializer(DetailSupplierSerializer):
    supplier = fields.IntegerField(
        required=False,
        allow_null=True,
    )

    products = fields.ListField(
        child=serializers.IntegerField(),
        required=False,
    )

    contacts = EditContactSerializer(
        many=True,
        required=False,
    )

    def validate_products(self, value):
        product_ids = set(value)
        old_products_list = {
            item.id: item for item in self.instance.products.all()
        }

        added_product_ids = product_ids.difference(old_products_list.keys())
        added_products = Product.objects.filter(pk__in=added_product_ids)

        not_found_ids = added_product_ids.difference(
            [p.id for p in added_products]
        )

        if not_found_ids:
            raise ValidationError(
                detail={"not_exists_products": list(not_found_ids)},
                code=status.HTTP_404_NOT_FOUND,
            )

        return value

    @staticmethod
    def __update_contacts(instance, validated_data):
        if "contacts" not in validated_data:
            return
        contacts = validated_data.pop("contacts")

        remove_items = {item.id: item for item in instance.contacts.all()}
        for item in contacts:
            item_id = item.get("id", None)
            if item_id is None:
                instance.contacts.create(**item)
            elif remove_items.get(item_id, None) is not None:
                instance_item = remove_items.pop(item_id)
                Contact.objects.filter(id=instance_item.id).update(**item)
        for item in remove_items.values():
            item.delete()

    @staticmethod
    def __update_supplier(instance, validated_data):
        if "supplier" not in validated_data:
            return
        supplier_id = validated_data.pop("supplier")

        if supplier_id is None:
            instance.supplier = None
            return

        if supplier_id == instance.id:
            raise ValidationError(
                detail={
                    "supplier": "Сannot appoint self as a supplier",
                },
            )

        supplier = Supplier.objects.filter(pk=supplier_id)
        if not supplier:
            raise ValidationError(
                detail={
                    "supplier": f"Supplier with id {supplier_id} not found",
                },
            )

        instance.supplier = supplier.first()
        return

    def update(self, instance, validated_data):
        self.__update_contacts(instance, validated_data)
        self.__update_supplier(instance, validated_data)

        for field in validated_data:
            setattr(
                instance,
                field,
                validated_data.get(field, getattr(instance, field)),
            )
        instance.save()
        return instance
