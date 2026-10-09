import hashlib
import hmac
import json
import subprocess
import sys
import secrets
import tkinter as tk
from pathlib import Path
from tkinter import ttk


SECURITY_QUESTIONS = (
    "Who is my favourite professor?",
    "What is my favourite book?",
    "What is my favourite animal?",
)
PASSWORD_MAX_LENGTH = 6
ANSWER_MAX_LENGTH = 20
HASH_ITERATIONS = 200_000


def _create_secret_record(secret):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        secret.encode("utf-8"),
        salt,
        HASH_ITERATIONS,
    )
    return {"salt": salt.hex(), "hash": digest.hex()}


def _verify_secret(secret, record):
    try:
        salt = bytes.fromhex(record["salt"])
        expected_hash = record["hash"]
        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            secret.encode("utf-8"),
            salt,
            HASH_ITERATIONS,
        ).hex()
    except (KeyError, TypeError, ValueError):
        return False
    return hmac.compare_digest(actual_hash, expected_hash)


class SecurityModule:
    def __init__(self, app, credentials_path=None):
        self.app = app
        self.credentials_path = Path(
            credentials_path
            if credentials_path is not None
            else Path.home() / ".noongar_seasons_security.json"
        )
        self.credentials = self._load_credentials()
        self.info_label = None
        self.password_entry = None

    def _load_credentials(self):
        try:
            credentials = json.loads(self.credentials_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

        if not isinstance(credentials, dict):
            return None
        password_record = credentials.get("password")
        answer_records = credentials.get("answers")
        if not isinstance(password_record, dict) or not isinstance(answer_records, list):
            return None
        if len(answer_records) != len(SECURITY_QUESTIONS):
            return None
        if any(
            not isinstance(record, dict)
            or not isinstance(record.get("salt"), str)
            or not isinstance(record.get("hash"), str)
            for record in [password_record, *answer_records]
        ):
            return None
        return credentials

    def _save_credentials(self, credentials):
        self.credentials_path.write_text(
            json.dumps(credentials),
            encoding="utf-8",
        )

    def show_startup_page(self):
        if self.credentials is None:
            self.show_create_password_page()
        else:
            self.show_login_page()

    def _prepare_root(self, title, geometry, minimum_size):
        self.app.root.title(title)
        self.app.set_windowed_size(geometry, minimum_size)
        self.app.root.configure(bg="#f4efe7")

    def _password_within_limit(self, proposed_value):
        return len(proposed_value) <= PASSWORD_MAX_LENGTH

    def _answer_within_limit(self, proposed_value):
        return len(proposed_value) <= ANSWER_MAX_LENGTH

    def _create_password_entry(self, parent):
        return tk.Entry(
            parent,
            font=("Segoe UI", 11),
            show="*",
            width=30,
            validate="key",
            validatecommand=(
                self.app.root.register(self._password_within_limit),
                "%P",
            ),
        )

    def _create_answer_entries(self, parent):
        entries = []
        validate_command = (
            self.app.root.register(self._answer_within_limit),
            "%P",
        )
        for question in SECURITY_QUESTIONS:
            tk.Label(
                parent,
                text=question,
                font=("Segoe UI", 10, "bold"),
                fg="#24381d",
                bg="#f4efe7",
                anchor="w",
                wraplength=460,
            ).pack(fill="x", pady=(8, 2))
            answer_entry = tk.Entry(
                parent,
                font=("Segoe UI", 11),
                width=38,
                validate="key",
                validatecommand=validate_command,
            )
            answer_entry.pack(fill="x")
            entries.append(answer_entry)
        return entries

    def _set_status(self, status_label, message):
        status_label.config(text=message)

    def show_create_password_page(self):
        self.app.clear_page()
        self._prepare_root("Create password", "600x700", (520, 600))

        tk.Label(
            self.app.current_frame,
            text="Create password",
            font=("Segoe UI", 22, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
        ).pack(pady=(0, 8))
        tk.Label(
            self.app.current_frame,
            text="Choose a password of up to 6 characters and answer all three questions.",
            font=("Segoe UI", 10),
            fg="#4a4a4a",
            bg="#f4efe7",
            wraplength=460,
            justify="center",
        ).pack(pady=(0, 12))

        tk.Label(
            self.app.current_frame,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            fg="#24381d",
            bg="#f4efe7",
        ).pack(anchor="w", padx=20)
        password_entry = self._create_password_entry(self.app.current_frame)
        password_entry.pack(fill="x", padx=20, pady=(2, 6))

        answer_entries = self._create_answer_entries(self.app.current_frame)
        status_label = tk.Label(
            self.app.current_frame,
            text="",
            font=("Segoe UI", 10),
            fg="#9a3e32",
            bg="#f4efe7",
            wraplength=460,
        )
        status_label.pack(pady=(8, 4))
        ttk.Button(
            self.app.current_frame,
            text="Save password",
            command=lambda: self._create_credentials(
                password_entry,
                answer_entries,
                status_label,
            ),
        ).pack(pady=(2, 8))
        password_entry.focus_set()

    def _create_credentials(self, password_entry, answer_entries, status_label):
        password = password_entry.get()
        answers = [entry.get().strip() for entry in answer_entries]
        if not password:
            self._set_status(status_label, "Enter a password to continue.")
            return
        if not all(answers):
            self._set_status(status_label, "Answer all three security questions.")
            return
        credentials = {
            "password": _create_secret_record(password),
            "answers": [
                _create_secret_record(answer.casefold()) for answer in answers
            ],
        }
        try:
            self._save_credentials(credentials)
        except OSError:
            self._set_status(status_label, "Could not save your security details.")
            return
        self.credentials = credentials
        self.show_login_page()

    def show_login_page(self):
        self.app.clear_page()
        self._prepare_root("Login", "500x390", (420, 330))

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
        ).pack(pady=(0, 6))
        ttk.Button(
            self.app.current_frame,
            text="Forgot password?",
            command=self.show_forgot_password_window,
        ).pack()
        self.password_entry.focus_set()

    def check_password(self):
        entered_password = self.password_entry.get()

        if _verify_secret(entered_password, self.credentials["password"]):
            self._play_login_sound(True)
            self.app.show_home_page()
        else:
            self._play_login_sound(False)
            self.password_entry.delete(0, tk.END)
            self.info_label.config(text="Password incorrect. Please try again.")
            self.password_entry.focus_set()

    def _play_login_sound(self, succeeded):
        try:
            if sys.platform == "darwin":
                sound_name = "Glass.aiff" if succeeded else "Basso.aiff"
                subprocess.Popen(
                    ["afplay", f"/System/Library/Sounds/{sound_name}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            elif sys.platform.startswith("win"):
                import winsound

                sound = winsound.MB_OK if succeeded else winsound.MB_ICONHAND
                winsound.MessageBeep(sound)
            else:
                self.app.root.bell()
        except (AttributeError, OSError):
            self.app.root.bell()

    def show_forgot_password_window(self):
        if self.credentials is None:
            self.show_create_password_page()
            return

        window = tk.Toplevel(self.app.root)
        window.title("Forgot password")
        window.geometry("560x530")
        window.transient(self.app.root)
        window.configure(bg="#f4efe7")
        window.grab_set()

        tk.Label(
            window,
            text="Verify your security answers",
            font=("Segoe UI", 18, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
        ).pack(pady=(18, 10))
        answer_entries = self._create_answer_entries(window)
        status_label = tk.Label(
            window,
            text="",
            font=("Segoe UI", 10),
            fg="#9a3e32",
            bg="#f4efe7",
            wraplength=460,
        )
        status_label.pack(pady=(10, 4))
        ttk.Button(
            window,
            text="Verify answers",
            command=lambda: self._verify_recovery_answers(
                answer_entries,
                window,
                status_label,
            ),
        ).pack(pady=(2, 12))
        answer_entries[0].focus_set()

    def _verify_recovery_answers(self, answer_entries, window, status_label):
        answers = [entry.get().strip() for entry in answer_entries]
        if not all(answers):
            self._set_status(status_label, "Answer all three security questions.")
            return

        stored_answers = self.credentials["answers"]
        answers_match = all(
            _verify_secret(answer.casefold(), record)
            for answer, record in zip(answers, stored_answers)
        )
        if not answers_match:
            self._set_status(status_label, "One or more answers are incorrect.")
            return
        self._show_new_password_form(window)

    def _show_new_password_form(self, window):
        for child in window.winfo_children():
            child.destroy()
        window.title("Create new password")
        window.geometry("500x350")

        tk.Label(
            window,
            text="Create new password",
            font=("Segoe UI", 18, "bold"),
            fg="#2b2b2b",
            bg="#f4efe7",
        ).pack(pady=(24, 12))

        password_entry = self._create_password_entry(window)
        password_entry.pack(pady=(0, 10))
        password_entry.focus_set()

        confirm_entry = self._create_password_entry(window)
        confirm_entry.pack(pady=(0, 10))
        status_label = tk.Label(
            window,
            text="Enter and confirm a password of up to 6 characters.",
            font=("Segoe UI", 10),
            fg="#4a4a4a",
            bg="#f4efe7",
            wraplength=420,
        )
        status_label.pack(pady=(4, 10))
        ttk.Button(
            window,
            text="Set new password",
            command=lambda: self._save_new_password(
                password_entry,
                confirm_entry,
                window,
                status_label,
            ),
        ).pack()

    def _save_new_password(self, password_entry, confirm_entry, window, status_label):
        password = password_entry.get()
        if not password:
            self._set_status(status_label, "Enter a new password.")
            return
        if password != confirm_entry.get():
            self._set_status(status_label, "The passwords do not match.")
            return

        credentials = dict(self.credentials)
        credentials["password"] = _create_secret_record(password)
        try:
            self._save_credentials(credentials)
        except OSError:
            self._set_status(status_label, "Could not save your new password.")
            return

        self.credentials = credentials
        window.destroy()
        self.show_login_page()
