"""Django management command to synchronize courses from Open edX to Saleor e-commerce platform."""


import logging

from django.core.management.base import BaseCommand
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview  # pylint: disable=import-error

from platform_plugin_saleor.saleor_client.client import SaleorApiClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Management command to synchronize courses from Open edX to Saleor.

    This command:
    1. Creates base product attributes in Saleor
    2. Creates a course product type
    3. Creates products for all courses in the platform
    """

    help = 'Synchronize Open edX courses with Saleor e-commerce platform'

    def handle(self, *args, **options):
        client = SaleorApiClient()

        self.stdout.write("Creating base product attributes...")
        try:
            client.create_base_product_attributes()
            self.stdout.write(self.style.SUCCESS("Successfully created product attributes"))
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.stdout.write(self.style.ERROR(f"Failed to create product attributes: {e}"))
            return

        self.stdout.write("Creating product type 'Course'...")
        try:
            product_type = client.create_course_product_type(name="Course")
            if not product_type or 'id' not in product_type:
                self.stdout.write(self.style.ERROR("Failed to get product type ID"))
                return

            product_type_id = product_type['id']
            self.stdout.write(self.style.SUCCESS(
                f"Successfully created product type with ID: {product_type_id}"
            ))
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.stdout.write(self.style.ERROR(f"Failed to create product type: {e}"))
            return

        courses = CourseOverview.objects.all()
        total_courses = courses.count()

        self.stdout.write(f"Found {total_courses} courses to synchronize")

        success_count = 0
        error_count = 0

        for index, course in enumerate(courses, 1):
            try:
                self.stdout.write(f"[{index}/{total_courses}] Syncing '{course.display_name}'...")
                client.create_course_product(course, product_type_id)
                success_count += 1
                if index % 10 == 0 or index == total_courses:
                    self.stdout.write(self.style.SUCCESS(
                        f"Progress: {index}/{total_courses} courses processed"
                    ))
            except Exception as e:  # pylint: disable=broad-exception-caught
                error_count += 1
                self.stdout.write(self.style.ERROR(
                    f"Failed to sync course {course.id}: {e}"
                ))

        self.stdout.write(self.style.SUCCESS(
            f"Completed synchronization: {success_count} succeeded, {error_count} failed"
        ))
