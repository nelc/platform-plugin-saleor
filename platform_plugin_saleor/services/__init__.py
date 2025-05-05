"""
"""
from urllib.parse import urlencode, urljoin

import waffle
from common.djangoapps.course_modes.models import CourseMode
from crum import get_current_user
from django.conf import settings
from django.urls import reverse
from lms.djangoapps.commerce.models import CommerceConfiguration
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers

from platform_plugin_saleor.services.helpers import get_saleor_api_client_instance


def is_account_activation_requirement_disabled():
    """
    Checks to see if the django-waffle switch for disabling the account activation requirement is active

    Returns:
        Boolean value representing switch status
    """
    switch_name = configuration_helpers.get_value(
        'DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH',
        settings.DISABLE_ACCOUNT_ACTIVATION_REQUIREMENT_SWITCH
    )
    return waffle.switch_is_active(switch_name)


class SaleorService:
    """ Helper class for ecommerce service integration. """

    def __init__(self):
        self.client = get_saleor_api_client_instance()
        self.config = CommerceConfiguration.current()

    @property
    def ecommerce_url_root(self):
        """ Retrieve Ecommerce service public url root. """
        return configuration_helpers.get_value('SALEOR_STOREFRONT_HOST', settings.SALEOR_STOREFRONT_HOST)

    def get_absolute_ecommerce_url(self, ecommerce_page_url):
        """ Return the absolute URL to the ecommerce page.

        Args:
            ecommerce_page_url (str): Relative path to the ecommerce page.

        Returns:
            Absolute path to the ecommerce page.
        """
        return urljoin(self.ecommerce_url_root, ecommerce_page_url)

    def get_order_dashboard_url(self):
        """ Return the URL to the ecommerce dashboard orders page.

        Returns:
            String: order dashboard url.
        """
        return configuration_helpers.get_value('SALEOR_DASHBOARD_HOST', settings.SALEOR_DASHBOARD_HOST)

    def get_receipt_page_url(self, order_number):
        """
        Gets the URL for the Order Receipt page hosted by the ecommerce service.

        Args:
            order_number (str): Order number.

        Returns:
            Receipt page for the specified Order.
        """

        return self.get_absolute_ecommerce_url(CommerceConfiguration.DEFAULT_RECEIPT_PAGE_URL + order_number)

    def is_enabled(self, user):
        """
        Determines the availability of the EcommerceService based on user activation and service configuration.
        Note: If the user is anonymous we bypass the user activation gate and only look at the service config.

        Returns:
            Boolean
        """
        user_is_active = user.is_active or is_account_activation_requirement_disabled()
        allow_user = user_is_active or user.is_anonymous
        return allow_user

    def payment_page_url(self):
        """ Return the URL for the checkout page.

        Example:
            http://localhost:8002/basket/add/
        """
        return self.get_absolute_ecommerce_url(self.config.basket_checkout_page)

    def get_add_to_basket_url(self):
        """ Return the URL for the payment page based on the waffle switch.

        Example:
            http://localhost/enabled_service_api_path
        """
        return self.payment_page_url()

    def get_checkout_page_url(self, *skus, **kwargs):
        """ Construct the URL to the ecommerce checkout page and include products.

        Args:
            skus (list): List of SKUs associated with products to be added to basket
            program_uuid (string): The UUID of the program, if applicable

        Returns:
            Absolute path to the ecommerce checkout page showing basket that contains specified products.

        Example:
            http://localhost:8002/basket/add/?sku=5H3HG5&sku=57FHHD
            http://localhost:8002/basket/add/?sku=5H3HG5&sku=57FHHD&bundle=3bdf1dd1-49be-4a15-9145-38901f578c5a
        """
        skus = "".join([f"sku={sku}" for sku in skus])
        return f'{reverse("saleor-services:checkout")}?{skus}'

    def upgrade_url(self, user, course_key):
        """
        Returns the URL for the user to upgrade, or None if not applicable.
        """
        verified_mode = CourseMode.verified_mode_for_course(course_key)
        if verified_mode:
            if self.is_enabled(user):
                return self.get_checkout_page_url(verified_mode.sku)
            else:
                return reverse('dashboard')
        return None
