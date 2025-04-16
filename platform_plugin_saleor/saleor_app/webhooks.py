import json
import logging

from django.http import JsonResponse


logger = logging.getLogger(__name__)

def order_created_webhook(request):
    """
    Handle the order created webhook from Saleor.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
        logger.info(f"Received order created webhook: {json.dumps(payload, indent=2)}")

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
