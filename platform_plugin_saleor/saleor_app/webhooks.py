"""Webhook handlers for Saleor events."""

import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
