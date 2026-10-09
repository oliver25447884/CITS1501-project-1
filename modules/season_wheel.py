"""Seasonal content, wheel navigation, and detail-page visuals for the app."""

import math
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import ttk
from PIL import Image, ImageTk


# Display content is grouped by season; keys also select matching image assets.
# Seasonal text and styling used by the wheel and its detail pages.
SEASONS = {
    "Birak": {
        "months": "December to January",
        "description": "First summer, when warmer and drier weather becomes established across the south-west.",
        "meaning": "A public West Coast account describes Birak as the season of the young, with young animals beginning to leave nests. It also describes cultural burning as one way Noongar people cared for Country. Burning is guided by local knowledge and conditions; this summary is not a how-to guide.",
        "image_context": "The image shows a laughing kookaburra hunting from a branch. Kookaburras eat insects and small animals; this species was introduced to Western Australia. It is included as a present-day wildlife example, not as a Noongar seasonal symbol.",
        "weather": "Around Perth, hot easterly winds are common in the morning. Coastal areas often cool later with a south-westerly sea breeze, sometimes called the Fremantle Doctor. These are typical patterns, not a daily forecast.",
        "background": "#F4EEE8", "accent": "#9A5948",
    },
    "Bunuru": {
        "months": "February to March",
        "description": "Second summer, often the hottest and driest part of the year around Perth.",
        "meaning": "A public West Coast account describes families spending time near coastal estuaries and waterways during Bunuru. Fish and other seafood were important foods. These practices and teachings are connected to particular places and communities.",
        "image_context": "The photo shows white blossom and a visiting insect. Flower visitors may gather nectar or pollen and can transfer pollen between flowers. The plant and insect have not been identified, so the image is a general ecological example rather than a claimed seasonal marker.",
        "weather": "February and March are usually Perth's hottest, driest months. Hot easterlies and a cooler afternoon sea breeze are common near the coast, although wind and temperature change from day to day.",
        "background": "#F5EEE3", "accent": "#A66B3F",
    },
    "Djeran": {
        "months": "April to May",
        "description": "An autumn transition as warm days ease and nights begin to cool.",
        "meaning": "A public West Coast account connects Djeran with cooler nights, dewy mornings, red flowers and fresh green shoots. It describes seasonal changes in where families travelled for food and shelter. Local signs and practices differ between places.",
        "image_context": "The photo shows a black cockatoo among flowering plants. Black cockatoos feed on native seeds, flowers or insect larvae, with diets differing by species. The bird is not identified to species here, and the image is not presented as a cultural symbol.",
        "weather": "Around Perth, nights cool and rain becomes more likely as Djeran progresses. South-westerly winds can become more noticeable. Daily conditions vary, and the graph shows temperature and rainfall rather than wind.",
        "background": "#EDF1E9", "accent": "#61785B",
    },
    "Makuru": {
        "months": "June to July",
        "description": "The cold, wet season, when rain and cold fronts become more frequent.",
        "meaning": "A public West Coast account describes waterways filling and animals beginning to pair during Makuru. It also records movement between coastal and inland places. This is one regional account; seasonal knowledge varies across Noongar Country.",
        "image_context": "The photo shows a blue wildflower. The species is not identified. Flowers can provide food for insects, while flowering time can respond to local rain and temperature; this photo is an ecological illustration, not a universal seasonal sign.",
        "weather": "Perth winter brings more rain, cold fronts and stronger westerly or southerly winds. The supplied 2024 record has one missing temperature reading for Makuru; wind is described here but is not plotted in the graph.",
        "background": "#EAF1F3", "accent": "#54788A",
    },
    "Djilba": {
        "months": "August to September",
        "description": "A changeable transition toward spring, with cool days mixed with warmer spells.",
        "meaning": "A public West Coast account describes cold, rainy or windy days alternating with sunshine. It also notes newborn animals and woodland birds tending nests. These signs are regional observations and vary with local conditions.",
        "image_context": "The photo shows yellow blossoms. The plant is not identified. Flowering can be one of many local signs of seasonal change, and blossoms may provide pollen or nectar for insects; no specific cultural meaning is assigned to this image.",
        "weather": "Djilba can bring cooler, wet and windy days followed by warmer, sunnier spells. The graph shows temperature and rainfall; wind is part of the seasonal context but is not measured in this chart.",
        "background": "#F2EDF3", "accent": "#8A6C8B",
    },
    "Kambarang": {
        "months": "October to November",
        "description": "Second spring, when warmer weather returns and many plants flower.",
        "meaning": "A public West Coast account describes orchids, kangaroo paws and banksias flowering during Kambarang. It also notes fruiting plants and increased animal activity. Flowering times and other signs vary by place and year.",
        "image_context": "The photo shows orange flowering plants, but the species is not identified. Flowering plants can provide nectar and pollen for insects and birds. This image is a general ecological example, not a claim that this plant marks Kambarang everywhere.",
        "weather": "Around Perth, warmer conditions and longer dry periods build toward summer, with fewer cold fronts. Wind direction varies and is not measured in this chart.",
        "background": "#F4F0E1", "accent": "#8E793C",
    },
}

