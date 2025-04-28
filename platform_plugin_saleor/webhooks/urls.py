"""URLs for Saleor app views and webhooks."""

from django.urls import path

from platform_plugin_saleor.webhooks.views import (
    enroll_user_in_courses,
    get_saleor_app_manifest,
    register_saleor_app_token,
)

urlpatterns = [
    path("manifest", get_saleor_app_manifest, name="get_app_manifest"),
    path("register", register_saleor_app_token, name="register_saleor_app_token"),
    path("enroll-user", enroll_user_in_courses, name="order_created_webhook"),
]
