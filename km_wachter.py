"""KM-Waechter: decides when a Vossberg Mobility car needs a service."""

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return how much of the service interval is used up, as a percentage (e.g. 99.33)."""
    return km_since_service / interval * 100


def needs_service(car: dict) -> bool:
    """Return True when the car has used WARN_AT_PERCENT or more of its service interval.

    A car with no "last_service_km" reading cannot be judged, so it is not flagged.
    """
    last = car.get("last_service_km")
    if last is None:
        return False
    pct = wear_percent(car["odometer"] - last, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Print and return the ids of all cars that are due for service."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
