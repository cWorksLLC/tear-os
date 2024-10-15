from consolemenu import *
from consolemenu.items import *
import os
import json
import shutil

# --- Configuration ---
APPS_DIR = "/tearOS/apps"  # Path to your main apps directory
CUSTOM_APPS_DIR = "/tearOS/custom_apps"  # Directory for storing custom apps

# --- Helper Functions ---
def is_valid_app_dir(app_dir):
    """Checks if a directory contains a valid TearOS app."""
    app_info_path = os.path.join(app_dir, "app_info.json")
    return os.path.exists(app_info_path)

def get_app_info(app_dir):
    """Reads app information from the app_info.json file."""
    app_info_path = os.path.join(app_dir, "app_info.json")
    try:
        with open(app_info_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def install_app(app_dir):
    """Installs an app from a custom app directory to the main apps directory."""
    app_info = get_app_info(app_dir)
    if app_info:
        app_name = app_info['name']
        target_dir = os.path.join(APPS_DIR, app_name)

        # Check if the app is already installed
        if os.path.exists(target_dir):
            print(f"Error: An app named '{app_name}' is already installed.")
            return

        try:
            shutil.copytree(app_dir, target_dir)  # Copy the app directory
            print(f"App '{app_name}' installed successfully!")
        except Exception as e:
            print(f"Error installing app: {e}")
    else:
        print(f"Error: Invalid app directory '{app_dir}'")

# --- Menu Actions ---
def show_custom_apps():
    """Displays a list of custom apps available for installation."""
    if os.path.exists(CUSTOM_APPS_DIR):
        custom_apps = [
            d for d in os.listdir(CUSTOM_APPS_DIR) 
            if os.path.isdir(os.path.join(CUSTOM_APPS_DIR, d)) and 
            is_valid_app_dir(os.path.join(CUSTOM_APPS_DIR, d))
        ]
        if custom_apps:
            menu = ConsoleMenu("Custom Apps", "Select an app to install")
            for app_name in custom_apps:
                app_dir = os.path.join(CUSTOM_APPS_DIR, app_name)
                app_info = get_app_info(app_dir)
                app_description = app_info.get('description', 'No description available')
                menu.append_item(FunctionItem(f"{app_name} - {app_description}", install_app, [app_dir]))
            menu.show()
        else:
            print("No custom apps found.")
    else:
        print("Custom apps directory not found.")

# --- Main Menu ---
menu = ConsoleMenu("TearOS Menu", "Manage your TearOS environment")
menu.append_item(FunctionItem("Install Custom App", show_custom_apps))
menu.show()
