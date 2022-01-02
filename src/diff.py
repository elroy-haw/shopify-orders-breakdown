from cfg.utils import load
from datetime import datetime, timedelta
from notification.email import Email, Sender, Recipient
from os import environ
from notification.notification import NotificationType
from shopify.client import Client
from shopify.config import OrderProcessorConfig, ShopifyConfig
from shopify.order_processor import OrderProcessor
from utils.utils import (
    get_look_ahead_dates,
    validate_env_vars,
    CONFIG_FILENAME_KEY,
)


def lambda_handler(event, context):
    # Validate env vars
    err = validate_env_vars()
    if err != None:
        raise err

    # Load config
    cfg_filename = environ.get(CONFIG_FILENAME_KEY)
    cfg, err = load(cfg_filename)
    if err != None:
        raise err

    # Get orders
    shopify_client = Client(ShopifyConfig(cfg.shop_url, cfg.api_key, cfg.api_secret))
    from_timestamp = cfg.from_timestamp
    to_timestamp = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S%z")
    orders_computed_today = shopify_client.get_orders_with_timestamps(from_timestamp)
    orders_computed_yesterday = shopify_client.get_orders_with_timestamps(
        from_timestamp, to_timestamp
    )
    if err != None:
        raise err

    # Diff consolidated and breakdown items computed yesterday vs today
    order_processor = OrderProcessor(
        OrderProcessorConfig(
            cfg.static_breakdown_template, cfg.dynamic_breakdown_template
        )
    )
    dates = [datetime.now().strftime("%d/%m/%Y")]
    (
        consolidated_items_computed_today,
        breakdown_items_computed_today,
    ) = order_processor.process_orders(orders_computed_today, dates)
    (
        consolidated_items_computed_yesterday,
        breakdown_items_computed_yesterday,
    ) = order_processor.process_orders(orders_computed_yesterday, dates)
    consolidated_items_diff = order_processor.diff_items(
        consolidated_items_computed_today.get(dates[0]),
        consolidated_items_computed_yesterday.get(dates[0]),
    )
    breakdown_items_diff = order_processor.diff_items(
        breakdown_items_computed_today.get(dates[0]),
        breakdown_items_computed_yesterday.get(dates[0]),
    )

    # Notify
    if cfg.notification_type == NotificationType.EMAIL.value:
        email = Email(
            Sender(cfg.sender_name, cfg.sender_email),
            Recipient(cfg.recipient_email),
            cfg.aws_region,
        )
        err = email.notify(
            f"Difference between orders for {dates[0]}", consolidated_items_diff
        )
        if err != None:
            raise err
        err = email.notify(
            f"Difference between breakdown of orders for {dates[0]}",
            breakdown_items_diff,
        )
        if err != None:
            raise err

    return {"status": 200, "message": "success"}


if __name__ == "__main__":
    lambda_handler({}, {})
