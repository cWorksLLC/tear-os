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
import psutil
import time 

import time

start_time = time.time()
# Run the app code here
end_time = time.time()

execution_time = end_time - start_time
print(f"App execution time: {execution_time} seconds")

def uninstall_app(app_name):
    """Uninstalls a .tear app."""
    target_dir = os.path.join(APPS_DIR, app_name)

    if os.path.exists(target_dir):
        try:
            shutil.rmtree(target_dir)  # Delete the app's directory
            print(f"App '{app_name}' uninstalled successfully!")
        except OSError as e:
            print(f"Error uninstalling app: {e}")
    else:
        print(f"App '{app_name}' not found.")


# --- Command History ---
command_history = []
command_history_list = []

# --- Configuration ---
GITHUB_REPO = "https://api.github.com/repos/Alejandrix2456github/tearOS/contents/tearOS/apps"
APPS_DIR = "/tearOS/apps"
FILE_SYSTEM_DATA_FILE = "file_system_data.json"  # File to store file system data
SETTINGS_FILE = "tearOS_settings.json"

# --- Command History ---
def command_history(command):
    """Adds a command to the command history."""
    global command_history_list  # Use the new list variable name
    command_history_list.append(command)
    if len(command_history_list) > 10:
        command_history_list.pop(0)


# ... other imports ...

