import math
import tkinter as tk
from tkinter import ttk


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

SEASON_BY_MONTH = {
    12: "Birak",
    1: "Birak",
    2: "Bunuru",
    3: "Bunuru",
    4: "Djeran",
    5: "Djeran",
    6: "Makuru",
    7: "Makuru",
    8: "Djilba",
    9: "Djilba",
    10: "Kambarang",
    11: "Kambarang",
}


def season_for_month(month):
    return SEASON_BY_MONTH[month]


class SeasonWheel:
    def __init__(self, app):
        self.app = app

    def show_information_page(self):
        app = self.app
        app.clear_page()
        app.root.title("Wheel of Noongar Seasons")
        app.set_windowed_size("950x900", (760, 780))
        current_frame = app.current_frame

        title = tk.Label(
            current_frame,
            text="Noongar Seasons",
            font=("Segoe UI", 24, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
            pady=15,
        )
        title.pack()

        intro = tk.Label(
            current_frame,
            text="The six seasons recognised by Noongar people in the South West of Western Australia.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#f4efe7",
            wraplength=780,
            justify="center",
        )
        intro.pack(pady=(0, 12))

        wheel_section = tk.Frame(current_frame, bg="#f4efe7")
        wheel_section.pack(fill="x", padx=20, pady=(0, 5))

        canvas = tk.Canvas(
            wheel_section,
            width=500,
            height=470,
            bg="#f4efe7",
            highlightthickness=0,
        )
        canvas.pack(side="left", padx=(0, 16))

        preview_panel = tk.Frame(
            wheel_section,
            bg="#f7f3ee",
            padx=22,
            pady=22,
            highlightbackground="#d8c8b4",
            highlightthickness=1,
        )
        preview_panel.pack(side="left", fill="both", expand=True, pady=55)
        preview_title = tk.Label(
            preview_panel,
            text="Season insight",
            font=("Segoe UI", 17, "bold"),
            fg="#24381d",
            bg="#f7f3ee",
        )
        preview_title.pack(anchor="w", pady=(0, 12))
        preview_description = tk.Label(
            preview_panel,
            text="interact with the wheel to unlock knowledge",
            font=("Segoe UI", 11),
            fg="#4e5c46",
            bg="#f7f3ee",
            wraplength=300,
            justify="left",
        )
        preview_description.pack(anchor="w", fill="x")

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
            canvas.tag_bind(
                arc_tag,
                "<Button-1>",
                lambda event, name=season_name: self.show_season_page(name),
            )

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

        hovered_season = {"name": None}

        def update_season_preview(event):
            distance = math.hypot(event.x - center_x, event.y - center_y)
            if inner_radius <= distance <= outer_radius:
                angle = math.degrees(
                    math.atan2(center_y - event.y, event.x - center_x)
                ) % 360
                season_index = int(((90 - angle) % 360) // 60)
                season_name = season_names[season_index]
            else:
                season_name = None

            if season_name == hovered_season["name"]:
                return
            hovered_season["name"] = season_name

            if season_name is None:
                preview_title.configure(text="Season insight")
                preview_description.configure(
                    text="interact with the wheel to unlock knowledge"
                )
            else:
                preview_title.configure(text=season_name)
                preview_description.configure(
                    text=SEASONS[season_name]["description"]
                )

        canvas.bind("<Motion>", update_season_preview)
        canvas.bind("<Leave>", update_season_preview)

        ttk.Button(
            current_frame,
            text="Back to explore",
            command=app.show_home_page,
        ).pack(pady=(0, 8))

        close_button = ttk.Button(
            current_frame, text="Close", command=app.root.destroy
        )
        close_button.pack(pady=(0, 15))

    def show_season_page(self, season_name):
        app = self.app
        app.clear_page()
        app.root.title(f"{season_name} | Noongar Seasons")
        app.set_windowed_size("700x500", (550, 400))
        current_frame = app.current_frame

        season = SEASONS[season_name]

        tk.Label(
            current_frame,
            text=season_name,
            font=("Segoe UI", 26, "bold"),
            bg="#f4efe7",
            fg="#24381d",
        ).pack(pady=(25, 8))
        tk.Label(
            current_frame,
            text=f"Months: {season['months']}",
            font=("Segoe UI", 12, "bold"),
            bg="#f4efe7",
            fg="#4e5c46",
        ).pack(pady=(0, 25))

        detail_panel = tk.Frame(current_frame, bg="#f7f3ee", bd=1, relief="solid")
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
            current_frame,
            text="Back to seasons",
            command=self.show_information_page,
        ).pack(pady=(0, 20))
