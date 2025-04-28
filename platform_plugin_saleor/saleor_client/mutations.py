"""Mutations for Saleor GraphQL API """


CREATE_PRODUCT_ATTRIBUTES = """
mutation AttributeBulkCreate(
  $attributes: [AttributeCreateInput!]!
) {
    #Take a look at AttributeCreateInput in Saleor GraphQL API
    #https://docs.saleor.io/api-reference/attributes/inputs/attribute-create-input

    attributeBulkCreate(attributes: $attributes) {
        results {
            attribute { id, name },
            errors { message, code }
        }
        errors { message, code  }
    }
}
"""

CREATE_PRODUCT_TYPE = """
mutation CreateProductType(
    $input: ProductTypeInput!
) {
    #Take a look at ProductTypeInput in Saleor GraphQL API
    #https://docs.saleor.io/api-reference/products/inputs/product-type-input

    productTypeCreate(input: $input) {
        productType { id, name }
        errors { message, code }
    }
}
"""

CREATE_COURSE_PRODUCT = """
mutation CreateCourseProduct(
    $input: ProductCreateInput!
) {
    #Take a look at ProductCreateInput in Saleor GraphQL API
    #https://docs.saleor.io/api-reference/products/inputs/product-create-input

    productCreate(input: $input) {
        product { id, description }
        errors { message, code, field, values }
    }
}
"""

CREATE_CHECKOUT = """
mutation CreateCheckout(
    $input: CheckoutCreateInput!
) {
    #Take a look at CheckoutCreateInput in Saleor GraphQL API
    #https://docs.saleor.io/api-reference/checkout/inputs/checkout-create-input

    checkoutCreate(input: $input) {
        checkout { id }
        errors { message }
    }
}
"""

FULLFILL_ORDER = """
mutation orderFulfill(
    $input: OrderFulfillInput!
    $order: ID
){
  orderFulfill(input: $input, order: $order) {
    fulfillments {
      created
      status
    }
    errors { field, message }
  }
}
"""
