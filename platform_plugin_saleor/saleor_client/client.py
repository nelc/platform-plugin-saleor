"""Saleor API client for creating course products and attributes."""


import logging

from django.conf import settings
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from platform_plugin_saleor.saleor_client.exceptions import GraphQLError
from platform_plugin_saleor.saleor_client.utils import find_errors

logger = logging.getLogger(__name__)


class SaleorApiClient:
    """Client for interacting with the Saleor GraphQL API."""

    def __init__(self, base_url: str = None, token: str = None, timeout: int = None):
        """
        Initialize the Saleor API client.

        Args:
            base_url: Saleor API URL, defaults to settings.SALEOR_API_URL
            token: Saleor API token, defaults to settings.SALEOR_API_TOKEN
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url or settings.SALEOR_API_URL
        self.token = token or settings.SALEOR_API_TOKEN

        try:
            transport = AIOHTTPTransport(
                url=self.base_url,
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=timeout,
            )
            self.client = Client(
                transport=transport,
                fetch_schema_from_transport=False,
            )
        except Exception as e:
            logger.error(f"Failed to initialize Saleor API client: {str(e)}")
            raise

    def execute(self, query: str, variables: dict):
        """
        Execute a GraphQL query.

        Args:
            query: The GraphQL query string.
            variables: A dictionary of variables for the query.

        Returns:
            The response data from the GraphQL API.

        Raises:
            GraphQLError: If the API returns errors.
        """
        response_data = self.client.execute(
            gql(query),
            variable_values=variables,
        )

        if errors := find_errors(response_data):
            raise GraphQLError(
                errors=errors,
                response_data=response_data,
            )

        return response_data
