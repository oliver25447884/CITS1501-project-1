"""Question data and screens; page controllers use the shared app shell."""

import math
import tkinter as tk
import textwrap
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from tkinter import ttk

from modules.season_calendar import season_for_month
from modules.season_wheel import SEASONS


# Council-name membership powers lookup; shared names can map to two regions.
# These are indicative lookup associations, not definitive cultural boundaries.
NOONGAR_REGIONS = {
    "Whadjuk": {
        "Armadale", "Bassendean", "Bayswater", "Belmont", "Cambridge",
        "Canning", "Cockburn", "Claremont", "Cottesloe",
        "East Fremantle", "Fremantle", "Gosnells", "Joondalup", "Kalamunda",
        "Kwinana", "Melville", "Mosman Park", "Mundaring", "Nedlands",
        "Perth", "Rockingham", "Serpentine-Jarrahdale",
        "South Perth", "Stirling", "Subiaco", "Swan", "Victoria Park", "Vincent",
        "Wanneroo",
    },
    "Yued": {"Dandaragan", "Gingin", "Moora", "Victoria Plains"},
    "Ballardong": {
        "Beverley", "Brookton", "Bruce Rock",
        "Cunderdin", "Dowerin", "Goomalling", "Kellerberrin", "Kondinin",
        "Koorda", "Kulin", "Merredin", "Mount Marshall", "Nungarin", "Pingelly",
        "Quairading", "Tammin", "Toodyay", "Trayning", "Westonia", "Wickepin",
        "Wongan-Ballidu", "Wyalkatchem", "Yilgarn", "York", "Corrigin", "Cuballing",
        "Dumbleyung", "Lake Grace", "Wandering", "West Arthur", "Williams", "Wagin",
    },
    "Gnaala Karla Booja": {
        "Mandurah", "Bunbury", "Capel", "Collie", "Donnybrook-Balingup",
        "Dardanup", "Harvey",
    },
    "South West Boojarah": {
        "Busselton", "Augusta-Margaret River", "Nannup", "Manjimup", "Boyup Brook",
    },
    "Wagyl Kaip & Southern Noongar": {
        "Albany", "Denmark", "Plantagenet", "Cranbrook", "Gnowangerup",
        "Jerramungup", "Katanning", "Kojonup", "Kent", "Broomehill-Tambellup",
        "Woodanilling", "Ravensthorpe", "Wagin", "Walpole-Nornalup", "Wandering",
        "West Arthur",
    },
}


