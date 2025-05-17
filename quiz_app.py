import tkinter as tk
from tkinter import ttk, messagebox
import random
from gui_frames import create_selection_frame, create_quiz_frame, create_feedback_correct_frame, create_feedback_incorrect_frame, create_score_frame
from gemini_api import load_quiz_data # Import the function to load data

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz de Aprendizado")
        self.root.geometry("600x400") # Set a default window size

        self.current_question_index = 0
        self.score = 0
        self.total_questions = 0
        self.hint_shown = False
        self.quiz_data = [] # Store the loaded quiz data

        # References to frames and key widgets managed by this class
        self.selection_frame = None
        self.quiz_frame = None
        self.feedback_correct_frame = None
        self.feedback_incorrect_frame = None
        self.score_frame = None

        self.quiz_subject_label = None # Will be set when quiz frame is created
        self.question_label = None     # Will be set when quiz frame is created
        self.answer_buttons = []     # Will be set when quiz frame is created
        self.hint_label = None         # Will be set when quiz frame is created
        self.final_score_label = None  # Will be set when score frame is created

        self.create_frames()
        self.show_selection_screen()

    def create_frames(self):
        # Create frames using functions from gui_frames.py
        self.selection_frame, selection_widgets = create_selection_frame(self.root,
                                                                         start_quiz_callback=self.start_quiz,
                                                                         grade_values=["5º Ano", "6º Ano", "7º Ano", "8º Ano", "9º Ano"])
        self.grade_var = selection_widgets['grade_var']
        self.topic_entry = selection_widgets['topic_entry']

        self.quiz_frame, quiz_widgets = create_quiz_frame(self.root,
                                                        check_answer_callback=self.check_answer,
                                                        show_hint_callback=self.show_hint,
                                                        next_question_callback=self.next_question,
                                                        end_quiz_callback=self.end_quiz)
        self.quiz_subject_label = quiz_widgets['quiz_subject_label']
        self.question_label = quiz_widgets['question_label']
        self.answer_buttons = quiz_widgets['answer_buttons']
        self.hint_label = quiz_widgets['hint_label']

        self.feedback_correct_frame, feedback_correct_widgets = create_feedback_correct_frame(self.root,
                                                                                             next_question_callback=self.next_question)
        # You might want to store references to labels in feedback frames if you need to update them dynamically

        self.feedback_incorrect_frame, feedback_incorrect_widgets = create_feedback_incorrect_frame(self.root,
                                                                                                   next_question_callback=self.next_question)
         # You might want to store references to labels in feedback frames

        self.score_frame, score_widgets = create_score_frame(self.root,
                                                            quit_callback=self.root.quit)
        self.final_score_label = score_widgets['final_score_label']


    def show_selection_screen(self):
        self.hide_all_frames()
        self.selection_frame.pack(expand=True, fill="both") # Use pack with expand/fill

    def show_quiz_screen(self):
        self.hide_all_frames()
        self.quiz_frame.pack(expand=True, fill="both")
        self.display_question()

    def show_feedback_correct_screen(self):
        self.hide_all_frames()
        self.feedback_correct_frame.pack(expand=True, fill="both")
        # Update feedback screen content (copy from quiz screen)
        # In a real app, you'd need to pass the current question data or update labels more robustly
        # For this example, we'll manually update some labels based on the state
        self.feedback_correct_frame.children['!label'].config(text=self.quiz_subject_label["text"]) # Subject
        self.feedback_correct_frame.children['!label2'].config(text=self.question_label["text"]) # Question


    def show_feedback_incorrect_screen(self, selected_answer_key):
        self.hide_all_frames()
        self.feedback_incorrect_frame.pack(expand=True, fill="both")
        # Update feedback screen content
        self.feedback_incorrect_frame.children['!label'].config(text=self.quiz_subject_label["text"]) # Subject
        self.feedback_incorrect_frame.children['!label2'].config(text=self.question_label["text"]) # Question
        # Update the "Errou" label with the selected answer
        # Note: This assumes a specific label order/name, better to store references in create_feedback_incorrect_frame
        feedback_incorrect_labels = self.feedback_incorrect_frame.winfo_children()
        # Find the label that starts with a letter (A, B, C, D, E)
        for child in feedback_incorrect_labels:
            if isinstance(child, tk.Label) and child.cget("text").startswith(('A)', 'B)', 'C)', 'D)', 'E)')):
                 # This is a simplification; ideally, you'd have references to all option labels
                 # We just update the first one for demonstration
                 if child.cget("text").startswith(f'{selected_answer_key})'):
                     child.config(text=f"{selected_answer_key}) Errou", fg="red")
                 # Reset other options to default appearance if needed


    def show_score_screen(self):
        self.hide_all_frames()
        self.final_score_label.config(text=f"Você acertou {self.score} de {self.total_questions} perguntas.")
        self.score_frame.pack(expand=True, fill="both")


    def hide_all_frames(self):
        for frame in [self.selection_frame, self.quiz_frame, self.feedback_correct_frame, self.feedback_incorrect_frame, self.score_frame]:
            if frame: # Check if frame exists
                frame.pack_forget()

    def start_quiz(self):
        grade = self.grade_var.get()
        topic = self.topic_entry.get().strip()

        if not topic or topic == "Ex: Matemática ou 'Advérbios de lugar'":
            messagebox.showwarning("Aviso", "Por favor, digite a matéria ou tema.")
            return

        # Use the function from gemini_api.py to load/generate quiz data
        self.quiz_data = load_quiz_data(grade, topic)
        if not self.quiz_data:
            messagebox.showinfo("Info", "Não foi possível carregar perguntas para o tema/série selecionado. Tente outro tema.")
            return

        self.current_question_index = 0
        self.score = 0
        self.total_questions = len(self.quiz_data)
        self.hint_shown = False
        self.quiz_subject_label.config(text=f"{grade} - {topic.title()}") # Update subject label in quiz frame
        self.show_quiz_screen()

    def display_question(self):
        if self.current_question_index < len(self.quiz_data):
            question_data = self.quiz_data[self.current_question_index]

            # --- Basic Validation Check (based on placeholder validation) ---
            # In a real app with API validation, you'd check question_data["validation"]
            if not question_data.get("validation", {}).get("curricular", False) or not question_data.get("validation", {}).get("answers_hints", False):
                 print(f"Skipping invalid question: {question_data['question']}")
                 self.next_question() # Skip this question and go to the next
                 return
            # --- End Validation Check ---

            self.question_label.config(text=question_data["question"])

            options = question_data["options"]
            # Update the text and state of the answer buttons
            for btn, option_key in zip(self.answer_buttons, options.keys()):
                 btn.config(text=f"{option_key}) {options[option_key]}", state="normal") # Enable buttons

            self.hint_label.config(text="") # Clear previous hint
            self.hint_shown = False # Reset hint state
            self.hint_label.pack_forget() # Hide hint initially


        else:
            self.end_quiz()

    def check_answer(self, selected_option_key):
        current_question = self.quiz_data[self.current_question_index]
        correct_answer_key = current_question["correct_answer"]

        if selected_option_key == correct_answer_key:
            self.score += 1
            self.show_feedback_correct_screen()
        else:
            self.show_feedback_incorrect_screen(selected_option_key)

        # Disable answer buttons after selection
        for btn in self.answer_buttons:
            btn.config(state="disabled")


    def show_hint(self):
        if not self.hint_shown:
            current_question = self.quiz_data[self.current_question_index]
            self.hint_label.config(text="Dica: " + current_question.get("hint", "Sem dica disponível."))
            # Re-pack the hint label
            if not self.hint_label.winfo_ismapped(): # Check if it's not already packed
                 self.hint_label.pack(pady=5)
            self.hint_shown = True

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.quiz_data):
            self.show_quiz_screen()
        else:
            self.end_quiz()

    def end_quiz(self):
        self.total_questions = len(self.quiz_data) # Ensure total questions is correct
        self.show_score_screen()