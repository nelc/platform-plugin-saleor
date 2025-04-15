"""Utility functions for Saleor GraphQL client."""


def format_course_attribute_to_string(attribute: dict) -> str:
    """
    Format a course attribute dictionary into a GraphQL string.

    Args:
        attribute: Dictionary containing attribute details

    Returns:
        str: Formatted GraphQL attribute string
    """
    return f"""
    {{
        name: "{attribute["name"]}",
        externalReference: "{attribute["model_reference"]}",
        type: {attribute["type"]},
        inputType: {attribute["input_type"]}
    }}
    """


def clean_edges_and_nodes(response: dict) -> list[dict]:
    """
    Clean the edges and nodes from the GraphQL response.

    Args:
        response: The response from the GraphQL query

    Returns:
        list: A list of cleaned nodes
    """
    cleaned_data = []
    edges = response.get("edges", [])

    for edge in edges:
        node = edge.get("node", {})
        if node:
            cleaned_data.append(node)

    return cleaned_data


def convert_to_camel_case(snake_str: str) -> str:
    """
    Convert snake_case string to camelCase.

    Args:
        snake_str: The snake_case string

    Returns:
        str: The camelCase string
    """
    snake_str = snake_str.lower()
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


COURSE_ATTRIBUTES_DICT: list[dict] = [
    {
        "name": "Course ID",
        "model_reference": "id",
        "type": "PRODUCT_TYPE",
        "input_type": "PLAIN_TEXT",
    },
    {
        "name": "Banner Image URL",
        "model_reference": "banner_image_url",
        "type": "PRODUCT_TYPE",
        "input_type": "PLAIN_TEXT",
    },
    {
        "name": "Course Image URL",
        "model_reference": "course_image_url",
        "type": "PRODUCT_TYPE",
        "input_type": "PLAIN_TEXT",
    },
    {
        "name": "Course Start Date",
        "model_reference": "start",
        "type": "PRODUCT_TYPE",
        "input_type": "DATE_TIME",
    },
    {
        "name": "Course End Date",
        "model_reference": "end",
        "type": "PRODUCT_TYPE",
        "input_type": "DATE_TIME",
    },
    {
        "name": "Enrollment Start Date",
        "model_reference": "enrollment_start",
        "type": "PRODUCT_TYPE",
        "input_type": "DATE_TIME",
    },
    {
        "name": "Enrollment End Date",
        "model_reference": "enrollment_end",
        "type": "PRODUCT_TYPE",
        "input_type": "DATE_TIME",
    },
    {
        "name": "Self Paced",
        "model_reference": "self_paced",
        "type": "PRODUCT_TYPE",
        "input_type": "BOOLEAN",
    },
    {
        "name": "Mobile Available",
        "model_reference": "mobile_available",
        "type": "PRODUCT_TYPE",
        "input_type": "BOOLEAN",
    },
    {
        "name": "Certificate Name",
        "model_reference": "cert_name_long",
        "type": "PRODUCT_TYPE",
        "input_type": "PLAIN_TEXT",
    },
    {
        "name": "Lowest Passing Grade",
        "model_reference": "lowest_passing_grade",
        "type": "PRODUCT_TYPE",
        "input_type": "PLAIN_TEXT",
    },
    {
        "name": "Invitation Only",
        "model_reference": "invitation_only",
        "type": "PRODUCT_TYPE",
        "input_type": "BOOLEAN",
    },
    {
        "name": "Max Student Enrollments Allowed",
        "model_reference": "max_student_enrollments_allowed",
        "type": "PRODUCT_TYPE",
        "input_type": "NUMERIC",
    },
    {
        "name": "Eligible For Financial Aid",
        "model_reference": "eligible_for_financial_aid",
        "type": "PRODUCT_TYPE",
        "input_type": "BOOLEAN",
    },
    {
        "name": "Organization",
        "model_reference": "org",
        "type": "PRODUCT_TYPE",
        "input_type": "PLAIN_TEXT",
    },
    {
        "name": "Language",
        "model_reference": "language",
        "type": "PRODUCT_TYPE",
        "input_type": "PLAIN_TEXT",
    },
    {
        "name": "Entrance Exam Minimum Score Percentage",
        "model_reference": "entrance_exam_minimum_score_pct",
        "type": "PRODUCT_TYPE",
        "input_type": "NUMERIC",
    },
]
