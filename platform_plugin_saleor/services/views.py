"""
TO-DO
"""
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect

from platform_plugin_saleor.saleor_client.client import SaleorApiClient


def checkout(request):
    """
    Basic view that creates a Saleor checkout record and redirects to the storefront checkout page.
    """
    client = SaleorApiClient(
        base_url=settings.SALEOR_API_URL,
        token=settings.SALEOR_API_TOKEN,
    )
    skus = request.GET.getlist("sku", [])
    product_variant = client.get_product_variant(sku=skus[0])["productVariant"]
    user = request.user

    if not product_variant or not user:
        raise Http404

    checkout_response = client.create_checkout(
        email=user.email,
        product_variant=product_variant["id"],
    )["checkoutCreate"]["checkout"]

    # Hard coded value, this will be replace after defining the openedx storefront implementation.
    response = redirect(f"http://saleor-storefront.local.overhang.io:18020/checkout?checkout={checkout_response['id']}")

    return response
