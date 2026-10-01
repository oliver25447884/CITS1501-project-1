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


SEASONS = {
    "Birak": {
        "months": "December to January",
        "description": "Birak is the hottest and driest time of the year. It is a season of warmth, long daylight hours, and strong sunshine. The land is often dry and the weather can be very hot.",
        "meaning": "This season marks the height of summer in the Noongar calendar, when people traditionally paid close attention to weather, water, and the changing landscape.",
    },
    "Bunuru": {
        "months": "February to March",
        "description": "Bunuru is the second part of summer. It remains warm and can feel very intense, but the weather begins to shift as the season progresses.",
        "meaning": "This time is associated with long hot days, with the landscape beginning to prepare for the cooler months ahead.",
    },
    "Djeran": {
        "months": "April to May",
        "description": "Djeran brings the first cooler weather of the year. Days become milder and the landscape begins to change as autumn settles in.",
        "meaning": "This season is linked with leaves falling, cooler winds, and the start of a time of transition as the land moves from warm to cool.",
    },
    "Makuru": {
        "months": "June to July",
        "description": "Makuru is the wettest part of the year. It brings cooler temperatures, rain, and the strongest winter conditions.",
        "meaning": "This season is closely connected with the colder months, more rainfall, and the deeper seasonal rhythms of the environment.",
    },
    "Djilba": {
        "months": "August to September",
        "description": "Djilba is the time of early spring. The weather becomes less cold and the landscape begins to wake up again.",
        "meaning": "This season signals renewal and the first signs of new growth, as nature starts to become active after winter.",
    },
    "Kambarang": {
        "months": "October to November",
        "description": "Kambarang is a season of flowering and new life. The land is green, vibrant, and full of movement as spring grows stronger.",
        "meaning": "This is a time of growth, abundance, and the return of energy across the environment as the warmer season approaches.",
    },
}

CLIMATE_DATA = {
    "Birak": {"rainfall": 23, "temperature": 27.4},
    "Bunuru": {"rainfall": 28, "temperature": 26.1},
    "Djeran": {"rainfall": 91, "temperature": 21.1},
    "Makuru": {"rainfall": 173, "temperature": 16.2},
    "Djilba": {"rainfall": 119, "temperature": 15.7},
    "Kambarang": {"rainfall": 61, "temperature": 19.6},
}
REGION_IMAGE_FILES = {
    "Whadjuk": "Whadjuk.png",
    "Yued": "Yued.png",
    "Ballardong": "Ballardong.png",
    "Gnaala Karla Booja": "Gnaala Karla Boodja.png",
    "South West Boojarah": "Southwest Boodjarah.png",
    "Wagyl Kaip & Southern Noongar": "Wagyl Kaip Southern Noongar.png",
}
}


