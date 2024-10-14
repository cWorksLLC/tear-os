import time
from datetime import datetime, date
import pytz
import json
import calendar
import os

# --- File System ---
file_system = {
    "root": {
        "home": {
            "user": {
                "documents": {},
                "downloads": {},
                "pictures": {},
                "music": {},
                "myfile.txt": "This is the content of my file."
            }
        },
        "bin": {},  # For system binaries (you can add commands here later)
        "etc": {},  # For system configuration files
        "tearApps": {}
    }
}



current_dir = ["root", "home", "user"]  # Start in the user directory

def list_directory():
    temp_dir = file_system
    for d in current_dir:
        temp_dir = temp_dir[d]
    print(" ".join(temp_dir.keys()))

def change_directory(new_dir):
    global current_dir
    if new_dir == "..":  # Go up one directory
        if len(current_dir) > 1:
            current_dir.pop()
    else:
        # Check if the new directory exists
        temp_dir = file_system
        for d in current_dir + [new_dir]:
            if d not in temp_dir:
                print("Invalid directory.")
                return
            temp_dir = temp_dir[d]
        current_dir.append(new_dir)

# --- File Management Commands ---
def make_directory(dir_name):
    global current_dir
    temp_dir = file_system
    for d in current_dir:
        temp_dir = temp_dir[d]
    if dir_name in temp_dir:
        print(f"Directory '{dir_name}' already exists.")
    else:
        temp_dir[dir_name] = {}
        print(f"Directory '{dir_name}' created.")

def create_file(file_name):
    global current_dir
    temp_dir = file_system
    for d in current_dir:
        temp_dir = temp_dir[d]
    if file_name in temp_dir:
        print(f"File '{file_name}' already exists.")
    else:
        temp_dir[file_name] = ""
        print(f"File '{file_name}' created.")

def remove(item_name):
    global current_dir
    temp_dir = file_system
    for d in current_dir:
        temp_dir = temp_dir[d]
    if item_name in temp_dir:
        del temp_dir[item_name]
        print(f"'{item_name}' removed.")
    else:
        print(f"'{item_name}' not found.")

