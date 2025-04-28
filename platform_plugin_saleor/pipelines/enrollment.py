"""Course enrollment pipeline for Saleor orders."""

import logging

from common.djangoapps.student.models.course_enrollment import (  # pylint: disable=import-error
    CourseEnrollment,
    CourseEnrollmentException,
)
from django.conf import settings
from django.contrib.auth import get_user_model
from opaque_keys.edx.keys import CourseKey  # pylint: disable=import-error

from platform_plugin_saleor.pipelines.utils import module_member

User = get_user_model()

logger = logging.getLogger(__name__)


def run_course_enrollment_pipeline(order, *args, **kwargs):
    """
    Run the course enrollment pipeline by executing a sequence of functions.
;
    Args:
        order (dict): The order data containing enrollment information.
        *args: Positional arguments passed to each pipeline function.
        **kwargs: Keyword arguments passed to each pipeline function.

    Returns:
        dict: The final accumulated results from the pipeline execution.
    """
    pipeline = settings.COURSE_ENROLLMENT_PIPELINE

    order_lines = order.get("lines", [])
    user = order.get("user", None)

    out = kwargs.copy()
    out.setdefault("order_lines", order_lines)
    out.setdefault("user", user)
    out.setdefault("order", order)

    for name in pipeline:
        func = module_member(name)
        result = func(*args, **out)

        if not isinstance(result, dict):
            logger.error(f"pipeline step {name} did not return a dict: {result}")
            return result

        logger.debug(f"Pipeline step {name} returned: {result}")
        out.update(result)

    return out


def get_lms_user(user, *args, **kwargs):
    """
    Check if the user exists in the LMS.

    Args:
        user (dict): The user information containing email.

    Returns:
        dict: Containing the user instance.
    """

    email = user.get("email")
    user = User.objects.get(email=email)

    return {"user": user}


def get_selected_courses_keys(order_lines, *args, **kwargs):
    """
    Extract course ID and mode from order lines.

    Args:
        order_lines (list): A list of order line items.

    Returns:
        dict: Containing a list of courses with their IDs and modes.
    """

    courses_info = []

    for line in order_lines:
        line_variant = line.get("variant", {})

        course_mode = line_variant.get("name")
        course_id = line_variant.get("product", {}).get("externalReference")

        if not course_id or not course_mode:
            logger.error(f"Missing course ID or mode in order line: {line}")

        course_data = {
            "course_id": course_id,
            "course_mode": course_mode.lower(),
        }

        courses_info.append(course_data)

    logger.debug(f"Extracted {len(courses_info)} courses from order lines.")

    return {"courses": courses_info}


def enroll_user_in_courses(user, courses, *args, **kwargs):
    """
    Enroll the user in the courses.

    Args:
        user (User): The user to enroll.
        courses (list): List of courses with course IDs and modes.

    Returns:
        dict: Indicating success or failure with details.
    """

    for course_data in courses:
        course_id = course_data.get("course_id")
        mode = course_data.get("course_mode")

        try:
            course_key = CourseKey.from_string(course_id)
            CourseEnrollment.enroll(user, course_key, mode)
            logger.info(f"User {user.username} enrolled in course {course_id} with mode {mode}")

        except CourseEnrollmentException as e:
            logger.error(f"Failed to enroll user {user.username} in course {course_id}. Error: {e}")
            return {"success": False, "error": str(e)}

    return {"success": True}
