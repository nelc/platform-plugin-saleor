"""Django management command to create a product type in Saleor."""

import logging

from django.core.management.base import BaseCommand
from gql.transport.aiohttp import log as aiohttp_logger

from platform_plugin_saleor.saleor_client.client import SaleorApiClient
from platform_plugin_saleor.saleor_client.exceptions import GraphQLError
from platform_plugin_saleor.saleor_client.mutations import CREATE_PRODUCT_TYPE
from platform_plugin_saleor.saleor_client.queries import GET_PRODUCT_ATTRIBUTES, GET_PRODUCT_TYPES
from platform_plugin_saleor.saleor_client.utils import clean_edges_and_nodes, get_product_attributes_configuration

aiohttp_logger.setLevel(logging.WARNING)


class Command(BaseCommand):
    """
    Django management command to create a product type in Saleor.

    This command creates a product type in Saleor and associates it with
    the previously created attributes. The product type name is defined in
    the configuration returned by get_product_attributes_configuration().
    """

    help = "Create a product type in Saleor and associate it with attributes"

    def handle(self, *args, **options):
        """
        Execute the command to create a product type in Saleor.
        """

        config = get_product_attributes_configuration()
        product_type_name = config.get('product_type', 'Course')

        self.stdout.write(f"Creating product type '{product_type_name}' in Saleor...")

        try:
            client = SaleorApiClient()

            product_type_id = self.get_product_type_id(client, product_type_name)

            if product_type_id:
                self.stdout.write(self.style.WARNING(
                    f"Product type '{product_type_name}' already exists - ID: {product_type_id}"))
                return

            attribute_ids = self.get_attribute_ids(client)
            self.stdout.write(f"Found {len(attribute_ids)} attributes to associate with product type")

            self.stdout.write(f"Creating product type with {len(attribute_ids)} attributes...")
            product_type = self.create_product_type(client, product_type_name, attribute_ids)

            if product_type:
                self.stdout.write(self.style.SUCCESS(
                    f"Type '{product_type.get('name')}' created - ID: {product_type.get('id')}"))

        except GraphQLError as e:
            self.stdout.write(self.style.ERROR(f"{e}"))

    def get_attribute_ids(self, client):
        """
        Get attribute IDs from Saleor.

        Args:
            client: The Saleor API client

        Returns:
            list: List of attribute IDs
        """
        variables = {"limit": 100}
        response = client.execute(GET_PRODUCT_ATTRIBUTES, variables)

        attributes = clean_edges_and_nodes(response.get("attributes", {}))
        attribute_ids = [attr.get("id") for attr in attributes if attr.get("id")]

        return attribute_ids

    def get_product_type_id(self, client, product_type_name):
        """
        Get the ID of a product type by its name.

        Args:
            client: The Saleor API client
            product_type_name: The name of the product type

        Returns:
            str or None: The ID of the product type, or None if not found.
        """

        variables = {"limit": 100}
        response = client.execute(GET_PRODUCT_TYPES, variables)
        product_types = clean_edges_and_nodes(response.get("productTypes", {}))

        for product_type in product_types:
            if product_type.get("name") == product_type_name:
                return product_type.get("id")

        return None

    def create_product_type(self, client, product_type_name, attribute_ids):
        """
        Create a product type in Saleor.

        Args:
            client: The Saleor API client
            product_type_name: The name of the product type
            attribute_ids: List of attribute IDs to associate with the product type
        """

        variables = {
            "input": {
                "name": product_type_name,
                "hasVariants": True,
                "isShippingRequired": False,
                "productAttributes": attribute_ids,
            }
        }

        response = client.execute(CREATE_PRODUCT_TYPE, variables)
        product_type = response.get("productTypeCreate", {}).get("productType", {})

        return product_type
