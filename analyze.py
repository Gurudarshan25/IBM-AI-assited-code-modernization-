# Summary: km_since_service matters most (corr 0.40), then avg_daily_km (0.25) and load_factor (0.22).
# Total mileage (odometer_km, corr 0.00) and age (age_years, 0.00) do NOT predict a breakdown.
"""Breakdown-risk analysis for KM-Waechter.

The 80% rule only warns once a car is nearly worn. This ranks every car by breakdown risk from its
history, so the fleet team can service the risky ones first. fleet_history.csv has one row per car
(120 of them) and a "broke_down" column (1 = it later broke down).
"""

import pandas as pd

from km_wachter import SERVICE_INTERVAL_KM, WARN_AT_PERCENT

FEATURES = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
MIN_CORRELATION = 0.1   # a column must correlate at least this much with breakdowns to be used


def compare_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Mean of each column for cars that did / did not break down, plus correlation with breakdown."""
    table = df.groupby("broke_down")[FEATURES].mean().T
    table.columns = ["no_breakdown", "broke_down"]
    table["difference_pct"] = (table["broke_down"] / table["no_breakdown"] - 1) * 100
    table["correlation"] = df[FEATURES].corrwith(df["broke_down"])
    return table


def risk_scores(df: pd.DataFrame, weights: pd.Series) -> pd.Series:
    """Risk 0-100: each predictive column scaled to 0-1, weighted by its correlation."""
    cols = weights.index
    scaled = (df[cols] - df[cols].min()) / (df[cols].max() - df[cols].min())
    return (scaled * weights).sum(axis=1) / weights.sum() * 100


def ranking_quality(score: pd.Series, outcome: pd.Series) -> float:
    """Chance that a random broken-down car scores higher than a random healthy one (AUC)."""
    broke, healthy = score[outcome == 1], score[outcome == 0]
    wins = sum((b > h) + 0.5 * (b == h) for b in broke for h in healthy)
    return wins / (len(broke) * len(healthy))


def main() -> None:
    df = pd.read_csv("fleet_history.csv")
    print(f"{len(df)} cars, {df['broke_down'].sum()} broke down\n")

    table = compare_groups(df)
    print("Broken-down cars vs. the rest (means):")
    print(table.round(2).to_string(), "\n")

    weights = table["correlation"][table["correlation"] >= MIN_CORRELATION]
    ignored = [c for c in FEATURES if c not in weights.index]
    print(f"Used for the score: {', '.join(weights.index)}")
    print(f"Ignored (no real difference between the groups): {', '.join(ignored)}\n")

    df["risk"] = risk_scores(df, weights).round(1)
    print(f"Ranking quality (AUC, 0.5 = coin flip, 1.0 = perfect): "
          f"{ranking_quality(df['risk'], df['broke_down']):.2f}")

    warn_km = SERVICE_INTERVAL_KM * WARN_AT_PERCENT / 100
    broke = df[df["broke_down"] == 1]
    missed = (broke["km_since_service"] < warn_km).sum()
    print(f"Breakdowns the 80% rule would NOT have flagged (< {warn_km:.0f} km since service): "
          f"{missed} of {len(broke)}\n")

    ranked = df.sort_values("risk", ascending=False)
    print("Cars ranked by risk, highest first:")
    print(ranked[["car_id", "risk", "km_since_service", "avg_daily_km", "load_factor",
                  "broke_down"]].to_string(index=False))


if __name__ == "__main__":
    main()
