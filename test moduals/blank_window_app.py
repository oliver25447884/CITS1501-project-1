import tkinter as tk


class BlankWindowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("800x500")
        self.root.configure(bg="#f2f2f2")

        self.current_page = None
        self.password = "123"

        # Add or edit question and answer pairs here.
        self.questions = [
            {
                "question": "What are the Noongar seasons?",
                "answer": "Birak, Bunuru, Djeran, Makuru, Djilba, and Kambarang.",
            },
            {
                "question": "What do the Noongar seasons describe?",
                "answer": "They describe changes in weather, plants, and animal activity.",
            },
            {
                "question": "Where is the Noongar seasonal calendar used?",
                "answer": "It is used by the Noongar people of south-western Australia.",
            },
        ]

        self.show_login_page()

    def clear_page(self):
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = tk.Frame(self.root, bg="#f2f2f2")
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def show_login_page(self):
        self.clear_page()

        title = tk.Label(
            self.current_page,
            text="The Noongar Seasons",
            font=("Segoe UI", 20, "bold"),
            bg="#f2f2f2",
            fg="#222222",
        )
        title.pack(pady=(0, 10))

        self.info_label = tk.Label(
            self.current_page,
            text="Enter Password To Continue.",
            font=("Segoe UI", 11),
            bg="#f2f2f2",
            fg="#444444",
            wraplength=600,
            justify="center",
        )
        self.info_label.pack(pady=(0, 10))

        self.password_entry = tk.Entry(
            self.current_page,
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#222222",
            show="*",
            width=30,
        )
        self.password_entry.pack(pady=(0, 10))
        self.password_entry.bind("<Return>", lambda event: self.check_password())

        submit_button = tk.Button(
            self.current_page,
            text="Submit",
            command=self.check_password,
        )
        submit_button.pack()

    def check_password(self):
        entered_password = self.password_entry.get()

        if entered_password == self.password:
            self.show_information_page()
        else:
            self.info_label.config(text="Password incorrect. Try again.")

    def show_information_page(self):
        self.clear_page()
        self.root.title("Information Page")

        title = tk.Label(
            self.current_page,
            text="About the Noongar Seasons",
            font=("Segoe UI", 22, "bold"),
            bg="#f2f2f2",
            fg="#222222",
        )
        title.pack(pady=(0, 20))

        info_text = (
            "The Noongar seasons are a traditional seasonal calendar used by the Noongar people "
            "of south-western Australia.\n\n"
            "These seasons reflect natural changes in weather, plant life, and animal activity.\n\n"
            "Examples include Birak, Bunuru, Djeran, Makuru, Djilba, and Kambarang."
        )

        details = tk.Label(
            self.current_page,
            text=info_text,
            font=("Segoe UI", 11),
            bg="#f2f2f2",
            fg="#333333",
            justify="left",
            wraplength=650,
        )
        details.pack(padx=20, pady=10)

        search_frame = tk.Frame(self.current_page, bg="#f2f2f2")
        search_frame.pack(fill="x", padx=20, pady=(15, 5))

        search_label = tk.Label(
            search_frame,
            text="Search questions:",
            font=("Segoe UI", 11, "bold"),
            bg="#f2f2f2",
            fg="#333333",
        )
        search_label.pack(side="left", padx=(0, 8))

        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#222222",
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda event: self.search_questions())
        self.search_entry.bind("<Return>", lambda event: self.search_questions())

        show_all_button = tk.Button(
            search_frame,
            text="Show all",
            command=self.show_all_questions,
        )
        show_all_button.pack(side="left", padx=(8, 0))

        self.search_results = tk.Text(
            self.current_page,
            height=8,
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#222222",
            wrap="word",
            state="disabled",
        )
        self.search_results.pack(fill="both", expand=True, padx=20, pady=(5, 10))
        self.show_all_questions()

        logout_button = tk.Button(
            self.current_page,
            text="Log out",
            command=self.show_login_page,
        )
        logout_button.pack(pady=20)

    def search_questions(self):
        search_term = self.search_entry.get().strip().lower()
        matching_questions = [
            item
            for item in self.questions
            if search_term in item["question"].lower()
            or search_term in item["answer"].lower()
        ]
        self.display_questions(matching_questions)

    def show_all_questions(self):
        self.search_entry.delete(0, tk.END)
        self.display_questions(self.questions)

    def display_questions(self, questions):
        self.search_results.config(state="normal")
        self.search_results.delete("1.0", tk.END)

        if not questions:
            self.search_results.insert(tk.END, "No matching questions found.")
        else:
            for number, item in enumerate(questions, start=1):
                self.search_results.insert(
                    tk.END,
                    f"{number}. {item['question']}\nAnswer: {item['answer']}\n\n",
                )

        self.search_results.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = BlankWindowApp(root)
    root.mainloop()
