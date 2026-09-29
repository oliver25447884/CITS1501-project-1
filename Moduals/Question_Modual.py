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
    },
]
#An interactive map of perths subburbs will be placed here

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

