class Config:
    def __init__(
        self,
        shop_url,
        api_key,
        api_secret,
        static_breakdown_template,
        dynamic_breakdown_template,
    ):
        self.shop_url = shop_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.static_breakdown_template = static_breakdown_template
        self.dynamic_breakdown_template = dynamic_breakdown_template