def list_running_processes():
    """Lists currently running processes."""
    print("Running Processes:")
    for process in psutil.process_iter():  # Use psutil.process_iter()
        try:
            process_info = process.as_dict(attrs=['pid', 'name', 'username'])
            print(f"PID: {process_info['pid']}, Name: {process_info['name']}, User: {process_info['username']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass  # Ignore processes that cannot be accessed



# Theme Change function
def change_theme(theme_name):
    global current_theme
    if theme_name in themes:
        current_theme = theme_name
        print(f"Theme changed to '{theme_name}'.")
    else:
        print(f"Invalid theme: '{theme_name}'. Available themes are: {', '.join(themes.keys())}")

# Theme Class
class Theme:
    def __init__(self, prompt_color, dir_color, text_color):
        self.prompt_color = prompt_color
        self.dir_color = dir_color
        self.text_color = text_color

# Theme Dictionary
themes = {
    "default": Theme("\033[32m", "\033[34m", "\033[0m"),  # Green prompt, blue dir, reset text
    "sunset": Theme("\033[33m", "\033[31m", "\033[0m"),  # Orange prompt, red dir, reset text
    "matrix": Theme("\033[32m", "\033[37m", "\033[0m"),  # Green prompt, white dir, reset text
    "pinker": Theme("\033[35m", "\033[38;5;206m", "\033[0m"), # Pink prompt, light pink dir, reset text
    "blue_ocean": Theme("\033[34m", "\033[36m", "\033[0m"),  # Blue prompt, cyan dir, reset text
}

# --- Configuration ---
GITHUB_REPO = "https://api.github.com/repos/Alejandrix2456github/tear-os-apps-extras/contents/tearOS/apps"
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
osname = "TearOS beta 1.4"
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
        print("\n1. List Available Apps")
        print("2. Search Apps")
        print("3. Install App")
        print("4. Update Apps")
        print("5. Back to TearOS")
        choice = input("Enter your choice: ")

        if choice == "1":
            list_available_apps()
        elif choice == "2":
            search_term = input("Enter search term: ")
            search_apps(search_term)
        elif choice == "3":
            download_app()
        elif choice == "4":
            update_apps()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
            
def load_app_store_data():
    """Loads app data from the GitHub repository and categorizes them."""
    global app_store_data
    try:
        response = requests.get(GITHUB_REPO)
        response.raise_for_status()
        apps_data = response.json()

        app_store_data = {}  # Reset the data
        for app in apps_data:
            app_name = app['name']
            app_description = app.get('description', 'No description available')
            app_category = app.get('category', 'Uncategorized')  # Get category

            # If the category doesn't exist, create it
            if app_category not in app_store_data:
                app_store_data[app_category] = {}

            app_store_data[app_category][app_name] = app_description

    except requests.exceptions.RequestException as e:
        print(f"Error fetching app data: {e}")

def search_apps(search_term):
    """Searches for apps by name or description."""
    load_app_store_data()
    if not app_store_data:
        print("No apps found in the app store.")
        return

    matching_apps = []
    for category, apps in app_store_data.items():
        for app_name, app_description in apps.items():
            if (search_term.lower() in app_name.lower() or 
                search_term.lower() in app_description.lower()):
                matching_apps.append((app_name, app_description, category))

    if not matching_apps:
        print("No matching apps found.")
    else:
        print("Matching Apps:")
        for app_name, app_description, category in matching_apps:
            print(f"- {app_name}: {app_description} (Category: {category})")


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
    """Lists available apps by category."""
    load_app_store_data()  # Reload data to reflect any changes
    if not app_store_data:
        print("No apps found in the app store.")
        return

    print("Available Apps:")
    for category, apps in app_store_data.items():
        print(f"\nCategory: {category}")
        for app_name, app_description in apps.items():
            print(f"- {app_name}: {app_description}") 

def extract_app(app_package_path):
    """Installs a .tear app package to the APPS_DIR."""

    if not app_package_path.endswith(".tear"):
        print("Error: Invalid app package format. Must end with '.tear'")
        return

    try:
        app_name = os.path.basename(app_package_path).replace(".tear", "")
        target_dir = os.path.join(APPS_DIR, app_name)

        # Check for existing installation
        if os.path.exists(target_dir):
            print(f"Error: An app named '{app_name}' is already installed.")
            return

        # Extract the .tear package
        shutil.unpack_archive(app_package_path, target_dir) 

        print(f"App '{app_name}' installed successfully!")

    except Exception as e:
        print(f"Error installing app: {e}")




def download_app():  # Renamed function
    app_name = input("Enter the name of the app to install: ")
    try:
        response = requests.get(f"{GITHUB_REPO}/{app_name}")
        response.raise_for_status()
        app_data = response.json()
        download_url = app_data['download_url']

        # Download the app
        response = requests.get(download_url)
        response.raise_for_status()
        with open(f"{app_name}.tear", "wb") as f:
            f.write(response.content)
        print(f"App '{app_name}' downloaded successfully!")

        # Extract the app using the correct function
        extract_app(f"{app_name}.tear") 

    except requests.exceptions.RequestException as e:
        print(f"Error installing app: {e}")

def update_apps():
    print("Updating apps...")
    print("Apps updated successfully!")

def install_app():
    pass
    

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
        return datetime.now(user_tz).user_tzinfo.tzname(datetime.now())
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
# --- Main OS Loop ---
def main():
    global username, dir, user_tz, settings, current_theme  # user_tz is not used anymore
    user_data = load_user_data()
    settings = load_settings()
    current_theme = "default"  # Initialize the theme

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
        prompt = f"{themes[current_theme].prompt_color}{prompt}{themes[current_theme].text_color}"  # Apply theme color

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
        elif command == "history":
            for i, cmd in enumerate(command_history_list):
                print(f"{i+1}. {cmd}")
        elif command == "tasks":  # Add a basic task manager command
            list_running_processes()    
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
        elif command == "settings":
            change_settings()
        elif command.startswith("theme"):  # Add the theme command
            parts = command.split(" ", 1)
            if len(parts) == 2:
                change_theme(parts[1])
            else:
                print("Invalid command. Usage: theme [theme_name]")
                
        elif command in apps:
            run_app(command)
        elif command == "exit":
            print("Exiting TearOS...")
            save_file_system()
            break # Exit the OS loop
        elif command == "logout":
            print("Logging out...")
            save_file_system()
            logged_in = False  # Reset the login status
            break  # Exit the OS loop, going back to login/signup
        elif command.startswith("install"):
            parts = command.split(" ", 1)
            if len(parts) == 2:
                extract_app(parts[1])
            else:
                print("Invalid command. Usage: install [app_package.tear]")
        elif command.startswith("uninstall"): # This is the code you're looking for
            parts = command.split(" ", 1)
            if len(parts) == 2:
                uninstall_app(parts[1])
            else:
                print("Invalid command. Usage: uninstall [app_name]")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

