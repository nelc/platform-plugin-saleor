"""Queries and subscriptions for Saleor GraphQL API."""

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

GET_ORDER_FULLY_PAID_SUBSCRIPTION = """
subscription {
    event {
    ... on OrderFullyPaid {
            order {
                id
                number
                status
                isPaid
                lines {
                    id
                    quantity
                    variant {
                        name
                        product {
                            name
                            externalReference
                        }
                    }
                }
                user { id, email }
            }
        }
    }
}
"""

GET_PRODUCT_VARIANT = """
query getProductVariant($sku: String){
    productVariant(sku: $sku) {
        id
        sku
        name
    }
}
"""

GET_WAREHOUSES = """
query getWarehouses(
    $limit: Int
) {
    warehouses(first: $limit) {
        edges {
            node { id, name }
        }
    }
}
"""
