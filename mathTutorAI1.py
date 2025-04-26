import json
import os
import random
import time
import tkinter as tk
from tkinter import ttk

import sympy as sp


class MathTutorAI:
    """Math Tutor AI for generating and solving math problems."""

    def __init__(self):
        self.operations = ["+", "-", "*", "/"]
        self.grade_level = 0
        self.difficulty = "Easy"
        self.correct_answers = 0
        self.total_questions = 0
        self.start_time = None
        self.language = "en"

    def set_grade_level(self, grade):
        self.grade_level = grade

    def set_difficulty(self, difficulty):
        if difficulty not in ["Easy", "Medium", "Hard"]:
            raise ValueError("Difficulty must be 'Easy', 'Medium', or 'Hard'")
        self.difficulty = difficulty

    def set_language(self, language):
        supported_languages = ["en", "es", "fr"]
        if language not in supported_languages:
            raise ValueError(f"Language must be one of {supported_languages}")
        self.language = language

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time

    def generate_problem(self):
        if self.grade_level <= 5:
            return self.generate_elementary_problem()
        elif self.grade_level <= 8:
            return self.generate_middle_school_problem()
        elif self.grade_level <= 12:
            return self.generate_high_school_problem()
        else:
            raise ValueError("Grade level must be between 0 and 12")

    def generate_elementary_problem(self):
        num1, num2 = self.get_random_numbers(self.difficulty)
        operation = random.choice(self.operations)
        if operation == "/":
            num2 = self.make_divisible(num1)
        problem = f"{num1} {operation} {num2}"
        solution = self.solve_problem(num1, num2, operation)
        return problem, solution

    def generate_middle_school_problem(self):
        num1, num2 = self.get_random_numbers(self.difficulty, range_start=-20)
        operation = random.choice(self.operations)
        if operation == "/":
            num2 = self.make_divisible(num1, extended_range=True)
        problem = f"{num1} {operation} {num2}"
        solution = self.solve_problem(num1, num2, operation)
        return problem, solution

    def generate_high_school_problem(self):
        problem_types = ["algebra", "geometry", "calculus", "word"]
        problem_type = random.choice(problem_types)
        if problem_type == "algebra":
            return self.generate_algebra_problem()
        elif problem_type == "geometry":
            return self.generate_geometry_problem()
        elif problem_type == "calculus":
            return self.generate_calculus_problem()
        else:
            return self.generate_word_problem()

    def generate_algebra_problem(self):
        x = sp.symbols("x")
        if self.difficulty == "Easy":
            a, b, c = random.randint(1, 5), random.randint(1, 10), random.randint(1, 20)
            equation = sp.Eq(a * x + b, c)
            solution = sp.solve(equation, x)[0]
        else:
            a, b, c = random.randint(1, 5), random.randint(-10, 10), random.randint(-20, 20)
            equation = sp.Eq(a * x**2 + b * x + c, 0)
            solution = sp.solve(equation, x)
        problem = f"Solve for x: {sp.latex(equation)}"
        return problem, solution

    def generate_geometry_problem(self):
        if self.difficulty == "Easy":
            radius = random.randint(1, 5)
            area = sp.pi * radius**2
            problem = f"Find the area of a circle with radius {radius} units."
            return problem, float(area.evalf())
        elif self.difficulty == "Medium":
            l, w, h = random.randint(5, 10), random.randint(5, 10), random.randint(5, 10)
            volume = l * w * h
            problem = f"Find the volume of a rectangular prism with length {l}, width {w}, height {h} units."
            return problem, volume
        else:
            a, b = random.randint(5, 15), random.randint(5, 15)
            hypotenuse = sp.sqrt(a**2 + b**2)
            problem = f"Find the hypotenuse of a right triangle with legs {a} and {b} units."
            return problem, float(hypotenuse.evalf())

    def generate_calculus_problem(self):
        x = sp.symbols("x")
        if self.difficulty == "Easy":
            coeff = [random.randint(1, 5) for _ in range(3)]
            func = coeff[0]*x**2 + coeff[1]*x + coeff[2]
        elif self.difficulty == "Medium":
            func = sp.sin(x) + sp.cos(x)
        else:
            func = sp.exp(x) * sp.log(x)
        derivative = sp.diff(func, x)
        problem = f"Find the derivative of f(x) = {sp.latex(func)}"
        return problem, derivative

    def generate_word_problem(self):
        if self.difficulty == "Easy":
            a, b = random.randint(1, 10), random.randint(1, 10)
            problem = f"A farmer has {a} apples and buys {b} more. How many apples total?"
            return problem, a + b
        elif self.difficulty == "Medium":
            speed, time_ = random.randint(10, 50), random.randint(1, 10)
            problem = f"A car travels {speed} mph. How far in {time_} hours?"
            return problem, speed * time_
        else:
            dist, time_ = random.randint(50, 200), random.randint(1, 5)
            problem = f"A train travels {dist} miles in {time_} hours. What is its speed?"
            return problem, dist / time_

    def solve_problem(self, num1, num2, operation):
        if operation == "+":
            return num1 + num2
        elif operation == "-":
            return num1 - num2
        elif operation == "*":
            return num1 * num2
        elif operation == "/":
            if num2 == 0:
                raise ValueError("Division by zero is not allowed")
            return num1 / num2

    def explain_problem(self, problem, solution):
        if "Solve for x" in problem:
            return f"Isolate x to find the solution: x = {solution}."
        if "area of a circle" in problem:
            return f"Use area = πr². Area = {solution}."
        if "hypotenuse" in problem:
            return f"Use a²+b²=c². Hypotenuse = {solution}."
        if "volume of a rectangular prism" in problem:
            return f"Volume = length × width × height = {solution}."
        if "derivative" in problem:
            return f"Apply differentiation rules. Derivative = {solution}."
        return f"The solution is {solution}."

    def get_random_numbers(self, difficulty, range_start=1, range_end=10):
        if difficulty == "Easy":
            return random.randint(1, 10), random.randint(1, 10)
        elif difficulty == "Medium":
            return random.randint(range_start, 20), random.randint(range_start, 20)
        else:
            return random.randint(range_start, 50), random.randint(range_start, 50)

    def make_divisible(self, num1, extended_range=False):
        if num1 == 0:
            return 1
        divisors = [i for i in range(1, (20 if extended_range else 10)+1) if num1 % i == 0]
        return random.choice(divisors) if divisors else 1

    def track_progress(self, correct):
        self.total_questions += 1
        if correct:
            self.correct_answers += 1

    def get_progress_report(self):
        acc = (self.correct_answers / self.total_questions) * 100 if self.total_questions else 0
        return f"Progress: {self.correct_answers}/{self.total_questions} correct ({acc:.2f}% accuracy)"

    def save_progress(self, file_path="progress.json"):
        data = {
            "grade_level": self.grade_level,
            "difficulty": self.difficulty,
            "correct_answers": self.correct_answers,
            "total_questions": self.total_questions,
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_progress(self, file_path="progress.json"):
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.grade_level = data.get("grade_level", 0)
                self.difficulty = data.get("difficulty", "Easy")
                self.correct_answers = data.get("correct_answers", 0)
                self.total_questions = data.get("total_questions", 0)
            except (json.JSONDecodeError, IOError):
                print("Error loading progress, starting fresh.")


class MathTutor:
    """GUI Application for MathTutorAI."""

    def __init__(self, root):
        self.root = root
        self.root.title("Math Tutor AI")
        self.tutor_ai = MathTutorAI()
        self.tutor_ai.load_progress()

        self.problem = ""
        self.solution = None

        self.timer_running = False
        self.start_time = None

        self.create_widgets()

    def save_progress(self):
        """Manually save progress."""
        self.tutor_ai.save_progress()
        self.feedback_var.set("Progress saved! 💾")

    def reset_progress(self):
        """Reset user progress."""
        self.tutor_ai.correct_answers = 0
        self.tutor_ai.total_questions = 0
        self.tutor_ai.save_progress()
        self.progress_var.set(self.tutor_ai.get_progress_report())
        self.feedback_var.set("Progress reset! 🔄")

    def create_widgets(self):
        """Create all GUI widgets."""

        # --- Settings Frame ---
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Grade Level
        ttk.Label(settings_frame, text="Grade Level:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.grade_level_var = tk.IntVar(value=self.tutor_ai.grade_level)
        grade_entry = ttk.Entry(settings_frame, textvariable=self.grade_level_var, width=10)
        grade_entry.grid(row=0, column=1, padx=5, pady=5)

        # Difficulty
        ttk.Label(settings_frame, text="Difficulty:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.difficulty_var = tk.StringVar(value=self.tutor_ai.difficulty)
        difficulty_combo = ttk.Combobox(
            settings_frame, textvariable=self.difficulty_var,
            values=["Easy", "Medium", "Hard"], width=8, state="readonly"
        )
        difficulty_combo.grid(row=1, column=1, padx=5, pady=5)

        # Language
        ttk.Label(settings_frame, text="Language:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.language_var = tk.StringVar(value=self.tutor_ai.language)
        language_combo = ttk.Combobox(
            settings_frame, textvariable=self.language_var,
            values=["en", "es", "fr"], width=8, state="readonly"
        )
        language_combo.grid(row=2, column=1, padx=5, pady=5)

        # Start Button
        start_button = ttk.Button(settings_frame, text="Start", command=self.start_tutoring_session)
        start_button.grid(row=3, column=0, columnspan=2, pady=10)

        # --- Problem Frame ---
        problem_frame = ttk.LabelFrame(self.root, text="Problem")
        problem_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.problem_var = tk.StringVar(value="Click Start to begin.")
        self.problem_label = ttk.Label(problem_frame, textvariable=self.problem_var, wraplength=300)
        self.problem_label.grid(row=0, column=0, padx=5, pady=5)

        # Save/Reset Buttons
        button_frame = ttk.Frame(problem_frame)
        button_frame.grid(row=6, column=0, pady=5)

        save_button = ttk.Button(button_frame, text="Save Progress", command=self.save_progress)
        save_button.grid(row=0, column=0, padx=5)

        reset_button = ttk.Button(button_frame, text="Reset Progress", command=self.reset_progress)
        reset_button.grid(row=0, column=1, padx=5)

        # Answer Entry
        answer_frame = ttk.Frame(problem_frame)
        answer_frame.grid(row=1, column=0, pady=5)

        ttk.Label(answer_frame, text="Your Answer:").grid(row=0, column=0, padx=5)
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(answer_frame, textvariable=self.answer_var, width=15)
        self.answer_entry.grid(row=0, column=1, padx=5)
        self.answer_entry.bind("<Return>", self.check_answer)

        submit_button = ttk.Button(answer_frame, text="Submit", command=self.check_answer)
        submit_button.grid(row=0, column=2, padx=5)

        # Hint Button
        self.hint_button = ttk.Button(problem_frame, text="Hint", command=self.show_hint)
        self.hint_button.grid(row=2, column=0, pady=5)

        # Feedback Label
        self.feedback_var = tk.StringVar()
        self.feedback_label = ttk.Label(problem_frame, textvariable=self.feedback_var, foreground="blue")
        self.feedback_label.grid(row=3, column=0, pady=5)

        # Timer and Progress
        self.timer_var = tk.StringVar(value="Time: 0 seconds")
        self.timer_label = ttk.Label(problem_frame, textvariable=self.timer_var)
        self.timer_label.grid(row=4, column=0, pady=2)

        self.progress_var = tk.StringVar(value="Progress: 0/0 correct (0.00% accuracy)")
        self.progress_label = ttk.Label(problem_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=5, column=0, pady=2)

    def start_tutoring_session(self):
        """Initialize a new tutoring session."""
        self.tutor_ai.set_grade_level(self.grade_level_var.get())
        self.tutor_ai.set_difficulty(self.difficulty_var.get())
        self.tutor_ai.set_language(self.language_var.get())

        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

        self.next_problem()

    def next_problem(self):
        """Generate and display the next problem."""
        self.problem, self.solution = self.tutor_ai.generate_problem()
        self.problem_var.set(self.problem)
        self.answer_var.set("")
        self.feedback_var.set("")

    def check_answer(self):
        """Check user's answer."""
        user_answer = self.answer_var.get().strip()

        if not user_answer:
            self.feedback_var.set("Please enter an answer.")
            return

        try:
            if isinstance(self.solution, (list, tuple)):
                correct = any(abs(float(user_answer) - float(sol)) < 0.01 for sol in self.solution)
            elif isinstance(self.solution, sp.Expr):
                correct = sp.sympify(user_answer) == self.solution
            else:
                correct = abs(float(user_answer) - float(self.solution)) < 0.01

            self.tutor_ai.track_progress(correct)

            if correct:
                self.feedback_var.set("Correct! 🎉")
            else:
                explanation = self.tutor_ai.explain_problem(self.problem, self.solution)
                self.feedback_var.set(f"Incorrect. {explanation}")

            self.progress_var.set(self.tutor_ai.get_progress_report())
            self.tutor_ai.save_progress()

            self.root.after(2000, self.next_problem)  # Move to next after 2 seconds

        except ValueError:
            self.feedback_var.set("Invalid input. Please enter a valid number.")

    def show_hint(self):
        """Show a hint based on the problem type."""
        if "Solve for x" in self.problem:
            hint = self.tutor_ai.provide_hint("algebra")
        elif "area" in self.problem or "volume" in self.problem or "hypotenuse" in self.problem:
            hint = self.tutor_ai.provide_hint("geometry")
        elif "derivative" in self.problem:
            hint = self.tutor_ai.provide_hint("calculus")
        else:
            hint = self.tutor_ai.provide_hint("word")

        self.feedback_var.set(f"Hint: {hint}")

    def provide_hint(self):
        """Provide a hint for the current problem."""
        # Placeholder implementation for providing hints
        return "Hints are not yet implemented for this problem type."

    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_var.set(f"Time: {elapsed} seconds")
            self.root.after(1000, self.update_timer)
