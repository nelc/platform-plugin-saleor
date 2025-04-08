"""Generic views for the platform plugin saleor."""

from os.path import dirname, realpath
from subprocess import CalledProcessError, check_output

from django.http import JsonResponse

import platform_plugin_saleor


def info_view(request):
    """
    Provide basic information about the plugin.

    This view returns a JSON response with the version of the plugin and the git commit hash.
    """
    try:
        working_dir = dirname(realpath(__file__))
        git_data = check_output(["git", "rev-parse", "HEAD"], cwd=working_dir)
        git_data = git_data.decode().rstrip('\r\n')
    except CalledProcessError:
        git_data = ""
    response_data = {
        "version": platform_plugin_saleor.__version__,
        "name": "platform-plugin-saleor",
        "git": git_data
    }
    return JsonResponse(response_data)
