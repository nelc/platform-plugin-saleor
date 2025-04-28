"""Common Django settings for the Saleor project."""


def plugin_settings(settings):
    """Update the common settings for the Saleor project."""

    settings.COURSE_ENROLLMENT_PIPELINE = [
        "platform_plugin_saleor.pipelines.enrollment.get_lms_user",
        "platform_plugin_saleor.pipelines.enrollment.get_selected_courses_keys",
        "platform_plugin_saleor.pipelines.enrollment.enroll_user_in_courses",
    ]
