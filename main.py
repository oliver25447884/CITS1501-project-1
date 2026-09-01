import tkinter as tk
from tkinter import ttk


SEASONS = {
    "Birak": {
        "months": "December to January",
        "description": "Birak is the hottest and driest time of the year. It is a season of warmth, long daylight hours, and strong sunshine. The land is often dry and the weather can be very hot.",
        "meaning": "This season marks the height of summer in the Noongar calendar, when people traditionally paid close attention to weather, water, and the changing landscape.",
    },
    "Bunur": {
        "months": "February to March",
        "description": "Bunuru is the second part of summer. It remains warm and can feel very intense, but the weather begins to shift as the season progresses.",
        "meaning": "This time is associated with long hot days, with the landscape beginning to prepare for the cooler months ahead.",
    },
    "Djeran": {
        "months": "April to May",
        "description": "Djeran brings the first cooler weather of the year. Days become milder and the landscape begins to change as autumn settles in.",
        "meaning": "This season is linked with leaves falling, cooler winds, and the start of a time of transition as the land moves from warm to cool.",
    },
    "Makuru": {
        "months": "June to July",
        "description": "Makuru is the wettest part of the year. It brings cooler temperatures, rain, and the strongest winter conditions.",
        "meaning": "This season is closely connected with the colder months, more rainfall, and the deeper seasonal rhythms of the environment.",
    },
    "Djilba": {
        "months": "August to September",
        "description": "Djilba is the time of early spring. The weather becomes less cold and the landscape begins to wake up again.",
        "meaning": "This season signals renewal and the first signs of new growth, as nature starts to become active after winter.",
    },
    "Kambarang": {
        "months": "October to November",
        "description": "Kambarang is a season of flowering and new life. The land is green, vibrant, and full of movement as spring grows stronger.",
        "meaning": "This is a time of growth, abundance, and the return of energy across the environment as the warmer season approaches.",
    },
}


class NoongarSeasonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Noongar Seasons")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)
        self.root.configure(bg="#f4efe7")

        title = tk.Label(
            root,
            text="Noongar Seasons",
            font=("Segoe UI", 24, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
            pady=15,
        )
        title.pack()

        intro = tk.Label(
            root,
            text="The six seasons recognised by Noongar people in the South West of Western Australia.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#f4efe7",
            wraplength=780,
            justify="center",
        )
        intro.pack(pady=(0, 12))

        main_frame = tk.Frame(root, bg="#f4efe7")
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        left_panel = tk.Frame(main_frame, bg="#efe5d6", bd=1, relief="solid")
        left_panel.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(
            left_panel,
            text="Seasons",
            font=("Segoe UI", 12, "bold"),
            bg="#efe5d6",
            padx=12,
            pady=10,
        ).pack(anchor="w")

        self.season_list = tk.Listbox(
            left_panel,
            width=20,
            height=18,
            font=("Segoe UI", 11),
            bg="#fffdfb",
            fg="#1d1d1d",
            selectbackground="#c5d6b7",
            selectforeground="#1d1d1d",
            activestyle="none",
        )
        self.season_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for season_name in SEASONS:
            self.season_list.insert(tk.END, season_name)

        self.season_list.bind("<<ListboxSelect>>", self.update_details)

        right_panel = tk.Frame(main_frame, bg="#f7f3ee", bd=1, relief="solid")
        right_panel.pack(side="left", fill="both", expand=True)

        self.season_name = tk.Label(
            right_panel,
            text="",
            font=("Segoe UI", 20, "bold"),
            bg="#f7f3ee",
            fg="#24381d",
            pady=10,
        )
        self.season_name.pack(anchor="w", padx=20)

        self.season_months = tk.Label(
            right_panel,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg="#f7f3ee",
            fg="#4e5c46",
            anchor="w",
            justify="left",
        )
        self.season_months.pack(anchor="w", padx=20, pady=(0, 10))

        self.description = tk.Label(
            right_panel,
            text="",
            font=("Segoe UI", 11),
            bg="#f7f3ee",
            fg="#2b2b2b",
            justify="left",
            wraplength=500,
            anchor="w",
        )
        self.description.pack(anchor="w", padx=20, pady=(0, 14))

        self.meaning = tk.Label(
            right_panel,
            text="",
            font=("Segoe UI", 10, "italic"),
            bg="#f7f3ee",
            fg="#414141",
            justify="left",
            wraplength=500,
            anchor="w",
        )
        self.meaning.pack(anchor="w", padx=20)

        self.season_list.selection_set(0)
        self.update_details()

        close_button = ttk.Button(root, text="Close", command=root.destroy)
        close_button.pack(pady=(0, 15))

    def update_details(self, event=None):
        selection = self.season_list.curselection()
        if not selection:
            return

        season_name = self.season_list.get(selection[0])
        season = SEASONS[season_name]

        self.season_name.config(text=season_name)
        self.season_months.config(text=f"Months: {season['months']}")
        self.description.config(text=season['description'])
        self.meaning.config(text=f"Meaning: {season['meaning']}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NoongarSeasonApp(root)
    root.mainloop()
