import json
import os
import random
import time
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import sympy as sp


class UserManager:
    """Class to manage multiple user profiles."""

    def __init__(self):
        self.users = {}  # Initialize users dictionary
        self.preferences = {"dark_mode": False}  # Initialize preferences with default values
        self.load_users()  # Load users and preferences from file on initialization

    def load_users(self, file_path="users.json"):
        """Load all users and preferences from a JSON file."""
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.users = data.get("users", {})
                    self.preferences = data.get("preferences", {"dark_mode": False})
            except (json.JSONDecodeError, IOError):
                tk.messagebox.showerror("Error", "Failed to load users or preferences. Starting with defaults.")
                self.users = {}
                self.preferences = {"dark_mode": False}
        else:
            self.users = {}
            self.preferences = {"dark_mode": False}

    def save_users(self, file_path="users.json"):
        """Save all users and preferences to a JSON file."""
        data = {
            "users": self.users,
            "preferences": self.preferences
        }
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
        except IOError:
            tk.messagebox.showerror("Error", "Failed to save user data. Please try again.")

    def load_user_data(self):
        """Load data for the current user."""
        user_data = self.user_manager.get_user_data(self.username)
        if user_data:
            self.grade_level = user_data["grade_level"]
            self.difficulty = user_data["difficulty"]
            self.correct_answers = user_data["correct_answers"]
            self.total_questions = user_data["total_questions"]
        else:
            raise ValueError("User data not found.")

    def save_user_data(self):
        """Save progress for the current user."""
        data = {
            "grade_level": self.grade_level,
            "difficulty": self.difficulty,
            "correct_answers": self.correct_answers,
            "total_questions": self.total_questions
        }
        self.user_manager.update_user_data(self.username, data)

    def add_user(self, username):
        """Add a new user."""
        try:
            if username in self.users:
                raise ValueError(f"User '{username}' already exists.")
            self.users[username] = {
                "grade_level": 0,
                "difficulty": "Easy",
                "correct_answers": 0,
                "total_questions": 0,
                "language": "en"  # Initialize language with a default value
            }
            self.save_users()
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def get_user_data(self, username):
        """Get data for a specific user."""
        user_data = self.users.get(username, None)
        if user_data:
            # Ensure 'language' key exists with a default value
            user_data.setdefault("language", "en")
        return user_data

    def update_user_data(self, username, data):
        """Update data for a specific user."""
        try:
            if username not in self.users:
                raise ValueError(f"User '{username}' does not exist.")
            self.users[username].update(data)
            self.save_users()
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def save_user_progress(self, username, grade_level, difficulty, correct_answers, total_questions, language):
        """Save progress for a specific user."""
        try:
            if username not in self.users:
                raise ValueError(f"User '{username}' does not exist.")
            self.users[username].update({
                "grade_level": grade_level,
                "difficulty": difficulty,
                "correct_answers": correct_answers,
                "total_questions": total_questions,
                "language": language
            })
            self.save_users()
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))

    def load_user_progress(self, username):
        """Load progress for a specific user."""
        try:
            user_data = self.get_user_data(username)
            if not user_data:
                raise ValueError(f"User '{username}' does not exist.")
            return user_data
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
            return None


