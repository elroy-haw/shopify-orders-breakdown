from os import environ

CONFIG_FILENAME_KEY = "CONFIG_FILENAME"
FROM_TIMESTAMP_KEY = "FROM_TIMESTAMP"


def validate_env_vars() -> LookupError:
    if CONFIG_FILENAME_KEY not in environ:
        return LookupError(f"{CONFIG_FILENAME_KEY} not found in env var")
    if FROM_TIMESTAMP_KEY not in environ:
        return LookupError(f"{FROM_TIMESTAMP_KEY} not found in env var")
    return None
