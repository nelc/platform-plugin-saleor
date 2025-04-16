import json
import logging

from django.http import JsonResponse

from platform_plugin_saleor.saleor_app.manifest import get_app_manifest

logger = logging.getLogger(__name__)


def get_saleor_app_manifest(request):
    """Provide the Saleor app manifest."""

    return JsonResponse(get_app_manifest(), safe=True)


def register_saleor_app_token(request):
    payload = json.loads(request.body.decode("utf-8"))
    token = payload.get("token")

    logger.info(f"Received token: {token}")

    return JsonResponse(
        {"success": True, "message": "Token received successfully."},
        status=200,
    )
