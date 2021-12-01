import json

from typing import Tuple
from cfg.config import Config
from notification.notification import NotificationType

SHOP_URL_KEY = "shop_url"
API_KEY_KEY = "api_key"
API_SECRET_KEY = "api_secret"
STATIC_BREAKDOWN_TEMPLATE_KEY = "static_breakdown_template"
DYNAMIC_BREAKDOWN_TEMPLATE_KEY = "dynamic_breakdown_template"
AWS_REGION_KEY = "aws_region"
FROM_TIMESTAMP_KEY = "from_timestamp"
NUM_DAYS_TO_LOOK_AHEAD_KEY = "num_days_to_look_ahead"
NOTIFICATION_TYPE_KEY = "notification_type"
SENDER_NAME_KEY = "sender_name"
SENDER_EMAIL_KEY = "sender_email"
RECIPIENT_EMAIL_KEY = "recipient_email"


def load(filename) -> Tuple[Config, Exception]:
    with open(filename, "r") as f:
        cfg = json.load(f)
        err = validate(cfg)
        if err != None:
            return None, err
        return (
            Config(
                shop_url=cfg.get(SHOP_URL_KEY),
                api_key=cfg.get(API_KEY_KEY),
                api_secret=cfg.get(API_SECRET_KEY),
                static_breakdown_template=cfg.get(STATIC_BREAKDOWN_TEMPLATE_KEY),
                dynamic_breakdown_template=cfg.get(DYNAMIC_BREAKDOWN_TEMPLATE_KEY),
                aws_region=cfg.get(AWS_REGION_KEY),
                from_timestamp=cfg.get(FROM_TIMESTAMP_KEY),
                num_days_to_look_ahead=cfg.get(NUM_DAYS_TO_LOOK_AHEAD_KEY),
                notification_type=cfg.get(NOTIFICATION_TYPE_KEY),
                sender_name=cfg.get(SENDER_NAME_KEY, ""),
                sender_email=cfg.get(SENDER_EMAIL_KEY, ""),
                recipient_email=cfg.get(RECIPIENT_EMAIL_KEY, ""),
            ),
            None,
        )


def validate(cfg: Config) -> KeyError:
    if SHOP_URL_KEY not in cfg:
        return KeyError(f"{SHOP_URL_KEY} is missing in config")
    if API_KEY_KEY not in cfg:
        return KeyError(f"{API_KEY_KEY} is missing in config")
    if API_SECRET_KEY not in cfg:
        return KeyError(f"{API_SECRET_KEY} is missing in config")
    if STATIC_BREAKDOWN_TEMPLATE_KEY not in cfg:
        return KeyError(f"{STATIC_BREAKDOWN_TEMPLATE_KEY} is missing in config")
    if DYNAMIC_BREAKDOWN_TEMPLATE_KEY not in cfg:
        return KeyError(f"{DYNAMIC_BREAKDOWN_TEMPLATE_KEY} is missing in config")
    if AWS_REGION_KEY not in cfg:
        return KeyError(f"{AWS_REGION_KEY} is missing in config")
    if FROM_TIMESTAMP_KEY not in cfg:
        return KeyError(f"{FROM_TIMESTAMP_KEY} is missing in config")
    if NUM_DAYS_TO_LOOK_AHEAD_KEY not in cfg:
        return KeyError(f"{NUM_DAYS_TO_LOOK_AHEAD_KEY} is missing in config")
    if NOTIFICATION_TYPE_KEY not in cfg:
        return KeyError(f"{NOTIFICATION_TYPE_KEY} is missing in config")
    if cfg.notification_type == NotificationType.EMAIL:
        return validate_email_notification_type(cfg)
    return None


def validate_email_notification_type(cfg: Config) -> KeyError:
    if SENDER_NAME_KEY not in cfg:
        return KeyError(f"{SENDER_NAME_KEY} is missing in config")
    if SENDER_EMAIL_KEY not in cfg:
        return KeyError(f"{SENDER_EMAIL_KEY} is missing in config")
    if RECIPIENT_EMAIL_KEY not in cfg:
        return KeyError(f"{RECIPIENT_EMAIL_KEY} is missing in config")
    if AWS_REGION_KEY not in cfg:
        return KeyError(f"{AWS_REGION_KEY} is missing in config")
    return None
