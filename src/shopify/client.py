import requests

from shopify.config import ShopifyConfig
from typing import Any, Dict, List
from urllib.parse import urlencode


class Client:
    def __init__(self, cfg: ShopifyConfig):
        self.orders_endpoint = f"https://{cfg.api_key}:{cfg.api_secret}@{cfg.shop_url}/admin/api/2021-10/orders.json"
        self.orders_default_query_params = {
            "status": "open",
            "financial_status": "any",
            "fulfillment_status": "unfulfilled",
        }

    def get_orders(self, query_params: Dict[str, str]) -> List[Any]:
        orders_endpoint_with_query_params = f"{self.orders_endpoint}?{urlencode(self.orders_default_query_params | query_params)}"
        response = requests.get(orders_endpoint_with_query_params)
        response.raise_for_status()
        orders = response.json()["orders"]

        # paginate orders
        link = response.headers.get("Link", None)
        has_next = "next" in link
        while has_next:
            pairs = {}
            for pair in link.split(","):
                left, right = pair.split("; ")
                query_param = left[1:-1].split("?")[1]
                rel = right.replace("rel=", "")[1:-1]
                pairs[rel] = query_param
            next_orders_endpoint_with_query_params = (
                f"{self.orders_endpoint}?{pairs['next']}"
            )
            response = requests.get(next_orders_endpoint_with_query_params)
            response.raise_for_status()
            orders.extend(response.json()["orders"])
            link = response.headers.get("Link", None)
            has_next = "next" in link

        return orders

    def get_orders_with_timestamps(
        self, created_at_min: str, created_at_max: str = ""
    ) -> List[Any]:
        if created_at_max == "":
            return self.get_orders({"created_at_min": created_at_min})
        return self.get_orders(
            {"created_at_min": created_at_min, "created_at_max": created_at_max}
        )
