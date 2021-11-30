# Shopify Orders Breakdown

## Assumptions
* Orders are tagged with delivery dates in the format of dd/mm/yyyy

## Configuration
### Overall format
```json
{
  "shop_url": "<SHOP URL>",
  "api_key": "<PRIVATE APP API KEY>",
  "api_secret": "<PRIVATE APP API SECRET>",
  "static_breakdown_template": {
    // ...
  },
  "dynamic_breakdown_template": {
    // ...
  }
}
```

### Static breakdown template format
* Static breakdown template is for products that do not have user selectable options and can be directly broken down to other child products.
* A product can be broken down to other child products by corresponding to their titles.
* If a product has variants (and each variant break down to different products), use a `map` instead of a `list` as shown in the example below `Product 2 Title`.
```json
"static_breakdown_template": {
  "Product 1 Title": [
    "Breakdown 1 Title",
    "Breakdown 2 Title",
    // ...
    "Breakdown n Title"
  ],
  "Product 2 Title": {
    "Variant 1": [
      "Breakdown 1 Title",
      "Breakdown 2 Title",
      // ...
      "Breakdown n Title"
    ],
    "Variant 2": [
      "Breakdown 1 Title",
      "Breakdown 2 Title",
      // ...
      "Breakdown n Title"
    ]
  },
  // ...
  "Product n Title": [
    // ...
  ]
},
```

### Dynamic breakdown template format
* Dynamic breakdown template is for products that have user selectable options and thus requires substitutions to match titles in other child products.
* Similar to static breakdown template, a product can be broken down into multiple child products. But in this case, the keys `properties`, `properties.name`, `properties.value_map`, and `template` are supported to facilitate dynamic substitution of values.
* The curly braces in the `template` value will be replaced in order of the `properties`.
```json
"dynamic_breakdown_template": {
  "Product 1 Title": [
    {
      "properties": [
        {
          "name": "Property 1",
          "value_map": {
            "Key": "Value"
          }
        }
      ],
      "template": "Example Template {0}"
    }
  ],
  "Product 2 Title": [
    {
      "properties": [
        {
          "name": "Property 1",
          "value_map": {
            "Key": "Value"
          }
        },
        {
          "name": "Property 2",
          "value_map": {
            "Key": "Value"
          }
        }
      ],
      "template": "Example Template {0} {1}"
    }
  ],
  // ...
  "Product n Title": [
    // ...
  ]
},
```
