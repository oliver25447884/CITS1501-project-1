# Add or edit region questions and answers in this list.
REGION_QUESTIONS = [
    {
        "question": "What Noongar region do I live in if I live in Perth?",
        "answer": "Perth is generally part of the Whadjuk Noongar region.",
    },
]


def search_questions(search_term):
    search_term = search_term.strip().lower()
    return [
        item
        for item in REGION_QUESTIONS
        if search_term in item["question"].lower()
        or search_term in item["answer"].lower()
    ]


def display_question_results(results_widget, questions, parent_window):
    results_widget.config(state="normal")
    results_widget.delete("1.0", "end")

    if not questions:
        results_widget.insert("end", "No matching questions found.")
    else:
        for index, item in enumerate(questions):
            tag_name = f"question_{index}"
            start_index = results_widget.index("end")
            results_widget.insert("end", item["question"])
            end_index = results_widget.index("end")
            results_widget.tag_add(tag_name, start_index, end_index)
            results_widget.tag_configure(
                tag_name,
                foreground="#2d6682",
                underline=True,
            )
            results_widget.tag_bind(
                tag_name,
                "<Button-1>",
                lambda event, question=item: show_question_answer(
                    parent_window, question
                ),
            )
            results_widget.insert("end", "\n\n")

    results_widget.config(state="disabled")


def show_question_answer(parent_window, question):
    import tkinter as tk
    from tkinter import ttk

    answer_window = tk.Toplevel(parent_window)
    answer_window.title("Question information")
    answer_window.geometry("500x280")
    answer_window.configure(bg="#f4efe7")
    answer_window.transient(parent_window)

    tk.Label(
        answer_window,
        text=question["question"],
        font=("Segoe UI", 15, "bold"),
        fg="#24381d",
        bg="#f4efe7",
        wraplength=430,
        justify="center",
    ).pack(padx=25, pady=(30, 18))
    tk.Label(
        answer_window,
        text=question["answer"],
        font=("Segoe UI", 12),
        fg="#2b2b2b",
        bg="#f4efe7",
        wraplength=430,
        justify="left",
    ).pack(padx=25, pady=(0, 25))
    ttk.Button(answer_window, text="Close", command=answer_window.destroy).pack()
