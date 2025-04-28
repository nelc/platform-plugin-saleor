"""Defines the manifest for the Saleor app."""

from django.conf import settings

from platform_plugin_saleor.saleor_client.queries import GET_ORDER_FULLY_PAID_SUBSCRIPTION

SALEOR_APP_ID = "platform.plugin.saleor"


def get_app_manifest():
    """
    Generate the application manifest for Saleor integration.

    The manifest defines the application's metadata, permissions, webhooks,
    and integration points that Saleor will use to interact with this plugin.

    Returns:
        dict: A dictionary containing the complete application manifest.
    """
    manifest = {
        'id': SALEOR_APP_ID,
        'version': '0.1.0',
        'requiredSaleorVersion': '^3.13',
        'name': 'platform-plugin-saleor',
        'author': 'NELC Team',
        'about': 'This is a test plugin for Saleor',

        'permissions': [
            'MANAGE_APPS',
            'MANAGE_USERS',
            'MANAGE_STAFF',
            'MANAGE_TAXES',
            'MANAGE_MENUS',
            'MANAGE_PAGES',
            'MANAGE_ORDERS',
            'MANAGE_PLUGINS',
            'MANAGE_CHANNELS',
            'MANAGE_PRODUCTS',
            'MANAGE_SHIPPING',
            'MANAGE_SETTINGS',
            'MANAGE_CHECKOUTS',
            'MANAGE_DISCOUNTS',
            'MANAGE_GIFT_CARD',
            'MANAGE_TRANSLATIONS',
            'MANAGE_OBSERVABILITY',
            'MANAGE_ORDERS_IMPORT',
            'MANAGE_PAGE_TYPES_AND_ATTRIBUTES',
            'MANAGE_PRODUCT_TYPES_AND_ATTRIBUTES'
        ],
        'appUrl': f'{settings.LMS_ROOT_URL}',
        'configurationUrl': f'{settings.LMS_ROOT_URL}/saleor/webhooks/configuration',
        'tokenTargetUrl': f'{settings.LMS_ROOT_URL}/saleor/webhooks/register',
        'dataPrivacy': 'Lorem ipsum',
        'brand': {
          'logo': {
            'default': f'{settings.LMS_ROOT_URL}/static/nelp-edx-theme-bragi/images/logo.png',
          }
        },
        'webhooks': [
          {
            'name': 'Order fully paid',
            'asyncEvents': ['ORDER_FULLY_PAID',],
            'query':  GET_ORDER_FULLY_PAID_SUBSCRIPTION,
            'targetUrl': f'{settings.LMS_ROOT_URL}/saleor/webhooks/fulfill-order',
            'isActive': True,
          }
        ]
    }

    return manifest
