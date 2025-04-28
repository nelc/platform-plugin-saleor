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

ACCOUNT_REGISTER = """
mutation accountRegister(
    $input: AccountRegisterInput!
) {
    #Take a look at AccountRegisterInput in Saleor GraphQL API
    #https://docs.saleor.io/api-reference/users/inputs/account-register-input

    accountRegister(input: $input) {
        user { id, email }
        errors { code, field, message }
    }
}
"""

ATTACH_CHECKOUT_CUSTOMER = """
mutation attachCustomer(
    $id: ID, $customerId: ID
) {
    checkoutCustomerAttach(id: $id, customerId: $customerId) {
        checkout { id }
        errors { message }
    }
}
"""

CREATE_TOKEN = """
mutation createToken(
    $email: String!, $password: String!
) {
    tokenCreate(email: $email, password: $password) {
        token
        errors { code, field, message }
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
UPDATE_DELIVERY = """
mutation UpdateDelivery($id: ID!, $methodId: ID!) {
  checkoutDeliveryMethodUpdate(id: $id, deliveryMethodId: $methodId) {
    checkout {
      id
      deliveryMethod {
        ... on ShippingMethod {
          id
        }
      }
    }
  }
}
"""

INITIALIZE_TRANSACTION = """
mutation InitializeTransaction($id: ID!, $data: JSON!) {
  transactionInitialize(
    id: $id
    paymentGateway: {id: "saleor.io.dummy-payment-app", data: $data}
  ) {
    errors {
      code
      field
      message
    }
    transaction {
      id
      pspReference
    }
    transactionEvent {
      id
      pspReference
      message
      externalUrl
      amount {
        currency
        amount
      }
      type
      idempotencyKey
    }
  }
}
"""
COMPLETE_CHECKOUT = """
mutation CompleteCheckout($id: ID!) {
  checkoutComplete(id: $id) {
    errors {
      field
      message
    }
    order {
      id
      number
      paymentStatus
    }
  }
}
"""
