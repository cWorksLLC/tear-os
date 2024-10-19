import random
import time
from datetime import datetime, date
import pytz
import json
import calendar
import os
import threading
import queue
import requests
import shutil
import subprocess
import sys

# --- Configuration ---

APPS_DIR = "/tearOS/apps"
FILE_SYSTEM_DATA_FILE = "file_system_data.json"  # File to store file system data
SETTINGS_FILE = "tearOS_settings.json"

# --- Load/Save Settings ---
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"run_mode": "built-in"}  # Default to running built-in apps directly

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

# --- File System ---
def load_file_system():
    """Loads the file system data from the data file."""
    try:
        with open(FILE_SYSTEM_DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {  # Return the default file system if the file is not found
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
                "bin": {},
                "etc": {},
                "tearApps": {}
            }
        }

def save_file_system():
    """Saves the current file system data to the data file."""
    with open(FILE_SYSTEM_DATA_FILE, "w") as f:
        json.dump(file_system, f, indent=4)  # Use indent for readability

# Load the file system at startup
file_system = load_file_system()

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
        save_file_system()  # Save the file system after creating the directory

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
        save_file_system()  # Save the file system after creating the file


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
            elif op == "*":
                print(num1 * num2)
            elif op == "/":
                if num2 == 0:
                    print("Cannot divide by zero.")
                else:
                    print(num1 / num2)
            else:
                print("Invalid operator.")
        except ValueError:
            print("Invalid input. Please enter numbers only.")

def app_guessing_game():
    print("Number Guessing Game")
    secret_number = random.randint(1, 100)
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

def app_text_editor(filename=None):
    print("Simple Text Editor")
    if filename is None:
        filename = input("Enter filename: ")
    try:
        # Get the full path based on the current directory
        filepath = os.path.join(*current_dir, filename)

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

def app_store():
    print("Welcome to the TearOS App Store!")
    while True:
        print("1. List Available Apps")
        print("2. Install App")
        print("3. Update Apps")
        print("4. Back to TearOS")
        choice = input("Enter your choice: ")

        if choice == "1":
            list_available_apps()
        elif choice == "2":
            install_app()
        elif choice == "3":
            update_apps()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
            



# --- Create app instances ---
calculator = App("calculator", "A simple calculator", "calculator", app_calculator)
guessing_game = App("guess", "Number guessing game", "guess", app_guessing_game)
text_editor = App("editor", "A simple text editor", "editor [filename]", app_text_editor)
calendar_app = App("calendar", "Displays a calendar", "calendar", app_calendar)
app_store = App("appstore", "TearOS App Store", "appstore", app_store)

apps = {
    calculator.name: calculator,
    guessing_game.name: guessing_game,
    text_editor.name: text_editor,
    calendar_app.name: calendar_app,
    app_store.name: app_store
}

# --- Functions to list, install, and update apps ---
def list_available_apps():
    pass
    print("tearOS 1.3 series has stopped recieving support.....go to 1.4...")

def install_app():
    pass
    print("installing apps isnt supported anymore for 1.3 series...")

def update_apps():
    print("Updating apps...")
    # Implement logic to check for updates and update apps
    # ... (Update code)
    print("Apps updated successfully!")

# --- Login/Signup ---
def login():
    username = input("Username: ")
    password = input("Password: ")

# --- Time zone selection ---
def choose_timezone():
    timezones = pytz.common_timezones
    print("Available Time Zones:")
    for i, tz in enumerate(timezones):
        print(f"{i+1}. {tz}")

    def get_input(queue):
        while True:
            try:
                choice = int(input("Enter the number of your time zone: "))
                queue.put(choice)
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

    # Create a queue to communicate between threads
    input_queue = queue.Queue()

    # Start a separate thread to get user input
    input_thread = threading.Thread(target=get_input, args=(input_queue,))
    input_thread.daemon = True  # Allow main thread to exit even if input thread is running
    input_thread.start()

    while True:
        if not input_queue.empty():
            choice = input_queue.get()
            if 1 <= choice <= len(timezones):
                return timezones[choice - 1]
            else:
                print("Invalid choice. Please enter a number from the list.")
        time.sleep(0.1)  # Avoid busy-waiting

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
    print("- install [app_package.tear]: Install an app from a .tear package.")

