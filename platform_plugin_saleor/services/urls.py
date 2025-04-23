"""
TO-DO
"""
from django.urls import path

from platform_plugin_saleor.services.views import checkout

app_name = "platform_plugin_saleor"

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
]
