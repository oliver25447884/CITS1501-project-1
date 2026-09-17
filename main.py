import tkinter as tk
import math
from tkinter import ttk
from Moduals.Question_Modual import (
    REGION_QUESTIONS,
    display_question_results,
)


SEASONS = {
    "Birak": {
        "months": "December to January",
        "description": "Birak is the hottest and driest time of the year. It is a season of warmth, long daylight hours, and strong sunshine. The land is often dry and the weather can be very hot.",
        "meaning": "This season marks the height of summer in the Noongar calendar, when people traditionally paid close attention to weather, water, and the changing landscape.",
    },
    "Bunuru": {
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
        self.root.title("Login")
        self.root.geometry("500x350")
        self.root.minsize(400, 250)
        self.root.configure(bg="#f4efe7")
        self.password = "123"
        self.current_frame = None

        self.show_login_page()

    def clear_page(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg="#f4efe7")
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_login_page(self):
        self.clear_page()
        self.root.title("Login")
        self.root.geometry("500x350")

        title = tk.Label(
            self.current_frame,
            text="The Noongar Seasons",
            font=("Segoe UI", 22, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
        )
        title.pack(pady=(0, 10))

        self.info_label = tk.Label(
            self.current_frame,
            text="Enter password to continue.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#f4efe7",
            wraplength=350,
            justify="center",
        )
        self.info_label.pack(pady=(0, 10))

        self.password_entry = tk.Entry(
            self.current_frame,
            font=("Segoe UI", 11),
            show="*",
            width=30,
        )
        self.password_entry.pack(pady=(0, 10))
        self.password_entry.bind("<Return>", lambda event: self.check_password())

        submit_button = ttk.Button(
            self.current_frame,
            text="Submit",
            command=self.check_password,
        )
        submit_button.pack()

    def check_password(self):
        entered_password = self.password_entry.get()

        if entered_password == self.password:
            self.show_home_page()
        else:
            self.info_label.config(text="Password incorrect. Please try again.")

    def show_home_page(self):
        self.clear_page()
        self.root.title("Explore Noongar Seasons")
        self.root.geometry("850x550")
        self.root.minsize(700, 500)

        tk.Label(
            self.current_frame,
            text="Explore the Noongar Seasons",
            font=("Segoe UI", 24, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
        ).pack(pady=(10, 8))

        tk.Label(
            self.current_frame,
            text="Choose an activity below to learn more.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#f4efe7",
        ).pack(pady=(0, 18))

        content = tk.Frame(self.current_frame, bg="#f4efe7")
        content.pack(fill="both", expand=True, padx=10)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        seasons_panel = tk.Frame(content, bg="#e7d8c4", bd=1, relief="solid")
        seasons_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(
            seasons_panel,
            text="Explore the Noongar Seasons",
            font=("Segoe UI", 16, "bold"),
            fg="#24381d",
            bg="#e7d8c4",
            wraplength=300,
        ).pack(pady=(55, 15))
        tk.Label(
            seasons_panel,
            text="Visit the wheel of seasons and select a season to learn more.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#e7d8c4",
            wraplength=300,
            justify="center",
        ).pack(padx=25, pady=(0, 25))
        ttk.Button(
            seasons_panel,
            text="Open wheel of seasons",
            command=self.show_information_page,
        ).pack()

        region_panel = tk.Frame(content, bg="#f7f3ee", bd=1, relief="solid")
        region_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(
            region_panel,
            text="Explore some questions",
            font=("Segoe UI", 16, "bold"),
            fg="#24381d",
            bg="#f7f3ee",
            wraplength=300,
        ).pack(pady=(25, 12))

        self.region_results = tk.Frame(
            region_panel,
            bg="#ffffff",
            height=12,
        )
        self.region_results.pack(fill="both", expand=True, padx=20, pady=12)
        display_question_results(
            self.region_results,
            REGION_QUESTIONS,
            self.show_question_page,
        )

        ttk.Button(
            self.current_frame,
            text="Log out",
            command=self.show_login_page,
        ).pack(pady=(12, 0))

    def show_question_page(self, question):
        self.clear_page()
        self.root.title("Question information")
        self.root.geometry("700x500")
        self.root.minsize(550, 400)

        tk.Label(
            self.current_frame,
            text=question["question"],
            font=("Segoe UI", 20, "bold"),
            fg="#24381d",
            bg="#f4efe7",
            wraplength=600,
            justify="center",
        ).pack(padx=30, pady=(45, 25))

        answer_panel = tk.Frame(
            self.current_frame,
            bg="#f7f3ee",
            bd=1,
            relief="solid",
        )
        answer_panel.pack(fill="both", expand=True, padx=45, pady=(0, 25))

        tk.Label(
            answer_panel,
            text=question["answer"],
            font=("Segoe UI", 13),
            fg="#2b2b2b",
            bg="#f7f3ee",
            wraplength=540,
            justify="left",
        ).pack(anchor="w", padx=30, pady=35)

        ttk.Button(
            self.current_frame,
            text="Back to explore",
            command=self.show_home_page,
        ).pack(pady=(0, 20))

    def show_information_page(self):
        self.clear_page()
        self.root.title("Wheel of Noongar Seasons")
        self.root.geometry("850x650")
        self.root.minsize(700, 600)

        title = tk.Label(
            self.current_frame,
            text="Noongar Seasons",
            font=("Segoe UI", 24, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
            pady=15,
        )
        title.pack()

        intro = tk.Label(
            self.current_frame,
            text="The six seasons recognised by Noongar people in the South West of Western Australia.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#f4efe7",
            wraplength=780,
            justify="center",
        )
        intro.pack(pady=(0, 12))

        canvas = tk.Canvas(
            self.current_frame,
            width=500,
            height=470,
            bg="#f4efe7",
            highlightthickness=0,
        )
        canvas.pack(padx=20, pady=(0, 5))

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
            canvas.tag_bind(arc_tag, "<Button-1>", lambda event, name=season_name: self.show_season_page(name))

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

        ttk.Button(
            self.current_frame,
            text="Back to explore",
            command=self.show_home_page,
        ).pack(pady=(0, 15))

    def show_season_page(self, season_name):
        self.clear_page()
        self.root.title(f"{season_name} | Noongar Seasons")
        self.root.geometry("700x500")

        season = SEASONS[season_name]

        tk.Label(
            self.current_frame,
            text=season_name,
            font=("Segoe UI", 26, "bold"),
            bg="#f4efe7",
            fg="#24381d",
        ).pack(pady=(25, 8))
        tk.Label(
            self.current_frame,
            text=f"Months: {season['months']}",
            font=("Segoe UI", 12, "bold"),
            bg="#f4efe7",
            fg="#4e5c46",
        ).pack(pady=(0, 25))

        detail_panel = tk.Frame(self.current_frame, bg="#f7f3ee", bd=1, relief="solid")
        detail_panel.pack(fill="both", expand=True, padx=45, pady=(0, 25))
        tk.Label(
            detail_panel,
            text=season["description"],
            font=("Segoe UI", 12),
            bg="#f7f3ee",
            fg="#2b2b2b",
            wraplength=540,
            justify="left",
        ).pack(anchor="w", padx=25, pady=(30, 20))
        tk.Label(
            detail_panel,
            text=f"Meaning: {season['meaning']}",
            font=("Segoe UI", 11, "italic"),
            bg="#f7f3ee",
            fg="#414141",
            wraplength=540,
            justify="left",
        ).pack(anchor="w", padx=25)

        ttk.Button(
            self.current_frame,
            text="Back to seasons",
            command=self.show_information_page,
        ).pack(pady=(0, 20))


if __name__ == "__main__":
    root = tk.Tk()
    app = NoongarSeasonApp(root)
    root.mainloop()