def run_app(app_name):
    """Runs an app based on the current run mode setting."""
    global settings

    if settings["run_mode"] == "built-in" and app_name in apps:
    
        apps[app_name].run()  # Run built-in function directly
    else:
        # Assume .tear app if not in built-in mode or not found in 'apps'
        app_dir = os.path.join(APPS_DIR, app_name)
        app_info_path = os.path.join(app_dir, "app_info.json")

        try:
            with open(app_info_path, "r") as f:
                app_info = json.load(f)

            entry_point = app_info.get("entry_point")
            if not entry_point:
                print("Error: App does not specify an entry point.")
                return

            app_process = subprocess.Popen(
                ["python", os.path.join(app_dir, entry_point)],
                cwd=app_dir
            )

        except (FileNotFoundError, json.JSONDecodeError, subprocess.CalledProcessError) as e:
            print(f"Error running app: {e}")

def list_apps():
    """Lists all available apps, considering the run mode."""
    global settings

    if settings["run_mode"] == "built-in":
        print("Built-in Apps:")
        for app_name in apps:
            print(f"- {app_name}: {apps[app_name].description}")
    else:  # "tear" mode
        print("Installed .tear Apps:")
        if os.path.exists(APPS_DIR):
            for app_folder in os.listdir(APPS_DIR):
                app_info_path = os.path.join(APPS_DIR, app_folder, "app_info.json")
                if os.path.exists(app_info_path):
                    with open(app_info_path, "r") as f:
                        app_info = json.load(f)
                        print(f"- {app_info['name']}: {app_info['description']}")
                else:
                    print(f"- {app_folder}: (App information not available)")
        else:
            print("No .tear apps installed.")
# --- Settings ---
def change_settings():
    """Allows the user to change TearOS settings."""
    global settings  # Add this line to declare settings as global

    settings = load_settings()  # Load settings at the beginning of the function
    while True:
        print("\nTearOS Settings:")
        print("1. App Run Mode:", settings["run_mode"])
        print("2. Back to TearOS")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nApp Run Modes:")
            print("1. Built-in (run apps directly)")
            print("2. .tear (run apps from .tear packages)")

            mode_choice = input("Enter your choice: ")
            if mode_choice == "1":
                settings["run_mode"] = "built-in"
                print("App run mode set to 'built-in'.")
            elif mode_choice == "2":
                settings["run_mode"] = "tear"
                print("App run mode set to '.tear'.")
            else:
                print("Invalid choice.")
        elif choice == "2":
            save_settings(settings)
            break
        else:
            print("Invalid choice.")


# --- Main OS Loop ---
def main():
    global username, dir, user_tz, settings  # user_tz is not used anymore
    user_data = load_user_data()
    settings = load_settings()

    logged_in = False # Flag to track login status

    while not logged_in: # Loop until successful login
        print("1. Login")
        print("2. Create New Account")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if username in user_data and user_data[username] == password:
                print(f"Welcome back, {username}!")
                logged_in = True # Set flag to True to exit loop
                break
            elif username in user_data:
                print("Incorrect password.")
            else:
                print("Invalid username or password.")
        elif choice == "2":
            username = input("New Username: ")
            password = input("New Password: ")
            if username in user_data:
                print("Username already exists.")
            else:
                user_data[username] = password
                save_user_data(user_data)
                print(f"Account created successfully, {username}!")
                logged_in = True # Set flag to True after account creation
                break # Exit the loop after successful account creation
        else:
            print("Invalid choice.")

    # This part will only execute after successful login or account creation
    print(f"Welcome to {osname}!, {username}!")
    print("Type 'help' for a list of commands!")

    # MAIN OS LOOP
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
        elif command == "appstore":
            app_store.run()
        elif command in apps:
            run_app(command)
        elif command == "exit":
            print("Exiting TearOS...")
            save_file_system()
            break # Exit the OS loop
        elif command == "logout":
            print("Logging out...")
            save_file_system()
            break  # Exit the OS loop, going back to login/signup
        elif command.startswith("install"):
            parts = command.split(" ", 1)
            if len(parts) == 2:
                install_app(parts[1])
            else:
                print("Invalid command. Usage: install [app_package.tear]")
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

