import math
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


INK = "#18231f"
MUTED = "#68776f"
PAPER = "#f3f0e7"
PANEL = "#fbf9f2"
GREEN = "#21473d"
SAGE = "#3c6154"
GOLD = "#d9a850"
TEAL = "#63b9a9"
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
RAINFALL = (15.9, 12.5, 21.6, 35.2, 84.5, 126.9, 144.3, 124.3, 79.9, 40.0, 24.0, 9.6)
MAX_TEMP = (31.4, 31.7, 29.7, 25.9, 22.4, 19.5, 18.5, 19.1, 20.7, 23.4, 26.8, 29.6)

SEASONS = (
	{
		"name": "Djilba", "months": "Jul - Aug", "ids": (6, 7), "color": "#91bda7",
		"animal": "Quenda",
		"description": "Cool mornings give way to brighter days. New growth appears as winter rain begins to ease.",
		"animal_note": "A small marsupial of south-west WA, the quenda forages among leaf litter and dense vegetation.",
		"land": ("#d7e3d5", "#8aa98b", "#587c67"),
	},
	{
		"name": "Kambarang", "months": "Sep - Oct", "ids": (8, 9), "color": "#e4b84f",
		"animal": "Carnaby's cockatoo",
		"description": "Wildflowers open across the south-west as days warm and the landscape begins to dry.",
		"animal_note": "This threatened south-west species feeds on seeds and flowering trees.",
		"land": ("#e8d9a5", "#a1ad70", "#667b50"),
	},
	{
		"name": "Birak", "months": "Nov - Dec", "ids": (10, 11), "color": "#e27c55",
		"animal": "Bobtail lizard",
		"description": "Hot, dry days arrive, with afternoon sea breezes bringing relief along the coast.",
		"animal_note": "Bobtails bask in the sun and seek shade when the ground becomes hot.",
		"land": ("#e9bc8d", "#c48355", "#72583d"),
	},
	{
		"name": "Bunuru", "months": "Jan - Feb", "ids": (0, 1), "color": "#cf684d",
		"animal": "Western grey kangaroo",
		"description": "The hottest, driest stretch of the year. Coastal breezes and shade become especially welcome.",
		"animal_note": "Kangaroos rest in shade during hot weather and forage when conditions cool.",
		"land": ("#e8b77d", "#bd8753", "#62523e"),
	},
	{
		"name": "Djeran", "months": "Mar - Apr", "ids": (2, 3), "color": "#a6bd68",
		"animal": "Black swan",
		"description": "Cooler mornings arrive with south-westerly winds; evenings become gentler.",
		"animal_note": "Black swans are familiar across Perth wetlands, estuaries and lakes.",
		"land": ("#d9d8ad", "#8b9869", "#536a52"),
	},
	{
		"name": "Makuru", "months": "May - Jun", "ids": (4, 5), "color": "#668faa",
		"animal": "Motorbike frog",
		"description": "Cool fronts bring the coldest and wettest weather, replenishing wetlands and waterways.",
		"animal_note": "Motorbike frogs are associated with wetlands, where seasonal rain can replenish habitat.",
		"land": ("#b6c9d0", "#738f91", "#425e5e"),
	},
)

REGIONS = {
	"Whadjuk": "Country around the Perth coastal plain and Swan River. This display does not define a fixed boundary.",
	"Yued": "A broad northern Wheatbelt and coastal-plain context, associated with sandplain, lakes and seasonal wildflowers.",
	"Ballardong": "A broad central Wheatbelt context, including open country, salt lakes and seasonal waterways.",
	"Wardandi": "A south-west coastal context where forest, estuary and ocean environments meet.",
	"Bibbulman": "A southern forest and coastal context, including jarrah, karri and tingle country.",
	"Minang": "A south-coast context around Albany, shaped by ocean, granite headlands and bushland.",
	"Goreng": "A Great Southern context connecting inland waterways, bush and coast.",
	"Njunga": "A far south-eastern coastal context toward Esperance and the Southern Ocean.",
}


def season_average(values, season):
	return sum(values[month] for month in season["ids"]) / len(season["ids"])


class BoodjaWeatherApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Boodja Weather | Noongar seasons")
		self.root.geometry("1180x820")
		self.root.minsize(850, 680)
		self.root.configure(bg=PAPER)
		self.selected_season = 5
		self.active_region = "Whadjuk"
		self.wheel_center = (0, 0)
		self.wheel_radius = 0
		self.display_font = tkfont.Font(family="Georgia", size=26, weight="bold")
		self.body_font = tkfont.Font(family="TkDefaultFont", size=11)
		self.small_font = tkfont.Font(family="TkFixedFont", size=9)
		self.show_login()

	def clear_window(self):
		for child in self.root.winfo_children():
			child.destroy()

	def make_button(self, parent, text, command, *, primary=False):
		background = GOLD if primary else PANEL
		foreground = INK if primary else GREEN
		return tk.Button(
			parent, text=text, command=command, font=("TkDefaultFont", 10, "bold"),
			fg=foreground, bg=background, activebackground="#edc36f" if primary else "#e8eadf",
			activeforeground=INK, relief="flat", bd=0, padx=15, pady=10, cursor="hand2",
		)

	def show_login(self):
		self.clear_window()
		frame = tk.Frame(self.root, bg=GREEN, padx=48, pady=42)
		frame.place(relx=0.5, rely=0.5, anchor="center")
		tk_label = tk.Label(frame, text="BOODJA WEATHER ATLAS", bg=GREEN, fg=GOLD, font=self.small_font)
		tk_label.pack(anchor="w")
		tk.Label(frame, text="Read the sky.", bg=GREEN, fg="white", font=("Georgia", 36, "bold")).pack(anchor="w", pady=(16, 5))
		tk.Label(frame, text="An interactive seasonal view of Noongar boodja.", bg=GREEN, fg="#d9e4da", font=self.body_font).pack(anchor="w", pady=(0, 25))
		tk.Label(frame, text="Passcode", bg=GREEN, fg="white", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
		self.password = tk.Entry(frame, show="•", font=self.body_font, relief="flat", width=30)
		self.password.pack(fill="x", pady=(7, 12), ipady=8)
		self.error_label = tk.Label(frame, text="", bg=GREEN, fg="#f4a38d", font=self.body_font)
		self.error_label.pack(anchor="w", pady=(8, 0))
		self.make_button(frame, "Open the atlas", self.unlock, primary=True).pack(fill="x", pady=(8, 0))
		self.password.bind("<Return>", lambda _event: self.unlock())
		self.password.focus_set()

	def unlock(self):
		if self.password.get() == "123":
			self.show_home()
		else:
			self.error_label.configure(text="That passcode is not recognised.")
			self.password.selection_range(0, tk.END)

	def add_header(self, parent, eyebrow, title, back_command=None):
		bar = tk.Frame(parent, bg=GREEN, padx=24, pady=15)
		bar.pack(fill="x")
		if back_command:
			self.make_button(bar, "‹  Back", back_command).pack(side="left", padx=(0, 18))
		tk.Label(bar, text="BOODJA / WEATHER ATLAS", bg=GREEN, fg="white", font=("Georgia", 13, "bold")).pack(side="left")
		if not back_command:
			self.make_button(bar, "Regional context", self.show_map).pack(side="right")
		body = tk.Frame(parent, bg=GREEN if back_command else PAPER, padx=24, pady=20)
		body.pack(fill="x")
		tk.Label(body, text=eyebrow.upper(), bg=body["bg"], fg=GOLD if back_command else SAGE, font=self.small_font).pack(anchor="w")
		tk.Label(body, text=title, bg=body["bg"], fg="white" if back_command else INK, font=("Georgia", 30, "bold")).pack(anchor="w", pady=(5, 0))
		return body

	def show_home(self):
		self.clear_window()
		page = tk.Frame(self.root, bg=PAPER)
		page.pack(fill="both", expand=True)
		self.add_header(page, "Noongar season calendar · Whadjuk boodja", "Weather has a rhythm.")
		content = tk.Frame(page, bg=PAPER, padx=22, pady=18)
		content.pack(fill="both", expand=True)
		left = tk.Frame(content, bg="#e8eadf", padx=12, pady=12)
		left.pack(side="left", fill="both", expand=True, padx=(0, 12))
		tk.Label(left, text="THE SIX SEASONS", bg="#e8eadf", fg=SAGE, font=self.small_font).pack(anchor="w", padx=10, pady=(4, 0))
		self.wheel = tk.Canvas(left, width=520, height=520, bg="#e8eadf", highlightthickness=0)
		self.wheel.pack(fill="both", expand=True)
		self.wheel.bind("<Configure>", lambda _event: self.draw_wheel())
		self.wheel.bind("<Button-1>", self.on_wheel_click)
		tk.Label(left, text="SEASON NAME  ·  LOCAL ANIMAL", bg="#e8eadf", fg=MUTED, font=("TkFixedFont", 8)).pack(pady=(0, 5))
		right = tk.Frame(content, bg=PANEL, padx=22, pady=20, highlightbackground="#dfe2d7", highlightthickness=1)
		right.pack(side="right", fill="both", expand=True)
		self.overview = right
		self.render_overview()
		footer = tk.Label(page, text="Climate profile: Perth monthly averages · Seasonal wildlife notes are ecological, not spiritual assignments.", bg=PAPER, fg=MUTED, font=("TkDefaultFont", 9), pady=12)
		footer.pack(fill="x")

	def draw_wheel(self):
		if not hasattr(self, "wheel") or not self.wheel.winfo_exists():
			return
		canvas = self.wheel
		canvas.delete("all")
		width, height = max(canvas.winfo_width(), 350), max(canvas.winfo_height(), 350)
		center_x, center_y = width / 2, height / 2
		radius = min(width, height) * 0.43
		self.wheel_center = (center_x, center_y)
		self.wheel_radius = radius
		for index, season in enumerate(SEASONS):
			start = -120 + index * 60
			points = [(center_x, center_y)]
			for step in range(13):
				angle = math.radians(start + step * 5)
				points.append((center_x + radius * math.cos(angle), center_y + radius * math.sin(angle)))
			points.append((center_x, center_y))
			canvas.create_polygon(
				points, fill=season["color"], outline="#fbf9f2" if index == self.selected_season else "#f3f0e7",
				width=4 if index == self.selected_season else 2,
			)
			middle = math.radians(start + 30)
			label_radius = radius * 0.64
			label_x = center_x + label_radius * math.cos(middle)
			label_y = center_y + label_radius * math.sin(middle)
			canvas.create_text(label_x, label_y - 7, text=season["name"], fill=INK, font=("Georgia", 12, "bold"), width=radius * 0.72)
			canvas.create_text(label_x, label_y + 10, text=season["animal"], fill="#314c40", font=("TkDefaultFont", 8), width=radius * 0.75)
		canvas.create_oval(center_x - radius * 0.32, center_y - radius * 0.32, center_x + radius * 0.32, center_y + radius * 0.32, fill=PANEL, outline="#dfe2d7", width=2)
		canvas.create_text(center_x, center_y - 8, text="BOODJA", fill=MUTED, font=self.small_font)
		canvas.create_text(center_x, center_y + 15, text="Perth", fill=INK, font=("Georgia", 17, "bold"))

	def on_wheel_click(self, event):
		center_x, center_y = self.wheel_center
		distance = math.hypot(event.x - center_x, event.y - center_y)
		if distance < self.wheel_radius * 0.34 or distance > self.wheel_radius:
			return
		angle = (math.degrees(math.atan2(event.y - center_y, event.x - center_x)) + 120) % 360
		self.selected_season = min(int(angle // 60), len(SEASONS) - 1)
		self.draw_wheel()
		self.render_overview()
		self.show_season(self.selected_season)

	def render_overview(self):
		if not hasattr(self, "overview") or not self.overview.winfo_exists():
			return
		for child in self.overview.winfo_children():
			child.destroy()
		season = SEASONS[self.selected_season]
		tk.Label(self.overview, text=season["months"], bg=PANEL, fg=SAGE, font=self.small_font).pack(anchor="w")
		tk.Label(self.overview, text=season["name"], bg=PANEL, fg=INK, font=("Georgia", 28, "bold")).pack(anchor="w", pady=(5, 2))
		tk.Label(self.overview, text=season["description"], bg=PANEL, fg=MUTED, font=self.body_font, wraplength=440, justify="left").pack(anchor="w", pady=(4, 14))
		metrics = tk.Frame(self.overview, bg=PANEL)
		metrics.pack(fill="x", pady=(0, 16))
		self.metric(metrics, "RAINFALL / MONTH", f"{season_average(RAINFALL, season):.1f} mm")
		self.metric(metrics, "MAX TEMPERATURE", f"{season_average(MAX_TEMP, season):.1f} °C")
		tk.Label(self.overview, text="PERTH MONTHLY CLIMATE", bg=PANEL, fg=SAGE, font=self.small_font).pack(anchor="w")
		graph = tk.Canvas(self.overview, height=225, bg=PANEL, highlightthickness=0)
		graph.pack(fill="both", expand=True, pady=(4, 8))
		graph.bind("<Configure>", lambda _event, widget=graph: self.draw_graph(widget, self.selected_season))
		self.make_button(self.overview, "Open season detail", lambda: self.show_season(self.selected_season), primary=True).pack(anchor="w", pady=(8, 0))

	def metric(self, parent, label, value):
		card = tk.Frame(parent, bg="#eff1e8", padx=12, pady=10)
		card.pack(side="left", fill="x", expand=True, padx=(0, 8))
		tk.Label(card, text=label, bg="#eff1e8", fg=MUTED, font=("TkFixedFont", 8)).pack(anchor="w")
		tk.Label(card, text=value, bg="#eff1e8", fg=INK, font=("Georgia", 17, "bold")).pack(anchor="w", pady=(4, 0))

	def draw_graph(self, canvas, season_index=None):
		if not canvas.winfo_exists():
			return
		canvas.delete("all")
		width = max(canvas.winfo_width(), 360)
		height = max(canvas.winfo_height(), 170)
		left, right, top, bottom = 42, width - 42, 18, height - 34
		plot_height = bottom - top
		plot_width = right - left
		for step, rain_tick in enumerate((150, 100, 50, 0)):
			y = top + step * plot_height / 3
			canvas.create_line(left, y, right, y, fill="#dfe2d7")
			canvas.create_text(left - 8, y, text=str(rain_tick), fill=MUTED, anchor="e", font=("TkFixedFont", 8))
			temp_tick = 35 - step * (20 / 3)
			canvas.create_text(right + 8, y, text=f"{temp_tick:.0f}°", fill=MUTED, anchor="w", font=("TkFixedFont", 8))
		canvas.create_text(left - 8, top - 10, text="mm", fill=MUTED, anchor="e", font=("TkFixedFont", 8))
		canvas.create_text(right + 8, top - 10, text="°C", fill=MUTED, anchor="w", font=("TkFixedFont", 8))
		x_positions = [left + month * plot_width / 11 for month in range(12)]
		rain_points = []
		temp_points = []
		for month in range(12):
			rain_y = bottom - RAINFALL[month] / 150 * plot_height
			temp_y = bottom - (MAX_TEMP[month] - 15) / 20 * plot_height
			rain_points.extend((x_positions[month], rain_y))
			temp_points.extend((x_positions[month], temp_y))
			canvas.create_text(x_positions[month], bottom + 15, text=MONTHS[month], fill=MUTED, font=("TkFixedFont", 7))
		canvas.create_line(*rain_points, fill=GOLD, width=3, smooth=True)
		canvas.create_line(*temp_points, fill=TEAL, width=3, smooth=True)
		for month in range(12):
			for series, color in ((rain_points, GOLD), (temp_points, TEAL)):
				x, y = series[month * 2:month * 2 + 2]
				radius = 4 if season_index is not None and month in SEASONS[season_index]["ids"] else 2.5
				canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)
		canvas.create_line(left, height - 3, left + 16, height - 3, fill=GOLD, width=3)
		canvas.create_text(left + 21, height - 3, text="Rainfall", fill=MUTED, anchor="w", font=("TkDefaultFont", 8))
		canvas.create_line(left + 100, height - 3, left + 116, height - 3, fill=TEAL, width=3)
		canvas.create_text(left + 122, height - 3, text="Max temperature", fill=MUTED, anchor="w", font=("TkDefaultFont", 8))

	def show_season(self, index):
		self.selected_season = index
		season = SEASONS[index]
		self.clear_window()
		page = tk.Frame(self.root, bg=PAPER)
		page.pack(fill="both", expand=True)
		self.add_header(page, season["months"], season["name"], self.show_home)
		content = tk.Frame(page, bg=PAPER, padx=24, pady=20)
		content.pack(fill="both", expand=True)
		left = tk.Frame(content, bg=PANEL, padx=12, pady=12)
		left.pack(side="left", fill="both", expand=True, padx=(0, 18))
		landscape = tk.Canvas(left, height=300, bg=season["land"][0], highlightthickness=0)
		landscape.pack(fill="both", expand=True)
		landscape.bind("<Configure>", lambda _event, widget=landscape, data=season: self.draw_landscape(widget, data))
		tk.Label(left, text="SEASONAL LANDSCAPE", bg=PANEL, fg=SAGE, font=self.small_font).pack(anchor="w", pady=(12, 0))
		right = tk.Frame(content, bg=PAPER)
		right.pack(side="right", fill="both", expand=True)
		tk.Label(right, text=season["description"], bg=PAPER, fg=INK, font=("Georgia", 17), wraplength=470, justify="left").pack(anchor="w", pady=(0, 16))
		metrics = tk.Frame(right, bg=PAPER)
		metrics.pack(fill="x", pady=(0, 15))
		self.metric(metrics, "RAINFALL / MONTH", f"{season_average(RAINFALL, season):.1f} mm")
		self.metric(metrics, "MAX TEMPERATURE", f"{season_average(MAX_TEMP, season):.1f} °C")
		animal = tk.Frame(right, bg=GREEN, padx=14, pady=12)
		animal.pack(fill="x", pady=(0, 15))
		tk.Label(animal, text=f"LOCAL WILDLIFE · {season['animal'].upper()}", bg=GREEN, fg=GOLD, font=self.small_font).pack(anchor="w")
		tk.Label(animal, text=season["animal_note"], bg=GREEN, fg="white", font=self.body_font, wraplength=440, justify="left").pack(anchor="w", pady=(5, 0))
		tk.Label(animal, text="Ecological observation only; not a spiritual or totemic claim.", bg=GREEN, fg="#c4d3ca", font=("TkDefaultFont", 9)).pack(anchor="w", pady=(7, 0))
		tk.Label(right, text="PERTH MONTHLY CLIMATE", bg=PAPER, fg=SAGE, font=self.small_font).pack(anchor="w")
		graph = tk.Canvas(right, height=230, bg=PANEL, highlightthickness=0)
		graph.pack(fill="both", expand=True, pady=(5, 0))
		graph.bind("<Configure>", lambda _event, widget=graph: self.draw_graph(widget, index))

	def draw_landscape(self, canvas, season):
		if not canvas.winfo_exists():
			return
		canvas.delete("all")
		width = max(canvas.winfo_width(), 320)
		height = max(canvas.winfo_height(), 220)
		sky, hill, foreground = season["land"]
		canvas.create_rectangle(0, 0, width, height, fill=sky, outline=sky)
		canvas.create_oval(width * 0.69, height * 0.12, width * 0.82, height * 0.34, fill="#f4d58c", outline="")
		canvas.create_polygon(0, height * 0.66, width * 0.22, height * 0.42, width * 0.43, height * 0.65, width * 0.67, height * 0.39, width, height * 0.66, width, height, 0, height, fill=hill, outline="")
		canvas.create_polygon(0, height * 0.79, width * 0.26, height * 0.62, width * 0.55, height * 0.8, width * 0.78, height * 0.57, width, height * 0.78, width, height, 0, height, fill=foreground, outline="")
		if season["name"] in ("Kambarang", "Djilba"):
			for x in (0.16, 0.28, 0.77, 0.88):
				base_y = height * (0.84 if x < 0.5 else 0.81)
				canvas.create_line(width * x, base_y, width * x, base_y - 25, fill="#405e45", width=2)
				for offset in (-5, 0, 5):
					canvas.create_oval(width * x + offset - 3, base_y - 31, width * x + offset + 3, base_y - 25, fill=GOLD if season["name"] == "Kambarang" else "#d9e4cf", outline="")
		if season["name"] == "Makuru":
			for x in range(20, int(width), 34):
				canvas.create_line(x, height * 0.16, x - 8, height * 0.28, fill="#eef4f1", width=2)
		canvas.create_text(18, height - 18, text=season["name"].upper(), anchor="w", fill="white", font=self.small_font)

	def show_map(self):
		self.clear_window()
		page = tk.Frame(self.root, bg=PAPER)
		page.pack(fill="both", expand=True)
		self.add_header(page, "Regional context", "Many places, one boodja.", self.show_home)
		content = tk.Frame(page, bg=PAPER, padx=24, pady=20)
		content.pack(fill="both", expand=True)
		map_frame = tk.Frame(content, bg="#d9e5dc", padx=14, pady=14)
		map_frame.pack(side="left", fill="both", expand=True, padx=(0, 18))
		canvas = tk.Canvas(map_frame, width=650, height=500, bg="#d9e5dc", highlightthickness=0)
		canvas.pack(fill="both", expand=True)
		self.map_canvas = canvas
		canvas.bind("<Configure>", lambda _event, widget=canvas: self.draw_regions(widget))
		panel = tk.Frame(content, bg=PANEL, padx=16, pady=16)
		panel.pack(side="right", fill="y")
		tk.Label(panel, text="SELECTED REGION", bg=PANEL, fg=SAGE, font=self.small_font).pack(anchor="w")
		self.region_title = tk.Label(panel, text=self.active_region, bg=PANEL, fg=INK, font=("Georgia", 21, "bold"))
		self.region_title.pack(anchor="w", pady=(8, 5))
		self.region_description = tk.Label(panel, text=REGIONS[self.active_region], bg=PANEL, fg=MUTED, font=self.body_font, wraplength=260, justify="left")
		self.region_description.pack(anchor="w", pady=(0, 14))
		for region in REGIONS:
			self.make_button(panel, region, lambda selected=region: self.select_region(selected)).pack(fill="x", pady=3)
		tk.Label(panel, text="Illustrative cultural context only. These shapes are not authoritative boundaries or suitable for land claims. Seek guidance from Traditional Owners.", bg=PANEL, fg=MUTED, font=("TkDefaultFont", 9), wraplength=260, justify="left").pack(anchor="w", pady=(15, 0))

	def draw_regions(self, canvas):
		canvas.delete("all")
		width, height = max(canvas.winfo_width(), 360), max(canvas.winfo_height(), 300)
		canvas.create_text(18, 17, text="SOUTH-WEST WESTERN AUSTRALIA · INDICATIVE", anchor="nw", fill=GREEN, font=self.small_font)
		shapes = {
			"Yued": ((0.13, 0.07), (0.35, 0.06), (0.37, 0.24), (0.19, 0.27)),
			"Whadjuk": ((0.25, 0.24), (0.44, 0.22), (0.47, 0.39), (0.39, 0.47), (0.24, 0.41)),
			"Ballardong": ((0.37, 0.08), (0.69, 0.09), (0.76, 0.32), (0.47, 0.39), (0.39, 0.23)),
			"Wardandi": ((0.21, 0.42), (0.39, 0.46), (0.36, 0.76), (0.25, 0.83), (0.17, 0.63)),
			"Bibbulman": ((0.39, 0.45), (0.75, 0.34), (0.84, 0.63), (0.68, 0.83), (0.37, 0.76)),
			"Minang": ((0.36, 0.76), (0.68, 0.83), (0.62, 0.97), (0.29, 0.94), (0.25, 0.83)),
			"Goreng": ((0.68, 0.83), (0.89, 0.77), (0.94, 0.89), (0.82, 0.98), (0.62, 0.97)),
			"Njunga": ((0.75, 0.34), (0.91, 0.31), (0.98, 0.47), (0.94, 0.77), (0.84, 0.63)),
		}
		for name, shape in shapes.items():
			points = [coordinate for x, y in shape for coordinate in (x * width, y * height)]
			selected = name == self.active_region
			canvas.create_polygon(points, fill="#d8b86f" if selected else "#8eaa8b", outline=PANEL, width=3, tags=(f"region-{name}",))
			center_x = sum(x for x, _ in shape) / len(shape) * width
			center_y = sum(y for _, y in shape) / len(shape) * height
			canvas.create_text(center_x, center_y, text=name.upper(), fill=INK, font=("TkDefaultFont", 8, "bold"))
			canvas.tag_bind(f"region-{name}", "<Button-1>", lambda _event, selected=name: self.select_region(selected))
		canvas.create_line(width * 0.14, height * 0.1, width * 0.13, height * 0.27, width * 0.17, height * 0.43, width * 0.16, height * 0.61, width * 0.25, height * 0.83, width * 0.35, height * 0.94, fill="#6c9ba0", width=4, smooth=True)
		canvas.create_text(width * 0.15, height * 0.52, text="INDIAN OCEAN", fill="#547c7b", angle=90, font=("TkDefaultFont", 9, "bold"))

	def select_region(self, name):
		self.active_region = name
		self.region_title.configure(text=name)
		self.region_description.configure(text=REGIONS[name])
		if hasattr(self, "map_canvas") and self.map_canvas.winfo_exists():
			self.draw_regions(self.map_canvas)


def main():
	root = tk.Tk()
	BoodjaWeatherApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()