class MathTutorAI:
    """Math Tutor AI for generating and solving math problems."""

    def __init__(self):
        self.operations = ["+", "-", "*", "/"]
        self.grade_level = 0  # Initialize grade_level
        self.difficulty = "Easy"  # Initialize difficulty
        self.language = "en"  # Initialize language
        self.correct_answers = 0  # Initialize correct_answers
        self.total_questions = 0  # Initialize total_questions
        self.start_time = None  # Initialize start_time
        self.problem_history = []  # Store past problems and solutions

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
        """Generate a problem based on grade level."""
        problem_generators = {
            "elementary": self.generate_elementary_problem,
            "middle_school": self.generate_middle_school_problem,
            "high_school": self.generate_high_school_problem
        }
        if self.grade_level <= 5:
            return problem_generators["elementary"]()
        elif self.grade_level <= 8:
            return problem_generators["middle_school"]()
        elif self.grade_level <= 12:
            return problem_generators["high_school"]()
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
        """Generate high school-level problems with expanded variety."""
        problem_types = ["algebra", "geometry", "calculus", "word", "trigonometry", "statistics"]
        problem_type = random.choice(problem_types)
        if problem_type == "algebra":
            return self.generate_algebra_problem()
        elif problem_type == "geometry":
            return self.generate_geometry_problem()
        elif problem_type == "calculus":
            return self.generate_calculus_problem()
        elif problem_type == "trigonometry":
            return self.generate_trigonometry_problem()
        elif problem_type == "statistics":
            return self.generate_statistics_problem()
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
        """Generate geometry problems with consolidated logic."""
        if self.difficulty == "Easy":
            return self._generate_circle_area_problem()
        elif self.difficulty == "Medium":
            return self._generate_prism_volume_problem()
        else:
            return self._generate_triangle_area_problem()

    def _generate_circle_area_problem(self):
        radius = random.randint(1, 5)
        area = sp.pi * radius**2
        problem = f"Find the area of a circle with radius {radius} units."
        return problem, float(area.evalf())

    def _generate_prism_volume_problem(self):
        l, w, h = random.randint(5, 10), random.randint(5, 10), random.randint(5, 10)
        volume = l * w * h
        problem = f"Find the volume of a rectangular prism with length {l}, width {w}, height {h} units."
        return problem, volume

    def _generate_triangle_area_problem(self):
        a, b, c = random.randint(5, 15), random.randint(5, 15), random.randint(5, 15)
        s = (a + b + c) / 2
        area = sp.sqrt(s * (s - a) * (s - b) * (s - c))
        problem = f"Find the area of a triangle with sides {a}, {b}, and {c} units."
        return problem, float(area.evalf())

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

    def generate_trigonometry_problem(self):
        """Generate trigonometry problems."""
        angle = random.randint(0, 90)
        if self.difficulty == "Easy":
            problem = f"Find sin({angle}°)."
            solution = round(sp.sin(sp.rad(angle)), 2)
        elif self.difficulty == "Medium":
            problem = f"Find cos({angle}°)."
            solution = round(sp.cos(sp.rad(angle)), 2)
        else:
            problem = f"Find tan({angle}°)."
            solution = round(sp.tan(sp.rad(angle)), 2)
        return problem, solution

    def generate_statistics_problem(self):
        """Generate statistics problems with consolidated logic."""
        data = [random.randint(1, 100) for _ in range(random.randint(5, 10))]
        if self.difficulty == "Easy":
            return self._generate_mean_problem(data)
        elif self.difficulty == "Medium":
            return self._generate_median_problem(data)
        else:
            return self._generate_mode_problem(data)

    def _generate_mean_problem(self, data):
        problem = f"Find the mean of the data set: {data}."
        solution = round(sum(data) / len(data), 2)
        return problem, solution

    def _generate_median_problem(self, data):
        data.sort()
        mid = len(data) // 2
        solution = data[mid] if len(data) % 2 != 0 else (data[mid - 1] + data[mid]) / 2
        problem = f"Find the median of the data set: {data}."
        return problem, solution

    def _generate_mode_problem(self, data):
        problem = f"Find the mode of the data set: {data}."
        solution = max(set(data), key=data.count)
        return problem, solution

    def generate_word_problem(self):
        """Expand word problems with more depth."""
        if self.difficulty == "Easy":
            a, b = random.randint(1, 10), random.randint(1, 10)
            problem = f"A farmer has {a} apples and buys {b} more. How many apples total?"
            return problem, a + b
        elif self.difficulty == "Medium":
            speed, time_ = random.randint(10, 50), random.randint(1, 10)
            problem = f"A car travels {speed} mph. How far in {time_} hours?"
            return problem, speed * time_
        else:
            principal, rate, time_ = random.randint(1000, 5000), random.randint(1, 10), random.randint(1, 5)
            problem = f"A bank offers {rate}% annual interest. How much interest will be earned on ${principal} in {time_} years?"
            solution = round(principal * (rate / 100) * time_, 2)
            return problem, solution

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

    def explain_problem(self, problem, solution, user_answer=None):
        """Explain the solution and provide targeted feedback."""
        explanation = ""
        if "Solve for x" in problem:
            explanation = f"Isolate x to find the solution: x = {solution}."
        elif "area of a circle" in problem:
            explanation = f"Use the formula for area: area = πr². Area = {solution}."
        elif "hypotenuse" in problem:
            explanation = f"Use the Pythagorean theorem: a² + b² = c². Hypotenuse = {solution}."
        elif "volume of a rectangular prism" in problem:
            explanation = f"Volume = length × width × height = {solution}."
        elif "derivative" in problem:
            explanation = f"Apply differentiation rules. Derivative = {solution}."
        else:
            explanation = f"The solution is {solution}."

        # Add targeted feedback if user_answer is provided
        if user_answer is not None:
            try:
                user_answer = float(user_answer)
                if isinstance(solution, (int, float)) and abs(user_answer - solution) > 10:
                    explanation += " It seems your answer is far off. Double-check your calculations."
                elif isinstance(solution, (list, tuple)) and not any(abs(user_answer - sol) < 0.01 for sol in solution):
                    explanation += " Your answer is close but not quite correct. Review the problem carefully."
            except ValueError:
                explanation += " Your answer doesn't seem to be a valid number. Please enter a numeric value."

        # Add learning resources
        explanation += "\nFor more help, visit: https://www.khanacademy.org/math"
        return explanation

    def track_common_mistakes(self, problem, user_answer):
        """Track common mistakes for learning support."""
        if not hasattr(self, "common_mistakes"):
            self.common_mistakes = {}
        if problem not in self.common_mistakes:
            self.common_mistakes[problem] = []
        self.common_mistakes[problem].append(user_answer)

    def track_progress(self, correct):
        """Track progress and adjust difficulty based on performance."""
        self.total_questions += 1
        if correct:
            self.correct_answers += 1

        # Adaptive difficulty logic
        accuracy = (self.correct_answers / self.total_questions) * 100
        if accuracy >= 80 and self.difficulty == "Easy":
            self.difficulty = "Medium"
        elif accuracy >= 90 and self.difficulty == "Medium":
            self.difficulty = "Hard"
        elif accuracy < 50 and self.difficulty == "Medium":
            self.difficulty = "Easy"
        elif accuracy < 40 and self.difficulty == "Hard":
            self.difficulty = "Medium"

    def provide_hint(self, topic):
        """Provide a hint for the given topic."""
        hints = {
            "algebra": "Try isolating the variable on one side of the equation.",
            "geometry": "Remember the formulas for area, volume, and the Pythagorean theorem.",
            "calculus": "Think about the rules for differentiation.",
            "word": "Break the problem into smaller parts and identify key information."
        }
        return hints.get(topic, "No hints available for this topic.")

    def get_progress_report(self):
        acc = (self.correct_answers / self.total_questions) * 100 if self.total_questions else 0
        return f"Progress: {self.correct_answers}/{self.total_questions} correct ({acc:.2f}% accuracy)"

    def save_progress(self):
        """Save progress for the current user."""
        pass

    def load_progress(self):
        """Load progress for the current user."""
        pass

    def save_problem_to_history(self, problem, solution, user_answer, correct):
        """Save a problem, its solution, the user's answer, and whether it was correct."""
        self.problem_history.append({
            "problem": problem,
            "solution": solution,
            "user_answer": user_answer,
            "correct": correct
        })


