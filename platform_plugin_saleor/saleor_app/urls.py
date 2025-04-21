"""URLs for Saleor app views and webhooks."""

from django.urls import path

from platform_plugin_saleor.saleor_app.views import get_saleor_app_manifest, register_saleor_app_token
from platform_plugin_saleor.saleor_app.webhooks import order_created_webhook, order_paid_webhook, order_updated_webhook

urlpatterns = [
    path("manifest", get_saleor_app_manifest, name="get_app_manifest"),
    path("register", register_saleor_app_token, name="register_saleor_app_token"),
    path("webhooks/order-updated", order_updated_webhook, name="order_updated_webhook"),
    path("webhooks/order-paid", order_paid_webhook, name="order_paid_webhook"),
    path("webhooks/order-created", order_created_webhook, name="order_created_webhook"),
]
