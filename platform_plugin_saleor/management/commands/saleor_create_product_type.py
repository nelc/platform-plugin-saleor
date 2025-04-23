"""Django management command to create a product type in Saleor."""

import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from gql.transport.aiohttp import log as aiohttp_logger

from platform_plugin_saleor.saleor_client.client import SaleorApiClient
from platform_plugin_saleor.saleor_client.config import EdxCourseOverviewSaleorConfig
from platform_plugin_saleor.saleor_client.exceptions import GraphQLError

aiohttp_logger.setLevel(logging.WARNING)


class Command(BaseCommand):
    """
    Management command to create a product type in Saleor.

    This command creates a product type in Saleor and associates it with
    attributes as defined in the configuration. The product type name and
    attributes are specified by EdxCourseOverviewSaleorConfig.
    """

    help = "Create a product type in Saleor and associate it with attributes"

    def handle(self, *args, **options):
        """
        Execute the command to create a product type in Saleor.
        """

        try:
            client = SaleorApiClient(
                base_url=settings.SALEOR_API_URL,
                token=settings.SALEOR_API_TOKEN
            )
            config = EdxCourseOverviewSaleorConfig()
            product_type = client.create_product_type(config=config)

            if product_type:
                self.stdout.write(self.style.SUCCESS(
                    f"Type '{product_type.get('name')}' created - ID: {product_type.get('id')}"))

        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"{e}"))

        except GraphQLError as e:
            self.stdout.write(self.style.ERROR(f"{e}"))
