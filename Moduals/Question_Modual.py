# Add or edit region questions and answers in this list.
REGION_QUESTIONS = [
    {
        "question": "What Noongar region do I live in if I live in Perth?",
        "answer": "Perth is generally part of the Whadjuk Noongar region.",
    },
]


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
