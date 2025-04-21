"""Webhook handlers for Saleor events."""

import json
import logging

from common.djangoapps.student.models.course_enrollment import CourseEnrollment  # pylint: disable=import-error
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from opaque_keys.edx.keys import CourseKey  # pylint: disable=import-error

logger = logging.getLogger(__name__)


@csrf_exempt
def order_updated_webhook(request):
    """
    Handle the order updated webhook from Saleor.

    This endpoint receives notifications when orders are updated in the Saleor system
    and logs the received payload for further processing.

    Args:
        request: The HTTP request object containing the webhook payload.

    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        logger.info(f"Received order UPDATED webhook: {json.dumps(payload, indent=2)}")

        return JsonResponse(
            {"success": True, "message": "Webhook received successfully."},
            status=200,
        )
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON payload: {str(e)}")
        return JsonResponse(
            {"success": False, "message": "Invalid JSON payload."},
            status=400,
        )


@csrf_exempt
def order_paid_webhook(request):
    """
    Handle the order paid webhook from Saleor.

    This endpoint receives notifications when orders are marked as paid in the Saleor system
    and logs the received payload for further processing.

    Args:
        request: The HTTP request object containing the webhook payload.

    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        logger.info(f"Received order PAID webhook: {json.dumps(payload, indent=2)}")

        return JsonResponse(
            {"success": True, "message": "Webhook received successfully."},
            status=200,
        )
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON payload: {str(e)}")
        return JsonResponse(
            {"success": False, "message": "Invalid JSON payload."},
            status=400,
        )


@csrf_exempt
def order_created_webhook(request):
    """
    Handle the order created webhook from Saleor.

    This endpoint receives notifications when new orders are created in the Saleor system
    and enrolls the user in the specified course.

    Args:
        request: The HTTP request object containing the webhook payload.

    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    try:
        User = get_user_model()
        payload = json.loads(request.body.decode("utf-8"))

        order = payload['order']
        email = order['user']['email']
        attributes = order['lines'][0]['variant']['product']['attributes']
        variant = order['lines'][0]['variant']['name']

        logger.info(f"Received order CREATED webhook: {json.dumps(payload, indent=2)}")

        course_id = None
        for attribute in attributes:
            if attribute['attribute']['slug'] == 'course-id':
                course_id = attribute['values'][0]['name']
                break

        logger.info(f"Received order CREATED webhook for user: {email}, course: {course_id}, variant: {variant}")

        user = User.objects.get(email=email)
        course_key = CourseKey.from_string(course_id)
        mode = variant.lower()
        CourseEnrollment.enroll(user, course_key, mode=mode)

        return JsonResponse(
            {"success": True, "message": "Webhook received successfully."},
            status=200,
        )

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON payload: {str(e)}")
        return JsonResponse(
            {"success": False, "message": "Invalid JSON payload."},
            status=400,
        )
