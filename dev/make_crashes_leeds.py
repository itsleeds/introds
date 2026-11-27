"""Generate crashes-leeds.csv from 2025 UK STATS19 data using stats19py.

Produces a casualty-level CSV for all police-recorded road collisions in Leeds
in 2025, sharing the same four core column names as 00_data/crashes.csv
(`casualty_type`, `casualty_age`, `vehicle_type`, `dark`) so students can use
it as a drop-in real-world replacement in the manipulation and visualisation
exercises, plus additional STATS19 columns for optional exploration.

Usage (from an environment with `stats19` / stats19py installed):
    python dev/make_crashes_leeds.py [output_path]

Default output path: crashes-leeds.csv (in the current working directory).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import stats19


def simplify_casualty_type(value: object) -> str:
    """Map STATS19 casualty_type labels to concise lowercase categories."""
    if pd.isna(value):
        return "other"
    text = str(value).lower()
    if text == "pedestrian":
        return "pedestrian"
    if text == "cyclist":
        return "cyclist"
    if "car occupant" in text or "taxi" in text:
        return "car"
    if "motorcycle" in text:
        return "motorcycle"
    if "bus" in text or "minibus" in text:
        return "bus"
    if "van" in text or "goods" in text:
        return "van/goods"
    return "other"


def simplify_vehicle_type(value: object) -> str:
    """Map STATS19 vehicle_type labels to concise lowercase categories."""
    if pd.isna(value):
        return "other"
    text = str(value).lower()
    if text == "car" or "taxi" in text:
        return "car"
    if "pedal cycle" in text:
        return "bicycle"
    if "motorcycle" in text:
        return "motorcycle"
    if "bus" in text or "minibus" in text:
        return "bus"
    if "van" in text or "goods" in text:
        return "van/goods"
    return "other"


def build_crashes_leeds(year: int = 2025) -> pd.DataFrame:
    """Build the Leeds casualty-level crash dataset for a given STATS19 year."""
    collisions = stats19.get_collisions(year=year, silent=True)
    casualties = stats19.get_casualties(year=year, silent=True)
    vehicles = stats19.get_vehicles(year=year, silent=True)

    leeds_col = collisions[
        collisions["local_authority_ons_district"] == "Leeds"
    ].copy()
    leeds_cas = casualties[
        casualties["collision_index"].isin(leeds_col["collision_index"])
    ].copy()
    leeds_veh = vehicles[
        vehicles["collision_index"].isin(leeds_col["collision_index"])
    ].copy()

    merged = leeds_cas.merge(
        leeds_veh[["collision_index", "vehicle_reference", "vehicle_type"]],
        on=["collision_index", "vehicle_reference"],
        how="left",
    ).merge(
        leeds_col[
            [
                "collision_index",
                "date",
                "light_conditions",
                "speed_limit",
                "longitude",
                "latitude",
            ]
        ],
        on="collision_index",
        how="left",
    )

    merged = merged.sort_values(
        ["date", "collision_index", "casualty_reference"]
    ).reset_index(drop=True)

    # Use TRUE/FALSE strings for `dark` so pandas.read_csv(), readr::read_csv(),
    # and base R read.csv() all parse it as boolean/logical automatically.
    dark_bool = merged["light_conditions"].str.startswith("Darkness", na=False)

    out = pd.DataFrame(
        {
            "casualty_type": merged["casualty_type"].map(simplify_casualty_type),
            "casualty_age": merged["age_of_casualty"].astype("Int64"),
            "vehicle_type": merged["vehicle_type"].map(simplify_vehicle_type),
            "dark": dark_bool.map({True: "TRUE", False: "FALSE"}),
            "collision_index": merged["collision_index"],
            "date": pd.to_datetime(merged["date"]).dt.strftime("%Y-%m-%d"),
            "casualty_severity": merged["casualty_severity"],
            "speed_limit": pd.to_numeric(
                merged["speed_limit"], errors="coerce"
            ).astype("Int64"),
            "light_conditions": merged["light_conditions"],
            "longitude": merged["longitude"],
            "latitude": merged["latitude"],
        }
    )
    return out


def main() -> None:
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("crashes-leeds.csv")
    df = build_crashes_leeds(year=2025)
    df.to_csv(output_path, index=False)
    n_collisions = df["collision_index"].nunique()
    print(
        f"Wrote {len(df)} casualties across {n_collisions} Leeds 2025 collisions "
        f"to {output_path} ({output_path.stat().st_size:,} bytes)"
    )


if __name__ == "__main__":
    main()
