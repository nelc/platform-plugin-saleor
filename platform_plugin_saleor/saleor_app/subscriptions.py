"""GraphQL subscriptions for Saleor webhooks."""

ORDER_PAID_SUBSCRIPTION = """
subscription {
    event {
    ... on OrderPaid {
        order {
            id
            number
            status
            isPaid
            lines {
                id
                productName
                variantName
            }
            user {
                id
                email
            }
        }
    }
    }
}
"""

ORDER_UPDATED_SUBSCRIPTION = """
subscription {
    event {
    ... on OrderCreated {
            order {
                id
                number
                status
                isPaid
                lines {
                    id
                    variant {
                        name
                        product {
                            name
                            attributes {
                                attribute {
                                    id
                                    name
                                    slug
                                }
                                values {
                                    id
                                    name
                                }
                            }
                        }
                    }
                }
                user {
                    id
                    email
                }
            }
        }
    }
}
"""

ORDER_CREATED_SUBSCRIPTION = """
subscription {
    event {
    ... on OrderCreated {
            order {
                id
                number
                status
                isPaid
                lines {
                    id
                    variant {
                        name
                        product {
                            name
                            attributes {
                                attribute {
                                    id
                                    name
                                    slug
                                }
                                values {
                                    id
                                    name
                                }
                            }
                        }
                    }
                }
                user {
                    id
                    email
                }
            }
        }
    }
}
"""
