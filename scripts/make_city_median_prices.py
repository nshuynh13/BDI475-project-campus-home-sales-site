"""Write data/city_median_sale_price.json: the median sale price for each city.

Reads data/college_town_home_sales.csv (read only) and counts only sales of $10,000 or
more. Sales under $10,000 are left out because the data description sheet lists them as
implausible. Run from the repository root:

    python3 scripts/make_city_median_prices.py
"""

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "college_town_home_sales.csv"
OUTPUT = ROOT / "data" / "city_median_sale_price.json"
MIN_PRICE = 10_000

prices = defaultdict(list)
excluded = 0
total = 0
with SOURCE.open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        total += 1
        price = int(row["sale_price"])
        if price < MIN_PRICE:
            excluded += 1
            continue
        key = (row["city"], row["state"])
        prices[key].append(price)

cities = [
    {
        "city": city,
        "state": state,
        "sales": len(values),
        "median_sale_price": statistics.median(values),
    }
    for (city, state), values in prices.items()
    if len(values) >= 90  # the same cutoff the data sheet used to drop small places
]
cities.sort(key=lambda c: c["median_sale_price"], reverse=True)

result = {
    "source": "data/college_town_home_sales.csv",
    "rule": f"Sales with sale_price of ${MIN_PRICE:,} or more. Sales below that are excluded.",
    "rows_in_source": total,
    "rows_excluded_by_rule": excluded,
    "cities": cities,
}
OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {OUTPUT.relative_to(ROOT)}: {len(cities)} cities, "
      f"{excluded} sales under ${MIN_PRICE:,} excluded of {total}.")
