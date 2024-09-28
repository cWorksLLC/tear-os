#TearOS beta 1.2

import time
import datetime

print("Welcome to the login script!")
username = input("What is your name? ")
password = input("What is your password? ")

print("Welcome to TearOS beta 1.2!)
print("Type 'help' for a list of commands.")

while True:
	# The command script
	print("What to run?")
	cmd = input()
	
	if cmd == "help":
		print("The commands are:")
		print("help - Views all the commands")
		print("time - Tells the time")
		print("date - Tells the current date")
		print("sysinfo - Tells the system information")
		print("su - Switches to Superuser")
	
	elif cmd == "time":
		print(datetime.datetime.now().strftime('%H:%M:%S'))
		
	elif cmd == "date":
		print(datetime.datetime.now().strftime('%Y-%m-%d'))

	elif cmd == "sysinfo":
		 print(f"TearOS beta 1.2 is registered to: {username}")

	elif cmd == "su":
		supass = input("What is your password?")
		if supass == password:
			print("Success!")
		else:
			print("Incorrect.")
		
		# Commands after the first one must be written with an "elif"
		# Statement. the commands end at the "else" mentioned here:
		
	else:
		print("Not a valid command.")
