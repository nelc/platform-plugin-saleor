"""
TO-DO
"""
from django.urls import path

from platform_plugin_saleor.services import views

app_name = "platform_plugin_saleor"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("authenticate/", views.authenticate, name="authenticate"),
]
