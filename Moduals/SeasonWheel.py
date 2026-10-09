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
        "description": "Birak is a hot, dry part of the year around Perth, with long daylight hours and strong sunshine. Rainfall is usually low and inland areas can become very warm, while afternoon sea breezes may bring some relief near the coast.",
        "meaning": "In this local guide, Birak marks the transition into summer conditions. Heat, available water, and changes in plants and animal activity are useful things to notice, while recognising that conditions vary from year to year and place to place.",
        "flora": (
            ("Honky nuts", "In Birak, honky nuts drop, providing a seasonal food source for cockatoos."),
        ),
        "fauna": (
            ("Cockatoos", "In Birak, cockatoos feed on the fallen honky nuts."),
            ("Fledgling birds", "Birak is described as a time when young birds take flight."),
            ("Reptiles and young frogs", "In Birak's warming conditions, reptiles shed their skins and young frogs develop toward adulthood."),
        ),
    },
    "Bunuru": {
        "months": "February to March",
        "description": "Bunuru is commonly the hottest and driest stretch of the year around Perth. Long, sunny days and little rain can leave soils and vegetation dry; coastal breezes and shade can make a noticeable difference.",
        "meaning": "This is a useful time to observe how plants and animals respond to heat and limited water. The timing and severity of hot, dry conditions differ between years, so these are seasonal tendencies rather than fixed rules.",
        "flora": (
            ("Jarrah, marri, and ghost gums", "In Bunuru, these trees are described as flowering with white blossoms."),
            ("Female zamia cones", "During Bunuru, female zamia cones ripen from green to bright red."),
        ),
        "fauna": (
            ("Emus (weitj)", "In Bunuru, emus are attracted to the bright red, ripening zamia cones."),
            ("Coastal and estuary foods", "Bunuru's warm, dry conditions are associated with Noongar people staying near coasts, rivers, and estuaries and gathering seafood."),
        ),
    },
    "Djeran": {
        "months": "April to May",
        "description": "Djeran brings a gradual move away from summer heat. Cooler mornings and evenings become more noticeable, winds change, and the first seasonal rains may begin to affect the ground and local waterways.",
        "meaning": "Djeran is a time of transition in this local seasonal guide. Watching for cooler weather, changing water levels, and the response of plants and animals can reveal how the environment is shifting toward the wetter months.",
        "flora": (
            ("Red flowering gum and Summer Flame", "During Djeran, their red flowers are seasonal signs of the cooler change."),
            ("Sheoaks", "Around Perth in Djeran, sheoaks develop reddish foliage and seed cones."),
            ("Banksias", "Banksias bloom in Djeran, providing nectar for small mammals and birds."),
        ),
        "fauna": (
            ("Small mammals and birds", "In Djeran, they can feed on nectar from blooming banksias."),
            ("Salmon", "Djeran is associated with the beginning of the salmon run."),
        ),
    },
    "Makuru": {
        "months": "June to July",
        "description": "Makuru is generally the coldest and wettest part of the year around Perth. Cold fronts and rainfall become more frequent, replenishing soils, wetlands, and waterways, although rainfall totals vary from year to year.",
        "meaning": "The wetter conditions shape what can be observed across the landscape. Changes in water, shelter, and food availability influence plants and wildlife, but no single sign appears everywhere or in every year.",
        "flora": (
            ("Blueberry lilies", "In Makuru, their blue flowers are among the seasonal blooms described for the wet winter landscape."),
            ("Purple flags", "Makuru's wet season is associated with their purple flowers, signalling the approach of Djilba."),
        ),
        "fauna": (
            ("Black swans", "During Makuru, black swans prepare to nest."),
            ("Breeding animals", "Makuru is described as a time when animals pair up to breed."),
            ("Kangaroos", "In Makuru, movement inland and hunting kangaroos are described as seasonal practices as food sources shift from sea to land."),
        ),
    },
    "Djilba": {
        "months": "August to September",
        "description": "Djilba is a changeable transition from winter toward spring. Cool, wet days may alternate with warmer weather, and early signs of new growth and flowering begin to appear in parts of the south-west.",
        "meaning": "The seasonal shift is gradual rather than a fixed date on the calendar. New flowers, warmer spells, and changes in animal activity can be noticed, with their timing depending on local conditions.",
        "flora": (
            ("Golden Acacia", "Djilba's first wildflower blooms are described as beginning with Golden Acacia."),
            ("Balgas", "During Djilba, balgas prepare for Kambarang as their flower stalks begin to unfurl."),
        ),
        "fauna": (
            ("Kangaroos, emus, and possums (koomal)", "Djilba's land-based seasonal foods are described as sustaining people as the weather warms."),
            ("Newborn animals", "During Djilba, young animals are described as learning from their parents as warmth returns."),
            ("Woodland birds", "In Djilba, woodland birds guard their nests."),
        ),
    },
    "Kambarang": {
        "months": "October to November",
        "description": "Kambarang brings warmer spring weather and especially noticeable flowering in many parts of the south-west. As the season progresses, the landscape moves toward the hotter, drier months.",
        "meaning": "Flowering plants and the wildlife that feed around them can be striking seasonal observations. The display differs by habitat, species, and year; stay on paths and leave flowers and wildlife undisturbed.",
        "flora": (
            ("Acacias, banksias, and kangaroo paws", "Kambarang is associated with these plants flowering and adding colour to the landscape."),
            ("Balgas", "In Kambarang, balgas are described as blooming after fires."),
            ("Moodjar tree", "Its orange-yellow flowers are described as a seasonal sign of the approaching heat in Kambarang."),
        ),
        "fauna": (
            ("Snakes", "As Kambarang warms in October, snakes become active."),
            ("Young birds and magpies", "During Kambarang, young birds call for food while magpies guard them."),
            ("Reptiles", "Warmer, sunnier Kambarang conditions are associated with reptiles stirring from dormancy."),
        ),
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
        app.set_windowed_size("1050x760", (850, 620))
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
        title_font = tkfont.Font(
            root=self.app.root, family="Georgia", size=30, weight="bold"
        )
        section_font = tkfont.Font(
            root=self.app.root, family="TkDefaultFont", size=11, weight="bold"
        )
        margin = min(34, max(20, int(width * 0.045)))
        column_gap = 28
        available_width = max(1, width - margin * 2 - column_gap)
        original_left_width = int(available_width * 0.43)
        original_graph_width = max(1, original_left_width - 24)
        enlarged_graph_width = round(original_graph_width * 1.3)
        left_width = max(original_left_width, enlarged_graph_width + 24)
        right_width = available_width - left_width
        left_x = margin
        right_x = left_x + left_width + column_gap
        left_y = 30
        right_y = 30
        text_items = []

        def add_text(text, font, colour, gap, x, text_width, align="left"):
            nonlocal left_y, right_y
            current_y = left_y if align == "left" else right_y
            wrapped = self._wrap_text(text, font, text_width)
            text_items.append((x, current_y, wrapped, font, colour, text_width))
            line_count = max(1, len(wrapped.splitlines()))
            next_y = current_y + line_count * font.metrics("linespace") + gap
            if align == "left":
                left_y = next_y
            else:
                right_y = next_y

        add_text(
            season["months"].upper(), small_font, "#f5d985", 4, left_x, left_width
        )
        add_text(season_name, title_font, "#ffffff", 12, left_x, left_width)
        add_text(
            "ABOUT THIS SEASON",
            section_font,
            "#f5d985",
            5,
            right_x,
            right_width,
            "right",
        )
        add_text(
            season["description"],
            body_font,
            "#ffffff",
            10,
            right_x,
            right_width,
            "right",
        )
        add_text(
            season["meaning"],
            body_font,
            "#f3f2ec",
            18,
            right_x,
            right_width,
            "right",
        )
        add_text(
            "FLORA EXAMPLES",
            section_font,
            "#f5d985",
            5,
            right_x,
            right_width,
            "right",
        )
        flora_text = "\n".join(
            f"- {name}: {detail}"
            for name, detail in season["flora"]
        )
        add_text(flora_text, body_font, "#ffffff", 16, right_x, right_width, "right")
        add_text(
            "FAUNA EXAMPLES",
            section_font,
            "#f5d985",
            5,
            right_x,
            right_width,
            "right",
        )
        fauna_text = "\n".join(
            f"- {name}: {detail}"
            for name, detail in season["fauna"]
        )
        add_text(fauna_text, body_font, "#ffffff", 5, right_x, right_width, "right")
        add_text(
            "Examples are general observations, not fixed seasonal indicators; "
            "species and timing vary by habitat and year.",
            small_font,
            "#f3f2ec",
            0,
            right_x,
            right_width,
            "right",
        )

        graph_data = SEASON_GRAPH_DATA.get(season_name, {})
        graph_summary = (
            f"{graph_data.get('period', '')}  ·  Mean maximum "
            f"{graph_data.get('temperature', 0):.1f} °C  ·  Mean rainfall "
            f"{graph_data.get('rainfall_daily', 0):.2f} mm/day  ·  Total "
            f"{graph_data.get('rainfall_total', 0):.1f} mm"
        )
        graph_path = (
            Path(__file__).resolve().parent.parent
            / "Data"
            / "Noongar season graphs"
            / SEASON_GRAPH_FILES[season_name]
        )
        graph_source = self._open_image(graph_path)
        graph_width = (
            min(enlarged_graph_width, graph_source.width)
            if graph_source
            else enlarged_graph_width
        )
        graph_height = (
            round(graph_source.height * graph_width / graph_source.width)
            if graph_source
            else 0
        )
        chart_text_width = left_width - 24
        chart_note = graph_data.get("note", "")
        chart_note_height = (
            max(1, len(self._wrap_text(chart_note, small_font, chart_text_width).splitlines()))
            * small_font.metrics("linespace")
            if chart_note
            else 0
        )
        summary_height = max(
            1,
            len(self._wrap_text(graph_summary, small_font, chart_text_width).splitlines()),
        ) * small_font.metrics("linespace")
        chart_heading_height = small_font.metrics("linespace")
        chart_text_height = (
            chart_heading_height
            + 5
            + summary_height
            + (5 + chart_note_height if chart_note else 0)
        )
        graph_panel_padding = 12
        graph_panel_height = graph_height + graph_panel_padding * 2
        chart_block_height = (
            chart_text_height + graph_panel_height + margin + 10
        )
        content_height = max(
            right_y + margin,
            left_y + chart_block_height,
            canvas.winfo_height(),
        )
        graph_panel_y = content_height - margin - graph_panel_height
        climate_y = graph_panel_y - chart_text_height - 10
        climate_heading = "PERTH DAILY CLIMATE - TEMPERATURE AND RAINFALL"
        text_items.append(
            (
                left_x,
                climate_y,
                climate_heading,
                small_font,
                "#ffffff",
                chart_text_width,
            )
        )
        climate_y += chart_heading_height + 5
        summary = self._wrap_text(graph_summary, small_font, chart_text_width)
        text_items.append(
            (left_x, climate_y, summary, small_font, "#f3f2ec", chart_text_width)
        )
        climate_y += summary_height + 5
        if chart_note:
            note = self._wrap_text(chart_note, small_font, chart_text_width)
            text_items.append(
                (left_x, climate_y, note, small_font, "#ffffff", chart_text_width)
            )

        photo_path = (
            Path(__file__).resolve().parent.parent
            / "Data"
            / "Flora Fauna"
            / SEASON_IMAGE_FILES[season_name]
        )
        photo_source = self._open_image(photo_path)
        if photo_source:
            backdrop = ImageOps.fit(
                photo_source,
                (width, content_height),
                method=Image.Resampling.LANCZOS,
            ).convert("RGBA")
        else:
            backdrop = Image.new("RGBA", (width, content_height), "#20352d")

        left_panel = Image.new(
            "RGBA",
            (left_width + 12, content_height),
            (17, 40, 31, 188),
        )
        right_panel = Image.new(
            "RGBA",
            (right_width + 12, content_height),
            (17, 40, 31, 188),
        )
        backdrop.alpha_composite(left_panel, (left_x - 6, 0))
        backdrop.alpha_composite(right_panel, (right_x - 6, 0))

        if graph_source:
            panel_padding = 12
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
                (
                    left_x + (left_width - panel_width) // 2,
                    graph_panel_y,
                ),
            )

        self.page_photo = ImageTk.PhotoImage(backdrop.convert("RGB"), master=canvas)
        canvas.delete("all")
        canvas.create_image(0, 0, image=self.page_photo, anchor="nw")
        for text_x, text_y, text, font, colour, wrap_width in text_items:
            canvas.create_text(
                text_x,
                text_y,
                text=text,
                fill=colour,
                font=font,
                width=wrap_width,
                anchor="nw",
                justify="left",
            )
        canvas.configure(scrollregion=(0, 0, width, content_height))
