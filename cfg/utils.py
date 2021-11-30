import json

from os import error, stat
from typing import Tuple
from cfg.config import Config

SHOP_URL_KEY = "shop_url"
API_KEY_KEY = "api_key"
API_SECRET_KEY = "api_secret"
STATIC_BREAKDOWN_TEMPLATE_KEY = "static_breakdown_template"
DYNAMIC_BREAKDOWN_TEMPLATE_KEY = "dynamic_breakdown_template"


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
            ),
            None,
        )


def validate(cfg: Config) -> KeyError:
    if SHOP_URL_KEY not in cfg.keys():
        return KeyError(f"{SHOP_URL_KEY} is missing in config")
    if API_KEY_KEY not in cfg.keys():
        return KeyError(f"{API_KEY_KEY} is missing in config")
    if API_SECRET_KEY not in cfg.keys():
        return KeyError(f"{API_SECRET_KEY} is missing in config")
    if STATIC_BREAKDOWN_TEMPLATE_KEY not in cfg.keys():
        return KeyError(f"{STATIC_BREAKDOWN_TEMPLATE_KEY} is missing in config")
    if DYNAMIC_BREAKDOWN_TEMPLATE_KEY not in cfg.keys():
        return KeyError(f"{DYNAMIC_BREAKDOWN_TEMPLATE_KEY} is missing in config")
    return None
