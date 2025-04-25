"""
TO-DO
"""
import os
import time
from base64 import b64encode
from functools import cache

from django.conf import settings
from hashids import Hashids

from platform_plugin_saleor.saleor_client.client import SaleorApiClient


def get_saleor_api_client_instance():
    """
    TO-DO
    """
    @cache
    def generate_api_client(base_url: str, token: str):
        """
        TO-DO
        """
        return SaleorApiClient(
            base_url=base_url,
            token=token,
        )

    return generate_api_client(
        base_url=settings.SALEOR_API_URL,
        token=settings.SALEOR_API_TOKEN,
    )


def get_or_create_saleor_user(user) -> dict:
    """
    TO-DO
    """
    client = get_saleor_api_client_instance()
    saleor_user = client.get_user_by_email(user.email)["user"]

    if not saleor_user:
        saleor_user = client.account_register(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=generate_password(),
        )["accountRegister"]

    return saleor_user


def create_user_checkout(saleor_user: dict, product_variants) -> dict:
    """
    TO-DO
    """
    client = get_saleor_api_client_instance()
    checkout = client.create_checkout(
        email=saleor_user["email"],
        product_variants=product_variants,
    )["checkoutCreate"]["checkout"]

    checkout = client.attach_customer(customer_id=saleor_user["id"], checkout_id=checkout["id"])

    return checkout["checkoutCustomerAttach"]["checkout"]


def get_product_variant(sku: str) -> dict:
    """
    TO-DO
    """
    return get_saleor_api_client_instance().get_product_variant(sku=sku)["productVariant"]


def generate_password():
    """
    TO-DO
    """
    salt = b64encode(os.urandom(16)).decode('utf-8')
    hashids = Hashids(salt=salt, min_length=11)

    return hashids.encode(int(time.time()))
