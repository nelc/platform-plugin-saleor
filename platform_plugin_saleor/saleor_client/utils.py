"""Utility functions for Saleor GraphQL client."""

from datetime import datetime

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
    model_cls, model_field: str, product_attr_name: str
) -> dict:
    """
    Build a Saleor product attribute data dictionary from a Django model field.

    Args:
        model_cls: Django model class containing the field.
        model_field: Name of the field in the model.
        product_attrb_name: Name to use for the Saleor product attribute.

    Returns:
        dict: Saleor attribute data with keys: name, externalReference, type, inputType, slug.
    """
    model_field_type = get_model_field_type(model_cls, model_field)
    input_type = ATTRIBUTE_TYPES_MAP.get(model_field_type, "PLAIN_TEXT")

    return {
        'name': product_attr_name,
        'externalReference': model_field,
        'type': 'PRODUCT_TYPE',
        'inputType': input_type,
        'slug': convert_to_camel_case(model_field),
    }


def get_model_field_type(model_cls, field_name: str) -> str:
    """
    Return the internal Django type name for a given model field.

    Args:
        model_cls: Django model class.
        field_name: Name of the field to inspect.

    Returns:
        str: Internal type name (e.g., 'CharField', 'DateTimeField').

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
    Extract and return the list of nodes from a GraphQL response with an 'edges' structure.

    Args:
        response: GraphQL response dictionary containing an 'edges' key.

    Returns:
        list[dict]: List of node dictionaries extracted from the response.
    """
    cleaned_data = []
    edges = response.get("edges", [])

    for edge in edges:
        if node := edge.get("node", {}):
            cleaned_data.append(node)

    return cleaned_data


def convert_to_camel_case(snake_str: str) -> str:
    """
    Convert a snake_case string to camelCase.

    Args:
        snake_str: String in snake_case format.

    Returns:
        str: String converted to camelCase.
    """
    snake_str = snake_str.lower()
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def create_rich_text(text: str = "No description"):
    """
    Create a Saleor-compatible rich text block with the given text.

    Args:
        text: Text to include in the rich text block.

    Returns:
        dict: Rich text block dictionary.
    """
    return {"blocks": [{"type": "paragraph", "data": {"text": text}}]}


def format_attribute_value(product_input_key: str, value) -> dict:
    """
    Format a value for a Saleor product attribute based on its input type.

    Args:
        product_input_key (str): Attribute input type ('boolean', 'dateTime', 'numeric', 'plainText').
        value: Value to format.

    Returns:
        dict: Dictionary with the formatted value for the given input type.
    """
    if product_input_key == 'boolean':
        return {'boolean': bool(value)}
    elif product_input_key == 'dateTime':
        if value and isinstance(value, datetime):
            return {'dateTime': value.isoformat()}
        else:
            return {'dateTime': None}
    elif product_input_key == 'numeric':
        return {'numeric': str(value) if value is not None else '0'}
    else:
        return {'plainText': str(value) if value is not None else ''}


def find_errors(response_data: dict):
    """
    Recursively search for and return the first non-empty 'errors' key in a nested dictionary or list.

    Args:
        response_data: Dictionary or list to search for 'errors'.

    Returns:
        Any: Value of the first found non-empty 'errors' key, or None if not found.
    """
    if isinstance(response_data, dict):
        if "errors" in response_data and response_data["errors"]:
            return response_data["errors"]
        for value in response_data.values():
            errors = find_errors(value)
            if errors:
                return errors
    elif isinstance(response_data, list):
        for item in response_data:
            if errors := find_errors(item):
                return errors
    return None
