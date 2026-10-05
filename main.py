import tkinter as tk
import math
from pathlib import Path
from fractions import Fraction
from tkinter import ttk
from Moduals.Question_Modual import (
    NOONGAR_REGIONS,
    REGION_QUESTIONS,
    display_question_results,
)
from Moduals.Security_Modual import SecurityModule
from Moduals.SeasonWheel import SeasonWheel

REGION_IMAGE_FILES = {
    "Whadjuk": "Whadjuk.png",
    "Yued": "Yued.png",
    "Ballardong": "Ballardong.png",
    "Gnaala Karla Booja": "Gnaala Karla Boodja.png",
    "South West Boojarah": "Southwest Boodjarah.png",
    "Wagyl Kaip & Southern Noongar": "Wagyl Kaip Southern Noongar.png",
}


class NoongarSeasonApp:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.season_wheel = SeasonWheel(self)
        self.security = SecurityModule(self)

        self.security.show_startup_page()

    def clear_page(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg="#f4efe7")
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_home_page(self):
        self.clear_page()
        self.root.title("Explore Noongar Seasons")
        self.root.geometry("850x550")
        self.root.minsize(700, 500)

        tk.Label(
            self.current_frame,
            text="Explore the Noongar Seasons",
            font=("Segoe UI", 24, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
        ).pack(pady=(10, 8))

        tk.Label(
            self.current_frame,
            text="Choose an activity below to learn more.",
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
            text="Explore the Noongar Seasons",
            font=("Segoe UI", 16, "bold"),
            fg="#24381d",
            bg="#e7d8c4",
            wraplength=300,
        ).pack(pady=(55, 15))
        tk.Label(
            seasons_panel,
            text="Visit the wheel of seasons and select a season to learn more.",
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
            text="Explore some questions",
            font=("Segoe UI", 16, "bold"),
            fg="#24381d",
            bg="#f7f3ee",
            wraplength=300,
        ).pack(pady=(25, 12))

        self.region_results = tk.Frame(
            region_panel,
            bg="#ffffff",
            height=12,
        )
        self.region_results.pack(fill="both", expand=True, padx=20, pady=12)
        display_question_results(
            self.region_results,
            REGION_QUESTIONS,
            self.show_question_page,
        )

        ttk.Button(
            self.current_frame,
            text="Log out",
            command=self.security.show_login_page,
        ).pack(pady=(12, 0))

    def show_question_page(self, question):
        self.clear_page()
        self.current_frame.pack_configure(pady=(20, 0))
        self.root.title("Question information")
        self.root.geometry("700x760")
        self.root.minsize(550, 500)

        tk.Label(
            self.current_frame,
            text=question["question"],
            font=("Segoe UI", 20, "bold"),
            fg="#24381d",
            bg="#f4efe7",
            wraplength=600,
            justify="center",
        ).pack(padx=30, pady=(45, 25))

        search_panel = tk.Frame(
            self.current_frame,
            bg="#f7f3ee",
            bd=1,
            relief="solid",
        )
        search_panel.pack(fill="x", padx=45, pady=(0, 8))

        tk.Label(
            search_panel,
            text="Search your local council:",
            font=("Segoe UI", 12, "bold"),
            fg="#2b2b2b",
            bg="#f7f3ee",
        ).pack(anchor="w", padx=30, pady=(25, 8))

        search_entry = tk.Entry(
            search_panel,
            font=("Segoe UI", 12),
            width=35,
        )
        search_entry.pack(anchor="w", fill="x", padx=30)

        result_label = tk.Label(
            search_panel,
            text="Enter a council name to see your Noongar region.",
            font=("Segoe UI", 13),
            fg="#24381d",
            bg="#f7f3ee",
            wraplength=540,
            justify="left",
        )
        result_label.pack(anchor="w", padx=30, pady=(20, 10))

        image_placeholder = tk.Frame(self.current_frame, bg="#e7d8c4")
        tk.Label(
            image_placeholder,
            text="The region image will appear here.",
            font=("Segoe UI", 11, "italic"),
            fg="#6b6b6b",
            bg="#e7d8c4",
            height=5,
        ).pack(fill="both", expand=True)
        region_image_cache = {}
        image_state = {
            "regions": [],
            "fallback_text": "The region image will appear here.",
            "size": None,
        }

        def show_region_images(regions, fallback_text):
            image_width = image_placeholder.winfo_width()
            image_height = image_placeholder.winfo_height()
            if (
                image_state["regions"] == regions
                and image_state["fallback_text"] == fallback_text
                and image_state["size"] == (image_width, image_height)
            ):
                return

            image_state["regions"] = regions
            image_state["fallback_text"] = fallback_text
            image_state["size"] = (image_width, image_height)

            for child in image_placeholder.winfo_children():
                child.destroy()

            if image_width <= 1 or image_height <= 1:
                return

            image_row = tk.Frame(image_placeholder, bg="#e7d8c4")
            image_row.pack(side="bottom", anchor="center")
            max_image_width = max(1, image_width // max(1, len(regions)))
            for region in regions:
                image_filename = REGION_IMAGE_FILES.get(region)
                if image_filename is None:
                    continue

                if image_filename not in region_image_cache:
                    image_path = (
                        Path(__file__).resolve().parent
                        / "Data"
                        / "Regions"
                        / image_filename
                    )
                    try:
                        region_image_cache[image_filename] = tk.PhotoImage(
                            file=str(image_path)
                        )
                    except tk.TclError:
                        continue

                image = region_image_cache[image_filename]
                fit_scale = min(
                    1,
                    max_image_width / image.width(),
                    image_height / image.height(),
                )
                scale = Fraction(fit_scale).limit_denominator(12)
                if float(scale) > fit_scale:
                    scale = Fraction(max(1, math.floor(fit_scale * 12)), 12)
                display_image = (
                    image.zoom(scale.numerator, scale.numerator).subsample(
                        scale.denominator, scale.denominator
                    )
                    if scale < 1
                    else image
                )

                image_label = tk.Label(
                    image_row,
                    image=display_image,
                    bg="#e7d8c4",
                )
                image_label.image = display_image
                image_label.pack(side="left", anchor="s", padx=5)

            if not image_placeholder.winfo_children():
                tk.Label(
                    image_placeholder,
                    text=fallback_text,
                    font=("Segoe UI", 11, "italic"),
                    fg="#6b6b6b",
                    bg="#e7d8c4",
                    height=5,
                ).pack(fill="both", expand=True)
            elif not image_row.winfo_children():
                image_row.destroy()
                tk.Label(
                    image_placeholder,
                    text=fallback_text,
                    font=("Segoe UI", 11, "italic"),
                    fg="#6b6b6b",
                    bg="#e7d8c4",
                    height=5,
                ).pack(side="bottom", fill="x")

        def update_region_result(event=None):
            council = search_entry.get().strip().casefold()
            matching_regions = [
                region
                for region, councils in NOONGAR_REGIONS.items()
                if council in {name.casefold() for name in councils}
            ]
            if len(matching_regions) == 1:
                result_label.config(
                    text=f"You live in the {matching_regions[0]} region."
                )
            elif matching_regions:
                listed_regions = ", ".join(matching_regions[:-1])
                result_label.config(
                    text=(
                        f"This council is listed in the {listed_regions} and "
                        f"{matching_regions[-1]} regions."
                    )
                )
            elif council:
                result_label.config(text="Council not found in the Noongar council list.")
            else:
                result_label.config(
                    text="Enter a council name to see your Noongar region."
                )
            fallback_text = (
                "No region image is available."
                if council
                else "The region image will appear here."
            )
            show_region_images(matching_regions, fallback_text)

        def resize_region_images(event):
            if image_state["size"] != (event.width, event.height):
                show_region_images(
                    image_state["regions"], image_state["fallback_text"]
                )

        image_placeholder.bind("<Configure>", resize_region_images)

        search_entry.bind("<KeyRelease>", update_region_result)
        search_entry.bind("<Return>", update_region_result)
        search_entry.focus_set()

        ttk.Button(
            self.current_frame,
            text="Back to explore",
            command=self.show_home_page,
        ).pack(pady=(0, 8))
        image_placeholder.pack(fill="both", expand=True, padx=20, pady=0)

    def show_information_page(self):
        self.season_wheel.show_information_page()

    def show_season_page(self, season_name):
        self.season_wheel.show_season_page(season_name)


if __name__ == "__main__":
    root = tk.Tk()
    app = NoongarSeasonApp(root)
    root.mainloop()
