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
        self.load_users()  # Load users from file on initialization

    def load_users(self, file_path="users.json"):
        """Load all users from a JSON file."""
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
            except (json.JSONDecodeError, IOError):
                print("Error loading users. Starting with an empty user list.")
                self.users = {}
        else:
            self.users = {}

    def save_users(self, file_path="users.json"):
        """Save all users to a JSON file."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.users, f)

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
        if username in self.users:
            raise ValueError(f"User '{username}' already exists.")
        self.users[username] = {
            "grade_level": 0,
            "difficulty": "Easy",
            "correct_answers": 0,
            "total_questions": 0
        }
        self.save_users()

    def get_user_data(self, username):
        """Get data for a specific user."""
        return self.users.get(username, None)

    def update_user_data(self, username, data):
        """Update data for a specific user."""
        if username not in self.users:
            raise ValueError(f"User '{username}' does not exist.")
        self.users[username].update(data)
        self.save_users()


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
            return random.randint(range_start, range_end), random.randint(range_start, range_end)
        elif difficulty == "Medium":
            return random.randint(range_start, range_end * 2), random.randint(range_start, range_end * 2)
        else:
            return random.randint(range_start, range_end * 5), random.randint(range_start, range_end * 5)

    def make_divisible(self, num1, extended_range=False):
        if num1 == 0:
            return 1
        divisors = [i for i in range(1, (20 if extended_range else 10)+1) if num1 % i == 0]
        return random.choice(divisors) if divisors else 1

    def track_progress(self, correct):
        self.total_questions += 1
        if correct:
            self.correct_answers += 1

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

        self.problem = ""
        self.solution = None

        self.timer_running = False
        self.start_time = None

        self.create_user_selection_widgets()  # Start with user selection

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
        user_frame = ttk.LabelFrame(self.root, text="User Management")
        user_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(user_frame, text="Select User:").grid(row=0, column=0, padx=5, pady=5)
        self.user_dropdown = ttk.Combobox(
            user_frame, textvariable=self.user_var,
            values=list(self.user_manager.users.keys()), state="readonly"
        )
        self.user_dropdown.grid(row=0, column=1, padx=5, pady=5)

        select_button = ttk.Button(user_frame, text="Login", command=self.select_user)
        select_button.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(user_frame, text="New User:").grid(row=1, column=0, padx=5, pady=5)
        self.new_user_var = tk.StringVar()
        new_user_entry = ttk.Entry(user_frame, textvariable=self.new_user_var)
        new_user_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = ttk.Button(user_frame, text="Create User", command=self.add_user)
        add_button.grid(row=1, column=2, padx=5, pady=5)

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
            self.user = self.user_manager.get_user_data(username)
            if self.user:
                self.tutor_ai.grade_level = self.user["grade_level"]
                self.tutor_ai.difficulty = self.user["difficulty"]
                self.tutor_ai.correct_answers = self.user["correct_answers"]
                self.tutor_ai.total_questions = self.user["total_questions"]
                self.root.title(f"Math Tutor AI - User: {username}")
                self.create_widgets()
            else:
                tk.messagebox.showerror("Error", "User not found.")

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

    def save_user_progress(self, user, file_path="users_progress"):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        data = {
            "grade_level": user.grade_level,
            "difficulty": user.difficulty,
            "correct_answers": user.correct_answers,
            "total_questions": user.total_questions,
            "language": user.language  # Save language
        }
        with open(os.path.join(file_path, f"{user.username}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_user_progress(self, username, file_path="users_progress"):
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = os.path.join(file_path, f"{username}.json")
        if os.path.exists(file_name):
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return User(
                    username=username,
                    grade_level=data.get("grade_level", 0),
                    difficulty=data.get("difficulty", "Easy"),
                    language=data.get("language", "en"),
                    correct_answers=data.get("correct_answers", 0),
                    total_questions=data.get("total_questions", 0)
                )
            except (json.JSONDecodeError, IOError):
                print(f"Error loading progress for {username}, starting fresh.")
        return User(username=username)

    def save_progress(self):
        """Manually save progress."""
        self.user.grade_level = self.tutor_ai.grade_level
        self.user.difficulty = self.tutor_ai.difficulty
        self.user.correct_answers = self.tutor_ai.correct_answers
        self.user.total_questions = self.tutor_ai.total_questions
        self.user.language = self.tutor_ai.language
        self.save_user_progress(self.user)
        self.feedback_var.set("Progress saved! 💾")

    def reset_progress(self):
        """Reset user progress."""
        self.user.correct_answers = 0
        self.user.total_questions = 0
        self.save_user_progress(self.user)
        self.progress_var.set(self.get_progress_report())
        self.feedback_var.set("Progress reset! 🔄")

    def toggle_dark_mode(self):
        """Toggle dark mode for the app."""
        dark_bg = "#2e2e2e"
        dark_fg = "#ffffff"
        light_bg = "#f0f0f0"
        light_fg = "#000000"

        if self.root.cget("background") == light_bg or self.root.cget("background") == "SystemButtonFace":
            self.root.configure(background=dark_bg)
            for widget in self.root.winfo_children():
                widget.configure(style="Dark.TLabel")
        else:
            self.root.configure(background=light_bg)
            for widget in self.root.winfo_children():
                widget.configure(style="TLabel")

    def create_user_selection_widgets(self):
        """Create user selection and authentication widgets."""
        user_frame = ttk.LabelFrame(self.root, text="User Management")
        user_frame.grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(user_frame, text="Select User:").grid(row=0, column=0, padx=5, pady=5)
        self.user_dropdown = ttk.Combobox(user_frame, textvariable=self.user_var, values=list(self.user_manager.users.keys()), state="readonly")
        self.user_dropdown = ttk.Combobox(user_frame, textvariable=self.user_var, values=list(self.user_manager.users.keys()), state="readonly")
        self.user_dropdown.grid(row=0, column=1, padx=5, pady=5)

        select_button = ttk.Button(user_frame, text="Select", command=self.select_user)
        select_button.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(user_frame, text="New User:").grid(row=1, column=0, padx=5, pady=5)
        self.new_user_var = tk.StringVar()
        new_user_entry = ttk.Entry(user_frame, textvariable=self.new_user_var)
        new_user_entry.grid(row=1, column=1, padx=5, pady=5)

        add_button = ttk.Button(user_frame, text="Add User", command=self.add_user)
        add_button.grid(row=1, column=2, padx=5, pady=5)

        # Delete User Button
        delete_button = ttk.Button(user_frame, text="Delete User", command=self.delete_user)
        delete_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Leaderboard Button
        leaderboard_button = ttk.Button(user_frame, text="Leaderboard", command=self.show_leaderboard)
        leaderboard_button.grid(row=3, column=0, columnspan=3, pady=10)

    def select_user(self):
        """Select an existing user and initialize MathTutorAI."""
        username = self.user_var.get()
        self.user = self.load_user_progress(username)  # Correctly load user progress
        self.tutor_ai.grade_level = self.user.grade_level
        self.tutor_ai.difficulty = self.user.difficulty
        self.tutor_ai.language = self.user.language
        self.tutor_ai.correct_answers = self.user.correct_answers
        self.tutor_ai.total_questions = self.user.total_questions
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
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Then add a button to trigger it:
        dark_mode_button = ttk.Button(settings_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        dark_mode_button.grid(row=4, column=0, columnspan=2, pady=5)

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

        # Dark Mode Button
        dark_mode_button = ttk.Button(settings_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        dark_mode_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Return to Main Menu Button
        return_button = ttk.Button(settings_frame, text="Return to Main Menu", command=self.return_to_main_menu)
        return_button.grid(row=5, column=0, columnspan=2, pady=5)

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

            # Auto-save progress after each problem
            self.save_progress()

            self.root.after(2000, self.next_problem)  # Move to next after 2 seconds

        except ValueError:
            self.feedback_var.set("Invalid input. Please enter a valid number.")

    def save_progress(self):
        """Manually save progress."""
        self.user.grade_level = self.tutor_ai.grade_level
        self.user.difficulty = self.tutor_ai.difficulty
        self.user.correct_answers = self.tutor_ai.correct_answers
        self.user.total_questions = self.tutor_ai.total_questions
        self.user.language = self.tutor_ai.language
        self.save_user_progress(self.user)
        self.feedback_var.set("Progress saved! 💾")

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


if __name__ == "__main__":
    root = tk.Tk()
    app = MathTutor(root)
    root.mainloop()
