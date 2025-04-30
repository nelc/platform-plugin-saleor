"""Common Django settings for the Saleor project."""


def plugin_settings(settings):
    """Update the common settings for the Saleor project."""

    settings.COURSE_ENROLLMENT_PIPELINE = [
        "platform_plugin_saleor.webhooks.fulfillment.pipeline.get_lms_user",
        "platform_plugin_saleor.webhooks.fulfillment.pipeline.get_selected_courses_keys",
        "platform_plugin_saleor.webhooks.fulfillment.pipeline.enroll_user_in_courses",
        "platform_plugin_saleor.webhooks.fulfillment.pipeline.update_order_fulfillment",
    ]
