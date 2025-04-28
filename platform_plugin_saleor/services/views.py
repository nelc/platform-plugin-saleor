"""
TO-DO
"""
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect

from platform_plugin_saleor.services.helpers import (
    create_user_checkout,
    generate_password,
    get_or_create_saleor_user,
    get_product_variant,
    get_saleor_api_client_instance,
)


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
    response = redirect(f"http://local.overhang.io:18055/checkout?checkout={checkout_response['id']}")

    return response


def authenticate(request):
    """
    TO-DO
    """
    user = request.user
    client = get_saleor_api_client_instance()

    token = client.create_token(
        email=user.email,
        password=generate_password(user),
    )["tokenCreate"]["token"]

    response = HttpResponse()
    response.set_cookie("openedxSaleorToken", token, domain=settings.SESSION_COOKIE_DOMAIN)

    next_url = request.GET.get('next')

    if next_url:
        response['Location'] = next_url
        response.status_code = 302

    return response
