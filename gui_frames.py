import tkinter as tk
from tkinter import ttk

def create_selection_frame(parent, start_quiz_callback, grade_values):
    """Creates the selection screen frame."""
    frame = tk.Frame(parent)

    tk.Label(frame, text="Quiz de Aprendizado", font=("Arial", 16)).pack(pady=20)
    tk.Label(frame, text="Selecione sua Série:", font=("Arial", 12)).pack()

    grade_var = tk.StringVar()
    grade_combobox = ttk.Combobox(frame, textvariable=grade_var, values=grade_values, state="readonly")
    grade_combobox.pack(pady=5)
    grade_combobox.current(0) # Set default

    tk.Label(frame, text="Digite a matéria ou tema:", font=("Arial", 12)).pack()
    topic_entry = tk.Entry(frame, width=40)
    topic_entry.insert(0, "") # Placeholder text
    topic_entry.pack(pady=5)
    tk.Label(frame, text="Ex: Matemática ou 'Advérbios de lugar'", font=("Arial", 10)).pack()

    tk.Button(frame, text="Iniciar Quiz", command=start_quiz_callback).pack(pady=20)

    return frame, {'grade_var': grade_var, 'topic_entry': topic_entry}

def create_quiz_frame(parent, check_answer_callback, show_hint_callback, next_question_callback, end_quiz_callback):
    """Creates the quiz question display frame."""
    frame = tk.Frame(parent)

    quiz_subject_label = tk.Label(frame, text="", font=("Arial", 14, "bold"))
    quiz_subject_label.pack(pady=10)
    question_label = tk.Label(frame, text="", font=("Arial", 12), wraplength=400)
    question_label.pack(pady=10)

    answer_buttons = []
    option_keys = ["A", "B", "C", "D", "E"]
    for option in option_keys:
        btn = ttk.Button(frame, text=f"{option}) ", command=lambda opt=option: check_answer_callback(opt))
        btn.pack(fill="x", padx=50, pady=2)
        answer_buttons.append(btn)

    button_frame = tk.Frame(frame) # Frame to hold the bottom buttons
    button_frame.pack(pady=10)

    hint_button = ttk.Button(button_frame, text="Dica", command=show_hint_callback)
    hint_button.pack(side="left", padx=10)
    nao_sei_button = ttk.Button(button_frame, text="Não Sei", command=next_question_callback)
    nao_sei_button.pack(side="left", padx=10)
    sair_button = ttk.Button(button_frame, text="Sair", command=end_quiz_callback)
    sair_button.pack(side="left", padx=10)

    hint_label = tk.Label(frame, text="", font=("Arial", 10, "italic"), fg="gray")
    # Hint label is not packed initially

    return frame, {
        'quiz_subject_label': quiz_subject_label,
        'question_label': question_label,
        'answer_buttons': answer_buttons,
        'hint_label': hint_label
    }

def create_feedback_correct_frame(parent, next_question_callback):
    """Creates the feedback frame for a correct answer."""
    frame = tk.Frame(parent)

    # Placeholder labels - content will be set dynamically in QuizApp
    tk.Label(frame, text="", font=("Arial", 14, "bold")).pack(pady=10) # Subject
    tk.Label(frame, text="", font=("Arial", 12), wraplength=400).pack(pady=10) # Question
    tk.Label(frame, text="A) ACERTOU!", font=("Arial", 12), fg="green").pack(fill="x", padx=50, pady=2)
    for i in range(4): # Placeholders for other options
        tk.Label(frame, text=f"{chr(66+i)}) Possível Resposta de até uma linha...", fg="gray").pack(fill="x", padx=50, pady=2)

    ttk.Button(frame, text="Próxima Pergunta", command=next_question_callback).pack(pady=20)

    return frame, {} # Return frame and an empty dict for widgets (update logic is in QuizApp)


def create_feedback_incorrect_frame(parent, next_question_callback):
    """Creates the feedback frame for an incorrect answer."""
    frame = tk.Frame(parent)

     # Placeholder labels - content will be set dynamically in QuizApp
    tk.Label(frame, text="", font=("Arial", 14, "bold")).pack(pady=10) # Subject
    tk.Label(frame, text="", font=("Arial", 12), wraplength=400).pack(pady=10) # Question
    tk.Label(frame, text="A) Errou", font=("Arial", 12), fg="red").pack(fill="x", padx=50, pady=2) # This will be updated
    for i in range(4): # Placeholders for other options
         tk.Label(frame, text=f"{chr(66+i)}) Possível Resposta de até uma linha...", fg="gray").pack(fill="x", padx=50, pady=2)

    ttk.Button(frame, text="Próxima Pergunta", command=next_question_callback).pack(pady=20)

    return frame, {} # Return frame and an empty dict for widgets

def create_score_frame(parent, quit_callback):
    """Creates the final score display frame."""
    frame = tk.Frame(parent)

    tk.Label(frame, text="Quiz Finalizado!", font=("Arial", 16)).pack(pady=20)
    final_score_label = tk.Label(frame, text="", font=("Arial", 12))
    final_score_label.pack(pady=10)
    ttk.Button(frame, text="Sair", command=quit_callback).pack(pady=20)

    return frame, {'final_score_label': final_score_label}