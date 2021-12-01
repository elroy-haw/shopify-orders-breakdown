import csv

from datetime import datetime, timedelta
from os import environ

CONFIG_FILENAME_KEY = "CONFIG_FILENAME"


def validate_env_vars() -> LookupError:
    if CONFIG_FILENAME_KEY not in environ:
        return LookupError(f"{CONFIG_FILENAME_KEY} not found in env var")
    return None


def get_look_ahead_dates(num_days_to_look_ahead: int) -> list:
    today = datetime.today().date()
    dates = [today + timedelta(d) for d in range(num_days_to_look_ahead)]
    return [date.strftime("%d/%m/%Y") for date in dates]


def get_last_order_number(breakdown: dict) -> int:
    last_order_number = -1
    for _, pair in breakdown.items():
        for order_number in pair["order_numbers"]:
            if int(order_number) > last_order_number:
                last_order_number = int(order_number)
    return last_order_number


def write_to_csv(breakdowns: dict) -> list:
    filepaths = []
    for date, breakdown in breakdowns.items():
        last_order_number = get_last_order_number(breakdown)
        filepath = f"/tmp/orders_{date.replace('/', '')}_#{last_order_number}.csv"
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "quantity", "order_numbers"])
            for name, pair in breakdown.items():
                quantity = pair["quantity"]
                order_numbers = pair["order_numbers"]
                writer.writerow([name, quantity, order_numbers])
        filepaths.append(filepath)
    return filepaths
