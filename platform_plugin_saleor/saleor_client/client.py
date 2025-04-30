"""Saleor API client for managing course products, product types, and attributes.

This module provides the SaleorApiClient class, which interacts with the Saleor GraphQL API
to create and manage product attributes, product types, and course products. It also includes
utility methods for querying product types and attributes.
"""

import json
import logging

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from platform_plugin_saleor.saleor_client.config import EdxCourseOverviewSaleorConfig, SaleorConfig
from platform_plugin_saleor.saleor_client.exceptions import GraphQLError
from platform_plugin_saleor.saleor_client.mutations import (
    ACCOUNT_REGISTER,
    ATTACH_CHECKOUT_CUSTOMER,
    CREATE_CHECKOUT,
    CREATE_COURSE_PRODUCT,
    CREATE_PRODUCT_ATTRIBUTES,
    CREATE_PRODUCT_TYPE,
    CREATE_TOKEN,
    FULLFILL_ORDER,
)
from platform_plugin_saleor.saleor_client.queries import (
    GET_PRODUCT_ATTRIBUTES,
    GET_PRODUCT_TYPES,
    GET_PRODUCT_VARIANT,
    GET_USER,
    GET_WAREHOUSES,
)
from platform_plugin_saleor.saleor_client.utils import (
    ATTRIBUTE_TYPES_MAP,
    clean_edges_and_nodes,
    convert_to_camel_case,
    create_rich_text,
    find_errors,
    format_attribute_value,
    generate_saleor_product_attribute_data,
    get_model_field_type,
)

logger = logging.getLogger(__name__)


