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
            while num2 == 0:
                num2 = random.randint(-20, 20)
            # Make sure division results in a whole number for simplicity
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
            equation = sp.Eq(a*x + b, c)
            solution = sp.solve(equation, x)[0]
            problem = f"Solve for x: {sp.latex(equation)}"
            
        elif self.difficulty == 'Medium':
            a = random.randint(1, 5)
            b = random.randint(-10, 10)
            c = random.randint(-20, 20)
            equation = sp.Eq(a*x**2 + b*x + c, 0)
            solution = sp.solve(equation, x)
            problem = f"Solve for x: {sp.latex(equation)}"
            
        else:  # Hard difficulty
            a = random.randint(1, 3)
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
            equation = sp.Eq(a*x**2 + b*x + c, 0)
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
            area = sp.pi * radius**2
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
            c = sp.sqrt(a**2 + b**2)
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
            function = coefficients[0]*x**2 + coefficients[1]*x + coefficients[2]
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
        self.math_tutor = MathTutorAI()
        
        # Create and layout the main frames
        self.create_widgets()
        
        # Store the current problem and solution
        self.current_problem = None
        self.current_solution = None
        
        # History of problems
        self.problem_history = []
        
    def create_widgets(self):
        """Create and organize all the GUI widgets"""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Math Tutor AI", font=('Helvetica', 18, 'bold'))
        self.title_label.pack(pady=(0, 20))
        
        # Settings frame
        self.settings_frame = ttk.LabelFrame(self.main_frame, text="Settings", padding="10")
        self.settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Grade level selection
        ttk.Label(self.settings_frame, text="Grade Level:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.grade_var = tk.StringVar(value="0")
        grade_values = [str(i) for i in range(13)]  # 0-12 (Kindergarten to 12th grade)
        grade_descriptions = ["Kindergarten"] + [f"{i}st" if i % 10 == 1 and i != 11 else 
                                                f"{i}nd" if i % 10 == 2 and i != 12 else 
                                                f"{i}rd" if i % 10 == 3 and i != 13 else 
                                                f"{i}th" for i in range(1, 13)]
        
        grade_combobox_values = [f"{grade_values[i]} - {grade_descriptions[i]}" for i in range(len(grade_values))]
        self.grade_combobox = ttk.Combobox(self.settings_frame, values=grade_combobox_values, 
                                          state="readonly", width=25)
        self.grade_combobox.current(0)
        self.grade_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.grade_combobox.bind("<<ComboboxSelected>>", self.update_grade_level)
        
        # Difficulty selection
        ttk.Label(self.settings_frame, text="Difficulty:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.difficulty_var = tk.StringVar(value="Easy")
        self.difficulty_combobox = ttk.Combobox(self.settings_frame, values=["Easy", "Medium", "Hard"], 
                                              textvariable=self.difficulty_var, state="readonly", width=10)
        self.difficulty_combobox.current(0)
        self.difficulty_combobox.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        self.difficulty_combobox.bind("<<ComboboxSelected>>", self.update_difficulty)
        
        # Generate problem button
        self.generate_button = ttk.Button(self.settings_frame, text="Generate Problem", 
                                        command=self.generate_new_problem)
        self.generate_button.grid(row=0, column=4, padx=5, pady=5, sticky=tk.E)
        
        # Problem display frame
        self.problem_frame = ttk.LabelFrame(self.main_frame, text="Problem", padding="10")
        self.problem_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Problem text
        self.problem_text = scrolledtext.ScrolledText(self.problem_frame, height=5, width=50, 
                                                    font=('Helvetica', 12))
        self.problem_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.problem_text.config(state=tk.DISABLED)
        
        # Answer frame
        self.answer_frame = ttk.LabelFrame(self.main_frame, text="Your Answer", padding="10")
        self.answer_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Answer entry
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(self.answer_frame, textvariable=self.answer_var, font=('Helvetica', 12), width=20)
        self.answer_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())
        
        # Check answer button
        self.check_button = ttk.Button(self.answer_frame, text="Check Answer", command=self.check_answer)
        self.check_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Show solution button
        self.solution_button = ttk.Button(self.answer_frame, text="Show Solution", command=self.show_solution)
        self.solution_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Explanation frame
        self.explanation_frame = ttk.LabelFrame(self.main_frame, text="Explanation", padding="10")
        self.explanation_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Explanation text
        self.explanation_text = scrolledtext.ScrolledText(self.explanation_frame, height=8, width=50, 
                                                        font=('Helvetica', 11))
        self.explanation_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.explanation_text.config(state=tk.DISABLED)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                                   font=('Helvetica', 10), anchor=tk.W)
        self.status_bar.pack(fill=tk.X, padx=5, pady=5)
        
    def update_grade_level(self, event=None):
        """Update the grade level in the math tutor"""
        grade_text = self.grade_combobox.get()
        grade = int(grade_text.split(' ')[0])  # Extract the number from the combobox value
        self.math_tutor.set_grade_level(grade)
        self.status_var.set(f"Grade level set to {grade_text}")
        
    def update_difficulty(self, event=None):
        """Update the difficulty level in the math tutor"""
        difficulty = self.difficulty_var.get()
        self.math_tutor.set_difficulty(difficulty)
        self.status_var.set(f"Difficulty set to {difficulty}")
        
    def generate_new_problem(self):
        """Generate a new math problem"""
        try:
            # Clear previous answers and explanations
            self.answer_var.set("")
            self.set_explanation_text("")
            
            # Generate a new problem
            problem, solution = self.math_tutor.generate_problem()
            self.current_problem = problem
            self.current_solution = solution
            
            # Store in history
            self.problem_history.append((problem, solution))
            
            # Display the problem
            self.set_problem_text(problem)
            self.status_var.set("New problem generated")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating problem: {str(e)}")
            self.status_var.set("Error generating problem")
            
    def check_answer(self):
        """Check the user's answer against the solution"""
        if self.current_problem is None or self.current_solution is None:
            messagebox.showinfo("Info", "Please generate a problem first")
            return
            
        user_answer = self.answer_var.get().strip()
        
        if not user_answer:
            messagebox.showinfo("Info", "Please enter an answer")
            return
            
        try:
            # Convert user's answer to float or complex if possible
            try:
                user_val = float(user_answer)
                # For numerical solutions
                if isinstance(self.current_solution, (int, float)):
                    if isclose(user_val, float(self.current_solution), rel_tol=1e-2):
                        self.show_correct_answer()
                    else:
                        self.show_incorrect_answer()
                # For sympy solutions that may be a list
                elif hasattr(self.current_solution, '__iter__'):
                    # Check if answer matches any solution in the list
                    if any(isclose(user_val, float(sol), rel_tol=1e-2) 
                          for sol in self.current_solution if hasattr(sol, 'evalf')):
                        self.show_correct_answer()
                    else:
                        self.show_incorrect_answer()
                else:
                    # Try to convert sympy expression to float
                    try:
                        sol_val = float(self.current_solution.evalf())
                        if isclose(user_val, sol_val, rel_tol=1e-2):
                            self.show_correct_answer()
                        else:
                            self.show_incorrect_answer()
                    except:
                        # If conversion fails, show the solution
                        self.show_solution()
            except ValueError:
                # Non-numeric answers
                if str(user_answer) == str(self.current_solution):
                    self.show_correct_answer()
                else:
                    self.show_incorrect_answer()
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error checking answer: {str(e)}")
            self.status_var.set("Error checking answer")
            
    def show_correct_answer(self):
        """Display a correct answer message and explanation"""
        explanation = self.math_tutor.explain_problem(self.current_problem, self.current_solution)
        self.set_explanation_text(f"Correct! {explanation}")
        self.status_var.set("Answer is correct!")
        
    def show_incorrect_answer(self):
        """Display an incorrect answer message"""
        self.set_explanation_text(f"Incorrect. Try again or click 'Show Solution' for help.")
        self.status_var.set("Answer is incorrect")
        
    def show_solution(self):
        """Display the solution and explanation"""
        if self.current_problem is None or self.current_solution is None:
            messagebox.showinfo("Info", "Please generate a problem first")
            return
            
        explanation = self.math_tutor.explain_problem(self.current_problem, self.current_solution)
        
        # Format the solution nicely
        if isinstance(self.current_solution, (list, tuple)):
            solution_text = ", ".join(str(s) for s in self.current_solution)
        else:
            solution_text = str(self.current_solution)
            
        self.set_explanation_text(f"Solution: {solution_text}\n\n{explanation}")
        self.status_var.set("Solution shown")
        
    def set_problem_text(self, text):
        """Update the problem text display"""
        self.problem_text.config(state=tk.NORMAL)
        self.problem_text.delete(1.0, tk.END)
        self.problem_text.insert(tk.END, text)
        self.problem_text.config(state=tk.DISABLED)
        
    def set_explanation_text(self, text):
        """Update the explanation text display"""
        self.explanation_text.config(state=tk.NORMAL)
        self.explanation_text.delete(1.0, tk.END)
        self.explanation_text.insert(tk.END, text)
        self.explanation_text.config(state=tk.DISABLED)


def main():
    """Main function to launch the application"""
    root = tk.Tk()
    app = MathTutorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()