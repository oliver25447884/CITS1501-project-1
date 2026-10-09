"""Climate report UI; parsing and aggregation are delegated to climate_data."""

import tkinter as tk
from tkinter import ttk

from modules.climate_data import (
    annual_summary,
    load_climate_observations,
    monthly_summaries,
)
from modules.season_wheel import SEASONS


class ClimatePage:
    """Render climate summaries and route selected months to season details."""

    def __init__(self, app):
        """Use the app shell for window state and navigation callbacks."""
        self.app = app

    def show_climate_page(self):
        """Load validated records, show yearly metrics, and filter monthly rows."""
        self.app.clear_page()
        self.app.root.title("2024 Perth climate data | Noongar Seasons")
        self.app.set_windowed_size("1050x760", (800, 620))

        heading = tk.Label(
            self.app.current_frame,
            text="Perth climate in 2024",
            font=("Segoe UI", 24, "bold"),
            fg="#24381d",
            bg="#f4efe7",
        )
        heading.pack(pady=(15, 4))
        tk.Label(
            self.app.current_frame,
            text=(
                "Daily Bureau of Meteorology observations are loaded from the "
                "project CSV files and summarised by month."
            ),
            font=("Segoe UI", 10),
            fg="#4a4a4a",
            bg="#f4efe7",
            wraplength=900,
            justify="center",
        ).pack(padx=25, pady=(0, 12))

        try:
            # Data module owns parsing and calculations; this controller formats them.
            records = load_climate_observations()
            month_data = monthly_summaries(records)
            year_data = annual_summary(records)
        except (OSError, ValueError) as error:
            tk.Label(
                self.app.current_frame,
                text=f"The climate data could not be loaded.\n{error}",
                font=("Segoe UI", 11),
                fg="#9a3e32",
                bg="#f7f3ee",
                wraplength=700,
                justify="left",
                padx=20,
                pady=20,
            ).pack(fill="x", padx=40, pady=20)
            ttk.Button(
                self.app.current_frame,
                text="Back to explore",
                command=self.app.show_home_page,
            ).pack(pady=8)
            return

        summary_cards = tk.Frame(self.app.current_frame, bg="#f4efe7")
        summary_cards.pack(fill="x", padx=24, pady=(2, 14))
        metric_values = (
            ("DAILY RECORDS", f"{year_data['record_days']}"),
            (
                "MEAN DAILY MAX",
                f"{year_data['mean_maximum_temperature']:.1f} °C"
                if year_data["mean_maximum_temperature"] is not None
                else "No data",
            ),
            (
                "TOTAL RAINFALL",
                f"{year_data['rainfall_total']:.1f} mm"
                if year_data["rainfall_total"] is not None
                else "No data",
            ),
        )
        for column, (label, value) in enumerate(metric_values):
            # Grid weights keep all annual metric cards at matching widths.
            summary_cards.columnconfigure(column, weight=1, uniform="year_metric")
            card = tk.Frame(
                summary_cards,
                bg="#fffdf9",
                highlightbackground="#e1d8ca",
                highlightthickness=1,
                padx=12,
                pady=10,
            )
            card.grid(row=0, column=column, sticky="nsew", padx=5)
            tk.Label(
                card,
                text=value,
                font=("Segoe UI", 17, "bold"),
                fg="#345c4c",
                bg="#fffdf9",
            ).pack(pady=(0, 4))
            tk.Label(
                card,
                text=label,
                font=("Segoe UI", 8, "bold"),
                fg="#65715e",
                bg="#fffdf9",
            ).pack()

        filter_bar = tk.Frame(self.app.current_frame, bg="#f4efe7")
        filter_bar.pack(fill="x", padx=30, pady=(0, 8))
        tk.Label(
            filter_bar,
            text="Filter by season:",
            font=("Segoe UI", 10, "bold"),
            fg="#24381d",
            bg="#f4efe7",
        ).pack(side="left", padx=(0, 8))
        season_filter = tk.StringVar(value="All seasons")
        ttk.Combobox(
            filter_bar,
            textvariable=season_filter,
            values=("All seasons", *SEASONS.keys()),
            state="readonly",
            width=18,
        ).pack(side="left")

        table_frame = tk.Frame(self.app.current_frame, bg="#f4efe7")
        table_frame.pack(fill="both", expand=True, padx=24)
        columns = (
            "month", "season", "days", "temperature_days", "mean_temp",
            "rainy_days", "rainfall",
        )
        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12,
        )
        # Column identifiers match fields returned by monthly_summaries.
        headings = {
            "month": ("Month", 120),
            "season": ("Perth season guide", 150),
            "days": ("Days", 75),
            "temperature_days": ("Temp. readings", 115),
            "mean_temp": ("Mean max (°C)", 130),
            "rainy_days": ("Rainy days", 95),
            "rainfall": ("Rain total (mm)", 130),
        }
        for column, (label, width) in headings.items():
            table.heading(column, text=label)
            table.column(column, width=width, minwidth=70, anchor="center")
        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=table.yview
        )
        table.configure(yscrollcommand=scrollbar.set)
        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        season_colours = {
            "Birak": "#fbf0e8", "Bunuru": "#f8f0e3", "Djeran": "#edf1e9",
            "Makuru": "#eaf1f3", "Djilba": "#f2edf3", "Kambarang": "#f4f0e1",
        }
        for season_name, colour in season_colours.items():
            table.tag_configure(season_name, background=colour)

        result_note = tk.Label(
            self.app.current_frame,
            text="",
            font=("Segoe UI", 9),
            fg="#65715e",
            bg="#f4efe7",
        )
        result_note.pack(pady=(6, 2))

        def update_table(*_args):
            """Rebuild visible rows after the readonly season filter changes."""
            table.delete(*table.get_children())
            selected = season_filter.get()
            visible = [
                item for item in month_data
                if selected == "All seasons" or item["season"] == selected
            ]
            for item in visible:
                mean_temp = item["mean_maximum_temperature"]
                rain_total = item["rainfall_total"]
                table.insert(
                    "",
                    "end",
                    values=(
                        item["month_name"],
                        item["season"],
                        item["record_days"],
                        item["temperature_days"],
                        f"{mean_temp:.1f}" if mean_temp is not None else "—",
                        item["rainy_days"],
                        f"{rain_total:.1f}" if rain_total is not None else "—",
                    ),
                    tags=(item["season"],),
                )
            result_note.configure(
                text=(
                    f"Showing {len(visible)} months from {year_data['record_days']} "
                    "daily records. Double-click a row to open its season page."
                )
            )

        def open_selected_season(_event=None):
            """Route a selected month row to its corresponding season page."""
            selected_row = table.selection()
            if selected_row:
                season_name = table.item(selected_row[0], "values")[1]
                self.app.show_season_page(season_name)

        season_filter.trace_add("write", update_table)
        update_table()
        table.bind("<Double-1>", open_selected_season)

        tk.Label(
            self.app.current_frame,
            text=(
                "The season names are a Perth-area month guide. January and "
                "December are listed separately because these records cover "
                "the 2024 calendar year."
            ),
            font=("Segoe UI", 9),
            fg="#65715e",
            bg="#f4efe7",
            wraplength=900,
            justify="center",
        ).pack(padx=20, pady=(0, 4))
        ttk.Button(
            self.app.current_frame,
            text="Back to explore",
            command=self.app.show_home_page,
        ).pack(pady=(0, 10))
