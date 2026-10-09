import random
import re
import tkinter as tk
from tkinter import ttk

from Moduals.SeasonWheel import SEASONS


ENVIRONMENTAL_SIGNS = {
    "Birak": (
        "Rain eases and hot, dry days lengthen, with morning easterlies and "
        "afternoon sea breezes.",
        "Fledgling birds take flight as reptiles shed their skins.",
    ),
    "Bunuru": (
        "The hottest, driest weather arrives, with little rain and coastal "
        "breezes bringing relief.",
        "White blossoms appear on jarrah, marri, and ghost gums while zamia "
        "cones turn bright red.",
    ),
    "Djeran": (
        "Cooler nights and dewy mornings arrive as the first rains begin.",
        "Red flowers, reddish sheoak foliage, and banksia blooms become "
        "seasonal signs.",
    ),
    "Makuru": (
        "Cold fronts bring the wettest, coldest weather and waterways swell.",
        "Blue and purple flowers appear as the landscape approaches the "
        "next season.",
    ),
    "Djilba": (
        "Cold mornings alternate with warmer days and gentle rains.",
        "The first wildflowers appear, beginning with golden acacia blooms.",
    ),
    "Kambarang": (
        "Warmer spring days bring colourful wildflowers and signal the "
        "approach of hotter weather.",
        "Snakes become active and young birds call for food.",
    ),
}

_SEASON_CHOICES = tuple(SEASONS)


def _make_quiz_items():
    items = []
    for season_name, signs in ENVIRONMENTAL_SIGNS.items():
        for sign in signs:
            items.append(("Environmental signs", sign, season_name))

        for category, key in (("Flora observations", "flora"), ("Fauna observations", "fauna")):
            for example, description in SEASONS[season_name][key]:
                description = re.sub(
                    rf"\b{re.escape(season_name)}'s\b",
                    "this season's",
                    description,
                    flags=re.IGNORECASE,
                )
                description = re.sub(
                    rf"\b{re.escape(season_name)}\b",
                    "this season",
                    description,
                    flags=re.IGNORECASE,
                )
                items.append(
                    (category, f"{example}: {description}", season_name)
                )
    return items


QUIZ_ITEMS = tuple(_make_quiz_items())


def launch_season_quiz(parent):
    quiz_window = tk.Toplevel(parent)
    quiz_window.title("Test Your Knowledge | Noongar Seasons")
    quiz_window.geometry("900x720")
    quiz_window.minsize(700, 520)
    quiz_window.configure(bg="#f4efe7")
    quiz_window.transient(parent)

    tk.Label(
        quiz_window,
        text="Test Your Knowledge",
        font=("Segoe UI", 22, "bold"),
        fg="#24381d",
        bg="#f4efe7",
    ).pack(pady=(16, 5))
    tk.Label(
        quiz_window,
        text=(
            "Match each environmental sign, flora observation, and fauna "
            "observation to its Noongar season."
        ),
        font=("Segoe UI", 11),
        fg="#4a4a4a",
        bg="#f4efe7",
        wraplength=800,
        justify="center",
    ).pack(padx=20, pady=(0, 12))

    quiz_body = tk.Frame(quiz_window, bg="#f4efe7")
    quiz_body.pack(fill="both", expand=True, padx=18)
    quiz_body.rowconfigure(0, weight=1)
    quiz_body.columnconfigure(0, weight=1)

    canvas = tk.Canvas(quiz_body, bg="#f4efe7", highlightthickness=0)
    scrollbar = ttk.Scrollbar(quiz_body, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    questions_frame = tk.Frame(canvas, bg="#f4efe7")
    questions_window = canvas.create_window(
        (0, 0),
        window=questions_frame,
        anchor="nw",
    )
    questions_frame.bind(
        "<Configure>",
        lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
    )
    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(questions_window, width=event.width),
    )

    def scroll_questions(event):
        if getattr(event, "num", None) == 4:
            direction = -1
        elif getattr(event, "num", None) == 5:
            direction = 1
        else:
            direction = -1 if event.delta > 0 else 1
        canvas.yview_scroll(direction, "units")
        return "break"

    def bind_scrolling(widget):
        widget.bind("<MouseWheel>", scroll_questions)
        widget.bind("<Button-4>", scroll_questions)
        widget.bind("<Button-5>", scroll_questions)

    bind_scrolling(canvas)
    bind_scrolling(questions_frame)

    selections = []
    grouped_items = {}
    for category, clue, answer in QUIZ_ITEMS:
        grouped_items.setdefault(category, []).append((clue, answer))

    for category, category_items in grouped_items.items():
        random.shuffle(category_items)
        tk.Label(
            questions_frame,
            text=category,
            font=("Segoe UI", 13, "bold"),
            fg="#24381d",
            bg="#f4efe7",
        ).pack(anchor="w", pady=(10, 5))

        for clue, answer in category_items:
            row = tk.Frame(
                questions_frame,
                bg="#f7f3ee",
                highlightbackground="#d8c8b4",
                highlightthickness=1,
            )
            row.pack(fill="x", pady=3)
            row.columnconfigure(0, weight=1)
            tk.Label(
                row,
                text=clue,
                font=("Segoe UI", 10),
                fg="#2b2b2b",
                bg="#f7f3ee",
                justify="left",
                anchor="w",
                wraplength=560,
            ).grid(row=0, column=0, sticky="ew", padx=10, pady=8)

            selection = tk.StringVar(value="")
            selector = ttk.Combobox(
                row,
                textvariable=selection,
                values=_SEASON_CHOICES,
                state="readonly",
                width=16,
            )
            selector.grid(row=0, column=1, sticky="e", padx=10, pady=8)
            selections.append((selection, answer))
            bind_scrolling(row)
            bind_scrolling(selector)

    feedback = tk.Label(
        quiz_window,
        text="",
        font=("Segoe UI", 12, "bold"),
        fg="#24381d",
        bg="#f4efe7",
    )
    feedback.pack(pady=(8, 0))

    def check_answers():
        if all(selection.get() == answer for selection, answer in selections):
            feedback.configure(text="Good Job", fg="#24381d")
        else:
            feedback.configure(
                text="Some matches are missing or incorrect. Try again.",
                fg="#8b3f2f",
            )

    ttk.Button(
        quiz_window,
        text="Check Answer",
        command=check_answers,
    ).pack(pady=(8, 16))

    return quiz_window
