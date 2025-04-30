"""URLs for Saleor app views and webhooks."""

from django.urls import path

from platform_plugin_saleor.webhooks.views import fulfill_order, get_saleor_app_manifest, register_saleor_app_token

urlpatterns = [
    path("manifest", get_saleor_app_manifest, name="get_app_manifest"),
    path("register", register_saleor_app_token, name="register_saleor_app_token"),
    path("fulfill-order", fulfill_order, name="order_fulfillment"),
]
