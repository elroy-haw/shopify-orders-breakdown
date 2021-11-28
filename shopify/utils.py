import json

from os import error
from typing import Tuple
from shopify.config import Config


SHOP_URL_KEY = "shop_url"
API_KEY_KEY = "api_key"
API_SECRET_KEY = "api_secret"
STATIC_BREAKDOWN_KEY = "static_breakdown"
DYNAMIC_BREAKDOWN_KEY = "dynamic_breakdown"


def load(filename) -> Tuple[Config, Exception]:
    with open(filename, "r") as f:
        cfg = json.load(f)
        err = validate_config(cfg)
        if err != None:
            return None, err
        return (
            Config(
                shop_url=cfg.get(SHOP_URL_KEY),
                api_key=cfg.get(API_KEY_KEY),
                api_secret=cfg.get(API_SECRET_KEY),
            ),
            None,
        )


def validate_config(cfg: Config) -> KeyError:
    if SHOP_URL_KEY not in cfg.keys():
        return KeyError(f"{SHOP_URL_KEY} is missing in config")
    if API_KEY_KEY not in cfg.keys():
        return KeyError(f"{API_KEY_KEY} is missing in config")
    if API_SECRET_KEY not in cfg.keys():
        return KeyError(f"{API_SECRET_KEY} is missing in config")
    if STATIC_BREAKDOWN_KEY not in cfg.keys():
        return KeyError(f"{STATIC_BREAKDOWN_KEY} is missing in config")
    if DYNAMIC_BREAKDOWN_KEY not in cfg.keys():
        return KeyError(f"{DYNAMIC_BREAKDOWN_KEY} is missing in config")
    return None


def is_formattable_string(s: str) -> bool:
    return "{" in s and "}" in s
