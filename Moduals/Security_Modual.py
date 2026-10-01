import tkinter as tk
from tkinter import ttk


PASSWORD = "123"


def validate_password(entered_password):
    return entered_password == PASSWORD


class SecurityModule:
    def __init__(self, app):
        self.app = app
        self.info_label = None
        self.password_entry = None

    def show_login_page(self):
        self.app.clear_page()
        self.app.root.title("Login")
        self.app.root.geometry("500x350")
        self.app.root.minsize(400, 250)
        self.app.root.configure(bg="#f4efe7")

        tk.Label(
            self.app.current_frame,
            text="The Noongar Seasons",
            font=("Segoe UI", 22, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
        ).pack(pady=(0, 10))

        self.info_label = tk.Label(
            self.app.current_frame,
            text="Enter password to continue.",
            font=("Segoe UI", 11),
            fg="#4a4a4a",
            bg="#f4efe7",
            wraplength=350,
            justify="center",
        )
        self.info_label.pack(pady=(0, 10))

        self.password_entry = tk.Entry(
            self.app.current_frame,
            font=("Segoe UI", 11),
            show="*",
            width=30,
        )
        self.password_entry.pack(pady=(0, 10))
        self.password_entry.bind("<Return>", lambda event: self.check_password())

        ttk.Button(
            self.app.current_frame,
            text="Submit",
            command=self.check_password,
        ).pack()

    def check_password(self):
        entered_password = self.password_entry.get()

        if validate_password(entered_password):
            self.app.show_home_page()
        else:
            self.info_label.config(text="Password incorrect. Please try again.")