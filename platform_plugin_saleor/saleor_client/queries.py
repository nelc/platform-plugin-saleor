"""Queries for Saleor GraphQL API."""

GET_PRODUCT_ATTRIBUTES = """
query getAttributes(
    $limit: Int
) {
    attributes(first: $limit) {
        edges {
            node { id, name }
        }
    }
}
"""

GET_PRODUCT_TYPES = """
query getProductTypes(
    $limit: Int
) {
    productTypes(first: $limit) {
        edges {
            node { id, name }
        }
  }
}
"""