# --- User Data Management ---
def load_user_data():
    try:
        with open("user_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if no user data file exists

def save_user_data(user_data):
    with open("user_data.json", "w") as f:
        json.dump(user_data, f)

# --- Global Settings ---
osname = "TearOS beta 1.3.1"
default_dir = "home"
user_tz = None  # Will be set during login

# --- Appearance Mods ---
class Theme:
    def __init__(self, prompt_color="white", dir_color="blue"):
        self.prompt_color = prompt_color
        self.dir_color = dir_color

default_theme = Theme()  # You can create more themes later

# --- App Framework ---
class App:
    def __init__(self, name, description, usage, function):
        self.name = name
        self.description = description
        self.usage = usage
        self.function = function

    def run(self, *args):
        self.function(*args)

# --- Built-in Apps ---
def app_calculator():
    print("Simple Calculator")
    while True:
        try:
            num1 = float(input("Enter first number: "))
            op = input("Enter operator (+, -, *, /): ")
            num2 = float(input("Enter second number: "))

            if op == "+":
                print(num1 + num2)
            elif op == "-":
                print(num1 - num2)
            # ... (rest of the calculator code remains the same)
        except ValueError:
            print("Invalid input. Please enter numbers only.")

def app_guessing_game():
    print("Number Guessing Game")
    secret_number = 42  # You can change this to any number
    guesses_left = 5
    while guesses_left > 0:
        try:
            guess = int(input("Guess a number between 1 and 100: "))
            if guess == secret_number:
                print("Congratulations! You guessed it!")
                break
            elif guess < secret_number:
                print("Too low! Try again.")
            else:
                print("Too high! Try again.")
            guesses_left -= 1
        except ValueError:
            print("Invalid input. Please enter a number.")
    if guesses_left == 0:
        print(f"You ran out of guesses. The number was {secret_number}.")

def app_text_editor():
    print("Simple Text Editor")
    filename = input("Enter filename: ")
    try:
        # Get the full path based on the current directory
        filepath = "/".join(current_dir) + "/" + filename

        with open(filepath, "a+") as f:
            print("Enter text (type ':q' to quit):")
            while True:
                line = input()
                if line == ":q":
                    break
                f.write(line + "\n")
        print(f"File '{filename}' saved.")
    except Exception as e:
        print(f"Error: {e}")
def app_calendar():
    print("Calendar App")
    while True:
        try:
            year = int(input("Enter year (e.g., 2024): "))
            month = int(input("Enter month (1-12): "))
            if 1 <= month <= 12:
                print(calendar.month(year, month))
                break
            else:
                print("Invalid month. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter numbers only.")

# ... (other code)

# Create app instances
calculator = App("calculator", "A simple calculator", "calculator", app_calculator)
guessing_game = App("guess", "Number guessing game", "guess", app_guessing_game)
text_editor = App("editor", "A simple text editor", "editor [filename]", app_text_editor)
calendar_app = App("calendar", "Displays a calendar", "calendar", app_calendar)

apps = {  # Define the apps dictionary here
    calculator.name: calculator,
    guessing_game.name: guessing_game,
    text_editor.name: text_editor,
    calendar_app.name: calendar_app
}

# --- Time zone selection ---
def choose_timezone():
    timezones = pytz.common_timezones
    print("Available Time Zones:")
    for i, tz in enumerate(timezones):
        print(f"{i+1}. {tz}")
    while True:
        try:
            choice = int(input("Enter the number of your time zone: "))
            if 1 <= choice <= len(timezones):
                return timezones[choice - 1]
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_current_time():
    if user_tz:
        return datetime.now(user_tz).strftime("%H:%M:%S")
    else:
        return "Time zone not set."

def get_current_date():
    if user_tz:
        return date.today().strftime("%Y-%m-%d")  # Use date.today() directly
    else:
        return "Time zone not set."

def print_help():
    print("Commands:")
    print("- help: Show this help message.")
    print("- ls: List files and directories in the current directory.")
    print("- cd [directory]: Change directory.")
    print("- time: Display the current time.")
    print("- date: Display the current date.")
    print("- apps: List available apps.")
    print("- [app name]: Run an app.")
    print("- exit: Exit TearOS.")
    print("- logout: Logout from the current user.")
    print("- mkdir [directory_name]: Create a new directory.")
    print("- touch [file_name]: Create a new file.")
    print("- rm [item_name]: Remove a file or directory.")

def list_apps():
    print("Available Apps:")
    for app_name in apps:
        print(f"- {app_name}: {apps[app_name].description}")

def run_app(app_name):
    global apps  # Tell Python to use the global apps variable
    if app_name in apps:
        apps[app_name].run()
    else:
        print("App not found.")

# --- Main OS Loop ---
def main():
    global username, dir, user_tz
    user_data = load_user_data()

    while True:
        print("1. Login")
        print("2. Create New Account")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if username in user_data and user_data[username] == password:
                print(f"Welcome back, {username}!")
                user_tz = pytz.timezone(user_data.get(username + "_timezone", "UTC"))
                break # Exit the login/signup loop
            else:
                print("Invalid username or password.")
        elif choice == "2":
            username = input("New Username: ")
            password = input("New Password: ")
            if username in user_data:
                print("Username already exists.")
            else:
                user_data[username] = password
                user_tz = pytz.timezone(choose_timezone())
                user_data[username + "_timezone"] = user_tz.zone  # Store time zone
                save_user_data(user_data)
                print(f"Account created successfully, {username}!")
                break # Exit the login/signup loop
        else:
            print("Invalid choice.")

    print(f"Welcome to {osname}!, {username}!")
    print("Type 'help' for a list of commands!")

    current_dir = [default_dir]  # Start in the home directory

    # MAIN OS LOOP (This loop was missing)
    while True: 
        prompt = f"{username}@{osname}:{'/'.join(current_dir)} $"
        prompt = f"\033[32m{prompt}\033[0m"  # Apply green color and reset

        command = input(prompt)

        if command == "help":
            print_help()
        elif command == "ls":
            list_directory()
        elif command.startswith("cd"):
            parts = command.split(" ", 1)
            if len(parts) == 2:
                change_directory(parts[1])
            else:
                print("Invalid command. Usage: cd [directory]")
        elif command == "time":
            print(get_current_time())
        elif command == "date":
            print(get_current_date())
        elif command == "apps":
            list_apps()
        elif command.startswith("mkdir"):
            make_directory(command.split()[1])
        elif command.startswith("touch"):
            create_file(command.split()[1])
        elif command.startswith("rm"):
            remove(command.split()[1])
        elif command in apps:
            run_app(command)
        elif command == "exit":
            print("Exiting TearOS...")
            break # Exit the OS loop
        elif command == "logout":
            print("Logging out...")
            break # Exit the OS loop, going back to login/signup
        else:
            print("Invalid command.")
        
if __name__ == "__main__":
    main()

