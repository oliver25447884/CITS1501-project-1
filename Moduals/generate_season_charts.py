import csv
import re
from datetime import date, timedelta
from pathlib import Path
from statistics import median

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from Moduals.SeasonWheel import SEASON_GRAPH_DATA, SEASON_GRAPH_FILES, SEASONS


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "Data"
REGIONS_DIR = DATA_DIR / "Regions"
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
SEASON_PERIODS = {
    "Birak": (date(2023, 12, 1), date(2024, 1, 31)),
    "Bunuru": (date(2024, 2, 1), date(2024, 3, 31)),
    "Djeran": (date(2024, 4, 1), date(2024, 5, 31)),
    "Makuru": (date(2024, 6, 1), date(2024, 7, 31)),
    "Djilba": (date(2024, 8, 1), date(2024, 9, 30)),
    "Kambarang": (date(2024, 10, 1), date(2024, 11, 30)),
}
PAPER = "#f4efe7"
PANEL = "#f7f3ee"
INK = "#2b2b2b"
GREEN = "#345c4c"
TEMPERATURE = "#ad5b47"
RAINFALL = "#5c8188"
GRID = "#d8c8b4"


def load_daily_table(filename, blank_value=None):
    path = DATA_DIR / filename
    with path.open(newline="", encoding="utf-8-sig") as source:
        rows = list(csv.reader(source))

    header_index = next(
        index for index, row in enumerate(rows) if row and row[0].strip() == "2024"
    )
    daily_values = {}
    for row in rows[header_index + 1 :]:
        if not row or not re.fullmatch(r"\d+(?:st|nd|rd|th)", row[0].strip().lower()):
            continue
        day = int(re.match(r"\d+", row[0]).group())
        for month_index, month in enumerate(MONTHS, start=1):
            column_index = month_index
            if column_index >= len(row):
                continue
            try:
                observation_date = date(2024, month_index, day)
            except ValueError:
                continue
            value = row[column_index].strip()
            daily_values[observation_date] = float(value) if value else blank_value
    return daily_values


def _trace_temperature_pixels(image):
    trace_by_x = {}
    for x in range(60, image.width - 55):
        y_values = []
        for y in range(65, 294):
            red, green, blue = image.getpixel((x, y))
            if red > 100 and red > green * 1.6 and red > blue * 1.4:
                y_values.append(y)
        if y_values:
            trace_by_x[x] = median(y_values)
    return trace_by_x


def recover_birak_december(january_temperatures, target_season_mean):
    source_image = Image.open(
        REGIONS_DIR / "noongar_seasons_perth (dragged).jpg"
    ).convert("RGB")
    trace_by_x = _trace_temperature_pixels(source_image)

    def sample_y(x_position):
        center = round(x_position)
        candidates = [
            trace_by_x[x]
            for x in range(center - 2, center + 3)
            if x in trace_by_x
        ]
        return median(candidates) if candidates else None

    best_fit = None
    for x_start in np.arange(66, 77, 0.2):
        for x_step in np.arange(12.8, 13.4, 0.04):
            observed_y = []
            observed_temperature = []
            for day_index, temperature in enumerate(january_temperatures):
                if temperature is None:
                    continue
                y_position = sample_y(x_start + (31 + day_index) * x_step)
                if y_position is not None:
                    observed_y.append(y_position)
                    observed_temperature.append(temperature)
            if len(observed_y) < 25:
                continue
            slope, intercept = np.polyfit(observed_y, observed_temperature, 1)
            errors = slope * np.asarray(observed_y) + intercept - np.asarray(observed_temperature)
            root_mean_square_error = float(np.sqrt(np.mean(errors ** 2)))
            if best_fit is None or root_mean_square_error < best_fit[0]:
                best_fit = (
                    root_mean_square_error,
                    x_start,
                    x_step,
                    slope,
                    intercept,
                )

    if best_fit is None:
        raise RuntimeError("Could not calibrate the Birak source chart.")

    error, x_start, x_step, slope, intercept = best_fit
    december = []
    for day_index in range(31):
        y_position = sample_y(x_start + day_index * x_step)
        december.append(
            slope * y_position + intercept if y_position is not None else np.nan
        )

    december = np.asarray(december, dtype=float)
    missing = np.isnan(december)
    if missing.any():
        december[missing] = np.interp(
            np.flatnonzero(missing),
            np.flatnonzero(~missing),
            december[~missing],
        )

    valid_january = [value for value in january_temperatures if value is not None]
    target_count = len(december) + len(valid_january)
    correction = (
        target_season_mean * target_count
        - float(december.sum())
        - sum(valid_january)
    ) / len(december)
    december = np.clip(december + correction, 0, 50)
    print(f"Birak December trace calibrated against January (RMSE {error:.2f} C).")
    return december.tolist()


def season_observations(season_name, temperatures, rainfall):
    start, end = SEASON_PERIODS[season_name]
    dates = []
    temperature_values = []
    rainfall_values = []
    current_date = start
    december_values = None
    if season_name == "Birak":
        january = [temperatures.get(date(2024, 1, day)) for day in range(1, 32)]
        december_values = recover_birak_december(
            january,
            SEASON_GRAPH_DATA[season_name]["temperature"],
        )

    while current_date <= end:
        dates.append(current_date)
        if current_date.year == 2023:
            day_index = (current_date - start).days
            temperature_values.append(december_values[day_index])
            rainfall_values.append(0.0)
        else:
            temperature_values.append(temperatures.get(current_date))
            rainfall_values.append(rainfall.get(current_date, 0.0) or 0.0)
        current_date += timedelta(days=1)

    if season_name == "Birak":
        recorded_rainfall = sum(rainfall_values)
        expected_rainfall = SEASON_GRAPH_DATA[season_name]["rainfall_total"]
        if abs(recorded_rainfall - expected_rainfall) > 0.1:
            raise ValueError(
                "Birak's 2023 rainfall values are incomplete in the supplied CSVs."
            )
    return dates, temperature_values, rainfall_values


