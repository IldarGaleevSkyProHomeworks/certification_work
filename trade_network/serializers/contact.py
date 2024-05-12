from rest_framework import serializers

from trade_network.models import Contact


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id',
            'email',
            'country',
            'city',
            'street',
            'house_number',
        ]


class EditContactSerializer(ContactSerializer):
    id = serializers.IntegerField(
        required=False,
        write_only=False,
    )