# Special question types route to council and date lookup screens.
REGION_QUESTIONS = [
    {
        "question": "What Noongar region do I live in?",
        "answer": "Type in your council to find your Noongar region.",
        "type": "region_lookup",
    },
    {
        "question": "Which Noongar season is it?",
        "answer": "Enter a date to find its Noongar season.",
        "type": "season_lookup",
    },
    {
        "question": "What does the Noongar seasonal calendar describe?",
        "answer": (
            "It describes seasonal changes in the environment, including "
            "weather, plants and animal activity."
        ),
    },
    {
        "question": "How is the Noongar seasonal calendar different from a four-season calendar?",
        "answer": (
            "It recognises six seasons, each connected to changes in the local "
            "environment rather than dividing the year into just spring, "
            "summer, autumn and winter."
        ),
    },
    {
        "question": "What kinds of signs can indicate a change of season?",
        "answer": (
            "Changes in weather, flowering plants, animal behaviour and other "
            "natural events can signal a change of season."
        ),
    },
    {
        "question": (
            "How can animal behaviour help indicate changes in the Noongar "
            "seasons?"
        ),
        "scrollable": True,
        "answer": (
            "Animals respond to seasonal changes in temperature, rainfall, "
            "food availability and vegetation. Changes in their behaviour "
            "can therefore provide important environmental indicators. "
            "These patterns can vary by species and location.\n\n"
            "During Makuru (roughly June-July), the coldest and wettest part "
            "of the year, some animals alter their behaviour to cope with "
            "colder, wetter conditions. Food and water availability also "
            "changes. Frogs may call and breed more after rainfall.\n\n"
            "As the weather moves into Djilba and Kambarang (roughly "
            "August-November), temperatures rise and vegetation changes. "
            "These conditions can support increased activity in many "
            "species, including birds and insects. Western grey kangaroos "
            "may feed and move around places where fresh vegetation and "
            "water are available. Splendid fairy-wrens may show increased "
            "activity and breeding behaviour in favourable conditions. "
            "Red-capped parrots respond to seasonal food such as flowers "
            "and fruit.\n\n"
            "During Kambarang, abundant flowering plants provide nectar and "
            "pollen. Native bees and other insects, as well as nectar-feeding "
            "birds such as honeyeaters, may be seen feeding around flowers. "
            "Their presence and activity can be observed alongside the "
            "flowering of plants.\n\n"
            "As the environment moves into Birak and Bunuru, conditions "
            "become hotter and drier. Animals may change when and where they "
            "forage to avoid the hottest parts of the day and seek water or "
            "shade.\n\n"
            "Examples of fauna and seasonal indicators:\n"
            "- Western grey kangaroo (Macropus fuliginosus) | Throughout the "
            "year | Feeding and movement respond to vegetation and water.\n"
            "- Splendid fairy-wren (Malurus splendens) | More noticeable in "
            "warmer months | Activity and breeding can coincide with "
            "favourable conditions.\n"
            "- Red-capped parrot (Purpureicephalus spurius) | Seasonal food "
            "availability | Feeding responds to flowering and fruiting "
            "plants.\n"
            "- Honeyeaters | Flowering periods | Increased feeding around "
            "flowering plants.\n"
            "- Native bees and other insects | Djilba-Kambarang and warmer "
            "periods | Activity increases when flowers provide nectar and "
            "pollen.\n"
            "- Frogs | Wet seasons and rainfall, including Makuru | Calling "
            "and breeding can increase after rain."
        ),
    },
    {
        "question": (
            "How can flowering plants indicate seasonal change? Which plants "
            "flower in each season?"
        ),
        "scrollable": True,
        "answer": (
            "Flowering plants are important environmental indicators because "
            "different plants flower at particular times of the year in "
            "response to changes in temperature, rainfall and daylight. "
            "Observing when plants begin flowering can provide clues that "
            "the environment is moving from one season into another. "
            "Flowering times can vary with location and year.\n\n"
            "During Djilba (roughly August-September), the weather begins "
            "transitioning from Makuru's cold, wet conditions towards "
            "warmer conditions. Some plants begin producing new growth and "
            "flowers.\n\n"
            "During Kambarang (roughly October-November), flowering becomes "
            "particularly noticeable, with an abundance of wildflowers "
            "across Noongar boodja. Banksias (Banksia spp.), kangaroo paws "
            "(Anigozanthos spp.) and various everlastings are examples. "
            "Their flowers are visible signs of warmer spring conditions.\n\n"
            "As the seasons progress into Birak (roughly December-January) "
            "and Bunuru (roughly February-March), the landscape becomes "
            "increasingly hot and dry. Many plants respond by reducing "
            "growth or conserving water.\n\n"
            "Examples of flora and seasonal indicators:\n"
            "- Kangaroo paw (Anigozanthos spp.) | Djilba-Kambarang | Bright "
            "flowers appear as the weather becomes warmer.\n"
            "- Banksia (Banksia spp.) | Djilba-Kambarang and into warmer "
            "months, depending on species | Flowers provide nectar and "
            "signal seasonal change.\n"
            "- Everlastings | Djilba-Kambarang | Large displays of flowers "
            "occur as conditions become warmer.\n"
            "- Grass trees (Xanthorrhoea spp.) | Often associated with "
            "warmer months | Flower spikes provide food for insects and "
            "other animals.\n"
            "- Jarrah (Eucalyptus marginata) | Flowering varies by location "
            "and year | Flowers provide nectar for fauna and reflect "
            "seasonal conditions."
        ),
    },
]


# Images paired with the council mappings above.
REGION_IMAGE_FILES = {
    "Whadjuk": "Whadjuk.png",
    "Yued": "Yued.png",
    "Ballardong": "Ballardong.png",
    "Gnaala Karla Booja": "Gnaala Karla Boodja.png",
    "South West Boojarah": "Southwest Boodjarah.png",
    "Wagyl Kaip & Southern Noongar": "Wagyl Kaip Southern Noongar.png",
}

