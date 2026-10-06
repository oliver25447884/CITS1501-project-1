# Councils are stored by Noongar region for the region lookup question.
NOONGAR_REGIONS = {
    "Whadjuk": {
        "Armadale",
        "Bassendean",
        "Bayswater",
        "Belmont",
        "Cambridge",
        "Canning",
        "Cockburn",
        "Claremont",
        "Cottesloe",
        "Cottelsoe",
        "East Fremantle",
        "Fremantle",
        "Gosnells",
        "Joondalup",
        "Kalamunda",
        "Kwinana",
        "Melville",
        "Mosman Park",
        "Mundaring",
        "Nedlands",
        "Perth",
        "Rockingham",
        "Serpentine-Jarrandale",
        "Serpentine-Jarrahdale",
        "South Perth",
        "Stirling",
        "Subiaco",
        "Swan",
        "Victoria Park",
        "Vincent",
        "Wanneroo",
    },
    "Yued": {
        "Dandaragan",
        "Gingin",
        "Moora",
        "Victoria Plains",
    },
    "Ballardong": {
        "Beverly",
        "Beverley",
        "Brookton",
        "Bruce Rcok",
        "Bruce Rock",
        "Cunderdin",
        "Dowerin",
        "Goomalling",
        "Kellerberrin",
        "Kondinin",
        "Koorda",
        "Kulin",
        "Merredin",
        "Mount Marshall",
        "Nungarin",
        "Pingelly",
        "Quairading",
        "Tammin",
        "Toodyay",
        "Trayning",
        "Westonia",
        "Wickepin",
        "Wongan-Ballidu",
        "Wyalkatchem",
        "Yilgarn",
        "York",
        "Corrigin",
        "Cuballing",
        "Dumbleyung",
        "Lake Grace",
        "Wandering",
        "West Arthur",
        "Williams",
        "Wagin",
    },
    "Gnaala Karla Booja": {
        "Mandurah",
        "Bunbury",
        "Capel",
        "Collie",
        "Donnybrook-Balingup",
        "Dardanup",
        "Harvy",
        "Harvey",
    },
    "South West Boojarah": {
        "Busselton",
        "Augusta-Margaret River",
        "Nannup",
        "Manjimup",
        "Boyup Brook",
    },
    "Wagyl Kaip & Southern Noongar": {
        "Albany",
        "Denmark",
        "Plantagenet",
        "Cranbook",
        "Cranbrook",
        "Gnowangerup",
        "Jerramungup",
        "Katanning",
        "Kojonup",
        "Kent",
        "Broomehill-Tambellup",
        "Woodanilling",
        "Ravensthorpe",
        "Wagin",
        "Walpole-Nornalup",
        "Wandering",
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
]
#An interactive map of perths subburbs will be placed here


def display_question_answer(answer_frame, question, back_to_questions):
    import tkinter as tk
    from tkinter import ttk

    tk.Label(
        answer_frame,
        text=question["question"],
        font=("Segoe UI", 20, "bold"),
        fg="#24381d",
        bg="#f4efe7",
        wraplength=600,
        justify="center",
    ).pack(padx=30, pady=(45, 25))
    tk.Label(
        answer_frame,
        text=question["answer"],
        font=("Segoe UI", 14),
        fg="#2b2b2b",
        bg="#f7f3ee",
        wraplength=560,
        justify="left",
        padx=25,
        pady=25,
    ).pack(fill="x", padx=45, pady=(0, 20))
    ttk.Button(
        answer_frame,
        text="Back to explore",
        command=back_to_questions,
    ).pack(pady=(0, 8))


def display_question_results(results_frame, questions, open_question):
    import tkinter as tk
    from tkinter import ttk

    for child in results_frame.winfo_children():
        child.destroy()

    if not questions:
        tk.Label(
            results_frame,
            text="No questions available.",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#2b2b2b",
        ).pack(pady=15)
    else:
        for item in questions:
            ttk.Button(
                results_frame,
                text=item["question"],
                command=lambda question=item: open_question(question),
            ).pack(fill="x", padx=10, pady=5)
