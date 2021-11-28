import requests

from shopify.config import Config


class Client:
    def __init__(self, cfg: Config):
        self.orders_endpoint = f"https://{cfg.api_key}:{cfg.api_secret}@{cfg.shop_url}/admin/api/2021-10/orders.json"
        # TODO: review path params
        self.orders_query_params = (
            "status=any&financial_status=paid&fulfillment_status=unfulfilled"
        )

    # TODO: implement this
    def get_orders_from_ts(self, from_ts: str):
        # response = requests.get(
        #     f"{self.orders_endpoint}?{self.orders_query_params}&created_at_min={from_ts}"
        # )
        return ["order1"]
