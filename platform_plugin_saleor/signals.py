"""Signal receiver for LMS and CMS events."""

import logging

from django.conf import settings
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview  # pylint: disable=import-error

from platform_plugin_saleor.saleor_client.client import SaleorApiClient

logger = logging.getLogger(__name__)


def receive_course_published(  # pylint: disable=unused-argument
    sender, course_key, **kwargs
):
    """
    Signal receiver for course publish events.

    Args:
        sender: The sender of the signal.
        course_key: The key of the course being published.
        **kwargs: Additional keyword arguments.
    """
    course = CourseOverview.objects.get(id=course_key)
    client = SaleorApiClient(
        base_url=settings.SALEOR_API_URL,
        token=settings.SALEOR_API_TOKEN,
    )

    product = client.get_product_by_id(str(course.id))

    if product:
        client.update_course_product(course)
    else:
        client.create_course_product(course)
