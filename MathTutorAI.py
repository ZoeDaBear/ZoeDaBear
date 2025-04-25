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
        """
        Set the grade level for problem generation.

        Args:
            grade (int): Grade level (0-12, where 0 represents kindergarten)
        """
        self.grade_level = grade

    def set_difficulty(self, difficulty):
        """
        Set the difficulty level for problem generation.

        Args:
            difficulty (str): Difficulty level ('Easy', 'Medium', or 'Hard')
        """
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
        """
        Generate a math problem based on the current grade level and difficulty.

        Returns:
            tuple: (problem_statement, solution)
        """
        if self.grade_level <= 5:
            return self.generate_elementary_problem()
        elif self.grade_level <= 8:
            return self.generate_middle_school_problem()
        elif self.grade_level <= 12:
            return self.generate_high_school_problem()
        else:
            raise ValueError("Grade level must be between 0 and 12")

    def generate_elementary_problem(self):
        """
        Generate an elementary-level math problem.

        Returns:
            tuple: (problem_statement, solution)
        """
        num1, num2 = self.get_random_numbers(difficulty=self.difficulty)
        operation = random.choice(self.operations)

        # Ensure division problems have clean answers
        if operation == '/':
            num2 = self.make_divisible(num1)

        problem = f"{num1} {operation} {num2}"
        solution = self.solve_problem(num1, num2, operation)

        return problem, solution

    def generate_middle_school_problem(self):
        """
        Generate a middle school-level math problem.

        Returns:
            tuple: (problem_statement, solution)
        """
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
        """
        Generate a high school-level math problem.

        Returns:
            tuple: (problem_statement, solution)
        """
        # Generate different problem types based on difficulty and grade
        problem_type = random.choice(["algebra", "geometry", "calculus", "word"])

        if problem_type == "algebra":
            return self.generate_algebra_problem()
        elif problem_type == "geometry":
            return self.generate_geometry_problem()
        elif problem_type == "calculus":
            return self.generate_calculus_problem()
        elif problem_type == "word":
            return self.generate_word_problem()

    def generate_algebra_problem(self):
        """
        Generate an algebra problem.

        Returns:
            tuple: (problem_statement, solution)
        """
        x = sp.symbols('x')

        if self.difficulty == 'Easy':
            a = random.randint(1, 5)
            b = random.randint(1, 10)
            c = random.randint(1, 20)
            equation = sp.Eq(a * x + b, c)
            solution = sp.solve(equation, x)[0]
            problem = f"Solve for x: {sp.latex(equation)}"

        elif self.difficulty == 'Medium':
            a = random.randint(1, 5)
            b = random.randint(-10, 10)
            c = random.randint(-20, 20)
            equation = sp.Eq(a * x ** 2 + b * x + c, 0)
            solution = sp.solve(equation, x)
            problem = f"Solve for x: {sp.latex(equation)}"

        else:  # Hard difficulty
            a = random.randint(1, 3)
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
            equation = sp.Eq(a * x ** 2 + b * x + c, 0)
            solution = sp.solve(equation, x)
            problem = f"Solve for x: {sp.latex(equation)}"

        return problem, solution

    def generate_geometry_problem(self):
        """
        Generate a geometry problem.

        Returns:
            tuple: (problem_statement, solution)
        """
        if self.difficulty == 'Easy':
            radius = random.randint(1, 5)
            area = sp.pi * radius ** 2
            problem = f"Find the area of a circle with radius {radius} units."
            return problem, float(area.evalf())

        elif self.difficulty == 'Medium':
            length = random.randint(5, 10)
            width = random.randint(5, 10)
            height = random.randint(5, 10)
            volume = length * width * height
            problem = f"Find the volume of a rectangular prism with length {length} units, width {width} units, and height {height} units."
            return problem, volume

        else:  # Hard difficulty
            a = random.randint(5, 15)
            b = random.randint(5, 15)
            c = sp.sqrt(a ** 2 + b ** 2)
            problem = f"Given a right triangle with legs of length {a} units and {b} units, find the length of the hypotenuse."
            return problem, float(c.evalf())

    def generate_calculus_problem(self):
        """
        Generate a calculus problem.

        Returns:
            tuple: (problem_statement, solution)
        """
        x = sp.symbols('x')

        if self.difficulty == 'Easy':
            coefficients = [random.randint(1, 5) for _ in range(3)]
            function = coefficients[0] * x ** 2 + coefficients[1] * x + coefficients[2]
            derivative = sp.diff(function, x)
            problem = f"Find the derivative of f(x) = {sp.latex(function)}"
            return problem, derivative

        elif self.difficulty == 'Medium':
            function = sp.sin(x) + sp.cos(x)
            derivative = sp.diff(function, x)
            problem = f"Find the derivative of f(x) = sin(x) + cos(x)"
            return problem, derivative

        else:  # Hard difficulty
            function = sp.exp(x) * sp.log(x)
            derivative = sp.diff(function, x)
            problem = f"Find the derivative of f(x) = e^x * ln(x)"
            return problem, derivative

    def generate_word_problem(self):
        """
        Generate a word problem.

        Returns:
            tuple: (problem_statement, solution)
        """
        if self.difficulty == 'Easy':
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            problem = f"A farmer has {num1} apples. They buy {num2} more apples. How many apples do they have now?"
            solution = num1 + num2

        elif self.difficulty == 'Medium':
            num1 = random.randint(10, 50)
            num2 = random.randint(1, 10)
            problem = f"A car travels at {num1} miles per hour. How far will it travel in {num2} hours?"
            solution = num1 * num2

        else:  # Hard difficulty
            distance = random.randint(50, 200)
            time = random.randint(1, 5)
            speed = distance / time
            problem = f"A train travels {distance} miles in {time} hours. What is its average speed in miles per hour?"
            solution = speed

        return problem, solution

    def solve_problem(self, num1, num2, operation):
        """
        Solve a basic arithmetic problem.

        Args:
            num1 (int): First number
            num2 (int): Second number
            operation (str): Mathematical operation ('+', '-', '*', or '/')

        Returns:
            float: Solution to the problem
        """
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            if num2 == 0:
                raise ValueError("Division by zero is not allowed")
            return num1 / num2
        else:
            raise ValueError(f"Unsupported operation: {operation}")

    def explain_problem(self, problem, solution):
        """
        Provide an explanation for the given problem and solution.

        Args:
            problem (str): The problem statement
            solution: The solution to the problem

        Returns:
            str: Explanation of how to solve the problem
        """
        # Basic arithmetic problems
        if '+' in problem or '-' in problem or '*' in problem or '/' in problem:
            for op in ['+', '-', '*', '/']:
                if op in problem:
                    parts = problem.split(op)
                    if len(parts) == 2:
                        try:
                            num1 = float(parts[0].strip())
                            num2 = float(parts[1].strip())

                            if op == '+':
                                return f"Add {num1} and {num2}. The sum is {solution}."
                            elif op == '-':
                                return f"Subtract {num2} from {num1}. The difference is {solution}."
                            elif op == '*':
                                return f"Multiply {num1} by {num2}. The product is {solution}."
                            elif op == '/':
                                return f"Divide {num1} by {num2}. The quotient is {solution}."
                        except ValueError:
                            pass

        # Algebra problems
        if "Solve for x:" in problem:
            return f"To solve this equation, isolate x on one side. The solution is x = {solution}."

        # Geometry problems
        if "circle" in problem and "area" in problem:
            return f"To find the area of a circle, use the formula A = πr². The area is {solution} square units."

        if "triangle" in problem and "hypotenuse" in problem:
            return f"To find the hypotenuse of a right triangle, use the Pythagorean theorem: a² + b² = c². The hypotenuse is {solution} units."

        if "volume" in problem and "rectangular prism" in problem:
            return f"To find the volume of a rectangular prism, multiply length × width × height. The volume is {solution} cubic units."

        # Calculus problems
        if "derivative" in problem:
            return f"To find the derivative, apply the differentiation rules. The derivative is {solution}."

        # Word problems
        if "farmer" in problem and "apples" in problem:
            return f"Add the initial number of apples to the number of apples bought. The total is {solution} apples."

        if "car travels" in problem and "miles per hour" in problem:
            return f"Multiply the speed (miles per hour) by the time (hours) to get the distance. The distance is {solution} miles."

        if "train travels" in problem and "speed" in problem:
            return f"Divide the total distance by the time to get the speed. The speed is {solution} miles per hour."

        # Default explanation
        return f"The solution to this problem is {solution}."

    def get_random_numbers(self, difficulty, range_start=1, range_end=10):
        """
        Generate random numbers based on difficulty level.

        Args:
            difficulty (str): Difficulty level ('Easy', 'Medium', or 'Hard')
            range_start (int): Starting range for random numbers
            range_end (int): Ending range for random numbers

        Returns:
            tuple: Two random numbers
        """
        if difficulty == 'Easy':
            return random.randint(1, 10), random.randint(1, 10)
        elif difficulty == 'Medium':
            return random.randint(range_start, 20), random.randint(range_start, 20)
        else:  # Hard difficulty
            return random.randint(range_start, 50), random.randint(range_start, 50)

    def make_divisible(self, num1, extended_range=False):
        """
        Ensure a number divides another without remainder.

        Args:
            num1 (int): The number to be divided
            extended_range (bool): Whether to use an extended range of divisors

        Returns:
            int: A divisor that divides num1 without remainder
        """
        if num1 == 0:
            return 1  # Avoid division by zero issues

        if extended_range:
            divisors = [i for i in range(1, 21) if num1 % i == 0]
        else:
            divisors = [i for i in range(1, 11) if num1 % i == 0]

        if not divisors:
            return 1  # If no divisors found, return 1

        return random.choice(divisors)

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


class MathTutor
