"""Validate BOM CSV observations and calculate values for climate_page.py."""

import csv
import math
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from statistics import fmean

from modules.season_calendar import season_for_month


# CSV parsing expects month abbreviations; output uses full calendar names.
MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)
MONTH_NUMBER = {name[:3].casefold(): number for number, name in enumerate(MONTHS, 1)}
DAY_PATTERN = re.compile(r"^(\d{1,2})(?:st|nd|rd|th)?$", re.IGNORECASE)


@dataclass(frozen=True)
class ClimateDay:
    """Immutable joined observation; either measurement may be missing."""

    observed_on: date
    maximum_temperature: float | None
    rainfall: float | None


# CSV input is validated here before either page uses the observations.
def _load_measure(path, year, measure):
    """Parse one BOM table, validating dates and values for a single measure."""
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
    """Join rainfall and temperature CSVs while retaining missing readings."""
    data_dir = (
        Path(data_directory)
        if data_directory is not None
        else Path(__file__).resolve().parent.parent / "Data"
    )
    rainfall_by_day = _load_measure(data_dir / "1.csv", year, "rainfall")
    temperature_by_day = _load_measure(data_dir / "2.csv", year, "temperature")
    # Union dates so a missing measurement does not discard the other value.
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


# These aggregations feed the monthly climate page and annual summary cards.
def monthly_summaries(observations):
    """Aggregate daily records by calendar month for the climate table."""
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
                "season": season_for_month(month_number),
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
    """Summarize yearly coverage and totals for the climate page metric cards."""
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
