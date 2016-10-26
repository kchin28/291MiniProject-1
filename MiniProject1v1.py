import sqlite3
import hashlib
import sys
from userInfo import *

def main():
	conn = sqlite3.connect('hospital.db')   
	c = conn.cursor()
	c.execute('PRAGMA foreign_keys=ON;')
	
	scriptFile = open('p1-tables.sql', 'r')
	script = scriptFile.read()
	scriptFile.close()

	c.executescript(script)

	conn.commit()
	
	conn.close()

	sys.stdout.write("Welcome!\n")

	patterns = ['login','add']
	matches = set(patterns)

	validChoice = False
	choice = "dummy string"

	while not(validChoice):
		choice = raw_input("Do you wish to Login [login] or Add a user [add]? ")
		choice = choice.lower().strip()

		if choice in matches: 
			validChoice = True

	if choice == "login":
		user, pw = promptForLoginInfo() # login info from the user

		if verifyLoginInfo(user, pw):
			sys.stdout.write("You are logged in as: " + user + "\n");
	else:
		sys.stdout.write("your choice was add users!\n")
		addUsers()

def addUsers():
	userRole = promptForUserRole()
	name = promptForName()

	user, pw = promptForLoginInfo()
	sys.stdout.write(user + "\n")
	sys.stdout.write(pw + "\n")

	# conn = sqlite3.connect('hospital.db')   
	# c = conn.cursor()
	# c.execute('PRAGMA foreign_keys=ON;')
	
	# scriptFile = open(file_name.strip(), 'r')
	# script = scriptFile.read()
	# scriptFile.close()
	
	# c.executescript(script)
	# conn.commit()
	# conn.close()

if __name__ == "__main__":
	main()