# Extended seasonal FAQs shown alongside the shorter region questions.
FAQ_ITEMS = (
    {
        "season": "All seasons",
        "question": "What are the six Noongar seasons?",
        "answer": "Birak (December-January), Bunuru (February-March), Djeran (April-May), Makuru (June-July), Djilba (August-September), and Kambarang (October-November) are common month guides for Whadjuk Country around Perth.",
    },
    {
        "season": "All seasons",
        "question": "Are the season dates exact?",
        "answer": "No. Month ranges are a guide. Seasonal changes are understood through local signs in weather and the living environment, which do not follow fixed calendar dates.",
    },
    {
        "season": "Culture",
        "question": "Are the same seasonal signs used everywhere in Noongar Country?",
        "answer": "No. Noongar Country includes many places and environments. The signs, language, and knowledge connected with a season can vary between communities and locations.",
    },
    {
        "season": "Culture",
        "question": "How are seasonal changes recognised?",
        "answer": "People observe patterns in weather and the local environment, including plants and animals. The relevant signs are place-specific and are best learned from local Noongar knowledge holders.",
    },
    {
        "season": "Culture",
        "question": "Why are there six seasons instead of four?",
        "answer": "The six-season cycle describes finer changes through the year and reflects detailed observation of Country. It is a Noongar seasonal framework, not simply a different set of dates for the European calendar.",
    },
    {
        "season": "Culture",
        "question": "How are the seasons connected to Noongar culture?",
        "answer": "Seasonal knowledge is part of continuing relationships with Country, language, community, and living things. Specific teachings and responsibilities belong to Noongar people and places.",
    },
    {
        "season": "Culture",
        "question": "What does Country mean in seasonal knowledge?",
        "answer": "Country is more than a location: it includes relationships with lands, waters, living things, people, and responsibilities. Its meaning is specific to Noongar communities and places.",
    },
    {
        "season": "Culture",
        "question": "Is Noongar seasonal knowledge just about weather?",
        "answer": "No. Weather is one part of a broader understanding of place and environmental change, including plants, animals, and cultural knowledge. Learn local details from Noongar sources.",
    },
    {
        "season": "Culture",
        "question": "When does the Waugal, sometimes called the Rainbow Serpent, come out?",
        "answer": "There is no general Noongar season when the Waugal comes out. Waugal stories and knowledge are culturally significant and connected to particular places; learn what is appropriate to share from local Noongar knowledge holders.",
    },
    {
        "season": "Culture",
        "question": "Are all Noongar stories and seasonal teachings public?",
        "answer": "No. Some knowledge is shared publicly and some is not. Follow the guidance and protocols of the relevant Noongar community, and ask permission before recording or sharing cultural knowledge.",
    },
    {
        "season": "Culture",
        "question": "Are the animals in this guide cultural or totemic symbols?",
        "answer": "No. The wildlife notes are general ecological observations about species found in parts of south-west Western Australia. They do not assign cultural or spiritual meaning; that knowledge is specific to community and place.",
    },
    {
        "season": "Culture",
        "question": "How can I learn about Noongar seasons respectfully?",
        "answer": "Use resources created or endorsed by Noongar people, listen to local knowledge holders, and follow cultural and site protocols. Do not treat one account as universal or share knowledge without permission.",
    },
    {
        "season": "Birak",
        "question": "What is Birak like around Perth?",
        "answer": "Birak (roughly December-January) is commonly described as hot and dry, with long summer days. Local conditions change from year to year; check current heat and fire advice.",
    },
    {
        "season": "Birak",
        "question": "Which animals might I notice in Birak?",
        "answer": "The wildlife notes include bobtail skinks, western grey kangaroos, and ospreys in suitable habitats. Sightings are not guaranteed or exclusive to this season; watch quietly and give animals space.",
    },
    {
        "season": "Birak",
        "question": "Is Birak a good time for the beach?",
        "answer": "Birak is usually warm and dry around Perth, so it can be a popular beach season. Check surf and safety conditions, use sun protection, and swim at a patrolled beach.",
    },
    {
        "season": "Bunuru",
        "question": "What is Bunuru like?",
        "answer": "Bunuru (roughly February-March) is often described as the hottest, driest part of the year around Perth. Heat and low rainfall are typical, but vary between years.",
    },
    {
        "season": "Bunuru",
        "question": "Which month is usually driest in Bunuru?",
        "answer": "February is typically one of Perth's driest months. This is a long-term climate pattern, not a promise about any particular year.",
    },
    {
        "season": "Bunuru",
        "question": "Can I visit the beach in Bunuru?",
        "answer": "Yes. Bunuru is usually warm and dry, but high temperatures and strong UV need care. Check local surf conditions, protect yourself from the sun, and swim at a patrolled beach.",
    },
    {
        "season": "Djeran",
        "question": "What changes during Djeran?",
        "answer": "Djeran (roughly April-May) marks a shift toward cooler weather around Perth. Notice local changes in temperature and the landscape rather than expecting them on a set date.",
    },
    {
        "season": "Djeran",
        "question": "When should I plant a gum tree?",
        "answer": "Djeran into Makuru (roughly April-July) is often a useful time to plant a suitable seedling: cooler weather and seasonal rain can help it establish before summer. Check the species and local growing advice.",
    },
    {
        "season": "Djeran",
        "question": "Is cattle breeding tied to a Noongar season?",
        "answer": "No fixed Noongar season determines cattle breeding. The seasonal calendar describes patterns in Country; producers plan joining and calving around herd needs, pasture, water, and local agricultural advice.",
    },
    {
        "season": "Makuru",
        "question": "What is Makuru known for?",
        "answer": "Makuru (roughly June-July) is commonly described as the cold, wet season around Perth. Rain and cold fronts become more frequent, though totals vary each year.",
    },
    {
        "season": "Makuru",
        "question": "Which month and season are usually wettest around Perth?",
        "answer": "July is typically Perth's wettest month, and Makuru is generally the wettest Noongar season in this local guide. These are averages, not a forecast.",
    },
    {
        "season": "Makuru",
        "question": "When can I see humpback whales migrating north along the WA coast?",
        "answer": "Humpbacks generally migrate north during autumn and winter, broadly overlapping Djeran and Makuru in the south-west. Timing varies by location and year, and sightings are never guaranteed.",
    },
    {
        "season": "Djilba",
        "question": "What is Djilba like?",
        "answer": "Djilba (roughly August-September) is a changeable transition toward spring. Around Perth, cooler wet days may alternate with warmer weather.",
    },
    {
        "season": "Djilba",
        "question": "What might I see in Djilba?",
        "answer": "Early wildflowers may appear in parts of the south-west, and local wildlife remains active in suitable habitats. Species and flowering times vary; observe without picking or disturbing.",
    },
    {
        "season": "Djilba",
        "question": "When do humpback whales migrate south past the south-west?",
        "answer": "The southward migration is generally seen in spring, around Djilba and Kambarang (roughly August-November). Timing varies by year and location, so sightings are never guaranteed.",
    },
    {
        "season": "Kambarang",
        "question": "What is Kambarang like?",
        "answer": "Kambarang (roughly October-November) is commonly associated with warmer spring weather and many flowering plants in parts of the south-west. Local signs differ between places.",
    },
    {
        "season": "Kambarang",
        "question": "When should I look for south-west wildflowers?",
        "answer": "Djilba and Kambarang (roughly August-November) are good general seasons to look, though each plant flowers in its own time. Stay on paths and do not pick flowers in reserves.",
    },
    {
        "season": "Kambarang",
        "question": "How can I watch wildlife respectfully in any season?",
        "answer": "Observe quietly from a distance, stay on marked paths, and never feed, handle, or pursue wildlife. Follow local site advice and remember that seasonal patterns do not guarantee an animal sighting.",
    },
)


