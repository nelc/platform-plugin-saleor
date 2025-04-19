"""Django management command to create product attributes in Saleor."""

import logging

from django.core.management.base import BaseCommand
from gql.transport.aiohttp import log as aiohttp_logger
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview  # pylint: disable=import-error

from platform_plugin_saleor.saleor_client.client import SaleorApiClient
from platform_plugin_saleor.saleor_client.exceptions import GraphQLError
from platform_plugin_saleor.saleor_client.mutations import CREATE_PRODUCT_ATTRIBUTES
from platform_plugin_saleor.saleor_client.utils import (
    generate_saleor_product_attribute_data,
    get_product_attributes_configuration,
)

aiohttp_logger.setLevel(logging.WARNING)


class Command(BaseCommand):
    """
    Django management command to create product attributes in Saleor.

    This command creates the necessary product attributes in Saleor for
    course synchronization, based on the configuration in the utils module.
    """

    help = "Create product attributes in Saleor for course products"

    def handle(self, *args, **options):
        """
        Execute the command to create product attributes in Saleor.
        """
        self.stdout.write("Creating product attributes in Saleor...")

        try:
            client = SaleorApiClient()

            config = get_product_attributes_configuration()
            response = self.create_product_attributes(client, config)

            results = response["attributeBulkCreate"]["results"]
            self.stdout.write(f"Successfully created {len(results)} attributes in Saleor")

            for result in results:
                attribute = result["attribute"]
                self.stdout.write(f"  - Created attribute: {attribute['name']} (ID: {attribute['id']})")

            self.stdout.write(self.style.SUCCESS("Successfully created product attributes in Saleor"))

        except GraphQLError as e:
            self.stdout.write(self.style.ERROR(f"{e}"))

    def create_product_attributes(self, client, config):
        """
        Create product attributes in Saleor.

        Args:
            client: The Saleor API client
            config: The attribute configuration

        Returns:
            dict: The API response
        """
        attributes_data = []

        for attr_config in config["attributes"]:
            model_attribute = attr_config["model_attribute"]
            product_attribute = attr_config["product_attribute"]

            try:
                attribute_data = generate_saleor_product_attribute_data(
                    CourseOverview,
                    model_attribute,
                    product_attribute
                )
                attributes_data.append(attribute_data)
                self.stdout.write(f"  Prepared attribute: {product_attribute}")
            except ValueError as e:
                self.stdout.write(
                    self.style.WARNING(f"  Skipping attribute {model_attribute}: {e}")
                )

        self.stdout.write(f"Creating {len(attributes_data)} attributes in Saleor...")

        variables = {"attributes": attributes_data}
        response = client.execute(CREATE_PRODUCT_ATTRIBUTES, variables)

        return response
