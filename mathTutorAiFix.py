import winsound
import json
import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sympy as sp
from math import isclose


class MathTutorAI:
    """
    A mathematics tutoring AI that generates and explains math problems
    of varying difficulty for different grade levels.
    """

    def __init__(self):
        """Initialize the MathTutorAI with default settings."""
        self.operations = ['+', '-', '*', '/']
        self.grade_level = 0
        self.difficulty = 'Easy'  # Default difficulty

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
        problem_type = random.choice(["algebra", "geometry", "calculus", "word"])

        if problem_type == "algebra":
            return self.generate_algebra_problem()
        elif problem_type == "geometry":
            return self.generate_geometry_problem()
        elif problem_type == "calculus":
            return self.generate_calculus_problem()
        elif problem_type == "word":
            return self.generate_word_problem()

    # Other methods remain unchanged...


class MathTutorApp:
    """A GUI application for the Math Tutor AI"""

    def __init__(self, root):
        """Initialize the application with a tkinter root window"""
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
        self

