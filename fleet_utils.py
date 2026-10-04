"""Catch-all helpers since 2013. Much of this is unused; deletion is pending a decision."""

MILES_PER_KM = 0.621371                 # 1 km = 0.621371 miles (was 1.609, which is km per mile)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles (used by the nightly UK partner report)."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a number with one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a whole-number percentage (unused)."""
    return f"{value:.0f}%"


def mean(values: list[float]) -> float:
    """Average of values, 0 for an empty list (unused; statistics.mean does this)."""
    if not values:
        return 0
    return sum(values) / len(values)


def is_due(pct: float, threshold: float) -> bool:
    """Duplicate of the check in km_wachter.needs_service (unused)."""
    return pct >= threshold


def parse_service_date(text: str) -> tuple[int, int, int] | None:
    """Parse "DD.MM.YYYY" into (year, month, day) (unused since the 2014 garage form went away)."""
    parts = text.split(".")
    if len(parts) != 3:
        return None
    day, month, year = (int(p) for p in parts)
    return (year, month, day)


def chunk_list(items: list, size: int) -> list[list]:
    """Split items into lists of at most size (unused)."""
    return [items[i:i + size] for i in range(0, len(items), size)]
