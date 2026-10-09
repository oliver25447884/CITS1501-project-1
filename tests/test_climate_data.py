"""Automated tests for BOM CSV loading and climate calculations."""

import csv
import tempfile
import unittest
from datetime import date
from pathlib import Path

from modules.climate_data import (
    MONTHS,
    annual_summary,
    load_climate_observations,
    monthly_summaries,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def ordinal(day):
    suffix = "th" if 10 <= day % 100 <= 20 else {
        1: "st", 2: "nd", 3: "rd",
    }.get(day % 10, "th")
    return f"{day}{suffix}"


def write_bom_table(path, year, observations):
    """Create a small fixture in the supplied month-by-column CSV format."""
    rows = [
        ["Daily observations"], ["PERTH METRO"], [],
        [str(year), *[month[:3] for month in MONTHS]],
    ]
    for day in range(1, 32):
        row = [ordinal(day)]
        for month in range(1, 13):
            try:
                date(year, month, day)
            except ValueError:
                row.append("")
            else:
                row.append(observations.get((month, day), ""))
        rows.append(row)
    with path.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream).writerows(rows)


def write_fixture(directory, rainfall=None, temperature=None, year=2024):
    write_bom_table(directory / "1.csv", year, rainfall or {})
    write_bom_table(directory / "2.csv", year, temperature or {})


class ClimateDataTests(unittest.TestCase):
    def test_supplied_files_contain_at_least_200_records(self):
        records = load_climate_observations(PROJECT_ROOT / "Data")
        self.assertGreaterEqual(len(records), 200)

    def test_supplied_leap_year_files_cover_all_366_dates(self):
        records = load_climate_observations(PROJECT_ROOT / "Data")
        self.assertEqual(len(records), 366)
        self.assertEqual(records[0].observed_on, date(2024, 1, 1))
        self.assertEqual(records[-1].observed_on, date(2024, 12, 31))

    def test_monthly_summary_calculates_temperature_rain_and_rainy_days(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_fixture(directory, {(1, 1): "1.5", (1, 2): "0"},
                          {(1, 1): "20", (1, 2): "22"})
            january = monthly_summaries(
                load_climate_observations(directory, minimum_records=0)
            )[0]
        self.assertEqual(january["season"], "Birak")
        self.assertEqual(january["record_days"], 2)
        self.assertEqual(january["mean_maximum_temperature"], 21)
        self.assertEqual(january["rainfall_total"], 1.5)
        self.assertEqual(january["rainy_days"], 1)

    def test_blank_readings_remain_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_fixture(directory, {}, {(1, 1): "20"})
            january = monthly_summaries(
                load_climate_observations(directory, minimum_records=0)
            )[0]
        self.assertEqual(january["rainfall_days"], 0)
        self.assertIsNone(january["rainfall_total"])

    def test_impossible_calendar_date_is_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_fixture(directory, {(2, 1): "2.0"})
            rainfall_file = directory / "1.csv"
            with rainfall_file.open(encoding="utf-8") as source:
                rows = list(csv.reader(source))
            rows[4 + 29][2] = "4.0"  # February 30 is not a valid date.
            with rainfall_file.open("w", newline="", encoding="utf-8") as target:
                csv.writer(target).writerows(rows)
            records = load_climate_observations(directory, minimum_records=0)
        february = [item for item in records if item.observed_on.month == 2]
        self.assertEqual([item.observed_on.day for item in february], [1])

    def test_missing_year_header_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_fixture(directory)
            with self.assertRaisesRegex(ValueError, "2025 header"):
                load_climate_observations(directory, year=2025, minimum_records=0)

    def test_negative_rainfall_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_fixture(directory, {(1, 1): "-0.1"})
            with self.assertRaisesRegex(ValueError, "cannot be negative"):
                load_climate_observations(directory, minimum_records=0)

    def test_malformed_temperature_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_fixture(directory, temperature={(1, 1): "hot"})
            with self.assertRaisesRegex(ValueError, "Invalid temperature"):
                load_climate_observations(directory, minimum_records=0)

    def test_annual_summary_counts_data_and_calculates_mean(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_fixture(directory, {(1, 1): "2", (1, 2): "0"},
                          {(1, 1): "10", (1, 2): "20", (2, 1): "30"})
            summary = annual_summary(
                load_climate_observations(directory, minimum_records=0)
            )
        self.assertEqual(summary["record_days"], 3)
        self.assertEqual(summary["temperature_days"], 3)
        self.assertEqual(summary["rainfall_days"], 2)
        self.assertEqual(summary["mean_maximum_temperature"], 20)
        self.assertEqual(summary["rainfall_total"], 2)

    def test_month_summaries_follow_calendar_order_and_season_mapping(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_fixture(directory, {(1, 1): "1", (2, 1): "1"})
            summaries = monthly_summaries(
                load_climate_observations(directory, minimum_records=0)
            )
        self.assertEqual([item["month_name"] for item in summaries], list(MONTHS))
        self.assertEqual(summaries[0]["season"], "Birak")
        self.assertEqual(summaries[1]["season"], "Bunuru")

    def test_default_minimum_record_requirement_rejects_small_dataset(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            write_fixture(directory, {(1, 1): "1"})
            with self.assertRaisesRegex(ValueError, "at least 200"):
                load_climate_observations(directory)


if __name__ == "__main__":
    unittest.main()
