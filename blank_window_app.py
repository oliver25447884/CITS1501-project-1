import tkinter as tk


class BlankWindowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blank Window App")
        self.root.geometry("800x500")
        self.root.configure(bg="#f2f2f2")

        # Main container
        self.main_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Example label - replace or delete this as needed
        self.title_label = tk.Label(
            self.main_frame,
            text="The Noongar Seasons",
            font=("Segoe UI", 20, "bold"),
            bg="#f2f2f2",
            fg="#222222",
        )
        self.title_label.pack(pady=(0, 10))

        # Example text box or widget placeholder
        self.info_label = tk.Label(
            self.main_frame,
            text="Enter Password To Continue.",
            font=("Segoe UI", 11),
            bg="#f2f2f2",
            fg="#444444",
            wraplength=600,
            justify="center",
        )
        self.info_label.pack(pady=(0, 10))

        self.password_entry = tk.Entry(
            self.main_frame,
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#222222",
            show="*",
            width=30,
        )
        self.password_entry.pack(pady=(0, 10))

        self.submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            command=self.check_password,
        )
        self.submit_button.pack()

    def check_password(self):
        password = self.password_entry.get()
        if password == "123":
            self.info_label.config(text="Password correct!")
            self.info_label.config(text="Password correct! You can now access the app.")
        else:
            self.info_label.config(text="Password incorrect")


if __name__ == "__main__":
    root = tk.Tk()
    app = BlankWindowApp(root)
    root.mainloop()
