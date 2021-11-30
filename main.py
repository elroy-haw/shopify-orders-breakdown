from cfg.utils import load
from os import environ
from shopify.client import Client
from shopify.config import OrderProcessorConfig, ShopifyConfig
from shopify.order_processor import OrderProcessor
from utils.utils import (
    get_look_ahead_dates,
    validate_env_vars,
    CONFIG_FILENAME_KEY,
    FROM_TIMESTAMP_KEY,
)


def lambda_handler(event, context):
    err = validate_env_vars()

    # Load config
    if err != None:
        raise err
    cfg_filename = environ.get(CONFIG_FILENAME_KEY)
    cfg, err = load(cfg_filename)
    if err != None:
        raise err

    # Get orders
    shopify_client = Client(ShopifyConfig(cfg.shop_url, cfg.api_key, cfg.api_secret))
    from_ts = environ.get(FROM_TIMESTAMP_KEY)
    orders = shopify_client.get_orders_from_ts(from_ts)
    if err != None:
        raise err

    # Process orders
    order_processor = OrderProcessor(
        OrderProcessorConfig(
            cfg.static_breakdown_template, cfg.dynamic_breakdown_template
        )
    )
    dates = get_look_ahead_dates()
    breakdowns = order_processor.process_orders(orders, dates)

    # Send email

    return {"status": 200, "message": "success"}


if __name__ == "__main__":
    lambda_handler({}, {})
