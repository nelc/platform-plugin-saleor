"""Django management command to create Saleor products for Open edX courses."""

import logging

from django.core.management.base import BaseCommand
from gql.transport.aiohttp import log as aiohttp_logger
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview  # pylint: disable=import-error

from platform_plugin_saleor.saleor_client.client import SaleorApiClient
from platform_plugin_saleor.saleor_client.config import EdxCourseOverviewSaleorConfig
from platform_plugin_saleor.saleor_client.exceptions import GraphQLError

aiohttp_logger.setLevel(logging.WARNING)


class Command(BaseCommand):
    """
    Management command to create Saleor products for Open edX courses.

    Usage:
        - Provide a list of course IDs as positional arguments to create products for specific courses.
        - Use the --all flag to process all courses in the CourseOverview model.

    Example:
        python manage.py saleor_create_course_products course-v1:edX+DemoX+Demo_Course
        python manage.py saleor_create_course_products --all
    """

    help = "Creates Saleor products for courses from CourseOverview models."

    def add_arguments(self, parser):
        """
        Add command-line arguments for the management command.
        """
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
        """
        Execute the command to create Saleor products for courses.
        """
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
        config = EdxCourseOverviewSaleorConfig()

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
                client.create_course_product(course, config)
                self.stdout.write(
                    self.style.SUCCESS(f"Created product for course: {course.id}"))

            except ValueError as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating product for course {course.id}: {str(e)}"))

            except GraphQLError as e:
                self.stdout.write(
                    self.style.ERROR(f"Error creating product for course {course.id}: {str(e)}"))