def _bind_mousewheel(widget, canvas):
    """Add mouse-wheel scrolling to a widget/canvas pair on common platforms."""

    def scroll(event):
        """Normalize platform wheel input into a canvas scroll direction."""
        if getattr(event, "num", None) == 4:
            direction = -1
        elif getattr(event, "num", None) == 5:
            direction = 1
        else:
            delta = getattr(event, "delta", 0)
            direction = -1 if delta > 0 else 1
        canvas.yview_scroll(direction, "units")
        return "break"

    widget.bind("<MouseWheel>", scroll)
    widget.bind("<Button-4>", scroll)
    widget.bind("<Button-5>", scroll)


# Shared answer widgets are used by both the home-page list and detail screens.
def display_question_answer(answer_frame, question, back_to_questions=None):
    """Display one answer and an optional button to return to the questions."""
    tk.Label(
        answer_frame,
        text=question["question"],
        font=("Segoe UI", 20, "bold"),
        fg="#24381d",
        bg="#f4efe7",
        wraplength=600,
        justify="center",
    ).pack(padx=30, pady=(45, 25))

    if question.get("scrollable"):
        answer_panel = tk.Frame(
            answer_frame,
            bg="#f7f3ee",
            highlightbackground="#d8c8b4",
            highlightthickness=1,
        )
        answer_panel.pack(fill="both", expand=True, padx=45, pady=(0, 20))

        answer_text = tk.Text(
            answer_panel,
            font=("Segoe UI", 12),
            fg="#2b2b2b",
            bg="#f7f3ee",
            wrap="word",
            padx=20,
            pady=20,
            borderwidth=0,
            highlightthickness=0,
        )
        answer_scrollbar = ttk.Scrollbar(
            answer_panel,
            orient="vertical",
            command=answer_text.yview,
        )
        answer_text.configure(yscrollcommand=answer_scrollbar.set)
        answer_text.insert("1.0", question["answer"])
        answer_text.configure(state="disabled")
        answer_text.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        answer_scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=8)
        _bind_mousewheel(answer_text, answer_text)
    else:
        answer_panel = tk.Frame(
            answer_frame,
            bg="#f7f3ee",
            highlightbackground="#d8c8b4",
            highlightthickness=1,
        )
        answer_panel.pack(fill="x", padx=45, pady=(0, 20))
        tk.Label(
            answer_panel,
            text=question["answer"],
            font=("Segoe UI", 14),
            fg="#2b2b2b",
            bg="#f7f3ee",
            wraplength=560,
            justify="left",
            padx=25,
            pady=25,
        ).pack(fill="x", padx=4, pady=4)

    if back_to_questions is not None:
        ttk.Button(
            answer_frame,
            text="Back to explore",
            command=back_to_questions,
        ).pack(pady=(0, 8))


