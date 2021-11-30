from datetime import datetime, timedelta
from os import environ

CONFIG_FILENAME_KEY = "CONFIG_FILENAME"
FROM_TIMESTAMP_KEY = "FROM_TIMESTAMP"
NUM_DAYS_TO_LOOK_AHEAD_KEY = "NUM_DAYS_TO_LOOK_AHEAD"


def validate_env_vars() -> LookupError:
    if CONFIG_FILENAME_KEY not in environ:
        return LookupError(f"{CONFIG_FILENAME_KEY} not found in env var")
    if FROM_TIMESTAMP_KEY not in environ:
        return LookupError(f"{FROM_TIMESTAMP_KEY} not found in env var")
    if NUM_DAYS_TO_LOOK_AHEAD_KEY not in environ:
        return LookupError(f"{NUM_DAYS_TO_LOOK_AHEAD_KEY} not found in env var")
    return None


def get_look_ahead_dates() -> list:
    today = datetime.today().date()
    num_days_to_look_ahead = int(environ.get(NUM_DAYS_TO_LOOK_AHEAD_KEY))
    dates = [today + timedelta(d) for d in range(num_days_to_look_ahead)]
    return [date.strftime("%d/%m/%Y") for date in dates]
