from rest_framework import viewsets
from rest_framework.response import Response

from trade_network.models import Supplier
from trade_network.serializers import (
    SupplierSerializer,
    DetailSupplierSerializer,
    EditSupplierSerializer,
)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(DetailSupplierSerializer(instance).data)

    def get_serializer_class(self):

        if self.action == 'list':
            return SupplierSerializer
        if self.action == 'retrieve':
            return DetailSupplierSerializer
        if self.action in ['update', 'partial_update']:
            return EditSupplierSerializer
        return SupplierSerializer
