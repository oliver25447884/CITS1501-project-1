"""Load and summarise daily Perth weather observations from Bureau CSV files."""

import csv
import math
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from statistics import fmean


MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)
MONTH_NUMBER = {name[:3].casefold(): number for number, name in enumerate(MONTHS, 1)}
MONTH_TO_SEASON = {
    1: "Birak", 2: "Bunuru", 3: "Bunuru", 4: "Djeran", 5: "Djeran",
    6: "Makuru", 7: "Makuru", 8: "Djilba", 9: "Djilba",
    10: "Kambarang", 11: "Kambarang", 12: "Birak",
}
DAY_PATTERN = re.compile(r"^(\d{1,2})(?:st|nd|rd|th)?$", re.IGNORECASE)


@dataclass(frozen=True)
class ClimateDay:
    """One calendar day's temperature and rainfall readings."""

    observed_on: date
    maximum_temperature: float | None
    rainfall: float | None


def _load_measure(path, year, measure):
    """Read one BOM month-by-column table into date-to-value observations."""
    with Path(path).open(newline="", encoding="utf-8-sig") as source:
        rows = list(csv.reader(source))

    header_index = next(
        (
            index for index, row in enumerate(rows)
            if row and row[0].strip() == str(year)
        ),
        None,
    )
    if header_index is None:
        raise ValueError(f"No {year} header found in {Path(path).name}.")

    month_columns = []
    for column, label in enumerate(rows[header_index][1:], start=1):
        month_number = MONTH_NUMBER.get(label.strip()[:3].casefold())
        if month_number is not None:
            month_columns.append((column, month_number))
    if not month_columns:
        raise ValueError(f"No month columns found in {Path(path).name}.")

    observations = {}
    for row in rows[header_index + 1:]:
        if not row:
            continue
        day_match = DAY_PATTERN.fullmatch(row[0].strip())
        if day_match is None:
            continue
        day_number = int(day_match.group(1))

        for column, month_number in month_columns:
            if column >= len(row) or not row[column].strip():
                continue
            try:
                observed_on = date(year, month_number, day_number)
            except ValueError:
                # The table has rows through the 31st; skip impossible dates.
                continue
            try:
                value = float(row[column].strip())
            except ValueError:
                raise ValueError(
                    f"Invalid {measure} value on day {day_number}, "
                    f"month {month_number} in {Path(path).name}."
                ) from None

            if not math.isfinite(value):
                raise ValueError(f"Non-finite {measure} value in {Path(path).name}.")
            if measure == "rainfall" and value < 0:
                raise ValueError("Rainfall values cannot be negative.")
            if measure == "temperature" and not -50 <= value <= 60:
                raise ValueError("Temperature is outside the expected Celsius range.")
            observations[observed_on] = value

    return observations


def load_climate_observations(data_directory=None, year=2024, minimum_records=200):
    """Load and join the two BOM files into one record per observed date."""
    data_dir = (
        Path(data_directory)
        if data_directory is not None
        else Path(__file__).resolve().parent.parent / "Data"
    )
    rainfall_by_day = _load_measure(data_dir / "1.csv", year, "rainfall")
    temperature_by_day = _load_measure(data_dir / "2.csv", year, "temperature")
    dates = sorted(set(rainfall_by_day) | set(temperature_by_day))
    if len(dates) < minimum_records:
        raise ValueError(
            f"Expected at least {minimum_records} daily records; found {len(dates)}."
        )

    return tuple(
        ClimateDay(
            observed_on=observed_on,
            maximum_temperature=temperature_by_day.get(observed_on),
            rainfall=rainfall_by_day.get(observed_on),
        )
        for observed_on in dates
    )


def monthly_summaries(observations):
    """Calculate monthly means, rainfall totals, and data coverage counts."""
    months = defaultdict(list)
    for observation in observations:
        months[observation.observed_on.month].append(observation)

    summaries = []
    for month_number, month_name in enumerate(MONTHS, start=1):
        days = months[month_number]
        temperatures = [
            item.maximum_temperature
            for item in days
            if item.maximum_temperature is not None
        ]
        rainfall = [item.rainfall for item in days if item.rainfall is not None]
        summaries.append(
            {
                "month": month_number,
                "month_name": month_name,
                "season": MONTH_TO_SEASON[month_number],
                "record_days": len(days),
                "temperature_days": len(temperatures),
                "rainfall_days": len(rainfall),
                "rainy_days": sum(value > 0 for value in rainfall),
                "mean_maximum_temperature": (
                    fmean(temperatures) if temperatures else None
                ),
                "rainfall_total": sum(rainfall) if rainfall else None,
            }
        )
    return tuple(summaries)


def annual_summary(observations):
    """Calculate annual averages and observation coverage from daily records."""
    temperatures = [
        item.maximum_temperature
        for item in observations
        if item.maximum_temperature is not None
    ]
    rainfall = [item.rainfall for item in observations if item.rainfall is not None]
    return {
        "record_days": len(observations),
        "temperature_days": len(temperatures),
        "rainfall_days": len(rainfall),
        "mean_maximum_temperature": fmean(temperatures) if temperatures else None,
        "rainfall_total": sum(rainfall) if rainfall else None,
    }
