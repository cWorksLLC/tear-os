#TearOS beta 1.1

import time
from datetime import date

today = date.today()
chour = time.strftime("%H:")
cminute = time.strftime("%M:")
csecond = time.strftime("%S ")
osname = "TearOS beta 1.1"
#the variables (important i swear)

print("welcome to the login script!")
username = input("what is your name?")
password = input("what is your password?")

print("welcome to " + osname + "!")
print("type 'help' for a list of commands!")

while True:
	#the command script
	print("What to run?")
	cmd = input()
	
	if cmd=="help":
		print("the commands are:")
		print("help - Views all the commands")
		print("time - Tells the time")
		print("date - Tells the current date")
		print("sysinfo - Tells the system information")
	
	elif cmd=="time":
		print(chour + cminute + csecond)
		
	elif cmd=="date":
		print(str(today.day) + "." + str(today.month) + "." + str(today.year))

	elif cmd=="sysinfo":
		 print(osname + " is registered to: " + username)
		
		#commands after the first one must be written with an "elif"
		#statement. the commands end at the "else" mentioned here:
		
	else:
		print("not a valid command.")
#end
