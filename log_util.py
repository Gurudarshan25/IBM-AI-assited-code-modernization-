"""A homemade logger (the logging module felt like "too much magic" in 2013)."""

import time

LOG_LINES: list[str] = []               # global state, shared by everyone who imports this
DEBUG = False


def log(message: str) -> None:
    """Print a timestamped line and keep it for flush_log."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log only when DEBUG is on (it has been False since 2014, so this never fires)."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Append all kept log lines to the file at path, then forget them."""
    with open(path, "a", encoding="utf-8") as f:
        for line in LOG_LINES:
            f.write(f"{line}\n")
    LOG_LINES.clear()
