from email.email import send_email
from os import environ
from utils.utils import validate_env_vars, CONFIG_FILENAME_KEY, FROM_TIMESTAMP_KEY
from shopify.client import Client
from shopify.utils import load


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
    shopify_client = Client(cfg)
    from_ts = environ.get(FROM_TIMESTAMP_KEY)
    orders, err = shopify_client.get_orders_from_ts(from_ts)
    if err != None:
        raise err

    # Send email
    err = send_email()
    if err != None:
        raise err

    return {"status": 200, "message": "success"}


if __name__ == "__main__":
    lambda_handler({}, {})
