import csv
import math
import re
from pathlib import Path
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from PIL import Image, ImageDraw, ImageOps, ImageTk
from Moduals.UI_Modual import enable_mousewheel_scrolling, rounded_panel


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


def load_season_graph_data():
    data_path = Path(__file__).resolve().parent.parent / "Data" / "noongar_seasons_perth.csv"
    try:
        with data_path.open(newline="", encoding="utf-8-sig") as csv_file:
            rows = [row[0].strip().strip('"') for row in csv.reader(csv_file) if row]
    except OSError:
        return {}

    season_starts = {}
    for index, row in enumerate(rows):
        for season_name in SEASONS:
            if row.startswith(f"{season_name} ("):
                season_starts[season_name] = index
                break

    graph_data = {}
    for season_name in SEASONS:
        start = season_starts.get(season_name)
        if start is None:
            continue
        next_starts = [index for index in season_starts.values() if index > start]
        end = min(next_starts) if next_starts else len(rows)
        block = rows[start:end]
        block_text = " ".join(block)
        temperature_match = re.search(r"Season mean:\s*([\d.]+)\s*°C", block_text)
        rainfall_match = re.search(
            r"Season mean:\s*([\d.]+)\s*mm/day\s*\(total\s*([\d.]+)\s*mm\)",
            block_text,
        )
        period_match = re.search(
            r"Perth Metro,\s*([^\"]+)",
            next((row for row in block if "Daily maximum temperature and rainfall" in row), ""),
        )
        note = next(
            (row for row in block if "No temperature reading" in row),
            "",
        )
        if temperature_match and rainfall_match:
            graph_data[season_name] = {
                "temperature": float(temperature_match.group(1)),
                "rainfall_daily": float(rainfall_match.group(1)),
                "rainfall_total": float(rainfall_match.group(2)),
                "period": period_match.group(1).strip() if period_match else "",
                "note": note,
            }
    return graph_data


SEASON_GRAPH_DATA = load_season_graph_data()

SEASON_IMAGE_FILES = {
    "Birak": "birak.jpeg",
    "Bunuru": "bunuru.jpeg",
    "Djeran": "djeran.jpg",
    "Makuru": "makuru.jpg",
    "Djilba": "djilba.jpg",
    "Kambarang": "kambarang.jpg",
}

SEASON_IMAGE_CAPTIONS = {
    "Birak": "Kookaburra",
    "Bunuru": "White blossom and visiting insect",
    "Djeran": "Black cockatoo among flowering plants",
    "Makuru": "Blue wildflower",
    "Djilba": "Yellow wildflower",
    "Kambarang": "Orange spring blossoms",
}

