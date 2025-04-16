"""
URLs for platform_plugin_saleor.
"""
from django.urls import path, include

from platform_plugin_saleor import views

urlpatterns = [
    path('saleor-info/', views.info_view, name='saleor-info'),
    path('services/', include("platform_plugin_saleor.services.urls", namespace='saleor-services')),
    path('api/', include('platform_plugin_saleor.saleor_app.urls'), name='api'),
]
