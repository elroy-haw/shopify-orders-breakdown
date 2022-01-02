import csv

from datetime import datetime, timedelta
from os import environ
from typing import Dict, List, Union

CONFIG_FILENAME_KEY = "CONFIG_FILENAME"


def validate_env_vars() -> LookupError:
    if CONFIG_FILENAME_KEY not in environ:
        return LookupError(f"{CONFIG_FILENAME_KEY} not found in env var")
    return None


def get_look_ahead_dates(num_days_to_look_ahead: int) -> List[str]:
    today = datetime.today().date()
    dates = [today + timedelta(days=d) for d in range(num_days_to_look_ahead)]
    return [date.strftime("%d/%m/%Y") for date in dates]


def get_last_order_number(item: Dict[str, str]) -> Union[int, None]:
    last_order_number = -1
    for _, _item in item.items():
        if not _item.get("order_numbers", None):
            return None
        for order_number in _item["order_numbers"]:
            if int(order_number) > last_order_number:
                last_order_number = int(order_number)
    return last_order_number


def write_items_to_csv(items: Dict[str, Dict[str, str]]) -> List[str]:
    filepaths = []
    for date, _items in items.items():
        last_order_number = get_last_order_number(_items)
        filepath = (
            f"/tmp/orders_{date.replace('/', '')}_#{last_order_number}.csv"
            if last_order_number
            else f"/tmp/orders_{date.replace('/', '')}.csv"
        )
        write_to_csv([{"name": name} | item for name, item in _items.items()], filepath)
        filepaths.append(filepath)
    return filepaths


def write_to_csv(data: List[Dict[str, str]], filepath: str):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(list(data[0].keys()))
        for row in data:
            writer.writerow(list(row.values()))