# These summaries come from the supplied Perth Metro graphs for 2023-24.
# They describe one observed season and should not be read as climate averages.
SEASON_CLIMATE_SUMMARIES = {
    "Birak": ("31.6 °C", "1.8 mm", "Dec 2023 – Jan 2024"),
    "Bunuru": ("32.3 °C", "6.6 mm", "Feb – Mar 2024"),
    "Djeran": ("26.6 °C", "77.2 mm", "Apr – May 2024"),
    "Makuru": ("19.1 °C", "288.6 mm", "Jun – Jul 2024"),
    "Djilba": ("21.2 °C", "177.6 mm", "Aug – Sep 2024"),
    "Kambarang": ("25.4 °C", "58.0 mm", "Oct – Nov 2024"),
}

# Captions accompany the nature images loaded on season detail pages.
SEASON_IMAGE_CAPTIONS = {
    "Birak": "Kookaburra",
    "Bunuru": "White blossom and visiting insect",
    "Djeran": "Black cockatoo among flowering plants",
    "Makuru": "Blue wildflower",
    "Djilba": "Yellow wildflower",
    "Kambarang": "Orange spring blossoms",
}


def fit_window_to_screen(root, preferred_width, preferred_height):
    """Clamp requested geometry to screen bounds and return actual dimensions."""
    width = max(700, min(preferred_width, root.winfo_screenwidth() - 60))
    height = max(600, min(preferred_height, root.winfo_screenheight() - 80))
    root.minsize(min(700, width), min(600, height))
    root.geometry(f"{width}x{height}")
    return width, height


