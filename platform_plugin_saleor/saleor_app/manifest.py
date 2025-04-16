"""Defines the manifest for the Saleor app."""

from django.conf import settings

def get_app_manifest():
    manifest = {
        'id': 'platform.plugin.saleor',
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
        'configurationUrl': f'{settings.LMS_ROOT_URL}/api/configuration',
        'tokenTargetUrl': f'{settings.LMS_ROOT_URL}/api/register',

        'dataPrivacy': 'Lorem ipsum',
        'brand': {
          'logo': {
            'default': f'{settings.DEFAULT_EMAIL_LOGO_URL}'
          }
        },
        'webhooks': [
          {
            'name': 'Order created',
            'asyncEvents': ['ORDER_CREATED'],
            'query': 'subscription { event { ... on OrderCreated { order { id number status } } } }',
            'targetUrl': f'{settings.LMS_ROOT_URL}/api/webhooks/order-created',
            'isActive': True,
          },
        ]
    }

    return manifest
