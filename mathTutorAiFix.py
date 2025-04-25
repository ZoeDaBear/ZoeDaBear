import winsound
import json
import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sympy as sp
from math import isclose
import time
import os

class MathTutorAI:
    """
    A mathematics tutoring AI that generates and explains math problems
    of varying difficulty for different grade levels.
    Tracks user progress, provides hints, and supports multiple languages.
    """

    def __init__(self):
        """Initialize the MathTutorAI with default settings."""
        self.operations = ['+', '-', '*', '/']
        self.grade_level = 0
        self.difficulty = 'Easy'  # Default difficulty
        self.correct_answers = 0
        self.total_questions = 0
        self.start_time = None
        self.language = 'en'  # Default language

    def set_grade_level(self, grade):
        """Set the grade level for problem generation."""
        self.grade_level = grade

    def set_difficulty(self, difficulty):
        """Set the difficulty level for problem generation."""
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            raise ValueError("Difficulty must be 'Easy', 'Medium', or 'Hard'")
        self.difficulty = difficulty

    def set_language(self, language):
        """Set the language for the AI."""
        supported_languages = ['en', 'es', 'fr']
        if language not in supported_languages:
            raise ValueError(f"Language must be one of {supported_languages}")
        self.language = language

    def start_timer(self):
        """Start the timer."""
        self.start_time = time.time()

    def stop_timer(self):
        """Stop the timer and return the elapsed time."""
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

    def generate_problem(self):
        """Generate a math problem based on the current grade level and difficulty."""
        if self.grade_level <= 5:
            return self.generate_elementary_problem()
        elif self.grade_level <= 8:
            return self.generate_middle_school_problem()
        elif self.grade_level <= 12:
            return self.generate_high_school_problem()
        else:
            raise ValueError("Grade level must be between 0 and 12")

    def generate_elementary_problem(self):
        """Generate an elementary-level math problem."""
        num1, num2 = self.get_random_numbers(difficulty=self.difficulty)
        operation = random.choice(self.operations)

        # Ensure division problems have clean answers
        if operation == '/':
            num2 = self.make_divisible(num1)

        problem = f"{num1} {operation} {num2}"
        solution = self.solve_problem(num1, num2, operation)

        return problem, solution

    def generate_middle_school_problem(self):
        """Generate a middle school-level math problem."""
        num1, num2 = self.get_random_numbers(
            difficulty=self.difficulty,
            range_start=-20,
            range_end=20
        )
        operation = random.choice(self.operations)

        # Ensure no division by zero
        if operation == '/':
            num2 = self.make_divisible(num1, extended_range=True)

        problem = f"{num1} {operation} {num2}"
        solution = self.solve_problem(num1, num2, operation)

        return problem, solution

    def generate_high_school_problem(self):
        """Generate a high school-level math problem."""
        problem_type = random.choice(["algebra", "geometry", "calculus", "word"])

        if problem_type == "algebra":
            return self.generate_algebra_problem()
        elif problem_type == "geometry":
            return self.generate_geometry_problem()
        elif problem_type == "calculus":
            return self.generate_calculus_problem()
        elif problem_type == "word":
            return self.generate_word_problem()

    def provide_hint(self, problem_type):
        """Provide a hint for the current problem."""
        hints = {
            "algebra": "Remember to isolate the variable on one side of the equation.",
            "geometry": "Use geometric formulas such as area, perimeter, or the Pythagorean theorem.",
            "calculus": "Focus on derivatives or integrals as needed.",
            "word": "Break the problem into smaller parts and solve step by step."
        }
        return hints.get(problem_type, "Think carefully and try your best!")

    def track_progress(self, correct):
        """Track user progress."""
        self.total_questions += 1
        if correct:
            self.correct_answers += 1

    def get_progress_report(self):
        """Generate a progress report."""
        accuracy = (self.correct_answers / self.total_questions) * 100 if self.total_questions > 0 else 0
        return f"Progress: {self.correct_answers}/{self.total_questions} correct ({accuracy:.2f}% accuracy)"

    def save_progress(self, file_path="progress.json"):
        """Save user progress to a file."""
        data = {
            "grade_level": self.grade_level,
            "difficulty": self.difficulty,
            "correct_answers": self.correct_answers,
            "total_questions": self.total_questions
        }
        with open(file_path, "w") as file:
            json.dump(data, file)

    def load_progress(self, file_path="progress.json"):
        """Load user progress from a file."""
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
                self.grade_level = data.get("grade_level", 0)
                self.difficulty = data.get("difficulty", "Easy")
                self.correct_answers = data.get("correct_answers", 0)
                self.total_questions = data.get("total_questions", 0)

class MathTutorApp:
    """A GUI application for the Math Tutor AI."""

    def __init__(self, root):
        """Initialize the application with a tkinter root window."""
        self.root = root
        self.root.title("Math Tutor AI")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        # Configure the style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use 'clam' theme for a modern look

        # Define custom colors
        self.bg_color = "#F0F4F8"  # Light blue-gray background
        self.primary_color = "#3498DB"  # Blue for primary elements
        self.accent_color = "#2ECC71"  # Green for accents/success
        self.text_color = "#2C3E50"  # Dark blue-gray for text
        self.error_color = "#E74C3C"  # Red for errors

        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=('Helvetica', 11))
        self.style.configure('TButton', background=self.primary_color, foreground='white', font=('Helvetica', 11))

        # Create the math tutor object
        self.tutor_ai = MathTutorAI()
        self.tutor_ai.load_progress()  # Load saved progress if available

        # Add widgets and functionalities
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange widgets in the GUI."""
        # Add widgets such as buttons, labels, and progress display
        ttk.Label(self.root, text="Welcome to Math Tutor AI!").pack(pady=10)
        ttk.Button(self.root, text="Start New Problem", command=self.start_new_problem).pack(pady=5)
        ttk.Button(self.root, text="View Progress", command=self.view_progress).pack(pady=5)

    def start_new_problem(self):
        """Start a new problem."""
        problem, solution = self.tutor_ai.generate_problem()
        messagebox.showinfo("New Problem", f"Problem: {problem}\nSolution: {solution}")

    def view_progress(self):
        """View progress report."""
        progress = self.tutor_ai.get_progress_report()
        messagebox.showinfo("Progress Report", progress)

if __name__ == "__main__":
    root = tk.Tk()
    app = MathTutorApp(root)
    root.mainloop()