SEASON_GRAPH_FILES = {
    "Birak": "season_climate_birak.png",
    "Bunuru": "season_climate_bunuru.png",
    "Djeran": "season_climate_djeran.png",
    "Makuru": "season_climate_makuru.png",
    "Djilba": "season_climate_djilba.png",
    "Kambarang": "season_climate_kambarang.png",
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
        self.image_sources = {}
        self.image_cache = {}

    def show_information_page(self):
        app = self.app
        app.clear_page()
        app.root.title("Wheel of Noongar Seasons")
        app.set_windowed_size("950x760", (760, 700))
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

        wheel_section = tk.Frame(current_frame, bg="#f4efe7")
        wheel_section.pack(fill="both", expand=True, padx=20, pady=(0, 5))

        canvas = tk.Canvas(
            wheel_section,
            width=420,
            height=420,
            bg="#f4efe7",
            highlightthickness=0,
        )
        canvas.pack(side="left", padx=(0, 16))

        screen_width = self.app.root.winfo_screenwidth()
        window_width = min(950, max(400, screen_width - 48))
        preview_width = max(160, window_width - 476)
        preview_wraplength = max(150, min(300, preview_width - 36))
        details_column = tk.Frame(wheel_section, bg="#f4efe7")
        details_column.pack(side="left", fill="both", expand=True)

        preview_panel = tk.Frame(
            details_column,
            bg="#f7f3ee",
            height=148,
            padx=14,
            pady=12,
        )
        preview_panel.pack_propagate(False)
        rounded_panel(preview_panel, "#f7f3ee", "#d8c8b4", radius=6)
        preview_panel.pack(fill="x", pady=(0, 10))
        preview_font = tkfont.Font(root=app.root, family="Segoe UI", size=10)
        preview_title = tk.Label(
            preview_panel,
            text="Season insight",
            font=("Segoe UI", 14, "bold"),
            fg="#24381d",
            bg="#f7f3ee",
        )
        preview_title.pack(anchor="w", pady=(0, 5))
        preview_description = tk.Label(
            preview_panel,
            text="Move over or select a season to explore its local signs.",
            font=preview_font,
            fg="#4e5c46",
            bg="#f7f3ee",
            wraplength=preview_wraplength,
            height=5,
            anchor="nw",
            justify="left",
        )
        preview_description.pack(anchor="w", fill="x")

        overview_panel = tk.Frame(
            details_column,
            bg="#f7f3ee",
            padx=14,
            pady=12,
        )
        rounded_panel(overview_panel, "#f7f3ee", "#d8c8b4", radius=6)
        overview_panel.pack(fill="x", pady=(0, 10))
        tk.Label(
            overview_panel,
            text="ABOUT THE SIX SEASONS",
            font=("Segoe UI", 9, "bold"),
            fg="#345c4c",
            bg="#f7f3ee",
        ).pack(anchor="w", pady=(0, 4))
        tk.Label(
            overview_panel,
            text=(
                "The Noongar seasonal calendar describes six connected periods "
                "through the year, recognised through changes in weather, plants, "
                "animals and the condition of Country. Around Perth, Birak, Bunuru, "
                "Djeran, Makuru, Djilba and Kambarang offer a local guide; signs and "
                "timing vary between places and years rather than following fixed dates."
            ),
            font=("Segoe UI", 9),
            fg="#4a4a4a",
            bg="#f7f3ee",
            wraplength=preview_wraplength,
            justify="left",
        ).pack(anchor="w", fill="x")

        feature_path = Path(__file__).resolve().parent.parent / "Data" / "DjeranBlogFeatureNRM.jpg"
        feature_source = self._open_image(feature_path)
        if feature_source:
            feature_width = max(160, min(320, preview_width - 36))
            feature_image = ImageOps.contain(
                feature_source,
                (feature_width, round(feature_width * 9 / 16)),
                method=Image.Resampling.LANCZOS,
            )
            self.overview_photo = ImageTk.PhotoImage(
                feature_image,
                master=current_frame,
            )
            feature_panel = tk.Frame(details_column, bg="#f4efe7")
            feature_panel.pack(fill="x")
            tk.Label(
                feature_panel,
                image=self.overview_photo,
                bg="#f4efe7",
                bd=0,
            ).pack()

        center_x, center_y = 210, 210
        outer_radius = 176
        inner_radius = 74
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
                description = "Move over or select a season to explore its local signs."
            else:
                preview_title.configure(text=season_name)
                description = SEASONS[season_name]["description"]

            description_lines = self._wrap_text(
                description,
                preview_font,
                preview_wraplength,
            ).splitlines()
            if len(description_lines) > 5:
                description_lines = [*description_lines[:4], "..."]
            preview_description.configure(
                text="\n".join(description_lines)
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
        app.root.geometry("700x500")
        current_frame = app.current_frame

        season = SEASONS[season_name]

        header = tk.Frame(app.current_frame, bg="#17392f", padx=18, pady=10)
        header.pack(fill="x")
        ttk.Button(
            header,
            text="Back to seasons",
            command=self.show_information_page,
        ).pack(side="left")
        tk.Label(
            header,
            text="SEASON DETAIL",
            font=("TkDefaultFont", 10, "bold"),
            fg="#ffffff",
            bg="#17392f",
        ).pack(side="right", padx=8)

        scroll_area = tk.Frame(app.current_frame, bg="#f4efe7")
        scroll_area.pack(fill="both", expand=True)
        page_canvas = tk.Canvas(
            scroll_area,
            bg="#f4efe7",
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            scroll_area,
            orient="vertical",
            command=page_canvas.yview,
        )
        page_canvas.configure(yscrollcommand=scrollbar.set)
        page_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        page_canvas.bind(
            "<Configure>",
            lambda event: self.render_season_page(event, page_canvas, season_name, season),
        )
        page_canvas.after_idle(
            lambda: self.render_season_page(
                None,
                page_canvas,
                season_name,
                season,
            )
        )
        enable_mousewheel_scrolling(app.current_frame, page_canvas)

    def _open_image(self, image_path):
        path = Path(image_path)
        key = str(path)
        if key not in self.image_sources:
            try:
                self.image_sources[key] = Image.open(path).convert("RGB")
            except OSError:
                return None
        return self.image_sources[key]

    def _wrap_text(self, text, font, width):
        lines = []
        line = ""
        for word in text.split():
            candidate = f"{line} {word}".strip()
            if line and font.measure(candidate) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        if line:
            lines.append(line)
        return "\n".join(lines)

    def render_season_page(self, event, canvas, season_name, season):
        width = max(1, getattr(event, "width", canvas.winfo_width()))
        if width <= 1:
            return

        body_font = tkfont.Font(root=self.app.root, family="TkDefaultFont", size=12)
        small_font = tkfont.Font(root=self.app.root, family="TkDefaultFont", size=10)
        title_font = tkfont.Font(root=self.app.root, family="Georgia", size=30, weight="bold")
        margin = min(38, max(20, int(width * 0.055)))
        text_width = max(220, width - margin * 2)
        y = 34
        text_items = []
        section_panels = []

        def add_text(text, font, colour, gap):
            nonlocal y
            wrapped = self._wrap_text(text, font, text_width)
            text_items.append((y, wrapped, font, colour, text_width))
            line_count = max(1, len(wrapped.splitlines()))
            next_y = current_y + line_count * font.metrics("linespace") + gap
            if align == "left":
                left_y = next_y
            else:
                right_y = next_y

        add_text(season["months"].upper(), small_font, "#f5d985", 4)
        add_text(season_name, title_font, "#ffffff", 14)
        add_text(season["description"], body_font, "#ffffff", 10)
        add_text(season["meaning"], small_font, "#f3f2ec", 24)
        add_text("PERTH DAILY CLIMATE  ·  TEMPERATURE AND RAINFALL", small_font, "#ffffff", 5)

        graph_data = SEASON_GRAPH_DATA.get(season_name, {})
        graph_summary = (
            f"{graph_data.get('period', '')}  ·  Mean maximum "
            f"{graph_data.get('temperature', 0):.1f} °C  ·  Mean rainfall "
            f"{graph_data.get('rainfall_daily', 0):.2f} mm/day  ·  Total "
            f"{graph_data.get('rainfall_total', 0):.1f} mm"
        )
        add_text(graph_summary, small_font, "#f3f2ec", 10)

        graph_path = Path(__file__).resolve().parent.parent / "Data" / "Regions" / SEASON_GRAPH_FILES[season_name]
        graph_source = self._open_image(graph_path)
        graph_width = min(text_width, graph_source.width) if graph_source else text_width
        graph_height = (
            round(graph_source.height * graph_width / graph_source.width)
            if graph_source
            else 0
        )
        graph_y = y
        y += graph_height + 24

        if graph_data.get("note"):
            note = self._wrap_text(graph_data["note"], small_font, text_width)
            text_items.append((y, note, small_font, "#ffffff", text_width))
            y += max(1, len(note.splitlines())) * small_font.metrics("linespace") + 24

        content_height = max(y + 30, canvas.winfo_height())
        photo_path = Path(__file__).resolve().parent.parent / "Data" / "Regions" / SEASON_IMAGE_FILES[season_name]
        photo_source = self._open_image(photo_path)
        if photo_source:
            backdrop = ImageOps.fit(
                photo_source,
                (width, content_height),
                method=Image.Resampling.LANCZOS,
            ).convert("RGBA")
        else:
            backdrop = Image.new("RGBA", (width, content_height), "#20352d")

        text_band_height = max(1, graph_y - 12)
        band = Image.new(
            "RGBA",
            (width, text_band_height),
            (17, 40, 31, 172),
        )
        backdrop.alpha_composite(band, (0, 0))

        if graph_source:
            chart = graph_source.resize(
                (graph_width, graph_height),
                Image.Resampling.LANCZOS,
            ).convert("RGBA")
            panel_width = graph_width + panel_padding * 2
            panel_height = graph_height + panel_padding * 2
            panel = Image.new(
                "RGBA",
                (panel_width, panel_height),
                (250, 250, 247, 255),
            )
            ImageDraw.Draw(panel).rounded_rectangle(
                (0, 0, panel_width - 1, panel_height - 1),
                radius=7,
                fill=(250, 250, 247, 255),
                outline=(255, 255, 255, 255),
                width=1,
            )
            panel.alpha_composite(chart, (panel_padding, panel_padding))
            backdrop.alpha_composite(
                panel,
                ((width - panel_width) // 2, graph_y - panel_padding),
            )

        self.page_photo = ImageTk.PhotoImage(backdrop.convert("RGB"), master=canvas)
        canvas.delete("all")
        canvas.create_image(0, 0, image=self.page_photo, anchor="nw")
        for text_y, text, font, colour, wrap_width in text_items:
            canvas.create_text(
                margin,
                text_y,
                text=text,
                fill=colour,
                font=font,
                width=wrap_width,
                anchor="n" if justify == "center" else "nw",
                justify=justify,
            )
        canvas.configure(scrollregion=(0, 0, width, content_height))