class SeasonWheel:
    """Draw the season wheel and render detailed seasonal information."""

    def __init__(self, app):
        """Keep the shared app shell for page navigation and window access."""
        self.app = app

    def show_information_page(self):
        """Build the interactive wheel that links to each season detail page."""
        app = self.app
        app.clear_page()
        app.root.title("Wheel of Noongar Seasons")
        fit_window_to_screen(app.root, 1100, 940)
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
            text="Interact with the wheel to unlock knowledge",
            font=("Segoe UI", 11),
            fg="#4e5c46",
            bg="#f7f3ee",
            wraplength=300,
            justify="left",
        )
        preview_description.pack(anchor="w", fill="x")

        tk.Frame(preview_panel, bg="#d8c8b4", height=1).pack(
            fill="x", pady=(18, 14)
        )
        tk.Label(
            preview_panel,
            text="About the six seasons",
            font=("Segoe UI", 13, "bold"),
            fg="#24381d",
            bg="#f7f3ee",
        ).pack(anchor="w", pady=(0, 6))
        tk.Label(
            preview_panel,
            text=(
                "The Noongar seasonal calendar recognises six seasons across "
                "the South West. Changes are read through weather, plants, "
                "animals and Country, rather than fixed dates. This Perth-area "
                "guide is one regional view; signs and knowledge vary between "
                "Noongar communities."
            ),
            font=("Segoe UI", 10),
            fg="#4e5c46",
            bg="#f7f3ee",
            wraplength=330,
            justify="left",
        ).pack(anchor="w", fill="x")

        artwork_path = (
            Path(__file__).resolve().parent.parent
            / "Data" / "Season Visuals" / "djeran_overview.png"
        )
        try:
            self.wheel_art_photo = tk.PhotoImage(file=str(artwork_path))
            tk.Label(
                preview_panel,
                image=self.wheel_art_photo,
                bg="#f7f3ee",
                bd=0,
                highlightthickness=0,
            ).pack(anchor="center", pady=(14, 4))
            tk.Label(
                preview_panel,
                text="Djeran season artwork",
                font=("Segoe UI", 9, "italic"),
                fg="#6b7166",
                bg="#f7f3ee",
            ).pack(anchor="center")
        except tk.TclError:
            self.wheel_art_photo = None
            tk.Label(
                preview_panel,
                text="Djeran season artwork is unavailable.",
                font=("Segoe UI", 9, "italic"),
                fg="#6b7166",
                bg="#f7f3ee",
            ).pack(anchor="center", pady=(12, 0))

        # Each 60-degree arc maps one entry in SEASONS to one clickable segment.
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
            # Capture each segment's name in the callbacks to avoid late binding.
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
                lambda event, name=season_name: app.show_season_page(name),
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
            """Convert pointer coordinates into an arc index for the preview."""
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
                    text="Interact with the wheel to unlock knowledge"
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
        """Show seasonal notes, weather summaries, graph, and nature image."""
        app = self.app
        app.clear_page()
        app.root.title(f"{season_name} | Noongar Seasons")
        window_width, _ = fit_window_to_screen(app.root, 1420, 940)
        season = SEASONS[season_name]
        page_bg = season["background"]
        accent = season["accent"]
        app.current_frame.configure(bg=page_bg)
        data_dir = Path(__file__).resolve().parent.parent / "Data"
        self.detail_images = []

        header = tk.Frame(app.current_frame, bg=accent, padx=18, pady=12)
        header.pack(fill="x")
        ttk.Button(
            header,
            text="‹  Back to seasons",
            command=self.show_information_page,
        ).pack(side="left")
        tk.Label(
            header,
            text="NOONGAR SEASON GUIDE",
            font=("Segoe UI", 10, "bold"),
            fg="#f5e9cc",
            bg=accent,
        ).pack(side="right")

        scroll_area = tk.Frame(app.current_frame, bg=page_bg)
        scroll_area.pack(fill="both", expand=True)
        page = tk.Canvas(scroll_area, bg=page_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_area, orient="vertical", command=page.yview)
        page.configure(yscrollcommand=scrollbar.set)
        page.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        content = tk.Frame(page, bg=page_bg)
        content_window = page.create_window((0, 0), window=content, anchor="nw")
        # The content frame determines the canvas scroll extent as it grows.
        content.bind(
            "<Configure>",
            lambda _event: page.configure(scrollregion=page.bbox("all")),
        )
        wrapping_labels = []

        def resize_content(event):
            """Match content width to the viewport and reflow wrapped labels."""
            page.itemconfigure(content_window, width=event.width)
            for label in wrapping_labels:
                label.configure(wraplength=min(700, max(280, event.width - 135)))

        page.bind("<Configure>", resize_content)
        page.bind_all(
            "<MouseWheel>",
            lambda event: page.yview_scroll(-1 if event.delta > 0 else 1, "units"),
        )
        # Remove the global wheel binding when this page is destroyed.
        detail_frame = app.current_frame
        detail_frame.bind(
            "<Destroy>",
            lambda event: page.unbind_all("<MouseWheel>")
            if event.widget is detail_frame
            else None,
        )

        tk.Label(
            content,
            text="WHADJUK COUNTRY  ·  PERTH, WESTERN AUSTRALIA",
            font=("Segoe UI", 9, "bold"),
            bg=page_bg,
            fg=accent,
        ).pack(pady=(22, 8))
        tk.Label(
            content,
            text=season_name,
            font=("Segoe UI", 32, "bold"),
            bg=page_bg,
            fg=accent,
        ).pack(pady=(0, 2))
        tk.Label(
            content,
            text=f"{season['months'].upper()}  ·  APPROXIMATE MONTH GUIDE",
            font=("Segoe UI", 10, "bold"),
            bg=page_bg,
            fg=accent,
        ).pack(pady=(0, 6))
        tk.Label(
            content,
            text="Seasonal changes are read through Country; these month ranges are a local guide, not fixed dates.",
            font=("Segoe UI", 10),
            bg=page_bg,
            fg="#4e5c46",
            justify="center",
        ).pack(padx=24, pady=(0, 12))

        def make_card(title, body, *, italic=False):
            """Create a reusable text card and track its responsive label."""
            card = tk.Frame(
                content,
                bg="#fffdf9",
                highlightbackground="#e1d8ca",
                highlightthickness=1,
            )
            card.pack(fill="x", padx=28, pady=8)
            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 12, "bold"),
                fg=accent,
                bg="#fffdf9",
            ).pack(anchor="w", padx=20, pady=(15, 7))
            body_label = tk.Label(
                card,
                text=body,
                font=("Segoe UI", 11, "italic" if italic else "normal"),
                fg="#2b2b2b",
                bg="#fffdf9",
                wraplength=760,
                justify="left",
            )
            body_label.pack(anchor="w", fill="x", padx=20, pady=(0, 16))
            wrapping_labels.append(body_label)
            return card

        make_card(
            "Season story and signs",
            f"{season['description']}\n\n{season['meaning']}\n\n"
            "This summary draws on one public West Coast account. Noongar "
            "knowledge and seasonal signs vary between Country and communities.",
        )
        source_link = tk.Label(
            content,
            text="Read the DPIRD West Coast season fact sheet ↗",
            font=("Segoe UI", 9, "underline"),
            fg="#345c4c",
            bg=page_bg,
            cursor="hand2",
        )
        source_link.pack(anchor="w", padx=40, pady=(0, 6))
        source_link.bind(
            "<Button-1>",
            lambda _event: webbrowser.open(
                "https://marinewaters.fish.wa.gov.au/resource/fact-sheet-the-noongar-six-seasons/"
            ),
        )

        make_card("Perth weather and wind", season["weather"])

        stats_row = tk.Frame(content, bg=page_bg)
        stats_row.pack(fill="x", padx=28, pady=(2, 8))
        mean_temperature, rainfall_total, record_period = SEASON_CLIMATE_SUMMARIES[
            season_name
        ]
        for column, (heading, value) in enumerate(
            (
                ("MEAN DAILY MAX", mean_temperature),
                ("SEASON RAINFALL", rainfall_total),
                ("RECORD PERIOD", record_period),
            )
        ):
            stats_row.columnconfigure(column, weight=1, uniform="climate_stat")
            stat = tk.Frame(
                stats_row,
                bg="#fffdf9",
                highlightbackground="#e1d8ca",
                highlightthickness=1,
                padx=14,
                pady=10,
            )
            stat.grid(row=0, column=column, sticky="nsew", padx=4)
            tk.Label(
                stat,
                text=value,
                font=("Segoe UI", 17 if column < 2 else 12, "bold"),
                fg=accent,
                bg="#fffdf9",
            ).pack(pady=(0, 4))
            tk.Label(
                stat,
                text=heading,
                font=("Segoe UI", 8, "bold"),
                fg="#65715e",
                bg="#fffdf9",
            ).pack()

        detail_row = tk.Frame(content, bg=page_bg)
        # Graph and nature content share equal columns at the bottom of the page.
        detail_row.pack(fill="x", padx=28, pady=8)
        detail_row.columnconfigure(0, weight=1, uniform="season_detail")
        detail_row.columnconfigure(1, weight=1, uniform="season_detail")

        graph_card = tk.Frame(
            detail_row,
            bg="#fffdf9",
            highlightbackground="#e1d8ca",
            highlightthickness=1,
        )
        graph_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        tk.Label(
            graph_card,
            text="DAILY TEMPERATURE & RAINFALL",
            font=("Segoe UI", 12, "bold"),
            fg=accent,
            bg="#fffdf9",
        ).pack(anchor="w", padx=18, pady=(14, 8))
        graph_path = data_dir / "Graphs" / f"{season_name}.png"
        try:
            with Image.open(graph_path) as source:
                source_graph = source.convert("RGB")
            # Scale the chart to the left column; the viewer keeps full resolution.
            display_width = max(1, min(760, (window_width - 120) // 2))
            display_height = round(
                source_graph.height * display_width / source_graph.width
            )
            graph_preview = source_graph.resize(
                (display_width, display_height), Image.Resampling.LANCZOS
            )
            graph = ImageTk.PhotoImage(graph_preview, master=app.root)
            # Keep a Python reference so Tk does not collect the displayed image.
            self.detail_images.append(graph)
            tk.Label(graph_card, image=graph, bg="#fffdf9").pack(
                padx=8, pady=(0, 5)
            )
            tk.Label(
                graph_card,
                text="Bureau of Meteorology · Perth Metro · 2023–24 daily observations. This is one year, not a long-term average; wind is discussed above but is not plotted.",
                font=("Segoe UI", 9),
                fg="#65715e",
                bg="#fffdf9",
                wraplength=display_width,
                justify="left",
            ).pack(padx=8, pady=(0, 8))
            ttk.Button(
                graph_card,
                text="View high-resolution graph",
                command=lambda path=graph_path: self.open_graph_viewer(
                    path, season_name
                ),
            ).pack(padx=8, pady=(0, 14))
        except (tk.TclError, OSError):
            tk.Label(
                graph_card,
                text="The seasonal graph could not be loaded.",
                font=("Segoe UI", 10, "italic"),
                fg="#54624f",
                bg="#f7f3ee",
            ).pack(padx=20, pady=20)

        art_block = tk.Frame(
            detail_row,
            bg="#fffdf9",
            highlightbackground="#e1d8ca",
            highlightthickness=1,
        )
        art_block.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        art_path = data_dir / "Season Visuals" / f"{season_name.lower()}_nature.png"
        try:
            art = tk.PhotoImage(file=str(art_path))
            self.detail_images.append(art)
            tk.Label(art_block, image=art, bg="#fffdf9").pack(pady=(14, 0))
            tk.Label(
                art_block,
                text=SEASON_IMAGE_CAPTIONS[season_name],
                font=("Segoe UI", 9, "italic"),
                fg=accent,
                bg="#fffdf9",
            ).pack(pady=(4, 2))
            image_note = tk.Label(
                art_block,
                text=season["image_context"],
                font=("Segoe UI", 10),
                fg="#4e5c46",
                bg="#fffdf9",
                wraplength=max(240, (window_width - 120) // 2 - 40),
                justify="left",
            )
            image_note.pack(fill="x", padx=16, pady=(0, 14))
        except (tk.TclError, OSError):
            tk.Label(
                art_block,
                text="Seasonal plant and animal image unavailable.",
                font=("Segoe UI", 10, "italic"),
                fg="#54624f",
                bg="#fffdf9",
            ).pack(padx=24, pady=18)

    def open_graph_viewer(self, graph_path, season_name):
        """Show the source graph at full resolution with bounded zoom controls."""
        app = self.app
        viewer = tk.Toplevel(app.root)
        viewer.title(f"{season_name} climate graph")
        viewer_width, viewer_height = fit_window_to_screen(
            viewer, 1400, 900
        )
        viewer.minsize(min(760, viewer_width), min(600, viewer_height))
        viewer.transient(app.root)

        with Image.open(graph_path) as source:
            source_graph = source.convert("RGB")

        toolbar = tk.Frame(viewer, bg="#f4efe7", padx=12, pady=8)
        toolbar.pack(fill="x")
        canvas_frame = tk.Frame(viewer, bg="#f4efe7")
        canvas_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(canvas_frame, bg="#ffffff", highlightthickness=0)
        horizontal = ttk.Scrollbar(
            canvas_frame, orient="horizontal", command=canvas.xview
        )
        vertical = ttk.Scrollbar(
            canvas_frame, orient="vertical", command=canvas.yview
        )
        canvas.configure(
            xscrollcommand=horizontal.set,
            yscrollcommand=vertical.set,
        )
        canvas.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)

        zoom_text = tk.StringVar()
        zoom_state = {"value": 1.0}

        def render_graph(zoom):
            """Resize the graph for the selected zoom and update the scroll area."""
            # Bound zoom and size the scroll region to match the rendered image.
            zoom = max(0.2, min(1.0, zoom))
            zoom_state["value"] = zoom
            size = (
                round(source_graph.width * zoom),
                round(source_graph.height * zoom),
            )
            rendered = source_graph.resize(size, Image.Resampling.LANCZOS)
            viewer.graph_photo = ImageTk.PhotoImage(rendered, master=viewer)
            canvas.delete("all")
            canvas.create_image(0, 0, image=viewer.graph_photo, anchor="nw")
            canvas.configure(scrollregion=(0, 0, *size))
            zoom_text.set(f"{round(zoom * 100)}%")
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)

        ttk.Button(
            toolbar, text="−", width=3,
            command=lambda: render_graph(zoom_state["value"] / 1.25),
        ).pack(side="left", padx=(0, 5))
        ttk.Button(
            toolbar, text="+", width=3,
            command=lambda: render_graph(zoom_state["value"] * 1.25),
        ).pack(side="left", padx=(0, 10))
        tk.Label(
            toolbar,
            textvariable=zoom_text,
            font=("Segoe UI", 10, "bold"),
            bg="#f4efe7",
            fg="#345c4c",
        ).pack(side="left")
        ttk.Button(
            toolbar,
            text="Fit to window",
            command=lambda: render_graph(
                min(
                    (viewer_width - 90) / source_graph.width,
                    (viewer_height - 150) / source_graph.height,
                    1.0,
                )
            ),
        ).pack(side="left", padx=12)
        ttk.Button(
            toolbar, text="Close", command=viewer.destroy
        ).pack(side="right")

        fit_zoom = min(
            (viewer_width - 90) / source_graph.width,
            (viewer_height - 150) / source_graph.height,
            1.0,
        )
        render_graph(fit_zoom)
