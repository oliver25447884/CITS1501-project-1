import tkinter as tk
import math
from pathlib import Path
from fractions import Fraction
from tkinter import ttk
from Moduals.Question_Modual import (
    NOONGAR_REGIONS,
    REGION_QUESTIONS,
    display_question_results,
)
from Moduals.Security_Modual import SecurityModule
from Moduals.SeasonWheel import SeasonWheel

REGION_IMAGE_FILES = {
    "Whadjuk": "Whadjuk.png",
    "Yued": "Yued.png",
    "Ballardong": "Ballardong.png",
    "Gnaala Karla Booja": "Gnaala Karla Boodja.png",
    "South West Boojarah": "Southwest Boodjarah.png",
    "Wagyl Kaip & Southern Noongar": "Wagyl Kaip Southern Noongar.png",
}

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


class NoongarSeasonApp:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.season_wheel = SeasonWheel(self)
        self.security = SecurityModule(self)

        self.security.show_startup_page()

    def clear_page(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root, bg="#f4efe7")
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

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
            command=self.season_wheel.show_information_page,
        ).pack()

        region_panel = tk.Frame(content, bg="#f7f3ee", bd=1, relief="solid")
        region_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(
            region_panel,
            text="Questions & answers",
            font=("Segoe UI", 16, "bold"),
            fg="#24381d",
            bg="#f7f3ee",
            wraplength=300,
        ).pack(pady=(25, 12))

        ttk.Button(
            region_panel,
            text="Browse season questions",
            command=self.show_questions_page,
        ).pack(fill="x", padx=20, pady=(0, 12))

        tk.Label(
            region_panel,
            text="Or find your local Noongar region:",
            font=("Segoe UI", 10),
            fg="#4a4a4a",
            bg="#f7f3ee",
        ).pack(anchor="w", padx=20)

        self.region_results = tk.Frame(
            region_panel,
            bg="#ffffff",
            height=12,
        )
        self.region_results.pack(fill="x", padx=20, pady=(4, 12))
        display_question_results(
            self.region_results,
            REGION_QUESTIONS,
            self.show_question_page,
        )

        ttk.Button(
            self.current_frame,
            text="Log out",
            command=self.security.show_login_page,
        ).pack(pady=(12, 0))

    def show_questions_page(self):
        self.clear_page()
        self.root.title("Questions and answers | Noongar Seasons")
        self.root.geometry("850x760")
        self.root.minsize(650, 550)

        tk.Label(
            self.current_frame,
            text="Questions & answers",
            font=("Segoe UI", 22, "bold"),
            fg="#24381d",
            bg="#f4efe7",
        ).pack(pady=(8, 5))
        tk.Label(
            self.current_frame,
            text="Select a question to read its answer.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#f4efe7",
        ).pack(pady=(0, 12))

        list_frame = tk.Frame(self.current_frame, bg="#f4efe7")
        list_frame.pack(fill="both", expand=True, padx=10)
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        canvas = tk.Canvas(
            list_frame,
            bg="#f4efe7",
            highlightthickness=0,
        )
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=canvas.yview,
        )
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

        answer_labels = []

        def resize_questions(event):
            canvas.itemconfigure(questions_window, width=event.width)
            answer_wraplength = max(300, event.width - 90)
            for answer_label in answer_labels:
                answer_label.configure(wraplength=answer_wraplength)

        canvas.bind("<Configure>", resize_questions)

        def scroll_questions(event):
            if getattr(event, "num", None) == 4:
                direction = -1
            elif getattr(event, "num", None) == 5:
                direction = 1
            else:
                direction = -1 if event.delta > 0 else 1
            canvas.yview_scroll(direction, "units")
            return "break"

        def bind_question_scrolling(widget):
            widget.bind("<MouseWheel>", scroll_questions)
            widget.bind("<Button-4>", scroll_questions)
            widget.bind("<Button-5>", scroll_questions)

        bind_question_scrolling(canvas)
        bind_question_scrolling(questions_frame)

        current_section = None
        for item in FAQ_ITEMS:
            if item["season"] != current_section:
                current_section = item["season"]
                tk.Label(
                    questions_frame,
                    text=current_section,
                    font=("Segoe UI", 12, "bold"),
                    fg="#24381d",
                    bg="#f4efe7",
                ).pack(anchor="w", padx=8, pady=(14, 5))

            question_panel = tk.Frame(
                questions_frame,
                bg="#ffffff",
                highlightbackground="#d8c8b4",
                highlightthickness=1,
            )
            question_panel.pack(fill="x", padx=4, pady=3)
            bind_question_scrolling(question_panel)
            answer_label = tk.Label(
                question_panel,
                text=item["answer"],
                font=("Segoe UI", 11),
                fg="#3d453f",
                bg="#ffffff",
                justify="left",
                anchor="w",
                wraplength=650,
            )
            answer_labels.append(answer_label)
            bind_question_scrolling(answer_label)
            button_reference = {}

            def toggle_answer(
                label=answer_label,
                question=item["question"],
                button_reference=button_reference,
            ):
                question_button = button_reference["button"]
                if label.winfo_manager():
                    label.pack_forget()
                    question_button.configure(text=f"+  {question}")
                else:
                    label.pack(fill="x", padx=16, pady=(0, 14))
                    question_button.configure(text=f"-  {question}")

            question_button = ttk.Button(
                question_panel,
                text=f"+  {item['question']}",
                command=toggle_answer,
            )
            button_reference["button"] = question_button
            question_button.pack(fill="x", padx=6, pady=6)
            bind_question_scrolling(question_button)

        ttk.Button(
            self.current_frame,
            text="Back to explore",
            command=self.show_home_page,
        ).pack(pady=(10, 0))

    def show_question_page(self, question):
        self.clear_page()
        self.current_frame.pack_configure(pady=(20, 0))
        self.root.title("Question information")
        self.root.geometry("700x760")
        self.root.minsize(550, 500)

        tk.Label(
            self.current_frame,
            text=question["question"],
            font=("Segoe UI", 20, "bold"),
            fg="#24381d",
            bg="#f4efe7",
            wraplength=600,
            justify="center",
        ).pack(padx=30, pady=(45, 25))

        search_panel = tk.Frame(
            self.current_frame,
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

        image_placeholder = tk.Frame(self.current_frame, bg="#e7d8c4")
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
                        Path(__file__).resolve().parent
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
                result_label.config(text="Council not found in the Noongar council list.")
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
            if image_state["size"] != (event.width, event.height):
                show_region_images(
                    image_state["regions"], image_state["fallback_text"]
                )

        image_placeholder.bind("<Configure>", resize_region_images)

        search_entry.bind("<KeyRelease>", update_region_result)
        search_entry.bind("<Return>", update_region_result)
        search_entry.focus_set()

        ttk.Button(
            self.current_frame,
            text="Back to explore",
            command=self.show_home_page,
        ).pack(pady=(0, 8))
        image_placeholder.pack(fill="both", expand=True, padx=20, pady=0)

    def show_information_page(self):
        self.season_wheel.show_information_page()

    def show_season_page(self, season_name):
        self.season_wheel.show_season_page(season_name)


if __name__ == "__main__":
    root = tk.Tk()
    app = NoongarSeasonApp(root)
    root.mainloop()