class SaleorApiClient:
    """Client for interacting with the Saleor GraphQL API."""

    def __init__(self, base_url: str, token: str, timeout: int = None):
        """
        Initialize the SaleorApiClient.

        Args:
            base_url (str): The Saleor API URL.
            token (str): The Saleor API token.
            timeout (int): Request timeout in seconds.
        """
        self.base_url = base_url
        self.token = token

        transport = AIOHTTPTransport(
            url=self.base_url,
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=timeout,
        )
        self.client = Client(
            transport=transport,
            fetch_schema_from_transport=False,
        )

    def execute(self, query: str, variables: dict):
        """
        Execute a GraphQL query or mutation.

        Args:
            query (str): The GraphQL query or mutation string.
            variables (dict): Variables to pass to the query or mutation.

        Returns:
            dict: The response data from the Saleor API.

        Raises:
            GraphQLError: If the API response contains errors.
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

    def create_product_attributes(self, config: SaleorConfig = None):
        """
        Create product attributes in Saleor using the provided configuration.

        Args:
            config (SaleorConfig, optional): The configuration for product attributes.
                If not provided, uses EdxCourseOverviewSaleorConfig.

        Returns:
            dict: The response data from the Saleor API.

        Raises:
            GraphQLError: If the API response contains errors.
        """
        config = config or EdxCourseOverviewSaleorConfig()

        attributes_data = [
            generate_saleor_product_attribute_data(
                config.model,
                attrb.model_attribute,
                attrb.product_attribute,
            )
            for attrb in config.attributes_mapping
        ]

        variables = {"attributes": attributes_data}
        query = CREATE_PRODUCT_ATTRIBUTES

        return self.execute(query, variables)

    def create_product_type(self, config: SaleorConfig = None):
        """
        Create a product type in Saleor using the provided configuration.

        Args:
            config (SaleorConfig, optional): The configuration for the product type.
                If not provided, uses EdxCourseOverviewSaleorConfig.

        Returns:
            dict: The created product type data.

        Raises:
            ValueError: If the product type already exists.
            GraphQLError: If the API response contains errors.
        """
        config = config or EdxCourseOverviewSaleorConfig()
        type_name = config.product_type_name

        attributes_ids = self.get_attribute_ids()

        if self.get_product_type_id(type_name):
            message = f"Product type '{type_name}' already exists."
            logger.error(message)
            raise ValueError(message)

        variables = {
            "input": {
                "name": type_name,
                "hasVariants": True,
                "isShippingRequired": False,
                "productAttributes": attributes_ids,
            }
        }

        response = self.execute(CREATE_PRODUCT_TYPE, variables)
        product_type = response.get("productTypeCreate", {}).get(
            "productType", {}
        )

        return product_type

    def create_course_product(self, course, config: SaleorConfig = None):
        """
        Create a course product in Saleor based on the given course instance.

        Args:
            course: The course object containing product data.
            config (SaleorConfig, optional): The configuration for the course product.
                If not provided, uses EdxCourseOverviewSaleorConfig.

        Returns:
            dict: The response data from the Saleor API.

        Raises:
            ValueError: If the product type does not exist.
            GraphQLError: If the API response contains errors.
        """
        config = config or EdxCourseOverviewSaleorConfig()
        product_type_id = self.get_product_type_id(config.product_type_name)

        if not product_type_id:
            message = f"Product type '{config.product_type_name}' not found."
            logger.error(message)
            raise ValueError(message)

        query_attributes = []

        for attrb in config.attributes_mapping:
            model_attribute = attrb.model_attribute
            model_attribute_value = getattr(course, model_attribute, None)
            model_attribute_type = get_model_field_type(
                config.model, model_attribute
            )

            product_input_type = ATTRIBUTE_TYPES_MAP.get(
                model_attribute_type, "PLAIN_TEXT"
            )
            product_input_key = convert_to_camel_case(
                product_input_type.lower()
            )

            product_attribute_value = format_attribute_value(
                product_input_key, model_attribute_value
            )

            attribute_input = {
                "externalReference": model_attribute,
                **product_attribute_value,
            }

            query_attributes.append(attribute_input)

        description = create_rich_text(course.short_description)

        variables = {
            "input": {
                "productType": product_type_id,
                "name": str(course.display_name),
                "description": json.dumps(description),
                "attributes": query_attributes,
                "externalReference": str(course.id),
            }
        }

        return self.execute(CREATE_COURSE_PRODUCT, variables)

    def get_attribute_ids(self):
        """
        Retrieve all product attribute IDs from Saleor.

        Returns:
            list: A list of attribute IDs.
        """
        variables = {"limit": 100}
        response = self.execute(GET_PRODUCT_ATTRIBUTES, variables)

        attributes = clean_edges_and_nodes(response.get("attributes", {}))
        attribute_ids = [
            attr.get("id") for attr in attributes if attr.get("id")
        ]

        return attribute_ids

    def get_product_type_id(self, product_type_name: str):
        """
        Retrieve the ID of a product type by its name.

        Args:
            product_type_name (str): The name of the product type.

        Returns:
            str or None: The ID of the product type if found, otherwise None.
        """
        variables = {"limit": 100}
        response = self.execute(GET_PRODUCT_TYPES, variables)
        product_types = clean_edges_and_nodes(response.get("productTypes", {}))

        for product_type in product_types:
            if product_type.get("name") == product_type_name:
                return product_type.get("id")

        return None

    def get_product_variant(self, sku: str) -> dict:
        """
        TO-DO
        """
        variables = {
            "sku": sku,
        }
        return self.execute(GET_PRODUCT_VARIANT, variables)

    def get_user_by_email(self, email) -> dict:
        """
        TO-DO
        """
        variables = {
            "email": email,
        }
        return self.execute(GET_USER, variables)

    def create_checkout(self, email: str, product_variants: list) -> dict:
        """
        TO-DO
        """
        lines = [{"quantity": 1, "variantId": variant["id"]} for variant in product_variants]
        variables = {
            "input": {
                "email": email,
                "lines": lines,
            }
        }
        return self.execute(CREATE_CHECKOUT, variables)

    def attach_customer(self, customer_id: str, checkout_id: str) -> dict:
        """
        TO-DO
        """
        variables = {
            "id": checkout_id,
            "customerId": customer_id,
        }
        return self.execute(ATTACH_CHECKOUT_CUSTOMER, variables)

    def account_register(self, first_name: str, last_name: str, email: str, password: str) -> dict:
        """
        TO-DO
        """
        variables = {
            "input": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "password": password

            }
        }
        return self.execute(ACCOUNT_REGISTER, variables)

    def create_token(self, email: str, password: str) -> dict:
        """
        TO-DO
        """
        variables = {
            "email": email,
            "password": password
        }
        return self.execute(CREATE_TOKEN, variables)

    def get_warehouse_by_name(self, warehouse_name: str = "Default Warehouse"):
        """
        Retrieve the warehouse data by its name.

        Args:
            warehouse_name (str): The name of the warehouse to search for.

        Returns:
            dict or None: The warehouse data if found, otherwise None.
        """
        variables = {"limit": 100}
        response = self.execute(GET_WAREHOUSES, variables)
        warehouses = clean_edges_and_nodes(response.get("warehouses", {}))

        for warehouse in warehouses:
            if warehouse.get("name") == warehouse_name:
                return warehouse

        return None

    def fulfill_order(
        self,
        order_id: str,
        warehouse_id: str,
        lines: list,
        notify_customer: bool = False,
    ):
        """
        Fulfill an order in Saleor.

        Args:
            order_id (str): The ID of the order to fulfill.
            warehouse_id (str): The ID of the warehouse to use for fulfillment.
            lines (list): A list of line items to fulfill.
            notify_customer (bool): Whether to notify the customer.

        Returns:
            dict: The response data from the Saleor API.

        Raises:
            GraphQLError: If the API response contains errors.
        """
        formatted_lines = []

        for line in lines:
            formatted_line = {
                "orderLineId": line.get("id"),
                "stocks": [
                    {
                        "quantity": line.get("quantity", 1),
                        "warehouse": warehouse_id,
                    }
                ],
            }
            formatted_lines.append(formatted_line)

        variables = {
            "input": {
                "lines": formatted_lines,
                "notifyCustomer": notify_customer,
                "allowStockToBeExceeded": True,
            },
            "order": order_id,
        }

        response_data = self.execute(FULLFILL_ORDER, variables)

        return response_data.get("orderFulfill")
