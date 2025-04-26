import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
import json
import os
import bcrypt  # For password hashing (install: pip install bcrypt)

# ... (MathTutorAI, User classes)

class UserDataAccess:
    def __init__(self, db_file="users.json"):  # Or use a database
        self.db_file = db_file
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.db_file, "w") as f:
            json.dump(self.users, f)

    def create_user(self, username, password, grade_level=0, difficulty="Easy", language="en"):
        if username in self.users:
            raise ValueError("Username already exists")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
        self.users[username] = {
            "hashed_password": hashed_password,
            "grade_level": grade_level,
            "difficulty": difficulty,
            "language": language,
            "correct_answers": 0,
            "total_questions": 0
        }
        self.save_users()

    def get_user(self, username):
        if username in self.users:
            return self.users[username]
        return None

    def update_user(self, username, data):
        if username in self.users:
            self.users[username].update(data)
            self.save_users()
        else:
            raise ValueError("User not found")

    def verify_password(self, username, password):
        user_data = self.get_user(username)
        if user_data:
            return bcrypt.checkpw(password.encode('utf-8'), user_data["hashed_password"].encode('utf-8'))
        return False


class MathTutorGUI:  # Renamed from MathTutor for clarity
    def __init__(self, root):
        self.root = root
        self.root.title("Math Tutor AI")
        self.user_data_access = UserDataAccess()
        self.current_user = None  # No user logged in initially
        self.create_main_menu()

    def create_main_menu(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        main_menu_frame = ttk.Frame(self.root)
        main_menu_frame.pack(pady=20)

        ttk.Label(main_menu_frame, text="Welcome to Math Tutor AI", font=("Arial", 16)).pack(pady=10)
        ttk.Button(main_menu_frame, text="Login", command=self.show_login).pack(pady=5)
        ttk.Button(main_menu_frame, text="Register", command=self.show_register).pack(pady=5)

    def show_login(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = ttk.Frame(self.root)
        login_frame.pack(pady=20)

        ttk.Label(login_frame, text="Login", font=("Arial", 14)).pack(pady=10)
        ttk.Label(login_frame, text="Username:").pack()
        username_entry = ttk.Entry(login_frame)
        username_entry.pack()
        ttk.Label(login_frame, text="Password:").pack()
        password_entry = ttk.Entry(login_frame, show="*")  # Hide password
        password_entry.pack()

        def do_login():
            username = username_entry.get()
            password = password_entry.get()
            if self.user_data_access.verify_password(username, password):
                user_data = self.user_data_access.get_user(username)
                self.current_user = User(username=username, **user_data)
                self.show_tutoring_interface()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

        ttk.Button(login_frame, text="Login", command=do_login).pack(pady=10)
        ttk.Button(login_frame, text="Back to Main Menu", command=self.create_main_menu).pack(pady=5)

    def show_register(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        register_frame = ttk.Frame(self.root)
        register_frame.pack(pady=20)

        ttk.Label(register_frame, text="Register", font=("Arial", 14)).pack(pady=10)
        ttk.Label(register_frame, text="Username:").pack()
        username_entry = ttk.Entry(register_frame)
        username_entry.pack()
        ttk.Label(register_frame, text="Password:").pack()
        password_entry = ttk.Entry(register_frame, show="*")
        password_entry.pack()

        def do_register():
            username = username_entry.get()
            password = password_entry.get()
            try:
                self.user_data_access.create_user(username, password)
                messagebox.showinfo("Registration Successful", "Please log in.")
                self.show_login()
            except ValueError as e:
                messagebox.showerror("Registration Failed", str(e))

        ttk.Button(register_frame, text="Register", command=do_register).pack(pady=10)
        ttk.Button(register_frame, text="Back to Main Menu", command=self.create_main_menu).pack(pady=5)

    def show_tutoring_interface(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        if not self.current_user:
            self.create_main_menu()  # Go back if no user
            return

        tutoring_frame = ttk.Frame(self.root)
        tutoring_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Initialize MathTutor with the current user
        self.math_tutor = MathTutor(tutoring_frame, self.current_user, self.user_data_access)
        # Add a logout button
        logout_button = ttk.Button(tutoring_frame, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

    def logout(self):
        self.current_user = None
        self.create_main_menu()


class MathTutor:
    def __init__(self, root, user, user_data_access):
        self.root = root
        self.user = user
        self.user_data_access = user_data_access
        self.tutor_ai = MathTutorAI()
        self.tutor_ai.grade_level = self.user.grade_level
        self.tutor_ai.difficulty = self.user.difficulty
        self.tutor_ai.language = self.user.language
        # ... (rest of your MathTutor logic, using self.user and self.user_data_access)
        self.create_widgets()

    def save_progress(self):
        # Update user data via the data access layer
        user_data = {
            "grade_level": self.tutor_ai.grade_level,
            "difficulty": self.tutor_ai.difficulty,
            "correct_answers": self.user.correct_answers,
            "total_questions": self.user.total_questions,
            "language": self.tutor_ai.language
        }
        self.user_data_access.update_user(self.user.username, user_data)
        self.feedback_var.set("Progress saved! 💾")

    def create_widgets(self):
        # ... (Your GUI widgets, adapted to the frame)
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = MathTutorGUI(root)
    root.mainloop()