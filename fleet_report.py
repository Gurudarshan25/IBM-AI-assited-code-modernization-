"""Prints the nightly fleet-health summary for Vossberg Mobility."""

from km_wachter import wear_percent, needs_service, SERVICE_INTERVAL_KM
from config_loader import load_settings, get_setting
from log_util import log, flush_log
import fleet_utils


def car_wear(car: dict) -> float | None:
    """Return the car's wear percentage, or None if it has no last-service reading."""
    last = car.get("last_service_km")
    if last is None:
        return None
    return wear_percent(car["odometer"] - last, SERVICE_INTERVAL_KM)


def fleet_summary(fleet: list[dict]) -> dict:
    """Count cars, cars due for service, and average wear over the cars that have a reading."""
    wears = []
    due = 0
    for car in fleet:
        wear = car_wear(car)
        if wear is not None:
            wears.append(wear)
        if needs_service(car):
            due += 1
    average = sum(wears) / len(wears) if wears else 0.0
    return {
        "count": len(fleet),
        "due": due,
        "no_reading": len(fleet) - len(wears),
        "average_wear": average,
    }


def print_report(fleet: list[dict]) -> None:
    """Print the nightly report and append the log lines to the log file."""
    settings = load_settings()
    log(get_setting(settings, "report_title", "Nightly fleet report"))
    s = fleet_summary(fleet)
    print(f"Fleet: {s['count']} cars")
    print(f"Due for service: {s['due']}")
    print(f"No last-service reading: {s['no_reading']}")
    print(f"Average wear: {s['average_wear']:.1f}%")
    total_km = sum(car["odometer"] for car in fleet)
    # The partner garage in England wants the distance in miles (since 2015).
    print(f"Fleet distance: {fleet_utils.format_number(fleet_utils.km_to_miles(total_km))} miles")
    flush_log(get_setting(settings, "log_file", "km_wachter.log"))
