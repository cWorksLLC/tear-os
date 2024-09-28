#TearOS beta 1.3

import time
from datetime import date

today = date.today()
chour = time.strftime("%H:")
cminute = time.strftime("%M:")
csecond = time.strftime("%S ")
osname = "TearOS beta 1.3"
dir = "home"
#the variables (important i swear)

print("welcome to the login script!")
username = input("what is your name? ")
password = input("what is your password? ")

print("welcome to " + osname + "!")
print("type 'help' for a list of commands!")

while True:
	#the command script
	cmd = input(f"TearOS/{username}/{dir}>")
	
	if cmd=="help":
		print("the commands are:")
		print("help - Views all the commands")
		print("time - Tells the time")
		print("date - Tells the current date")
		print("sysinfo - Tells the system information")
		print("su - Switches to Superuser")
		print("changedir - params: --dirname - switches directory's")
	
	elif cmd=="time":
		print(chour + cminute + csecond)
		
	elif cmd=="date":
		print(str(today.day) + "." + str(today.month) + "." + str(today.year))

	elif cmd=="sysinfo":
		 print(osname + " this software copy is registered to: " + username)

	elif cmd=="su":
		supass = input("what is your password?")
		if supass == password:
			print("sucess!")
			username = "root" # or anything else the username for TearOS superuser would be.
			dir = "root"
		else:
			print("wrong.")
		
		#commands after the first one must be written with an "elif"
		#statement. the commands end at the "else" mentioned here:
	
	elif cmd=="changedir":
		print("changedir usage: changedir --dirname")
	elif cmd=="changedir --root":
		print("root")
		dir = "root"
	elif cmd=="changedir --home":
		print("home")
		dir = "home"
	else:
		print("not a valid command.")
#end
