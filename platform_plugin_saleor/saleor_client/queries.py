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

GET_USER = """
query getUser($email: String){
    user(email: $email) {
        id
        email
        externalReference
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

GET_CHECKOUT = """
query getCheckout($id: ID!) {
  checkout(id: $id) {
    id
    email
    lines {
      quantity
      totalPrice {
        currency
        gross {
          amount
          currency
        }
        tax {
          amount
          currency
        }
      }
      id
      variant {
        sku
        name
      }
      unitPrice {
        gross {
          amount
          currency
        }
      }
    }
    user {
      firstName
      lastName
      languageCode
    }
    isShippingRequired
    created
    channel {
      id
      name
    }
    updatedAt
    quantity
    totalPrice {
      currency
      gross {
        amount
      }
      tax {
        amount
        currency
      }
    }
  }
}
"""
