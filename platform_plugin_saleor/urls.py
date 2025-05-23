"""
URLs for platform_plugin_saleor.
"""
from django.urls import include, path

from platform_plugin_saleor import views

urlpatterns = [
    path('saleor-info/', views.info_view, name='saleor-info'),
    path('services/', include("platform_plugin_saleor.services.urls", namespace='saleor-services')),
    path('webhooks/', include('platform_plugin_saleor.webhooks.urls'), name='api'),
]
