import tkinter as tk


class BlankWindowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("800x500")
        self.root.configure(bg="#f2f2f2")

        self.current_page = None
        self.password = "123"

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

        logout_button = tk.Button(
            self.current_page,
            text="Log out",
            command=self.show_login_page,
        )
        logout_button.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = BlankWindowApp(root)
    root.mainloop()
