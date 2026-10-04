"""Reads settings.cfg (hand-rolled 2013 parser; values stay strings)."""

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict[str, str]:
    """Parse "key = value" lines, skipping blanks, comments, broken lines and unknown keys."""
    if path is None:
        path = SETTINGS_FILE
    settings = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)   # only the first "=" separates key from value
            key = key.strip()
            # Unknown keys are silently dropped, so a typo in the cfg never surfaces.
            if key in KNOWN_KEYS:
                settings[key] = value.strip()
    return settings


def get_int(settings: dict[str, str], key: str, fallback: int) -> int:
    """Return the setting as an int, or fallback if it is missing or not a number."""
    try:
        return int(settings[key])
    except (KeyError, ValueError):
        return fallback


def get_setting(settings: dict[str, str], key: str, fallback: str = "") -> str:
    """Return the setting, or fallback if missing (same as dict.get; kept for callers)."""
    return settings.get(key, fallback)
