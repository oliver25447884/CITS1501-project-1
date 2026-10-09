"""Application entry point, shared window state, styling, and screen routing."""

import tkinter as tk
from tkinter import ttk

# Feature controllers own screen-specific UI; the app shell supplies navigation.
from modules.question_module import (
    FAQ_ITEMS,
    QuestionPages,
    REGION_QUESTIONS,
    display_question_results,
)
from modules.security_module import SecurityModule
from modules.source_module import SourcePage
from modules.climate_page import ClimatePage
from modules.season_wheel import SeasonWheel


class NoongarSeasonApp:
    """Own the root window and wire navigation to feature controllers."""

    def __init__(self, root):
        """Create feature controllers around one shared Tk root window."""
        self.root = root
        self.root.configure(bg="#f4efe7")
        self._configure_styles()
        self.current_frame = None
        self.season_wheel = SeasonWheel(self)
        self.climate_page = ClimatePage(self)
        self.question_pages = QuestionPages(self)
        self.source_page = SourcePage(self)
        self.security = SecurityModule(self)

        self.security.show_startup_page()

    def _configure_styles(self):
        """Set the ttk button theme used consistently across feature screens."""
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure(
            "TButton",
            font=("TkDefaultFont", 10, "bold"),
            foreground="#ffffff",
            background="#345c4c",
            borderwidth=0,
            padding=(12, 8),
        )
        style.map(
            "TButton",
            foreground=[("active", "#ffffff")],
            background=[("active", "#244638")],
        )

    def set_windowed_size(self, geometry, minimum_size):
        """Clamp requested geometry to the display and apply a usable minimum."""
        requested_width, requested_height = map(int, geometry.split("x"))
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        width = min(requested_width, max(400, screen_width - 48))
        height = min(requested_height, max(360, screen_height - 80))
        self.root.minsize(1, 1)
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(min(minimum_size[0], width), min(minimum_size[1], height))

    def clear_page(self):
        """Destroy the active page and mount a fresh shared content frame."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg="#f4efe7")
        self.current_frame.pack(fill="both", expand=True)

    def show_home_page(self):
        """Build the landing screen and connect it to app feature controllers."""
        self.clear_page()
        self.root.title("Explore Noongar Seasons")
        self.set_windowed_size("850x620", (700, 540))

        ttk.Button(
            self.current_frame,
            text="Sources",
            command=self.show_sources_window,
        ).pack(anchor="nw", padx=4, pady=(0, 2))
        tk.Label(
            self.current_frame,
            text="Explore the Noongar Seasons",
            font=("Segoe UI", 24, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
        ).pack(pady=(10, 8))

        tk.Label(
            self.current_frame,
            text="A Perth-area guide to changing weather, plants, animals and Country.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#f4efe7",
        ).pack(pady=(0, 18))

        content = tk.Frame(self.current_frame, bg="#f4efe7")
        content.pack(fill="both", expand=True, padx=10)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        seasons_panel = tk.Frame(content, bg="#e7d8c4", bd=1, relief="solid")
        seasons_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(
            seasons_panel,
            text="The six-season cycle",
            font=("Segoe UI", 16, "bold"),
            fg="#24381d",
            bg="#e7d8c4",
            wraplength=300,
        ).pack(pady=(55, 15))
        tk.Label(
            seasons_panel,
            text="Choose a season to explore local signs and Perth weather.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#e7d8c4",
            wraplength=300,
            justify="center",
        ).pack(padx=25, pady=(0, 25))
        ttk.Button(
            seasons_panel,
            text="Open wheel of seasons",
            command=self.season_wheel.show_information_page,
        ).pack()

        region_panel = tk.Frame(content, bg="#f7f3ee", bd=1, relief="solid")
        region_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(
            region_panel,
            text="Questions & answers",
            font=("Segoe UI", 16, "bold"),
            fg="#24381d",
            bg="#f7f3ee",
            wraplength=300,
        ).pack(pady=(25, 12))

        tk.Label(
            region_panel,
            text="Select a question to read its answer:",
            font=("Segoe UI", 10),
            fg="#4a4a4a",
            bg="#f7f3ee",
        ).pack(anchor="w", padx=20, pady=(0, 8))

        self.region_results = tk.Frame(
            region_panel,
            bg="#ffffff",
            height=12,
        )
        self.region_results.pack(fill="both", expand=True, padx=20, pady=(0, 12))
        # FAQ buttons route through QuestionPages; its callbacks return here.
        display_question_results(
            self.region_results,
            (*REGION_QUESTIONS, *FAQ_ITEMS),
            self.question_pages.show_question_page,
        )

        ttk.Button(
            self.current_frame,
            text="Log out",
            command=self.security.show_login_page,
        ).pack(pady=(12, 0))

        ttk.Button(
            self.current_frame,
            text="Explore 2024 climate data",
            command=self.show_climate_page,
        ).pack(pady=(8, 0))

        tk.Label(
            self.current_frame,
            text=(
                "We acknowledge the Whadjuk Noongar people as the Traditional "
                "Owners of the lands and waters where Perth is situated, and "
                "pay our respects to Elders past and present."
            ),
            font=("Segoe UI", 9),
            fg="#53624d",
            bg="#f4efe7",
            wraplength=780,
            justify="center",
        ).pack(fill="x", padx=25, pady=(7, 6))

    def show_sources_window(self):
        """Delegate the references dialog to the sources feature."""
        self.source_page.show_sources_window()

    def show_climate_page(self):
        """Delegate climate rendering to the climate feature controller."""
        self.climate_page.show_climate_page()

    def show_season_page(self, season_name):
        """Route season selections from question and climate screens to the wheel."""
        self.season_wheel.show_season_page(season_name)


if __name__ == "__main__":
    # Importing main.py exposes the app class without starting a GUI.
    root = tk.Tk()
    app = NoongarSeasonApp(root)
    root.mainloop()
