"""
URLs for platform_plugin_saleor.
"""
from django.urls import path

from platform_plugin_saleor import views

urlpatterns = [
    path('saleor-info/', views.info_view, name='saleor-info'),
]
