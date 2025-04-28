"""Views for Saleor app integration."""

import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from platform_plugin_saleor.manifest import get_app_manifest
from platform_plugin_saleor.pipelines.enrollment import run_course_enrollment_pipeline

logger = logging.getLogger(__name__)


@csrf_exempt
def get_saleor_app_manifest(request):
    """
    Provide the Saleor app manifest.

    This endpoint returns the application manifest that Saleor uses to register
    and configure the application within its ecosystem.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the application manifest.
    """
    return JsonResponse(get_app_manifest(), safe=True)


@csrf_exempt
def register_saleor_app_token(request):
    """
    Register the authentication token received from Saleor.

    This endpoint receives and stores the authentication token that will be used
    for subsequent API calls to the Saleor API.

    Args:
        request: The HTTP request object containing the auth token.

    Returns:
        JsonResponse: A JSON response indicating the token was successfully received.
    """
    payload = json.loads(request.body.decode("utf-8"))
    token = payload.get("auth_token")
    settings.SALEOR_API_TOKEN = token

    return JsonResponse(
        {"success": True, "message": "Token received successfully."},
        status=200,
    )


@csrf_exempt
def enroll_user_in_courses(request):
    """
    Handle the order fully paid webhook from Saleor.

    This endpoint receives notifications when orders are fully paid in the Saleor system
    and enrolls the user in the specified course.

    Args:
        request: The HTTP request object containing the webhook payload.

    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """

    payload = json.loads(request.body)
    order = payload.get("order", {})

    status = run_course_enrollment_pipeline(order=order)

    if status.get("success") is False:
        return JsonResponse(
            {"success": False, "message": status.get("error")},
            status=400,
        )

    return JsonResponse(
        {"success": True, "message": "Webhook received successfully."},
        status=200,
    )
