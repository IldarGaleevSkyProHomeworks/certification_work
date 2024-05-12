from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trade_network.apps import TradeNetworkConfig
from trade_network.views import SupplierViewSet

router = DefaultRouter()
router.register('supplier', SupplierViewSet)

app_name = TradeNetworkConfig.name

urlpatterns = [
    path('', include(router.urls)),
]
