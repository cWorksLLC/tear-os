import time
from datetime import datetime, date
import pytz

# Time zone selection
def choose_timezone():
    print("Please choose your time zone:")
    timezones = pytz.all_timezones
    for i, tz in enumerate(timezones):
        print(f"{i + 1}. {tz}")
    while True:
        choice = input("Enter the number corresponding to your time zone: ")
        try:
            tz_index = int(choice) - 1
            if 0 <= tz_index < len(timezones):
                return timezones[tz_index]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Variables
osname = "TearOS beta 1.3"
dir = "home"
timezone = choose_timezone()
user_tz = pytz.timezone(timezone)
today = date.today()

print("Welcome to the login script!")
username = input("What is your name? ")
password = input("What is your password? ")

print(f"Welcome to {osname}!")
print("Type 'help' for a list of commands!")

while True:
    cmd = input(f"TearOS/{username}/{dir}>")

    if cmd == "help":
        print("The commands are:")
        print("help - Views all the commands")
        print("time - Tells the time")
        print("date - Tells the current date")
        print("sysinfo - Tells the system information")
        print("su - Switches to Superuser")
        print("changedir - params: --dirname - switches directories")
    
    elif cmd == "time":
        current_time = datetime.now(user_tz).strftime("%H:%M:%S")
        print(f"The current time is {current_time}")
        
    elif cmd == "date":
        print(f"{today.day}.{today.month}.{today.year}")
    
    elif cmd == "sysinfo":
        print(f"{osname} is registered to: {username}")
    
    elif cmd == "su":
        supass = input("What is your password? ")
        if supass == password:
            print("Success!")
            username = "root"  # Superuser
            dir = "root"
        else:
            print("Wrong password.")
    
    elif cmd == "changedir":
        print("changedir usage: changedir --dirname")
    
    elif cmd == "changedir --root":
        print("Root directory")
        dir = "root"
    
    elif cmd == "changedir --home":
        print("Home directory")
        dir = "home"
    
    else:
        print("Not a valid command.")