class User:
    def __init__(self, username, grade_level=0, difficulty="Easy", language="en", correct_answers=0, total_questions=0):
        self.username = username
        self.current_user = None  # Initialize current_user in __init__
        self.grade_level = grade_level
        self.difficulty = difficulty
        self.language = language
        self.correct_answers = correct_answers
        self.total_questions = total_questions


class MathTutor:
    """GUI Application for MathTutorAI."""

    def show_leaderboard(self):
        """Display a leaderboard of users based on their progress."""
        # Reload user data to ensure the leaderboard reflects the latest progress
        self.user_manager.load_users()

        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Leaderboard")

        sorted_users = sorted(
            self.user_manager.users.items(),
            key=lambda item: item[1]["correct_answers"],
            reverse=True
        )

        ttk.Label(leaderboard_window, text="Leaderboard", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)
        ttk.Label(leaderboard_window, text="Rank").grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(leaderboard_window, text="Username").grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(leaderboard_window, text="Correct/Total").grid(row=1, column=2, padx=10, pady=5)
        ttk.Label(leaderboard_window, text="Accuracy").grid(row=1, column=3, padx=10, pady=5)

        for i, (username, data) in enumerate(sorted_users):
            correct_answers = data.get("correct_answers", 0)
            total_questions = data.get("total_questions", 0)
            accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
            ttk.Label(leaderboard_window, text=f"{i+1}").grid(row=i+2, column=0, padx=10, pady=5)
            ttk.Label(leaderboard_window, text=username).grid(row=i+2, column=1, padx=10, pady=5)
            ttk.Label(leaderboard_window, text=f"{correct_answers}/{total_questions}").grid(row=i+2, column=2, padx=10, pady=5)
            ttk.Label(leaderboard_window, text=f"{accuracy:.2f}%").grid(row=i+2, column=3, padx=10, pady=5)


    def __init__(self, root):
        self.user_var = tk.StringVar()  # Initialize user_var
        self.root = root
        self.root.title("Math Tutor AI")
        self.tutor_ai = MathTutorAI()  # Initialize MathTutorAI
        self.user_manager = UserManager()  # Initialize UserManager
        self.user = None  # Initialize user as None
        self.review_window = None  # Initialize review window as None

        self.problem = ""
        self.solution = None

        self.timer_running = False
        self.start_time = None

        # Initialize ttk style
        self.style = ttk.Style()

        # Apply saved preferences (e.g., dark mode and theme)
        self.apply_preferences()

        self.create_user_selection_widgets()  # Start with user selection

    def apply_preferences(self):
        """Apply saved preferences such as dark mode and theme."""
        if self.user_manager.preferences.get("dark_mode", False):
            self.enable_dark_mode()
        else:
            self.disable_dark_mode()

        theme = self.user_manager.preferences.get("theme", "default")
        self.style.theme_use(theme)

    def toggle_dark_mode(self):
        """Toggle dark mode for the app and save the preference."""
        if self.root.cget("background") in ("#f0f0f0", "SystemButtonFace"):
            self.enable_dark_mode()
            self.user_manager.preferences["dark_mode"] = True
        else:
            self.disable_dark_mode()
            self.user_manager.preferences["dark_mode"] = False
        self.user_manager.save_users()

    def enable_dark_mode(self):
        """Enable dark mode."""
        dark_bg = "#2e2e2e"
        dark_fg = "#ffffff"
        self.root.configure(background=dark_bg)
        for widget in self.root.winfo_children():
            widget.configure(background=dark_bg, foreground=dark_fg)

    def disable_dark_mode(self):
        """Disable dark mode."""
        light_bg = "#f0f0f0"
        light_fg = "#000000"
        self.root.configure(background=light_bg)
        for widget in self.root.winfo_children():
            widget.configure(background=light_bg, foreground=light_fg)

    def change_theme(self, theme):
        """Change the ttk theme and save the preference."""
        self.style.theme_use(theme)
        self.user_manager.preferences["theme"] = theme
        self.user_manager.save_users()

    def delete_user(self):
        """Delete an existing user."""
        username = self.user_var.get()
        if username:
            confirm = tk.messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?")
            if confirm:
                try:
                    del self.user_manager.users[username]
                    self.user_manager.save_users()
                    self.user_var.set("")
                    self.user_dropdown["values"] = list(self.user_manager.users.keys())
                    tk.messagebox.showinfo("Success", f"User '{username}' deleted successfully.")
                except KeyError:
                    tk.messagebox.showerror("Error", f"User '{username}' does not exist.")
        else:
            tk.messagebox.showerror("Error", "No user selected.")

    def create_user_selection_widgets(self):
        """Create user selection and authentication widgets."""
        user_frame = ttk.LabelFrame(self.root, text="User Management", padding=10)
        user_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        ttk.Label(user_frame, text="Select User:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.user_dropdown = ttk.Combobox(
            user_frame, textvariable=self.user_var,
            values=list(self.user_manager.users.keys()), state="readonly", font=("Arial", 10)
        )
        self.user_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        select_button = ttk.Button(user_frame, text="Login", command=self.select_user)
        select_button.grid(row=0, column=2, padx=10, pady=5)

        ttk.Label(user_frame, text="New User:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.new_user_var = tk.StringVar()
        new_user_entry = ttk.Entry(user_frame, textvariable=self.new_user_var, font=("Arial", 10))
        new_user_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        add_button = ttk.Button(user_frame, text="Create User", command=self.add_user)
        add_button.grid(row=1, column=2, padx=10, pady=5)

        # Delete User Button
        delete_button = ttk.Button(user_frame, text="Delete User", command=self.delete_user)
        delete_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Leaderboard Button
        leaderboard_button = ttk.Button(user_frame, text="Leaderboard", command=self.show_leaderboard)
        leaderboard_button.grid(row=3, column=0, columnspan=3, pady=10)

    def select_user(self):
        """Select an existing user and initialize MathTutorAI."""
        username = self.user_var.get()
        if username:
            user_data = self.user_manager.load_user_progress(username)
            if user_data:
                self.tutor_ai.grade_level = user_data["grade_level"]
                self.tutor_ai.difficulty = user_data["difficulty"]
                self.tutor_ai.language = user_data.get("language", "en")  # Provide a default value
                self.tutor_ai.correct_answers = user_data["correct_answers"]
                self.tutor_ai.total_questions = user_data["total_questions"]
                self.root.title(f"Math Tutor AI - User: {username}")
                self.create_widgets()
            else:
                tk.messagebox.showerror("Error", "Failed to load user data. Please try again.")
        else:
            tk.messagebox.showerror("Error", "No user selected. Please select a user.")

    def add_user(self):
        """Add a new user profile."""
        new_username = self.new_user_var.get().strip()
        if new_username:
            try:
                self.user_manager.add_user(new_username)
                self.user_var.set(new_username)
                self.user_dropdown["values"] = list(self.user_manager.users.keys())
                tk.messagebox.showinfo("Success", f"User '{new_username}' created successfully.")
            except ValueError as e:
                tk.messagebox.showerror("Error", str(e))
        else:
            tk.messagebox.showerror("Error", "Username cannot be empty.")

    def save_progress(self):
        """Manually save progress."""
        try:
            self.user_manager.save_user_progress(
                username=self.user_var.get(),
                grade_level=self.tutor_ai.grade_level,
                difficulty=self.tutor_ai.difficulty,
                correct_answers=self.tutor_ai.correct_answers,
                total_questions=self.tutor_ai.total_questions,
                language=self.tutor_ai.language
            )
            self.feedback_var.set("Progress saved! 💾")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to save progress: {str(e)}")

    def reset_progress(self):
        """Reset user progress."""
        self.user.correct_answers = 0
        self.user.total_questions = 0
        self.save_progress()
        self.progress_var.set(self.get_progress_report())
        self.feedback_var.set("Progress reset! 🔄")

    def create_user_selection_widgets(self):
        """Create user selection and authentication widgets."""
        user_frame = ttk.LabelFrame(self.root, text="User Management", padding=10)
        user_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        ttk.Label(user_frame, text="Select User:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.user_dropdown = ttk.Combobox(user_frame, textvariable=self.user_var, values=list(self.user_manager.users.keys()), state="readonly", font=("Arial", 10))
        self.user_dropdown = ttk.Combobox(user_frame, textvariable=self.user_var, values=list(self.user_manager.users.keys()), state="readonly", font=("Arial", 10))
        self.user_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        select_button = ttk.Button(user_frame, text="Select", command=self.select_user)
        select_button.grid(row=0, column=2, padx=10, pady=5)

        ttk.Label(user_frame, text="New User:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.new_user_var = tk.StringVar()
        new_user_entry = ttk.Entry(user_frame, textvariable=self.new_user_var, font=("Arial", 10))
        new_user_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        add_button = ttk.Button(user_frame, text="Add User", command=self.add_user)
        add_button.grid(row=1, column=2, padx=10, pady=5)

        # Delete User Button
        delete_button = ttk.Button(user_frame, text="Delete User", command=self.delete_user)
        delete_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Leaderboard Button
        leaderboard_button = ttk.Button(user_frame, text="Leaderboard", command=self.show_leaderboard)
        leaderboard_button.grid(row=3, column=0, columnspan=3, pady=10)

    def select_user(self):
        """Select an existing user and initialize MathTutorAI."""
        username = self.user_var.get()
        user_data = self.user_manager.load_user_progress(username)
        self.tutor_ai.grade_level = user_data["grade_level"]
        self.tutor_ai.difficulty = user_data["difficulty"]
        self.tutor_ai.language = user_data.get("language", "en")  # Provide a default value
        self.tutor_ai.correct_answers = user_data["correct_answers"]
        self.tutor_ai.total_questions = user_data["total_questions"]
        self.create_widgets()

    def add_user(self):
        """Add a new user profile."""
        new_username = self.new_user_var.get().strip()
        if new_username:
            try:
                self.user_manager.add_user(new_username)
                self.user_var.set(new_username)
                self.user_dropdown["values"] = list(self.user_manager.users.keys())
                self.select_user()
            except ValueError as e:
                tk.messagebox.showerror("Error", str(e))

    def create_widgets(self):
        """Create all GUI widgets."""

    # --- Settings Frame ---
        settings_frame = ttk.LabelFrame(self.root, text="Settings", padding=10)
        settings_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # Grade Level Dropdown
        ttk.Label(settings_frame, text="Grade Level:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.grade_level_var = tk.StringVar(value="K")
        grade_levels = ["K"] + [str(i) for i in range(1, 13)]
        grade_dropdown = ttk.Combobox(
            settings_frame, textvariable=self.grade_level_var,
            values=grade_levels, state="readonly", width=5, font=("Arial", 10)
        )
        grade_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Difficulty Dropdown
        ttk.Label(settings_frame, text="Difficulty:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.difficulty_var = tk.StringVar(value=self.tutor_ai.difficulty)
        difficulty_combo = ttk.Combobox(
            settings_frame, textvariable=self.difficulty_var,
            values=["Easy", "Medium", "Hard"], width=8, state="readonly", font=("Arial", 10)
        )
        difficulty_combo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Language Dropdown
        ttk.Label(settings_frame, text="Language:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.language_var = tk.StringVar(value=self.tutor_ai.language)
        language_combo = ttk.Combobox(
            settings_frame, textvariable=self.language_var,
            values=["en", "es", "fr"], width=8, state="readonly", font=("Arial", 10)
        )
        language_combo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Theme Dropdown
        ttk.Label(settings_frame, text="Theme:", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.theme_var = tk.StringVar(value=self.style.theme_use())
        theme_dropdown = ttk.Combobox(
            settings_frame, textvariable=self.theme_var,
            values=self.style.theme_names(), state="readonly", font=("Arial", 10)
        )
        theme_dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        theme_dropdown.bind("<<ComboboxSelected>>", lambda e: self.change_theme(self.theme_var.get()))

        # Start Button
        start_button = ttk.Button(settings_frame, text="Start", command=self.start_tutoring_session)
        start_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Dark Mode Button
        dark_mode_button = ttk.Button(settings_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        dark_mode_button.grid(row=5, column=0, columnspan=2, pady=5)

        # Return to Main Menu Button
        return_button = ttk.Button(settings_frame, text="Return to Main Menu", command=self.return_to_main_menu)
        return_button.grid(row=6, column=0, columnspan=2, pady=5)

        # --- Problem Frame ---
        problem_frame = ttk.LabelFrame(self.root, text="Problem", padding=10)
        problem_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        self.problem_var = tk.StringVar(value="Click Start to begin.")
        self.problem_label = ttk.Label(problem_frame, textvariable=self.problem_var, wraplength=300, font=("Arial", 10))
        self.problem_label.grid(row=0, column=0, padx=10, pady=5)

        # Save/Reset Buttons
        button_frame = ttk.Frame(problem_frame)
        button_frame.grid(row=6, column=0, pady=10)

        save_button = ttk.Button(button_frame, text="Save Progress", command=self.save_progress)
        save_button.grid(row=0, column=0, padx=10)

        reset_button = ttk.Button(button_frame, text="Reset Progress", command=self.reset_progress)
        reset_button.grid(row=0, column=1, padx=10)

        # Answer Entry
        answer_frame = ttk.Frame(problem_frame)
        answer_frame.grid(row=1, column=0, pady=10)

        ttk.Label(answer_frame, text="Your Answer:", font=("Arial", 10)).grid(row=0, column=0, padx=10)
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(answer_frame, textvariable=self.answer_var, width=15, font=("Arial", 10))
        self.answer_entry.grid(row=0, column=1, padx=10)
        self.answer_entry.bind("<Return>", self.check_answer)

        submit_button = ttk.Button(answer_frame, text="Submit", command=self.check_answer)
        submit_button.grid(row=0, column=2, padx=10)

        # Hint Button
        self.hint_button = ttk.Button(problem_frame, text="Hint", command=self.show_hint)
        self.hint_button.grid(row=2, column=0, pady=10)

        # Feedback Label
        self.feedback_var = tk.StringVar()
        self.feedback_label = ttk.Label(problem_frame, textvariable=self.feedback_var, foreground="blue", font=("Arial", 10))
        self.feedback_label.grid(row=3, column=0, pady=10)

        # Timer and Progress
        self.timer_var = tk.StringVar(value="Time: 0 seconds")
        self.timer_label = ttk.Label(problem_frame, textvariable=self.timer_var, font=("Arial", 10))
        self.timer_label.grid(row=4, column=0, pady=5)

        self.progress_var = tk.StringVar(value="Progress: 0/0 correct (0.00% accuracy)")
        self.progress_label = ttk.Label(problem_frame, textvariable=self.progress_var, font=("Arial", 10))
        self.progress_label.grid(row=5, column=0, pady=5)

        # Add Review Button
        review_button = ttk.Button(self.root, text="Review Past Problems", command=self.show_review)
        review_button.grid(row=2, column=0, pady=10)

        # Add Common Mistakes Button
        mistakes_button = ttk.Button(self.root, text="View Common Mistakes", command=self.show_common_mistakes)
        mistakes_button.grid(row=3, column=0, pady=10)

    def start_tutoring_session(self):
        """Initialize a new tutoring session."""
        grade_level = self.grade_level_var.get()
        self.tutor_ai.set_grade_level(0 if grade_level == "K" else int(grade_level))
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
        self.feedback_var.set(f"Difficulty: {self.tutor_ai.difficulty}")  # Display current difficulty

    def check_answer(self):
        """Check user's answer and provide enhanced feedback."""
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
            self.tutor_ai.save_problem_to_history(self.problem, self.solution, user_answer, correct)

            if correct:
                self.feedback_var.set("Correct! 🎉")
            else:
                explanation = self.tutor_ai.explain_problem(self.problem, self.solution, user_answer)
                self.tutor_ai.track_common_mistakes(self.problem, user_answer)
                self.feedback_var.set(f"Incorrect. {explanation}")

            self.progress_var.set(self.tutor_ai.get_progress_report())

            # Auto-save progress after each problem
            self.save_progress()

            self.root.after(2000, self.next_problem)  # Move to next after 2 seconds

        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

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

    def provide_hint(self, topic):
        """Provide a hint for the given topic."""
        hints = {
            "algebra": "Try isolating the variable on one side of the equation.",
            "geometry": "Remember the formulas for area, volume, and the Pythagorean theorem.",
            "calculus": "Think about the rules for differentiation.",
            "word": "Break the problem into smaller parts and identify key information."
        }
        return hints.get(topic, "No hints available for this topic.")

    def update_timer(self):
        """Update the timer display."""
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            self.timer_var.set(f"Time: {elapsed} seconds")
            self.root.after(1000, self.update_timer)

    def return_to_main_menu(self):
        """Return to the main menu (user selection screen)."""
        for widget in self.root.winfo_children():
            widget.destroy()  # Clear all widgets
        self.create_user_selection_widgets()

    def show_review(self):
        """Display a review window with past problems and their solutions."""
        if self.review_window is not None and tk.Toplevel.winfo_exists(self.review_window):
            self.review_window.lift()
            return

        self.review_window = tk.Toplevel(self.root)
        self.review_window.title("Review Past Problems")

        ttk.Label(self.review_window, text="Past Problems", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        ttk.Label(self.review_window, text="Problem").grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(self.review_window, text="Your Answer").grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(self.review_window, text="Correct Answer").grid(row=1, column=2, padx=10, pady=5)
        ttk.Label(self.review_window, text="Result").grid(row=1, column=3, padx=10, pady=5)

        for i, entry in enumerate(self.tutor_ai.problem_history):
            ttk.Label(self.review_window, text=entry["problem"]).grid(row=i+2, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(self.review_window, text=entry["user_answer"]).grid(row=i+2, column=1, padx=10, pady=5)
            ttk.Label(self.review_window, text=entry["solution"]).grid(row=i+2, column=2, padx=10, pady=5)
            result_text = "Correct" if entry["correct"] else "Incorrect"
            result_color = "green" if entry["correct"] else "red"
            ttk.Label(self.review_window, text=result_text, foreground=result_color).grid(row=i+2, column=3, padx=10, pady=5)

    def show_common_mistakes(self):
        """Display a window showing common mistakes for learning support."""
        mistakes_window = tk.Toplevel(self.root)
        mistakes_window.title("Common Mistakes")

        ttk.Label(mistakes_window, text="Common Mistakes", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(mistakes_window, text="Problem").grid(row=1, column=0, padx=10, pady=5)
        ttk.Label(mistakes_window, text="Mistakes").grid(row=1, column=1, padx=10, pady=5)

        for i, (problem, mistakes) in enumerate(self.tutor_ai.common_mistakes.items()):
            ttk.Label(mistakes_window, text=problem).grid(row=i+2, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(mistakes_window, text=", ".join(mistakes)).grid(row=i+2, column=1, padx=10, pady=5, sticky="w")


if __name__ == "__main__":
    root = tk.Tk()
    app = MathTutor(root)
    root.mainloop()
