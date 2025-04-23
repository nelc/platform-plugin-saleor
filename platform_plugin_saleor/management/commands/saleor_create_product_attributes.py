"""Management command to create product attributes in Saleor for course products."""

import logging

from django.core.management.base import BaseCommand
from gql.transport.aiohttp import log as aiohttp_logger

from platform_plugin_saleor.saleor_client.client import SaleorApiClient
from platform_plugin_saleor.saleor_client.config import EdxCourseOverviewSaleorConfig
from platform_plugin_saleor.saleor_client.exceptions import GraphQLError

aiohttp_logger.setLevel(logging.WARNING)


class Command(BaseCommand):
    """
    Management command to create product attributes in Saleor for course products.

    This command uses the SaleorApiClient to create product attributes required
    for course synchronization, based on the configuration provided by
    EdxCourseOverviewSaleorConfig.
    """

    help = "Create product attributes in Saleor for course products"

    def handle(self, *args, **options):
        """
        Executes the creation of product attributes in Saleor.
        """
        self.stdout.write("Creating product attributes in Saleor...")

        try:
            client = SaleorApiClient()
            config = EdxCourseOverviewSaleorConfig()

            response = client.create_product_attributes(config=config)

            results = response["attributeBulkCreate"]["results"]
            self.stdout.write(f"Successfully created {len(results)} attributes in Saleor")

            for result in results:
                attribute = result["attribute"]
                self.stdout.write(f"  - Created attribute: {attribute['name']} (ID: {attribute['id']})")

            self.stdout.write(self.style.SUCCESS("Successfully created product attributes in Saleor"))

        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

        except GraphQLError as e:
            self.stdout.write(self.style.ERROR(f"{e}"))
