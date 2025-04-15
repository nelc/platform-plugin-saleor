"""Mutations for Saleor GraphQL API """


import json
from datetime import datetime

from platform_plugin_saleor.saleor_client.utils import (
    COURSE_ATTRIBUTES_DICT,
    convert_to_camel_case,
    format_course_attribute_to_string,
)


def create_product_attributes_mutation(attributes: list[dict]) -> str:
    """
    Create a product attributes mutation for Saleor GraphQL API.

    Args:
        attributes: List of attribute dictionaries containing name, model_reference, type and input_type

    Returns:
        str: GraphQL mutation string for creating product attributes
    """
    formatted_attributes = ",\n".join(
        format_course_attribute_to_string(attr) for attr in attributes
    )

    return f"""
    mutation CreateProductAttributes {{
        attributeBulkCreate(attributes: [{formatted_attributes}])
        {{
            results {{
                errors {{ message }}
                attribute {{ id, name }}
            }}
        }}
    }}
    """


def create_product_type_mutation(name: str, attributes_ids: list[str]) -> str:
    """
    Create a product type mutation for Saleor GraphQL API.

    Args:
        name: The name of the product type
        attributes_ids: List of attribute IDs to associate with the product type

    Returns:
        str: GraphQL mutation string for creating a product type
    """
    formatted_ids = ",".join(f'"{attr}"' for attr in attributes_ids)

    return f"""
    mutation CreateProductType {{
        productTypeCreate(input: {{
            name: "{name}",
            hasVariants: false,
            isShippingRequired: false,
            productAttributes: [ {formatted_ids} ],
            }}
        )
        {{
            productType {{ id, name }}
            errors {{ message }}
        }}
    }}
    """


def create_course_product_mutation(course, product_type: str) -> str:
    """
    Create a course product mutation for Saleor GraphQL API.

    Args:
        course: Course object containing the course data
        product_type: ID of the product type to use

    Returns:
        str: GraphQL mutation string for creating a course product
    """
    attributes_strings = []

    for attribute in COURSE_ATTRIBUTES_DICT:
        input_type = convert_to_camel_case(attribute['input_type'])
        value = getattr(course, attribute['model_reference'], None)

        if input_type == 'boolean':
            value = 'true' if value else 'false'
        elif input_type == 'dateTime':
            if value and isinstance(value, datetime):
                value = value.isoformat().replace(' ', 'T')
            value = f'"{value}"' if value else 'null'
        elif input_type == 'numeric':
            value = f'"{value}"' if value is not None else '"0"'
        else:
            value = f'"{value}"' if value is not None else '""'

        attributes_strings.append(
            f"""
            {{
                externalReference: "{attribute['model_reference']}",
                {input_type}: {value}
            }}
            """
        )

    description_json = {
        "blocks": [
            {
                "type": "paragraph",
                "data": {"text": getattr(course, "short_description", "")}
            }
        ]
    }
    description_string = json.dumps(description_json).replace('"', '\\"')

    return f"""
    mutation CreateCourseProduct {{
        productCreate(input: {{
            productType: "{product_type}",
            name: "{course.display_name}",
            description: "{description_string}",
            attributes: [
                {", ".join(attributes_strings)}
            ]
        }})
        {{
            product {{ id, description }},
            errors {{ code, message, field, values }}
        }}
    }}
    """
