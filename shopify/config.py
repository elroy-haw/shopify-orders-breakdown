class Config:
    def __init__(self, shop_url, api_key, api_secret):
        self.shop_url = shop_url
        self.api_key = api_key
        self.api_secret = api_secret

    def __str__(self) -> str:
        return f"Config{{shop_url={self.shop_url},api_key={self.api_key},api_secret={self.api_secret}}}"
