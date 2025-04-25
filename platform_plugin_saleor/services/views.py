"""
TO-DO
"""
from django.http import Http404
from django.shortcuts import redirect

from platform_plugin_saleor.services.helpers import create_user_checkout, get_or_create_saleor_user, get_product_variant


def checkout(request):
    """
    Basic view that creates a Saleor checkout record and redirects to the storefront checkout page.
    """
    skus = request.GET.getlist("sku", [])
    product_variant = get_product_variant(sku=skus[0])
    saleor_user = get_or_create_saleor_user(request.user)

    if not product_variant or not saleor_user:
        raise Http404

    checkout_response = create_user_checkout(saleor_user=saleor_user, product_variants=[product_variant])

    # Hard coded value, this will be replace after defining the openedx storefront implementation.
    response = redirect(f"http://saleor-storefront.local.overhang.io:18020/checkout?checkout={checkout_response['id']}")

    return response
