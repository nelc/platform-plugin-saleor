"""
TO-DO
"""
from functools import cache

from common.djangoapps.student.models.user import anonymous_id_for_user  # pylint: disable=import-error
from django.conf import settings

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
            password=generate_password(user=user),
        )["accountRegister"]["user"]

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


def generate_password(user):
    """
    TO-DO
    """
    return anonymous_id_for_user(user, None)
