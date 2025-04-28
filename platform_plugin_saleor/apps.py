"""
platform_plugin_saleor Django application initialization.
"""

from django.apps import AppConfig
from edx_django_utils.plugins import PluginSettings, PluginSignals, PluginURLs


class PlatformPluginSaleorConfig(AppConfig):
    """
    Configuration for the platform_plugin_saleor Django application.
    """

    name = 'platform_plugin_saleor'

    plugin_app = {
        PluginURLs.CONFIG: {
            "lms.djangoapp": {
                PluginURLs.NAMESPACE: "",
                PluginURLs.REGEX: r"^saleor/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
            "cms.djangoapp": {
                PluginURLs.NAMESPACE: "",
                PluginURLs.REGEX: r"^saleor/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
        },
        PluginSettings.CONFIG: {
            "lms.djangoapp": {
                "production": {PluginSettings.RELATIVE_PATH: "settings.production"},
                "common": {PluginSettings.RELATIVE_PATH: "settings.common"},
            },
            "cms.djangoapp": {
                "production": {PluginSettings.RELATIVE_PATH: "settings.production"},
                "common": {PluginSettings.RELATIVE_PATH: "settings.common"},
            },
        },
        PluginSignals.CONFIG: {
            "cms.djangoapp": {
                PluginSignals.RECEIVERS: [
                    {
                        PluginSignals.RECEIVER_FUNC_NAME: "receive_course_published",
                        PluginSignals.SIGNAL_PATH: (
                            "xmodule.modulestore.django.COURSE_PUBLISHED"
                        ),
                    },
                ],
            },
        }
    }
