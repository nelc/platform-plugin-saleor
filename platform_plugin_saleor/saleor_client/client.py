"""Saleor API client for creating course products and attributes."""


import logging

from django.conf import settings
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview  # pylint: disable=import-error

from platform_plugin_saleor.saleor_client.mutations import (
    create_course_product_mutation,
    create_product_attributes_mutation,
    create_product_type_mutation,
)
from platform_plugin_saleor.saleor_client.queries import get_attributes_ids_query
from platform_plugin_saleor.saleor_client.utils import COURSE_ATTRIBUTES_DICT, clean_edges_and_nodes

logger = logging.getLogger(__name__)


class SaleorApiClient:
    """Client for interacting with the Saleor GraphQL API."""

    def __init__(self, base_url: str = None, token: str = None):
        """
        Initialize the Saleor API client.

        Args:
            base_url: Saleor API URL, defaults to settings.SALEOR_API_URL
            token: Saleor API token, defaults to settings.SALEOR_API_TOKEN
        """
        self.base_url = base_url or settings.SALEOR_API_URL
        self.token = token or settings.SALEOR_API_TOKEN

        try:
            transport = AIOHTTPTransport(
                url=self.base_url,
                headers={"Authorization": f"Bearer {self.token}"},
            )
            self.client = Client(
                transport=transport,
                fetch_schema_from_transport=False,
            )
        except Exception as e:
            logger.error(f"Failed to initialize Saleor API client: {str(e)}")
            raise

    def create_base_product_attributes(self) -> dict:
        """
        Create course product attributes in Saleor.

        Returns:
            dict: Response from Saleor API
        """
        try:
            query = create_product_attributes_mutation(COURSE_ATTRIBUTES_DICT)
            response = self.client.execute(gql(query))
            return response
        except Exception as e:
            logger.error(f"Failed to create course product attributes: {str(e)}")
            raise

    def get_base_product_attributes_ids(self, limit: int = 50) -> list[dict]:
        """
        Get attribute IDs from Saleor.

        Args:
            limit: Maximum number of attributes to retrieve

        Returns:
            list: List of attribute objects with id and name
        """
        try:
            query = get_attributes_ids_query(limit)
            response = self.client.execute(gql(query))

            attributes = response.get("attributes", {})
            return clean_edges_and_nodes(attributes)
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(f"Failed to get attribute IDs: {str(e)}")
            return []

    def create_course_product_type(self, name: str = "Course") -> dict:
        """
        Create a course product type in Saleor.

        Args:
            name: Name of the product type

        Returns:
            dict: Product type data
        """
        try:
            attributes = self.get_base_product_attributes_ids()
            if not attributes:
                logger.warning("No attributes found to create product type")
                return {}

            attribute_ids = [attribute['id'] for attribute in attributes]
            query = create_product_type_mutation(name, attribute_ids)
            response = self.client.execute(gql(query))

            return response.get("productTypeCreate", {}).get("productType", {})
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(f"Failed to create course product type: {str(e)}")
            return {}

    def create_course_product(self,
                              course: CourseOverview,
                              product_type: str) -> dict:
        """
        Create a course product in Saleor.

        Args:
            course: Course to create a product for
            product_type: ID of the product type to use

        Returns:
            dict: Response from product creation
        """
        try:
            query = create_course_product_mutation(course, product_type)
            response = self.client.execute(gql(query))
            logger.info(f"Created product for course {course.id}")
            return response
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(f"Failed to create course product: {str(e)}")
            return {}
