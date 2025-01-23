import json
import tkinter as tk
from tkinter import messagebox

# Store quizzes and user data
quizzes = []
users = []


# Load existing data from JSON files
def load_data():
    global quizzes
    global users

    try:
        with open("quizzes.json", "r") as file:
            quizzes = json.load(file)
    except FileNotFoundError:
        quizzes = []

    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []


# Save data to JSON files
def save_data():
    with open("quizzes.json", "w") as file:
        json.dump(quizzes, file)
    with open("users.json", "w") as file:
        json.dump(users, file)


# Create a new user
def create_user(username, password):
    user = {"username": username, "password": password, "quiz_results": {}}
    users.append(user)
    save_data()


# User login
def login(username, password):
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None


# Take a quiz
def take_quiz(quiz, user):
    score = 0
    for question in quiz["questions"]:
        print(question["question"])
        for i, option in enumerate(question["options"]):
            print(f"{i + 1}. {option}")

        answer = int(input("Your answer (index): "))
        if answer == question["correct_answer"]:
            score += 1

    user["quiz_results"][quiz["title"]] = score
    save_data()

    # Display the score
    print(f"\nYour score for '{quiz['title']}': {score}/{len(quiz['questions'])}\n")
    return score


# List available quizzes
def list_quizzes():
    for i, quiz in enumerate(quizzes, 1):
        print(f"{i}. {quiz['title']}")


# List quiz results for a user
def list_quiz_results(user):
    print("Quiz Results:")
    for quiz_title, score in user["quiz_results"].items():
        print(f"{quiz_title}: {score}/{len(quizzes_by_title(quiz_title)['questions'])}")


# Function to get quizzes by title
def quizzes_by_title(title):
    for quiz in quizzes:
        if quiz["title"] == title:
            return quiz
    return None


# Main GUI window
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Quiz Generator")

        self.current_user = None

        # Load data
        load_data()

        # GUI components
        self.label = tk.Label(
            root, text="Welcome to Dynamic Quiz Generator", font=("Helvetica", 16)
        )
        self.label.pack(pady=20)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.create_user_button = tk.Button(
            root, text="Create User", command=self.create_user
        )
        self.create_user_button.pack(pady=10)

        # Additional buttons for logged-in users
        self.take_quiz_button = tk.Button(
            root, text="Take a Quiz", command=self.take_quiz
        )
        self.view_results_button = tk.Button(
            root, text="View Quiz Results", command=self.view_results
        )
        self.rankings_button = tk.Button(
            root, text="View Rankings", command=self.view_rankings
        )

    def login(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")

        tk.Label(login_window, text="Username: ").grid(row=0, column=0, padx=10, pady=5)
        username_entry = tk.Entry(login_window)
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(login_window, text="Password: ").grid(row=1, column=0, padx=10, pady=5)
        password_entry = tk.Entry(login_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        login_button = tk.Button(
            login_window,
            text="Login",
            command=lambda: self.process_login(
                username_entry.get(), password_entry.get(), login_window
            ),
        )
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def process_login(self, username, password, login_window):
        user = login(username, password)
        if user:
            self.current_user = user
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")

            # Hide login and create user buttons
            self.login_button.pack_forget()
            self.create_user_button.pack_forget()

            # Show additional buttons for logged-in users
            self.take_quiz_button.pack(pady=10)
            self.view_results_button.pack(pady=10)
            self.rankings_button.pack(pady=10)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_user(self):
        create_user_window = tk.Toplevel(self.root)
        create_user_window.title("Create User")

        tk.Label(create_user_window, text="Username: ").grid(
            row=0, column=0, padx=10, pady=5
        )
        username_entry = tk.Entry(create_user_window)
        username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(create_user_window, text="Password: ").grid(
            row=1, column=0, padx=10, pady=5
        )
        password_entry = tk.Entry(create_user_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        create_user_button = tk.Button(
            create_user_window,
            text="Create User",
            command=lambda: self.process_create_user(
                username_entry.get(), password_entry.get(), create_user_window
            ),
        )
        create_user_button.grid(row=2, column=0, columnspan=2, pady=10)

    def process_create_user(self, username, password, create_user_window):
        create_user(username, password)
        messagebox.showinfo("User Created", f"User {username} created successfully!")

        # Hide create user button after user creation
        self.create_user_button.pack_forget()

        # Show login button
        self.login_button.pack(pady=10)

    def take_quiz(self):
        if not quizzes:
            messagebox.showinfo("No Quizzes", "There are no quizzes available.")
            return

        quiz_selection_window = tk.Toplevel(self.root)
        quiz_selection_window.title("Select Quiz")

        tk.Label(quiz_selection_window, text="Choose a quiz:").grid(
            row=0, column=0, padx=10, pady=5
        )

        quiz_var = tk.StringVar(quiz_selection_window)
        quiz_var.set(quizzes[0]["title"])

        quiz_menu = tk.OptionMenu(
            quiz_selection_window, quiz_var, *([quiz["title"] for quiz in quizzes])
        )
        quiz_menu.grid(row=0, column=1, padx=10, pady=5)

        take_quiz_button = tk.Button(
            quiz_selection_window,
            text="Take Quiz",
            command=lambda: self.process_take_quiz(
                quiz_var.get(), quiz_selection_window
            ),
        )
        take_quiz_button.grid(row=1, column=0, columnspan=2, pady=10)

    def process_take_quiz(self, selected_quiz, quiz_selection_window):
        quiz = quizzes_by_title(selected_quiz)
        take_quiz(quiz, self.current_user)
        messagebox.showinfo(
            "Quiz Completed", f"You have completed the quiz '{selected_quiz}'."
        )
        quiz_selection_window.destroy()

    def view_results(self):
        if not self.current_user or not self.current_user["quiz_results"]:
            messagebox.showinfo(
                "No Results", "No quiz results available for the current user."
            )
            return

        view_results_window = tk.Toplevel(self.root)
        view_results_window.title("View Quiz Results")

        tk.Label(view_results_window, text="Quiz Results:").pack(pady=10)

        results_text = ""
        for quiz_title, score in self.current_user["quiz_results"].items():
            results_text += "{}: {}/{}\n".format(
                quiz_title, score, len(quizzes_by_title(quiz_title)["questions"])
            )

        results_label = tk.Label(view_results_window, text=results_text)
        results_label.pack(pady=10)

    def view_rankings(self):
        if not users:
            messagebox.showinfo("No Users", "There are no users available.")
            return

        rankings_window = tk.Toplevel(self.root)
        rankings_window.title("Quiz Rankings")

        tk.Label(rankings_window, text="Quiz Rankings:").pack(pady=10)

        # Sort users by total score
        sorted_users = sorted(
            users, key=lambda x: sum(x["quiz_results"].values()), reverse=True
        )

        rankings_text = ""
        for i, user in enumerate(sorted_users, 1):
            rankings_text += f"{i}. {user['username']} - Total Score: {sum(user['quiz_results'].values())}\n"

        rankings_label = tk.Label(rankings_window, text=rankings_text)
        rankings_label.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
