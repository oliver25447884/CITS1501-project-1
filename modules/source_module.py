"""Source metadata and the scrollable references dialog opened from home."""

import tkinter as tk
import webbrowser
from tkinter import ttk


# Reference content stays beside the dialog that presents it.
SOURCE_ITEMS = (
    {
        "title": "Dr Richard Walley — Heritage plaque artwork story",
        "description": (
            "Cultural context from Nyoongar-Yamatji Elder and artist Dr Richard "
            "Walley: Bonara (the seasons) connects Boodjar, kaatitj, people, "
            "plants and animals. The app attributes this explanation to him "
            "and recognises that knowledge differs between communities."
        ),
        "url": "https://www.wa.gov.au/government/document-collections/heritage-plaque-artwork-story-and-artist-biography",
    },
    {
        "title": "Department of Primary Industries and Regional Development — The Noongar Six Seasons",
        "description": (
            "Perth-region season names and examples of seasonal signs, "
            "including plants, animals, weather and cultural practices. "
            "These examples are place-specific, not a universal description."
        ),
        "url": "https://marinewaters.fish.wa.gov.au/resource/fact-sheet-the-noongar-six-seasons/",
    },
    {
        "title": "Kurongkurl Katitjin, Edith Cowan University — Nyoongar Six Seasons",
        "description": (
            "Educational overview of the six seasons and examples of how "
            "weather, plants and animal life help people read seasonal change."
        ),
        "url": "https://www.ecu.edu.au/centres/kurongkurl-katitjin/cultural-leadership/nyoongar-six-seasons",
    },
    {
        "title": "Your Move — Noongar Season: Makuru",
        "description": (
            "Government of Western Australia school resource noting the "
            "blueberry lily's blue and purple flowers during Makuru; adapted "
            "from Edith Cowan University's seasonal resource."
        ),
        "url": "https://yourmove.org.au/getmedia/97ac12e5-3f45-4b19-9f23-1dac79276d1d/YM-Schools-Noongar-Season-Makuru-%28Interactive%29.pdf",
    },
    {
        "title": "Bureau of Meteorology — Climate Data Online",
        "description": (
            "Daily rainfall and maximum-temperature records for Perth Metro, "
            "station 009225, in 2024. The climate summary view loads the CSV "
            "files and calculates monthly means and totals."
        ),
        "url": "https://www.bom.gov.au/climate/data/",
    },
    {
        "title": "Bureau of Meteorology — About rainfall data",
        "description": "Information about Bureau of Meteorology rainfall data.",
        "url": "https://www.bom.gov.au/climate/cdo/about/about-rain-data.shtml",
    },
    {
        "title": "Bureau of Meteorology — About air temperature data",
        "description": (
            "Information about Bureau of Meteorology air temperature data."
        ),
        "url": "https://www.bom.gov.au/climate/cdo/about/about-airtemp-data.shtml",
    },
)


class SourcePage:
    """Render source records in a transient window owned by the app root."""

    def __init__(self, app):
        """Use the app's root window as the source dialog's parent."""
        self.app = app

    def show_sources_window(self):
        """Build a scrollable source list with links opened in the browser."""
        sources_window = tk.Toplevel(self.app.root)
        sources_window.title("Sources | Noongar Seasons")
        sources_window.geometry("700x520")
        sources_window.minsize(560, 400)
        sources_window.configure(bg="#f4efe7")
        sources_window.transient(self.app.root)

        tk.Label(
            sources_window,
            text="Sources",
            font=("Segoe UI", 22, "bold"),
            fg="#24381d",
            bg="#f4efe7",
        ).pack(pady=(18, 6))
        tk.Label(
            sources_window,
            text="Data and references used by the application.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#f4efe7",
        ).pack(pady=(0, 12))

        list_frame = tk.Frame(sources_window, bg="#f4efe7")
        list_frame.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        canvas = tk.Canvas(
            list_frame,
            bg="#f4efe7",
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=canvas.yview,
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        sources_frame = tk.Frame(canvas, bg="#f4efe7")
        # The embedded frame expands to the canvas width and defines scroll extent.
        sources_window_id = canvas.create_window(
            (0, 0),
            window=sources_frame,
            anchor="nw",
        )
        sources_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                sources_window_id,
                width=event.width,
            ),
        )

        for source in SOURCE_ITEMS:
            source_panel = tk.Frame(
                sources_frame,
                bg="#f7f3ee",
                bd=1,
                relief="solid",
            )
            source_panel.pack(fill="x", padx=4, pady=5)
            tk.Label(
                source_panel,
                text=source["title"],
                font=("Segoe UI", 12, "bold"),
                fg="#24381d",
                bg="#f7f3ee",
                anchor="w",
                justify="left",
                wraplength=590,
            ).pack(fill="x", padx=14, pady=(12, 4))
            tk.Label(
                source_panel,
                text=source["description"],
                font=("Segoe UI", 10),
                fg="#2b2b2b",
                bg="#f7f3ee",
                anchor="w",
                justify="left",
                wraplength=590,
            ).pack(fill="x", padx=14, pady=(0, 6))
            source_link = tk.Label(
                source_panel,
                text=source["url"],
                font=("Segoe UI", 10, "underline"),
                fg="#345c4c",
                bg="#f7f3ee",
                anchor="w",
                cursor="hand2",
                wraplength=590,
            )
            source_link.pack(fill="x", padx=14, pady=(0, 12))
            source_link.bind(
                "<Button-1>",
                lambda event, url=source["url"]: webbrowser.open(url),
            )

        ttk.Button(
            sources_window,
            text="Close",
            command=sources_window.destroy,
        ).pack(pady=(0, 14))
