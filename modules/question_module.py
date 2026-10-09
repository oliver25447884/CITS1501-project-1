"""Question and Noongar-region lookup content for the Noongar Seasons app."""

import textwrap
import tkinter as tk
from tkinter import ttk


# Councils are stored by Noongar region for the region lookup question.
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


# Add or edit region questions and answers in this list.
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


def _bind_mousewheel(widget, canvas):
    """Add mouse-wheel scrolling to a widget/canvas pair on common platforms."""
    def scroll(event):
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
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_questions(event):
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
