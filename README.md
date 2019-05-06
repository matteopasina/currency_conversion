# Currency converter
REST API for converting currencies

## Getting Started

For running this project you need python 3.3+, flask, requests, jsonschema

## Running the tests

There are three classes of unittest in the test folder that you can run from the main folder with
```
python3 -m unittest test/<name_of_test>
```

In the postman folder there is a collection and an environment with 3 requests that the API can answer

### Request

`GET /rate`

Params: currency

### Response

Retrieve the rates of the currencies or the specified currency in input


### Request

`GET /convert`

Params: 
  - from_currency
  - to_currency
  - value

### Response

Convert the value in input from the specified currency to the desired currency


### Request

`POST /convert`

Swagger of the POST body:

type: object
required:
- to_currency
- amounts
properties:
  to_currency:
    type: string
  amounts:
    type: array
    items:
      type: object
      required:
      - from_currency
      - amounts
      properties:
        amounts:
          type: array
          items:
            type: string
        from_currency:
          type: string

### Response

Converted multiple values

Example:
{
    "to_currency": "EUR",
    "converted-amounts": [
        {
            "from_currency": "USD",
            "converted_amounts": [
                "0.8932",
                "1.7864"
            ]
        },
        {
            "from_currency": "PLN",
            "converted_amounts": [
                "0.7005",
                "0.674815",
                "2.17155"
            ]
        },
        {
            "from_currency": "EUR",
            "converted_amounts": [
                "37.0000",
                "2.890000",
                "9.30000"
            ]
        }
    ]
}
