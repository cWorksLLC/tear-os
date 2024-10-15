# THIS IS THE ORIGINAL REPO TEAROS FILE, ITS RECOMMENDED TO USE THE 1.3.1 , 1.3.1.1 OR THE LATEST
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
today = date.today()
chour = time.strftime("%H:")
cminute = time.strftime("%M:")
csecond = time.strftime("%S ")
osname = "TearOS beta 1.3"
dir = "home"

# Setting vars
print("welcome to the login script!")
username = input("what is your name? ")
password = input("what is your password? ")

# Set the time zone
user_tz = choose_timezone()
user_tz = pytz.timezone(user_tz)

print("welcome to " + osname + "!")
print("type 'help' for a list of commands!")

while True:
    # The command script
    cmd = input(f"TearOS/{username}/{dir}>")

    if cmd == "help":
        print("the commands are:")
        print("help - Views all the commands")
        print("time - Tells the time")
        print("date - Tells the current date")
        print("sysinfo - Tells the system information")
        print("su - Switches to Superuser")
        print("changedir - params: --dirname - switches directory's")

    elif cmd == "time":
        current_time = datetime.now(user_tz).strftime("%H:%M:%S")
        print(f"The current time is {current_time}")

    elif cmd == "date":
        print(f"{today.day}.{today.month}.{today.year}")

    elif cmd == "sysinfo":
        print(osname + " this software copy is registered to: " + username)

    elif cmd == "su":
        supass = input("what is your password?")
        if supass == password:
            print("success!")
            username = "root"  # or anything else the username for TearOS superuser would be.
            dir = "root"
        else:
            print("wrong.")

    elif cmd == "changedir":
        print("changedir usage: changedir --dirname")
    elif cmd == "changedir --root":
        print("root")
        dir = "root"
    elif cmd == "changedir --home":
        print("home")
        dir = "home"
    else:
        print("not a valid command.")
#end