def display_question_results(results_frame, questions, open_question):
    """Show question buttons inside a scrollable panel."""
    for child in results_frame.winfo_children():
        child.destroy()

    canvas = tk.Canvas(results_frame, bg="#ffffff", highlightthickness=0)
    scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    questions_frame = tk.Frame(canvas, bg="#ffffff")
    questions_window = canvas.create_window(
        (0, 0), window=questions_frame, anchor="nw"
    )

    def update_scroll_region(_event=None):
        """Refresh scroll bounds after embedded question widgets change size."""
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_questions(event):
        """Stretch the embedded question list to the canvas viewport width."""
        canvas.itemconfigure(questions_window, width=event.width)
        update_scroll_region()

    questions_frame.bind("<Configure>", update_scroll_region)
    canvas.bind("<Configure>", resize_questions)
    _bind_mousewheel(canvas, canvas)
    _bind_mousewheel(questions_frame, canvas)

    if not questions:
        tk.Label(
            questions_frame,
            text="No questions available.",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#2b2b2b",
        ).pack(pady=15)
        return

    current_section = None
    for item in questions:
        section = item.get("season", "General questions")
        if section != current_section:
            current_section = section
            tk.Label(
                questions_frame,
                text=section,
                font=("Segoe UI", 10, "bold"),
                fg="#24381d",
                bg="#ffffff",
            ).pack(anchor="w", padx=10, pady=(10, 3))

        question_button = ttk.Button(
            questions_frame,
            text=textwrap.fill(item["question"], width=38),
            command=lambda selected_question=item: open_question(selected_question),
        )
        question_button.pack(fill="x", padx=10, pady=3)
        _bind_mousewheel(question_button, canvas)