class NoongarSeasonApp:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.security = SecurityModule(self)

        self.security.show_login_page()

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
            command=self.show_information_page,
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
        self.clear_page()
        self.root.title("Wheel of Noongar Seasons")
        self.root.geometry("950x900")
        self.root.minsize(760, 780)

        title = tk.Label(
            self.current_frame,
            text="Noongar Seasons",
            font=("Segoe UI", 24, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
            pady=15,
        )
        title.pack()

        intro = tk.Label(
            self.current_frame,
            text="The six seasons recognised by Noongar people in the South West of Western Australia.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#f4efe7",
            wraplength=780,
            justify="center",
        )
        intro.pack(pady=(0, 12))

        canvas = tk.Canvas(
            self.current_frame,
            width=500,
            height=470,
            bg="#f4efe7",
            highlightthickness=0,
        )
        canvas.pack(padx=20, pady=(0, 5))

        center_x, center_y = 250, 225
        outer_radius = 190
        inner_radius = 82
        colours = ["#d77a61", "#e2a653", "#c9b458", "#7596a8", "#77a889", "#9cbd82"]
        season_names = list(SEASONS)

        canvas.create_oval(
            center_x - outer_radius - 5,
            center_y - outer_radius - 5,
            center_x + outer_radius + 5,
            center_y + outer_radius + 5,
            outline="#d8c8b4",
            width=2,
        )

        for index, season_name in enumerate(season_names):
            start_angle = 90 - index * 60
            arc_tag = f"season_{index}"
            canvas.create_arc(
                center_x - outer_radius,
                center_y - outer_radius,
                center_x + outer_radius,
                center_y + outer_radius,
                start=start_angle,
                extent=-60,
                fill=colours[index],
                outline="#f4efe7",
                width=3,
                tags=arc_tag,
            )

            label_angle = math.radians(start_angle - 30)
            label_x = center_x + 135 * math.cos(label_angle)
            label_y = center_y - 135 * math.sin(label_angle)
            canvas.create_text(
                label_x,
                label_y,
                text=season_name,
                font=("Segoe UI", 11, "bold"),
                fill="#fffdfb",
                tags=arc_tag,
            )
            canvas.tag_bind(
                arc_tag,
                "<Enter>",
                lambda event, tag=arc_tag: canvas.scale(
                    tag, center_x, center_y, 1.04, 1.04
                ),
            )
            canvas.tag_bind(
                arc_tag,
                "<Leave>",
                lambda event, tag=arc_tag: canvas.scale(
                    tag, center_x, center_y, 1 / 1.04, 1 / 1.04
                ),
            )
            canvas.tag_bind(arc_tag, "<Button-1>", lambda event, name=season_name: self.show_season_page(name))

        canvas.create_oval(
            center_x - inner_radius,
            center_y - inner_radius,
            center_x + inner_radius,
            center_y + inner_radius,
            fill="#f7f3ee",
            outline="#d8c8b4",
            width=2,
        )
        canvas.create_text(
            center_x,
            center_y - 12,
            text="Noongar",
            font=("Segoe UI", 15, "bold"),
            fill="#24381d",
        )
        canvas.create_text(
            center_x,
            center_y + 14,
            text="Seasons",
            font=("Segoe UI", 11),
            fill="#4e5c46",
        )

        graph_title = tk.Label(
            self.current_frame,
            text="Perth climate by season",
            font=("Segoe UI", 15, "bold"),
            fg="#24381d",
            bg="#f4efe7",
        )
        graph_title.pack(pady=(4, 0))

        graph_note = tk.Label(
            self.current_frame,
            text="Average rainfall and temperature across each two-month season",
            font=("Segoe UI", 10),
            fg="#4e5c46",
            bg="#f4efe7",
        )
        graph_note.pack(pady=(0, 4))

        graph = tk.Canvas(
            self.current_frame,
            width=760,
            height=190,
            bg="#f7f3ee",
            highlightthickness=0,
        )
        graph.pack(padx=20, pady=(0, 5))
        self.draw_climate_graph(graph)

        ttk.Button(
            self.current_frame,
            text="Back to explore",
            command=self.show_home_page,
        ).pack(pady=(0, 8))

        close_button = ttk.Button(self.current_frame, text="Close", command=self.root.destroy)
        close_button.pack(pady=(0, 15))

    def draw_climate_graph(self, graph):
        left, top, width, height = 62, 22, 650, 125
        max_rainfall = 180
        max_temperature = 30
        season_names = list(CLIMATE_DATA)
        column_width = width / len(season_names)

        for grid_value in (0, 60, 120, 180):
            y = top + height - (grid_value / max_rainfall) * height
            graph.create_line(left, y, left + width, y, fill="#d8cfc1")
            graph.create_text(left - 12, y, text=str(grid_value), anchor="e", fill="#6f756c", font=("Segoe UI", 8))

        graph.create_text(12, top - 8, text="mm", anchor="w", fill="#5a86a5", font=("Segoe UI", 8, "bold"))
        graph.create_text(left + width + 8, top - 8, text="°C", anchor="w", fill="#d47752", font=("Segoe UI", 8, "bold"))

        for index, season_name in enumerate(season_names):
            values = CLIMATE_DATA[season_name]
            center = left + column_width * index + column_width / 2
            rainfall_height = values["rainfall"] / max_rainfall * height
            temperature_height = values["temperature"] / max_temperature * height
            graph.create_rectangle(center - 17, top + height - rainfall_height, center - 3, top + height, fill="#5a86a5", outline="")
            graph.create_rectangle(center + 3, top + height - temperature_height, center + 17, top + height, fill="#d47752", outline="")
            graph.create_text(center - 10, top + height - rainfall_height - 8, text=str(values["rainfall"]), fill="#315b70", font=("Segoe UI", 8, "bold"))
            graph.create_text(center + 10, top + height - temperature_height - 8, text=str(values["temperature"]), fill="#a04f34", font=("Segoe UI", 8, "bold"))
            graph.create_text(center, top + height + 18, text=season_name, fill="#2b2b2b", font=("Segoe UI", 9, "bold"))

        graph.create_rectangle(left + width - 130, 2, left + width - 118, 14, fill="#5a86a5", outline="")
        graph.create_text(left + width - 112, 8, text="Rainfall", anchor="w", fill="#4e5c46", font=("Segoe UI", 8))
        graph.create_rectangle(left + width - 58, 2, left + width - 46, 14, fill="#d47752", outline="")
        graph.create_text(left + width - 40, 8, text="Temp", anchor="w", fill="#4e5c46", font=("Segoe UI", 8))

    def show_season_page(self, season_name):
        self.clear_page()
        self.root.title(f"{season_name} | Noongar Seasons")
        self.root.geometry("700x500")

        season = SEASONS[season_name]

        tk.Label(
            self.current_frame,
            text=season_name,
            font=("Segoe UI", 26, "bold"),
            bg="#f4efe7",
            fg="#24381d",
        ).pack(pady=(25, 8))
        tk.Label(
            self.current_frame,
            text=f"Months: {season['months']}",
            font=("Segoe UI", 12, "bold"),
            bg="#f4efe7",
            fg="#4e5c46",
        ).pack(pady=(0, 25))

        detail_panel = tk.Frame(self.current_frame, bg="#f7f3ee", bd=1, relief="solid")
        detail_panel.pack(fill="both", expand=True, padx=45, pady=(0, 25))
        tk.Label(
            detail_panel,
            text=season["description"],
            font=("Segoe UI", 12),
            bg="#f7f3ee",
            fg="#2b2b2b",
            wraplength=540,
            justify="left",
        ).pack(anchor="w", padx=25, pady=(30, 20))
        tk.Label(
            detail_panel,
            text=f"Meaning: {season['meaning']}",
            font=("Segoe UI", 11, "italic"),
            bg="#f7f3ee",
            fg="#414141",
            wraplength=540,
            justify="left",
        ).pack(anchor="w", padx=25)

        ttk.Button(
            self.current_frame,
            text="Back to seasons",
            command=self.show_information_page,
        ).pack(pady=(0, 20))


if __name__ == "__main__":
    root = tk.Tk()
    app = NoongarSeasonApp(root)
    root.mainloop()
