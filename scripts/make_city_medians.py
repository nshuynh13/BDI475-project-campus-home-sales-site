#!/usr/bin/env python3
"""Make data/city_median_sale_price.json from data/college_town_home_sales.csv.

Rule: a sale counts only if its sale_price is $10,000 or more. Blank prices are left out.
Each city's median is the median of the counted sale prices in that city.

Run from the repository root:
    python3 scripts/make_city_medians.py

The dataset files themselves are never changed.
"""

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

MIN_PRICE = 10_000

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "data" / "college_town_home_sales.csv"
OUTPUT = REPO / "data" / "city_median_sale_price.json"


def main() -> None:
    prices = defaultdict(list)
    state_of = {}
    total_rows = 0
    blank_rows = 0
    excluded_rows = 0

    with SOURCE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total_rows += 1
            raw = (row["sale_price"] or "").strip()
            if raw == "":
                blank_rows += 1
                continue
            price = int(raw)
            if price < MIN_PRICE:
                excluded_rows += 1
                continue
            key = (row["city"], row["state"])
            prices[key].append(price)
            state_of[key] = row["state"]

    cities = []
    for (city, state), values in prices.items():
        cities.append({
            "city": city,
            "state": state,
            "sales": len(values),
            "median_sale_price": statistics.median(values),
        })
    cities.sort(key=lambda c: (c["city"], c["state"]))

    result = {
        "source": "data/college_town_home_sales.csv",
        "rule": f"Sales with sale_price of ${MIN_PRICE:,} or more. Blank prices are left out.",
        "min_sale_price": MIN_PRICE,
        "total_rows": total_rows,
        "blank_price_rows": blank_rows,
        "excluded_under_min_rows": excluded_rows,
        "rows_used": sum(c["sales"] for c in cities),
        "cities": cities,
    }

    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(REPO)}: {len(cities)} cities, {result['rows_used']} rows used")


if __name__ == "__main__":
    main()