def draw_season_chart(season_name, dates, temperatures, rainfall):
    means = SEASON_GRAPH_DATA[season_name]
    figure, temperature_axis = plt.subplots(figsize=(12, 5.25), dpi=220)
    figure.patch.set_facecolor(PAPER)
    temperature_axis.set_facecolor(PANEL)
    rainfall_axis = temperature_axis.twinx()
    rainfall_axis.set_facecolor("none")

    temperature_axis.plot(
        dates,
        temperatures,
        color=TEMPERATURE,
        linewidth=1.8,
        marker="o",
        markersize=2.1,
        label="Daily maximum temperature",
        zorder=4,
    )
    temperature_axis.axhline(
        means["temperature"],
        color=TEMPERATURE,
        linewidth=1.3,
        linestyle=(0, (5, 3)),
        alpha=0.75,
        label=f"Season mean {means['temperature']:.1f} C",
    )
    rainfall_axis.plot(
        dates,
        rainfall,
        color=RAINFALL,
        linewidth=1.6,
        marker="o",
        markersize=2,
        label="Daily rainfall",
        zorder=3,
    )
    rainfall_axis.axhline(
        means["rainfall_daily"],
        color=RAINFALL,
        linewidth=1.3,
        linestyle=(0, (5, 3)),
        alpha=0.75,
        label=f"Season mean {means['rainfall_daily']:.2f} mm/day",
    )

    temperature_axis.set_ylim(0, 50)
    rainfall_axis.set_ylim(0, 50)
    temperature_axis.set_ylabel("Daily maximum temperature (C)", color=TEMPERATURE)
    rainfall_axis.set_ylabel("Daily rainfall (mm)", color=RAINFALL)
    temperature_axis.tick_params(axis="y", colors=TEMPERATURE)
    rainfall_axis.tick_params(axis="y", colors=RAINFALL)
    temperature_axis.set_yticks(range(0, 51, 10))
    rainfall_axis.set_yticks(range(0, 51, 10))
    temperature_axis.grid(axis="y", color=GRID, linewidth=0.7, alpha=0.7)
    temperature_axis.set_axisbelow(True)
    temperature_axis.set_xlim(dates[0], dates[-1])

    month_starts = [index for index, day in enumerate(dates) if day.day == 1]
    for month_index in month_starts[1:]:
        temperature_axis.axvline(
            dates[month_index],
            color=GRID,
            linewidth=0.9,
            linestyle=":",
            alpha=0.9,
        )

    temperature_axis.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    temperature_axis.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
    temperature_axis.tick_params(axis="x", colors=INK, labelsize=8, length=3)
    temperature_axis.set_xlabel("Daily observations", color=GREEN, labelpad=8)

    handles_left, labels_left = temperature_axis.get_legend_handles_labels()
    handles_right, labels_right = rainfall_axis.get_legend_handles_labels()
    figure.legend(
        handles_left + handles_right,
        labels_left + labels_right,
        loc="lower center",
        ncol=2,
        frameon=False,
        fontsize=8,
        labelcolor=INK,
        bbox_to_anchor=(0.5, 0.075),
    )

    period = means["period"]
    figure.suptitle(
        f"{season_name}  |  Perth daily climate",
        x=0.09,
        y=0.97,
        ha="left",
        fontsize=15,
        fontweight="bold",
        color=GREEN,
    )
    temperature_axis.set_title(period, loc="left", fontsize=9, color=INK, pad=8)
    for month_index, month_start in enumerate(month_starts):
        month_end = (
            month_starts[month_index + 1] - 1
            if month_index + 1 < len(month_starts)
            else len(dates) - 1
        )
        midpoint = dates[(month_start + month_end) // 2]
        temperature_axis.text(
            midpoint,
            -0.24,
            dates[month_start].strftime("%B %Y"),
            transform=temperature_axis.get_xaxis_transform(),
            ha="center",
            va="top",
            fontsize=8,
            color=GREEN,
        )

    source_note = (
        "Source: Bureau of Meteorology, Climate Data Online · Perth Metro · "
        "Station 009225 · IDCJAC0010 / IDCJAC0009"
    )
    figure.text(0.5, 0.015, source_note, ha="center", fontsize=6.5, color="#64716a")
    figure.subplots_adjust(left=0.10, right=0.90, top=0.85, bottom=0.27)

    output_path = REGIONS_DIR / SEASON_GRAPH_FILES[season_name]
    figure.savefig(output_path, dpi=220, facecolor=figure.get_facecolor())
    plt.close(figure)
    return output_path


def generate_charts():
    temperatures = load_daily_table("2.csv")
    rainfall = load_daily_table("1.csv", blank_value=0.0)
    for season_name in SEASONS:
        dates, temp_values, rain_values = season_observations(
            season_name,
            temperatures,
            rainfall,
        )
        output_path = draw_season_chart(
            season_name,
            dates,
            temp_values,
            rain_values,
        )
        print(output_path.relative_to(ROOT))


if __name__ == "__main__":
    generate_charts()