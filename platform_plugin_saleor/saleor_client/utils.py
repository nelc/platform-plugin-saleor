"""Utility functions for Saleor GraphQL client."""

ATTRIBUTE_TYPES_MAP = {
    'TextField': 'PLAIN_TEXT',
    'CharField': 'PLAIN_TEXT',
    'DateField': 'DATE',
    'DateTimeField': 'DATE_TIME',
    'BooleanField': 'BOOLEAN',
    'IntegerField': 'NUMERIC',
    'DecimalField': 'NUMERIC',
    'FloatField': 'NUMERIC',
}


def generate_saleor_product_attribute_data(
    model_cls, model_field: str, product_attrb_name: str
) -> dict:
    """
    Generate the data structure for a Saleor product attribute based on a model field.

    Args:
        model_cls: The Django model class.
        model_field: The name of the field in the model.
        product_attrb_name: The desired name for the Saleor product attribute.

    Returns:
        dict: A dictionary representing the Saleor attribute data.
    """
    model_field_type = get_model_field_type(model_cls, model_field)
    input_type = ATTRIBUTE_TYPES_MAP.get(model_field_type, "PLAIN_TEXT")

    return {
        'name': product_attrb_name,
        'externalReference': model_field,
        'type': 'PRODUCT_TYPE',
        'inputType': input_type,
    }


def get_model_field_type(model_cls, field_name: str) -> str:
    """
    Get the internal type name of a field in a Django model.

    Args:
        model_cls: The Django model class.
        field_name: The name of the field.

    Returns:
        str: The internal type name of the field (e.g., 'CharField', 'DateTimeField').

    Raises:
        ValueError: If the field does not exist in the model.
    """
    try:
        field = model_cls._meta.get_field(field_name)
        return field.get_internal_type()

    except AttributeError as exc:
        raise ValueError(
            f"Field '{field_name}' does not exist in model '{model_cls.__name__}'."
        ) from exc


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


def find_errors(response_data: dict):
    """
    Recursively search for a key named 'errors' in a dictionary or list of dictionaries.

    Args:
        data: The dictionary or list to search within.

    Returns:
        The value associated with the first non-empty 'errors' key found, or None if not found.
    """
    if isinstance(response_data, dict):
        if "errors" in response_data and response_data["errors"]:
            return response_data["errors"]
        for _, value in response_data.items():
            errors = find_errors(value)
            if errors:
                return errors
    elif isinstance(response_data, list):
        for item in response_data:
            errors = find_errors(item)
            if errors:
                return errors
    return None


def get_product_attributes_configuration() -> dict:
    """
    Returns the configuration for mapping CourseOverview attributes to Saleor product attributes.

    This defines which fields from the CourseOverview model should be mapped
    to which Saleor product attributes and their names.

    Returns:
        dict: A dictionary containing the product type name and a list of attribute mappings.
    """

    return {
        'product_type': 'Course',
        'attributes': [
            {
                'model_attribute': 'id',
                'product_attribute': 'Course ID'
            },
            {
                'model_attribute': 'banner_image_url',
                'product_attribute': 'Banner Image URL',
            },
            {
                'model_attribute': 'course_image_url',
                'product_attribute': 'Course Image URL',
            },
            {
                'model_attribute': 'start',
                'product_attribute': 'Course Start Date',
            },
            {
                'model_attribute': 'end',
                'product_attribute': 'Course End Date'
            },
            {
                'model_attribute': 'enrollment_start',
                'product_attribute': 'Enrollment Start Date',
            },
            {
                'model_attribute': 'enrollment_end',
                'product_attribute': 'Enrollment End Date',
            },
            {
                'model_attribute': 'self_paced',
                'product_attribute': 'Self Paced',
            },
            {
                'model_attribute': 'mobile_available',
                'product_attribute': 'Mobile Available',
            },
            {
                'model_attribute': 'cert_name_long',
                'product_attribute': 'Certificate Name',
            },
            {
                'model_attribute': 'lowest_passing_grade',
                'product_attribute': 'Lowest Passing Grade',
            },
            {
                'model_attribute': 'invitation_only',
                'product_attribute': 'Invitation Only',
            },
            {
                'model_attribute': 'max_student_enrollments_allowed',
                'product_attribute': 'Max Student Enrollments Allowed',
            },
            {
                'model_attribute': 'eligible_for_financial_aid',
                'product_attribute': 'Eligible For Financial Aid',
            },
            {
                'model_attribute': 'org',
                'product_attribute': 'Organization'
            },
            {
                'model_attribute': 'language',
                'product_attribute': 'Language'
            },
            {
                'model_attribute': 'entrance_exam_minimum_score_pct',
                'product_attribute': 'Entrance Exam Minimum Score Percentage',
            },
        ],
    }
