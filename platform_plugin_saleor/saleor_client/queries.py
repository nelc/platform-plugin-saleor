"""Queries for Saleor GraphQL API."""


def get_attributes_ids_query(limit: int) -> str:
    """
    Get the IDs of all attributes in Saleor.

    Args:
        limit: Maximum number of attributes to retrieve

    Returns:
        str: GraphQL query string for retrieving attribute IDs
    """
    return f"""
    query getAllAttributes {{
        attributes(first: {limit}) {{
            edges {{
                node {{ id, name }}
            }}
        }}
    }}
    """
