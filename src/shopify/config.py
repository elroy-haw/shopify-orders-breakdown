class ShopifyConfig:
    def __init__(self, shop_url: str, api_key: str, api_secret: str):
        self.shop_url = shop_url
        self.api_key = api_key
        self.api_secret = api_secret


class OrderProcessorConfig:
    def __init__(
        self, static_breakdown_template: dict, dynamic_breakdown_template: dict
    ):
        self.static_breakdown_template = static_breakdown_template
        self.dynamic_breakdown_template = dynamic_breakdown_template
