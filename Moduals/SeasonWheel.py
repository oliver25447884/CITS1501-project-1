import csv
import math
import re
from pathlib import Path
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from PIL import Image, ImageDraw, ImageOps, ImageTk


SEASONS = {
    "Birak": {
        "months": "December to January",
        "description": "Birak is a hot, dry part of the year around Perth, with long daylight hours and strong sunshine. Rainfall is usually low and inland areas can become very warm, while afternoon sea breezes may bring some relief near the coast.",
        "meaning": "In this local guide, Birak marks the transition into summer conditions. Heat, available water, and changes in plants and animal activity are useful things to notice, while recognising that conditions vary from year to year and place to place.",
        "flora": (
            ("Grass trees (Xanthorrhoea spp.)", "Their tall flower spikes can provide food for insects and other animals in warmer months; flowering varies by species and year."),
            ("Banksias (Banksia spp.)", "Some species may flower across different parts of the year, providing nectar when in bloom."),
        ),
        "fauna": (
            ("Bobtail skink", "May bask in mild conditions and shelter when the ground is very hot."),
            ("Western grey kangaroo", "Often forages in open areas during cooler parts of the day."),
            ("Osprey", "May be seen around suitable coastal and estuary habitats."),
        ),
    },
    "Bunuru": {
        "months": "February to March",
        "description": "Bunuru is commonly the hottest and driest stretch of the year around Perth. Long, sunny days and little rain can leave soils and vegetation dry; coastal breezes and shade can make a noticeable difference.",
        "meaning": "This is a useful time to observe how plants and animals respond to heat and limited water. The timing and severity of hot, dry conditions differ between years, so these are seasonal tendencies rather than fixed rules.",
        "flora": (
            ("Banksias (Banksia spp.)", "Flowering and seed cycles differ between species; flowers, when present, can provide nectar."),
            ("Native grasses and shrubs", "Many reduce visible growth or conserve water during hot, dry weather."),
        ),
        "fauna": (
            ("Western grey kangaroo", "May rest in shade and feed more during cooler hours."),
            ("Bobtail skink", "Uses shelter to avoid the hottest conditions."),
            ("Black swan", "Can be observed on suitable wetlands and estuaries throughout the year."),
        ),
    },
    "Djeran": {
        "months": "April to May",
        "description": "Djeran brings a gradual move away from summer heat. Cooler mornings and evenings become more noticeable, winds change, and the first seasonal rains may begin to affect the ground and local waterways.",
        "meaning": "Djeran is a time of transition in this local seasonal guide. Watching for cooler weather, changing water levels, and the response of plants and animals can reveal how the environment is shifting toward the wetter months.",
        "flora": (
            ("Jarrah (Eucalyptus marginata)", "A characteristic local woodland tree; flowering time varies with location and year."),
            ("Banksias (Banksia spp.)", "Different species flower at different times, and their response to seasonal conditions is not uniform."),
        ),
        "fauna": (
            ("Black swan", "A familiar waterbird on suitable wetlands, estuaries, and lakes."),
            ("Quenda", "Forages among leaf litter and dense vegetation, usually at night."),
            ("Carnaby's black-cockatoo", "Uses suitable woodland and feeding habitat across the south-west."),
        ),
    },
    "Makuru": {
        "months": "June to July",
        "description": "Makuru is generally the coldest and wettest part of the year around Perth. Cold fronts and rainfall become more frequent, replenishing soils, wetlands, and waterways, although rainfall totals vary from year to year.",
        "meaning": "The wetter conditions shape what can be observed across the landscape. Changes in water, shelter, and food availability influence plants and wildlife, but no single sign appears everywhere or in every year.",
        "flora": (
            ("Wetland sedges and rushes", "Grow in suitable damp habitats, where winter rain can replenish water and soil moisture."),
            ("Paperbarks (Melaleuca spp.)", "Can be found around suitable wetland and damp habitats; local species and flowering times vary."),
        ),
        "fauna": (
            ("Motorbike frog", "A south-west wetland frog; calling and breeding activity can increase after rain."),
            ("Black swan", "May be seen on wetlands and estuaries; observe from a respectful distance."),
            ("Western grey kangaroo", "Uses open woodland and grassy habitats across the region."),
        ),
    },
    "Djilba": {
        "months": "August to September",
        "description": "Djilba is a changeable transition from winter toward spring. Cool, wet days may alternate with warmer weather, and early signs of new growth and flowering begin to appear in parts of the south-west.",
        "meaning": "The seasonal shift is gradual rather than a fixed date on the calendar. New flowers, warmer spells, and changes in animal activity can be noticed, with their timing depending on local conditions.",
        "flora": (
            ("Kangaroo paws (Anigozanthos spp.)", "Some species begin flowering around the transition into spring; timing varies by species and location."),
            ("Banksias (Banksia spp.)", "Some species flower during the cooler-to-warmer transition, providing food when in bloom."),
            ("Early wildflowers", "The first flowers may appear in suitable local habitats; avoid picking or trampling them."),
        ),
        "fauna": (
            ("Quenda", "Forages among leaf litter and dense vegetation, usually at night."),
            ("Motorbike frog", "May be heard near suitable wetland habitat after rain."),
            ("Carnaby's black-cockatoo", "Moves between feeding and roosting sites across suitable habitat."),
        ),
    },
    "Kambarang": {
        "months": "October to November",
        "description": "Kambarang brings warmer spring weather and especially noticeable flowering in many parts of the south-west. As the season progresses, the landscape moves toward the hotter, drier months.",
        "meaning": "Flowering plants and the wildlife that feed around them can be striking seasonal observations. The display differs by habitat, species, and year; stay on paths and leave flowers and wildlife undisturbed.",
        "flora": (
            ("Banksias (Banksia spp.)", "Many species flower at different times and provide nectar for wildlife."),
            ("Kangaroo paws (Anigozanthos spp.)", "Their bright flowers are a familiar spring feature in parts of the south-west."),
            ("Everlastings", "Seasonal displays can occur in suitable locations as warmer conditions arrive."),
        ),
        "fauna": (
            ("Carnaby's black-cockatoo", "Feeds on seeds and native plants in suitable habitat."),
            ("Western honey possum", "A nectar-feeder of south-west heathland; found only where suitable habitat is present."),
            ("Splendid fairy-wren", "A small bushland bird that is best watched quietly from a distance."),
            ("Native bees and honeyeaters", "May feed around flowering plants when nectar and pollen are available."),
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

SEASON_GRAPH_FILES = {
    "Birak": "noongar_seasons_perth (dragged).jpg",
    "Bunuru": "noongar_seasons_perth (dragged) 2.jpg",
    "Djeran": "noongar_seasons_perth (dragged) 3.jpg",
    "Makuru": "noongar_seasons_perth (dragged) 4.jpg",
    "Djilba": "noongar_seasons_perth (dragged) 5.jpg",
    "Kambarang": "noongar_seasons_perth (dragged) 6.jpg",
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

        scroll_area = tk.Frame(app.current_frame, bg="#172a24")
        scroll_area.pack(fill="both", expand=True)
        page_canvas = tk.Canvas(
            scroll_area,
            bg="#172a24",
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
        page_canvas.bind("<MouseWheel>", lambda event: self._scroll_page(page_canvas, event))
        page_canvas.bind("<Button-4>", lambda event: self._scroll_page(page_canvas, event))
        page_canvas.bind("<Button-5>", lambda event: self._scroll_page(page_canvas, event))
        page_canvas.after_idle(
            lambda: self.render_season_page(
                None,
                page_canvas,
                season_name,
                season,
            )
        )

    def _scroll_page(self, canvas, event):
        if getattr(event, "num", None) == 4:
            direction = -1
        elif getattr(event, "num", None) == 5:
            direction = 1
        else:
            direction = -1 if event.delta > 0 else 1
        canvas.yview_scroll(direction, "units")
        return "break"

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
        left_width = int(available_width * 0.43)
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
        flora_text = "\n".join(f"- {name}: {detail}" for name, detail in season["flora"])
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
        fauna_text = "\n".join(f"- {name}: {detail}" for name, detail in season["fauna"])
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
            / "Regions"
            / SEASON_GRAPH_FILES[season_name]
        )
        graph_source = self._open_image(graph_path)
        graph_width = (
            min(max(1, left_width - 24), graph_source.width)
            if graph_source
            else max(1, left_width - 24)
        )
        graph_height = (
            round(graph_source.height * graph_width / graph_source.width)
            if graph_source
            else 280
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
            / "Regions"
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
            chart = graph_source.resize(
                (graph_width, graph_height),
                Image.Resampling.LANCZOS,
            ).convert("RGBA")
            panel_padding = 12
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
