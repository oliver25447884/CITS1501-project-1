import math
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


INK = "#202622"
MUTED = "#68736e"
PAPER = "#f4f5f4"
PANEL = "#ffffff"
GREEN = "#21473d"
SAGE = "#46675a"
GOLD = "#d5a64a"
TEAL = "#4c9c8c"
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
RAINFALL = (15.9, 12.5, 21.6, 35.2, 84.5, 126.9, 144.3, 124.3, 79.9, 40.0, 24.0, 9.6)
MAX_TEMP = (31.4, 31.7, 29.7, 25.9, 22.4, 19.5, 18.5, 19.1, 20.7, 23.4, 26.8, 29.6)

SEASONS = (
	{
		"name": "Djilba", "months": "Aug - Sep", "ids": (7, 8), "color": "#91bda7",
		"animal": "Quenda",
		"description": "A changeable transition from winter toward spring. Cool, wet days may alternate with warmer weather.",
		"animal_note": "A small marsupial of south-west WA, the quenda forages among leaf litter and dense vegetation.",
		"wildlife": (
			("Quenda", "A small marsupial that forages among leaf litter and dense vegetation, usually at night."),
			("Motorbike frog", "A south-west wetland frog; listen near suitable habitat without disturbing it."),
			("Carnaby's black-cockatoo", "A threatened south-west species that moves between feeding and roosting sites."),
		),
		"signs": "Cool days can give way to warmer ones as winter rain begins to ease.",
		"land": ("#d7e3d5", "#8aa98b", "#587c67"),
	},
	{
		"name": "Kambarang", "months": "Oct - Nov", "ids": (9, 10), "color": "#e4b84f",
		"animal": "Carnaby's cockatoo",
		"description": "Warmer spring weather arrives, with many flowering plants across parts of the south-west.",
		"animal_note": "This threatened south-west species feeds on seeds and flowering trees.",
		"wildlife": (
			("Carnaby's black-cockatoo", "A threatened south-west species that feeds on seeds and native plants."),
			("Western honey possum", "A nectar-feeder of south-west heathland; it is only found in suitable habitat."),
			("Splendid fairy-wren", "A small bushland bird that is best watched quietly from a distance."),
		),
		"signs": "Warmer spring days and flowering plants are noticeable in many local habitats.",
		"land": ("#e8d9a5", "#a1ad70", "#667b50"),
	},
	{
		"name": "Birak", "months": "Dec - Jan", "ids": (11, 0), "color": "#e27c55",
		"animal": "Bobtail lizard",
		"description": "Hot, dry days arrive, with afternoon sea breezes bringing relief along the coast.",
		"animal_note": "Bobtails bask in the sun and seek shade when the ground becomes hot.",
		"wildlife": (
			("Bobtail skink", "A familiar large skink; it may bask in mild sun and shelter during extreme heat."),
			("Western grey kangaroo", "Often seen in open woodland and grassy areas, especially in cooler hours."),
			("Osprey", "A fish-eating raptor associated with suitable coastal and estuary habitat."),
		),
		"signs": "Long, hot, dry days and coastal afternoon breezes are common around Perth.",
		"land": ("#e9bc8d", "#c48355", "#72583d"),
	},
	{
		"name": "Bunuru", "months": "Feb - Mar", "ids": (1, 2), "color": "#cf684d",
		"animal": "Western grey kangaroo",
		"description": "The hottest, driest stretch of the year. Coastal breezes and shade become especially welcome.",
		"animal_note": "Kangaroos rest in shade during hot weather and forage when conditions cool.",
		"wildlife": (
			("Western grey kangaroo", "Look for grazing in open areas during cooler parts of the day."),
			("Bobtail skink", "A ground-dwelling reptile that uses cover to avoid the hottest conditions."),
			("Black swan", "Common on suitable wetlands and estuaries across the south-west."),
		),
		"signs": "This is typically the hottest, driest part of the year in the Perth area.",
		"land": ("#e8b77d", "#bd8753", "#62523e"),
	},
	{
		"name": "Djeran", "months": "Apr - May", "ids": (3, 4), "color": "#a6bd68",
		"animal": "Black swan",
		"description": "Cooler mornings arrive with south-westerly winds; evenings become gentler.",
		"animal_note": "Black swans are familiar across Perth wetlands, estuaries and lakes.",
		"wildlife": (
			("Black swan", "A familiar waterbird on wetlands, estuaries and lakes."),
			("Quenda", "Look for foraging signs in dense vegetation; sightings are more likely around dusk."),
			("Carnaby's black-cockatoo", "This threatened cockatoo uses suitable woodland and urban feeding habitat."),
		),
		"signs": "Cooler mornings and evenings mark a shift away from summer heat.",
		"land": ("#d9d8ad", "#8b9869", "#536a52"),
	},
	{
		"name": "Makuru", "months": "Jun - Jul", "ids": (5, 6), "color": "#668faa",
		"animal": "Motorbike frog",
		"description": "Cool fronts bring the coldest and wettest weather, replenishing wetlands and waterways.",
		"animal_note": "Motorbike frogs are associated with wetlands, where seasonal rain can replenish habitat.",
		"wildlife": (
			("Motorbike frog", "A south-west frog associated with wetlands and seasonal water."),
			("Black swan", "Look for swans on wetlands and estuaries; observe from a respectful distance."),
			("Western grey kangaroo", "This species uses open woodland and grassy habitats across the region."),
		),
		"signs": "Cool fronts and winter rain are more frequent, replenishing waterways and wetlands.",
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

FAQ_ITEMS = (
	{"season": "All seasons", "question": "What are the six Noongar seasons?", "answer": "Birak (December-January), Bunuru (February-March), Djeran (April-May), Makuru (June-July), Djilba (August-September), and Kambarang (October-November) are common month guides for Whadjuk Country around Perth."},
	{"season": "All seasons", "question": "Are the season dates exact?", "answer": "No. Month ranges are a guide. Seasonal changes are understood through local signs in weather and the living environment, which do not follow fixed calendar dates."},
	{"season": "Culture", "question": "Are the same seasonal signs used everywhere in Noongar Country?", "answer": "No. Noongar Country includes many places and environments. The signs, language, and knowledge connected with a season can vary between communities and locations."},
	{"season": "Culture", "question": "How are seasonal changes recognised?", "answer": "People observe patterns in weather and the local environment, including plants and animals. The relevant signs are place-specific and are best learned from local Noongar knowledge holders."},
	{"season": "Culture", "question": "Why are there six seasons instead of four?", "answer": "The six-season cycle describes finer changes through the year and reflects detailed observation of Country. It is a Noongar seasonal framework, not simply a different set of dates for the European calendar."},
	{"season": "Culture", "question": "How are the seasons connected to Noongar culture?", "answer": "Seasonal knowledge is part of continuing relationships with Country, language, community, and living things. Specific teachings and responsibilities belong to Noongar people and places."},
	{"season": "Culture", "question": "What does Country mean in seasonal knowledge?", "answer": "Country is more than a location: it includes relationships with lands, waters, living things, people, and responsibilities. Its meaning is specific to Noongar communities and places."},
	{"season": "Culture", "question": "Is Noongar seasonal knowledge just about weather?", "answer": "No. Weather is one part of a broader understanding of place and environmental change, including plants, animals, and cultural knowledge. Learn local details from Noongar sources."},
	{"season": "Culture", "question": "When does the Waugal, sometimes called the Rainbow Serpent, come out?", "answer": "There is no general Noongar season when the Waugal comes out. Waugal stories and knowledge are culturally significant and connected to particular places; learn what is appropriate to share from local Noongar knowledge holders."},
	{"season": "Culture", "question": "Are all Noongar stories and seasonal teachings public?", "answer": "No. Some knowledge is shared publicly and some is not. Follow the guidance and protocols of the relevant Noongar community, and ask permission before recording or sharing cultural knowledge."},
	{"season": "Culture", "question": "Are the animals in this guide cultural or totemic symbols?", "answer": "No. The wildlife notes are general ecological observations about species found in parts of south-west Western Australia. They do not assign cultural or spiritual meaning; that knowledge is specific to community and place."},
	{"season": "Culture", "question": "How can I learn about Noongar seasons respectfully?", "answer": "Use resources created or endorsed by Noongar people, listen to local knowledge holders, and follow cultural and site protocols. Do not treat one account as universal or share knowledge without permission."},
	{"season": "Birak", "question": "What is Birak like around Perth?", "answer": "Birak (roughly December-January) is commonly described as hot and dry, with long summer days. Local conditions change from year to year; check current heat and fire advice."},
	{"season": "Birak", "question": "Which animals might I notice in Birak?", "answer": "The wildlife notes include bobtail skinks, western grey kangaroos, and ospreys in suitable habitats. Sightings are not guaranteed or exclusive to this season; watch quietly and give animals space."},
	{"season": "Birak", "question": "Is Birak a good time for the beach?", "answer": "Birak is usually warm and dry around Perth, so it can be a popular beach season. Check surf and safety conditions, use sun protection, and swim at a patrolled beach."},
	{"season": "Bunuru", "question": "What is Bunuru like?", "answer": "Bunuru (roughly February-March) is often described as the hottest, driest part of the year around Perth. Heat and low rainfall are typical, but vary between years."},
	{"season": "Bunuru", "question": "Which month is usually driest in Bunuru?", "answer": "February is typically one of Perth's driest months. This is a long-term climate pattern, not a promise about any particular year."},
	{"season": "Bunuru", "question": "Can I visit the beach in Bunuru?", "answer": "Yes. Bunuru is usually warm and dry, but high temperatures and strong UV need care. Check local surf conditions, protect yourself from the sun, and swim at a patrolled beach."},
	{"season": "Djeran", "question": "What changes during Djeran?", "answer": "Djeran (roughly April-May) marks a shift toward cooler weather around Perth. Notice local changes in temperature and the landscape rather than expecting them on a set date."},
	{"season": "Djeran", "question": "When should I plant a gum tree?", "answer": "Djeran into Makuru (roughly April-July) is often a useful time to plant a suitable seedling: cooler weather and seasonal rain can help it establish before summer. Check the species and local growing advice."},
	{"season": "Djeran", "question": "Is cattle breeding tied to a Noongar season?", "answer": "No fixed Noongar season determines cattle breeding. The seasonal calendar describes patterns in Country; producers plan joining and calving around herd needs, pasture, water, and local agricultural advice."},
	{"season": "Makuru", "question": "What is Makuru known for?", "answer": "Makuru (roughly June-July) is commonly described as the cold, wet season around Perth. Rain and cold fronts become more frequent, though totals vary each year."},
	{"season": "Makuru", "question": "Which month and season are usually wettest around Perth?", "answer": "July is typically Perth's wettest month, and Makuru is generally the wettest Noongar season in this local guide. These are averages, not a forecast."},
	{"season": "Makuru", "question": "When can I see humpback whales migrating north along the WA coast?", "answer": "Humpbacks generally migrate north during autumn and winter, broadly overlapping Djeran and Makuru in the south-west. Timing varies by location and year, and sightings are never guaranteed."},
	{"season": "Djilba", "question": "What is Djilba like?", "answer": "Djilba (roughly August-September) is a changeable transition toward spring. Around Perth, cooler wet days may alternate with warmer weather."},
	{"season": "Djilba", "question": "What might I see in Djilba?", "answer": "Early wildflowers may appear in parts of the south-west, and local wildlife remains active in suitable habitats. Species and flowering times vary; observe without picking or disturbing."},
	{"season": "Djilba", "question": "When do humpback whales migrate south past the south-west?", "answer": "The southward migration is generally seen in spring, around Djilba and Kambarang (roughly August-November). Timing varies by year and location, so sightings are never guaranteed."},
	{"season": "Kambarang", "question": "What is Kambarang like?", "answer": "Kambarang (roughly October-November) is commonly associated with warmer spring weather and many flowering plants in parts of the south-west. Local signs differ between places."},
	{"season": "Kambarang", "question": "When should I look for south-west wildflowers?", "answer": "Djilba and Kambarang (roughly August-November) are good general seasons to look, though each plant flowers in its own time. Stay on paths and do not pick flowers in reserves."},
	{"season": "Kambarang", "question": "How can I watch wildlife respectfully in any season?", "answer": "Observe quietly from a distance, stay on marked paths, and never feed, handle, or pursue wildlife. Follow local site advice and remember that seasonal patterns do not guarantee an animal sighting."},
)


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
		self.display_font = tkfont.Font(family="TkDefaultFont", size=27, weight="bold")
		self.body_font = tkfont.Font(family="TkDefaultFont", size=11)
		self.small_font = tkfont.Font(family="TkDefaultFont", size=9)
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
		tk.Label(frame, text="Read the sky.", bg=GREEN, fg="white", font=("TkDefaultFont", 32, "bold")).pack(anchor="w", pady=(16, 5))
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
		tk.Label(bar, text="BOODJA / WEATHER ATLAS", bg=GREEN, fg="white", font=("TkDefaultFont", 12, "bold")).pack(side="left")
		if not back_command:
			self.make_button(bar, "Questions", self.show_questions).pack(side="right", padx=(0, 8))
			self.make_button(bar, "Regional context", self.show_map).pack(side="right")
		body = tk.Frame(parent, bg=GREEN if back_command else PAPER, padx=24, pady=20)
		body.pack(fill="x")
		tk.Label(body, text=eyebrow.upper(), bg=body["bg"], fg=GOLD if back_command else SAGE, font=self.small_font).pack(anchor="w")
		tk.Label(body, text=title, bg=body["bg"], fg="white" if back_command else INK, font=self.display_font).pack(anchor="w", pady=(5, 0))
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
		footer = tk.Label(page, text="Approximate Perth climate averages. Season boundaries and wildlife vary by place and year.", bg=PAPER, fg=MUTED, font=("TkDefaultFont", 9), pady=12)
		footer.pack(fill="x")

	def show_questions(self):
		self.clear_window()
		page = tk.Frame(self.root, bg=PAPER)
		page.pack(fill="both", expand=True)
		self.add_header(page, "Field guide  /  Whadjuk boodja", "Season questions", self.show_home)
		content = tk.Frame(page, bg=PAPER, padx=24, pady=18)
		content.pack(fill="both", expand=True)
		controls = tk.Frame(content, bg=PAPER)
		controls.pack(fill="x", pady=(0, 14))
		tk.Label(controls, text="SEARCH", background=PAPER, foreground=SAGE, font=self.small_font).pack(side="left", padx=(0, 8))
		self.question_search = tk.StringVar(self.root)
		search = tk.Entry(
			controls, textvariable=self.question_search, font=self.body_font,
			bg=PANEL, fg=INK, relief="flat", highlightthickness=1,
			highlightbackground="#dfe4e0", highlightcolor=TEAL, insertbackground=INK,
		)
		search.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 16))
		tk.Label(controls, text="TOPIC", background=PAPER, foreground=SAGE, font=self.small_font).pack(side="left", padx=(0, 8))
		topics = ("All topics", "Culture", "All seasons") + tuple(season["name"] for season in SEASONS)
		self.question_filter = ttk.Combobox(controls, values=topics, state="readonly", width=16)
		self.question_filter.current(0)
		self.question_filter.pack(side="left")
		self.question_filter.bind("<<ComboboxSelected>>", self.refresh_question_list)

		browser = tk.Frame(content, bg=PAPER)
		browser.pack(fill="both", expand=True)
		list_panel = tk.Frame(browser, bg=PANEL, padx=12, pady=12, highlightbackground="#e1e6e2", highlightthickness=1, width=400)
		list_panel.pack(side="left", fill="both", padx=(0, 14))
		list_panel.pack_propagate(False)
		self.question_count = tk.Label(list_panel, text="30 QUESTIONS", bg=PANEL, fg=MUTED, font=self.small_font)
		self.question_count.pack(anchor="w", padx=4, pady=(2, 10))
		list_body = tk.Frame(list_panel, bg=PANEL)
		list_body.pack(fill="both", expand=True)
		scrollbar = ttk.Scrollbar(list_body, orient="vertical")
		scrollbar.pack(side="right", fill="y")
		self.question_list = tk.Listbox(
			list_body, font=self.body_font, bg=PANEL, fg=INK, relief="flat", bd=0,
			selectmode="browse", activestyle="none", selectbackground="#e3eee8",
			selectforeground=INK, highlightthickness=0, yscrollcommand=scrollbar.set,
		)
		self.question_list.pack(side="left", fill="both", expand=True)
		scrollbar.configure(command=self.question_list.yview)
		self.question_list.bind("<<ListboxSelect>>", self.select_question)

		answer_panel = tk.Frame(browser, bg=PANEL, padx=28, pady=26, highlightbackground="#e1e6e2", highlightthickness=1)
		answer_panel.pack(side="right", fill="both", expand=True)
		self.answer_topic = tk.Label(answer_panel, text="", bg=PANEL, fg=SAGE, font=self.small_font)
		self.answer_topic.pack(anchor="w")
		self.answer_title = tk.Label(answer_panel, text="", bg=PANEL, fg=INK, font=("TkDefaultFont", 21, "bold"), wraplength=590, justify="left")
		self.answer_title.pack(anchor="w", pady=(14, 12))
		self.answer_text = tk.Label(answer_panel, text="", bg=PANEL, fg=MUTED, font=self.body_font, wraplength=590, justify="left")
		self.answer_text.pack(anchor="nw")
		self.answer_text.bind("<Configure>", lambda event: self.answer_text.configure(wraplength=max(event.width - 4, 280)))
		tk.Label(
			answer_panel,
			text="Season windows are approximate. Cultural knowledge and seasonal signs are local; seek guidance from Noongar people.",
			bg=PANEL, fg=MUTED, font=("TkDefaultFont", 9), wraplength=590, justify="left",
		).pack(side="bottom", anchor="w", pady=(20, 0))
		self.question_search.trace_add("write", self.refresh_question_list)
		self.refresh_question_list()
		search.focus_set()

	def refresh_question_list(self, *_trace_info):
		query = self.question_search.get().strip().casefold()
		topic = self.question_filter.get()
		self.filtered_questions = [
			item for item in FAQ_ITEMS
			if (topic == "All topics" or item["season"] == topic)
			and (not query or query in (item["question"] + " " + item["answer"]).casefold())
		]
		self.question_list.delete(0, tk.END)
		self.question_count.configure(text=f"{len(self.filtered_questions)} QUESTIONS")
		for item in self.filtered_questions:
			self.question_list.insert(tk.END, item["question"])
		if self.filtered_questions:
			self.question_list.selection_set(0)
			self.question_list.activate(0)
			self.render_question(0)
		else:
			self.answer_topic.configure(text="NO MATCHES")
			self.answer_title.configure(text="Try another search")
			self.answer_text.configure(text="No questions match this search and topic.")

	def select_question(self, _event):
		selection = self.question_list.curselection()
		if selection:
			self.render_question(selection[0])

	def render_question(self, index):
		item = self.filtered_questions[index]
		self.answer_topic.configure(text=item["season"].upper())
		self.answer_title.configure(text=item["question"])
		self.answer_text.configure(text=item["answer"])

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
		tk.Label(self.overview, text=season["name"], bg=PANEL, fg=INK, font=self.display_font).pack(anchor="w", pady=(5, 2))
		tk.Label(self.overview, text=season["description"], bg=PANEL, fg=MUTED, font=self.body_font, wraplength=440, justify="left").pack(anchor="w", pady=(4, 14))
		tk.Label(self.overview, text="SEASONAL SIGNS", bg=PANEL, fg=SAGE, font=self.small_font).pack(anchor="w")
		tk.Label(self.overview, text=season["signs"], bg=PANEL, fg=INK, font=self.body_font, wraplength=440, justify="left").pack(anchor="w", pady=(4, 10))
		tk.Label(self.overview, text="WILDLIFE TO NOTICE", bg=PANEL, fg=SAGE, font=self.small_font).pack(anchor="w")
		tk.Label(self.overview, text="  ·  ".join(animal[0] for animal in season["wildlife"]), bg=PANEL, fg=MUTED, font=self.body_font, wraplength=440, justify="left").pack(anchor="w", pady=(4, 12))
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
		tk.Label(card, text=value, bg="#eff1e8", fg=INK, font=("TkDefaultFont", 17, "bold")).pack(anchor="w", pady=(4, 0))

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
		tk.Label(right, text=season["description"], bg=PAPER, fg=INK, font=("TkDefaultFont", 15), wraplength=470, justify="left").pack(anchor="w", pady=(0, 12))
		tk.Label(right, text="SEASONAL SIGNS", bg=PAPER, fg=SAGE, font=self.small_font).pack(anchor="w")
		tk.Label(right, text=season["signs"], bg=PAPER, fg=MUTED, font=self.body_font, wraplength=470, justify="left").pack(anchor="w", pady=(4, 14))
		metrics = tk.Frame(right, bg=PAPER)
		metrics.pack(fill="x", pady=(0, 15))
		self.metric(metrics, "RAINFALL / MONTH", f"{season_average(RAINFALL, season):.1f} mm")
		self.metric(metrics, "MAX TEMPERATURE", f"{season_average(MAX_TEMP, season):.1f} °C")
		animal = tk.Frame(right, bg=GREEN, padx=14, pady=12)
		animal.pack(fill="x", pady=(0, 15))
		tk.Label(animal, text="WILDLIFE TO NOTICE", bg=GREEN, fg=GOLD, font=self.small_font).pack(anchor="w")
		for animal_name, animal_note in season["wildlife"]:
			row = tk.Frame(animal, bg=GREEN)
			row.pack(fill="x", pady=(8, 0))
			tk.Label(row, text=animal_name, bg=GREEN, fg="white", font=("TkDefaultFont", 10, "bold"), width=25, anchor="w").pack(side="left", anchor="n")
			tk.Label(row, text=animal_note, bg=GREEN, fg="#d5dfd9", font=("TkDefaultFont", 9), wraplength=300, justify="left").pack(side="left", fill="x", expand=True)
		tk.Label(animal, text="Regional ecological notes only; no cultural or totemic meaning is implied.", bg=GREEN, fg="#c4d3ca", font=("TkDefaultFont", 9), wraplength=440, justify="left").pack(anchor="w", pady=(10, 0))
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
		self.region_title = tk.Label(panel, text=self.active_region, bg=PANEL, fg=INK, font=("TkDefaultFont", 20, "bold"))
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