class QuestionPages:
    """Build lookup screens and route selections through the shared app shell."""

    def __init__(self, app):
        """Keep the shared app shell for screen construction and navigation."""
        self.app = app

    def show_question_page(self, question):
        """Display an answer or open the council and season lookup screen."""
        self.app.clear_page()
        self.app.current_frame.pack_configure(pady=(20, 0))
        self.app.root.title("Question information")
        self.app.set_windowed_size("700x760", (550, 500))

        if question.get("type") == "season_lookup":
            self.show_season_lookup()
            return

        if question.get("type") != "region_lookup":
            display_question_answer(
                self.app.current_frame,
                question,
                self.app.show_home_page,
            )
            return

        tk.Label(
            self.app.current_frame,
            text=question["question"],
            font=("Segoe UI", 20, "bold"),
            fg="#24381d",
            bg="#f4efe7",
            wraplength=600,
            justify="center",
        ).pack(padx=30, pady=(45, 25))

        search_panel = tk.Frame(
            self.app.current_frame,
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

        image_placeholder = tk.Frame(self.app.current_frame, bg="#e7d8c4")
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
            """Load/cache maps and fit matching regions into the image placeholder."""
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
                        Path(__file__).resolve().parent.parent
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
            """Normalize council input and refresh its message and region maps."""
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
                result_label.config(
                    text="Council not found in the Noongar council list."
                )
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
            """Refresh map sizing when the image viewport is resized."""
            if image_state["size"] != (event.width, event.height):
                show_region_images(
                    image_state["regions"], image_state["fallback_text"]
                )

        image_placeholder.bind("<Configure>", resize_region_images)

        search_entry.bind("<KeyRelease>", update_region_result)
        search_entry.bind("<Return>", update_region_result)
        search_entry.focus_set()

        ttk.Button(
            self.app.current_frame,
            text="Back to explore",
            command=self.app.show_home_page,
        ).pack(pady=(0, 8))
        image_placeholder.pack(fill="both", expand=True, padx=20, pady=0)

    def show_season_lookup(self):
        """Let the user enter a day and month and find the matching season."""
        tk.Label(
            self.app.current_frame,
            text="Which Noongar season is it?",
            font=("Segoe UI", 20, "bold"),
            fg="#24381d",
            bg="#f4efe7",
            wraplength=600,
            justify="center",
        ).pack(padx=30, pady=(45, 25))

        tk.Label(
            self.app.current_frame,
            text="Enter the day and month, in that order:",
            font=("Segoe UI", 12, "bold"),
            fg="#2b2b2b",
            bg="#f7f3ee",
        ).pack(anchor="w", padx=30, pady=(25, 8))

        date_fields = tk.Frame(self.app.current_frame, bg="#f7f3ee")
        date_fields.pack(anchor="w", fill="x", padx=30)
        date_fields.columnconfigure(0, weight=1)
        date_fields.columnconfigure(1, weight=1)

        tk.Label(
            date_fields,
            text="Day",
            font=("Segoe UI", 10, "bold"),
            fg="#2b2b2b",
            bg="#f7f3ee",
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))
        tk.Label(
            date_fields,
            text="Month",
            font=("Segoe UI", 10, "bold"),
            fg="#2b2b2b",
            bg="#f7f3ee",
        ).grid(row=0, column=1, sticky="w", padx=(10, 0))

        day_entry = tk.Entry(date_fields, font=("Segoe UI", 12), width=12)
        day_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        month_entry = tk.Entry(date_fields, font=("Segoe UI", 12), width=12)
        month_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0))

        result_panel = tk.Frame(
            self.app.current_frame,
            bg="#f7f3ee",
            bd=1,
            relief="solid",
        )
        result_panel.pack(fill="both", expand=True, padx=45, pady=20)

        result_label = tk.Label(
            result_panel,
            text="Enter the day first, then the month (for example: 8, 10).",
            font=("Segoe UI", 13),
            fg="#24381d",
            bg="#f7f3ee",
            wraplength=540,
            justify="left",
        )
        result_label.pack(anchor="w", padx=25, pady=25)

        more_button = ttk.Button(
            self.app.current_frame,
            text="Tell me more",
            state="disabled",
        )

        def update_season_result(event=None):
            """Validate the entered date and show its season and extra details."""
            entered_day = day_entry.get().strip()
            entered_month = month_entry.get().strip()
            if not entered_day or not entered_month:
                result_label.configure(
                    text="Enter both the day and month to find the season."
                )
                more_button.configure(state="disabled")
                return

            try:
                day = int(entered_day)
                month = int(entered_month)
                parsed_date = datetime(2000, month, day)
            except ValueError:
                result_label.configure(
                    text="Enter a valid day first, followed by a month from 1 to 12."
                )
                more_button.configure(state="disabled")
                return

            season_name = season_for_month(parsed_date.month)
            season = SEASONS[season_name]
            result_label.configure(
                text=(
                    f"{season_name} ({season['months']})\n\n"
                    f"{season['description']}\n\n"
                    "Season dates are approximate month guides and can "
                    "vary with local conditions."
                )
            )
            more_button.configure(
                state="normal",
                command=lambda name=season_name: self.app.show_season_page(name),
            )

        for date_entry in (day_entry, month_entry):
            date_entry.bind("<KeyRelease>", update_season_result)
            date_entry.bind("<Return>", update_season_result)
        day_entry.focus_set()

        ttk.Button(
            self.app.current_frame,
            text="Back to explore",
            command=self.app.show_home_page,
        ).pack(pady=(0, 8))
        more_button.pack(pady=(0, 8))
