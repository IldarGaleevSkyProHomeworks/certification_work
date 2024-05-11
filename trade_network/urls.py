from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trade_network.apps import TradeNetworkConfig

router = DefaultRouter()

app_name = TradeNetworkConfig.name

urlpatterns = [
    path('', include(router.urls)),
]
