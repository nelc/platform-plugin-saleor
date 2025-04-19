"""Django management command to create course products in Saleor."""

import json
import logging
from datetime import datetime

from django.core.management.base import BaseCommand
from gql.transport.aiohttp import log as aiohttp_logger
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview  # pylint: disable=import-error

from platform_plugin_saleor.saleor_client.client import SaleorApiClient
from platform_plugin_saleor.saleor_client.exceptions import GraphQLError
from platform_plugin_saleor.saleor_client.mutations import CREATE_COURSE_PRODUCT
from platform_plugin_saleor.saleor_client.queries import GET_PRODUCT_TYPES
from platform_plugin_saleor.saleor_client.utils import (
    ATTRIBUTE_TYPES_MAP,
    clean_edges_and_nodes,
    convert_to_camel_case,
    get_model_field_type,
    get_product_attributes_configuration,
)

aiohttp_logger.setLevel(logging.WARNING)


class Command(BaseCommand):
    """Command to create course products in Saleor."""

    help = "Creates course products in Saleor from CourseOverview models"

    def add_arguments(self, parser):
        parser.add_argument(
            "course_ids",
            nargs="*",
            type=str,
            help="List of course IDs to process",
        )
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="Process all available courses",
        )

    def handle(self, *args, **options):
        course_ids = options.get("course_ids")
        process_all = options.get("all")

        if not course_ids and not process_all:
            self.stdout.write(
                self.style.ERROR(
                    "Please specify course IDs or use --all to process all courses."
                )
            )
            return

        client = SaleorApiClient()

        config = get_product_attributes_configuration()
        product_type_name = config["product_type"]

        product_type_id = self.get_product_type_id(client, product_type_name)
        self.stdout.write(f"Found Product type {product_type_name} - ID: {product_type_id}")

        if course_ids:
            self.stdout.write(f"Fetching specific courses: {', '.join(course_ids)}")
            courses = CourseOverview.objects.filter(id__in=course_ids)

            if not courses:
                self.stdout.write(
                    self.style.WARNING("No courses found for those IDs."))
                return

        if process_all:
            courses = CourseOverview.objects.all()

        self.stdout.write(f"Found {courses.count()} courses to process")

        for course in courses:
            try:
                self.create_course_product(client, course, product_type_id)
                self.stdout.write(
                    self.style.SUCCESS(f"Created product for course: {course.id}"))

            except GraphQLError as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating product for course {course.id}: {str(e)}"))

    def create_course_product(self, client, course, product_type_id):
        """Create a course product in Saleor."""

        config = get_product_attributes_configuration()

        attributes = []
        for attr_config in config["attributes"]:
            model_attribute = attr_config["model_attribute"]
            value = getattr(course, model_attribute, None)

            field_type = get_model_field_type(CourseOverview, model_attribute)
            input_type = ATTRIBUTE_TYPES_MAP.get(field_type, "PLAIN_TEXT")
            input_key = convert_to_camel_case(input_type.lower())

            attribute_input = {"externalReference": model_attribute}
            formatted_value = self.format_attribute_value(input_key, value)
            attribute_input.update(formatted_value)

            attributes.append(attribute_input)

        description = self.create_rich_text(course.short_description)

        variables = {
            "input": {
                "productType": product_type_id,
                "name": str(course.display_name),
                "description": json.dumps(description),
                "attributes": attributes,
            }
        }

        return client.execute(CREATE_COURSE_PRODUCT, variables)

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

    def create_rich_text(self, text: str = "No description"):
        """Create a rich text block."""
        return {"blocks": [{"type": "paragraph", "data": {"text": text}}]}

    def format_attribute_value(self, input_key, value):
        """
        Format an attribute value based on its input type.

        Args:
            input_key (str): The input key type (boolean, dateTime, numeric, plainText)
            value: The value to format

        Returns:
            dict: A dictionary with the formatted value for the given input type
        """
        if input_key == 'boolean':
            return {'boolean': bool(value)}
        elif input_key == 'dateTime':
            if value and isinstance(value, datetime):
                return {'dateTime': value.isoformat()}
            else:
                return {'dateTime': None}
        elif input_key == 'numeric':
            return {'numeric': str(value) if value is not None else '0'}
        else:
            return {'plainText': str(value) if value is not None else ''}
