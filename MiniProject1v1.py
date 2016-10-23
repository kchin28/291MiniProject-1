import sqlite3
import hashlib
import sys

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
		sys.stdout.write("your choice was login!\n")
		getLoginInfo()
	else:
		sys.stdout.write("your choice was add users!\n")
		addUsers()

def addUsers():
	file_name = raw_input("Please write the name of the sql containing your users.\n")
	file_name = "p1-tables.sql";

	userRole = "dummy"
	patterns = ['D','N', 'A']
	matches = set(patterns)
	validUserRole = False

	while not(validUserRole):
		userRole = raw_input("Please enter user role doctor [d], nurse [n], or administrator [a]: ")
		userRole = userRole.upper().strip()

		if userRole in matches:
			validUserRole = True

	if userRole == "D":
		sys.stdout.write("Doctor\n")
	elif userRole == "N":
		sys.stdout.write("Nurse\n")
	else:
		sys.stdout.write("Administrator\n")

	user, pw = getLoginInfo()
	sys.stdout.write(user + "\n")
	sys.stdout.write(pw + "\n")

	conn = sqlite3.connect('hospital.db')   
	c = conn.cursor()
	c.execute('PRAGMA foreign_keys=ON;')
	
	scriptFile = open(file_name.strip(), 'r')
	script = scriptFile.read()
	scriptFile.close()
	
	c.executescript(script)
	conn.commit()
	conn.close()

# get the log in info
# maybe split this up into get user
# get password
# since the login will need to check it

def getLoginInfo():
	validUserName = False;
	while not(validUserName):
		username = raw_input("Please enter your username: ")
		# check valid username
		
		validUserName = True;
		validPassword = False;

		while not(validPassword):
			password = raw_input("Please enter your password: ")
			# check valid password
			validPassword = True;

	return username, password

if __name__ == "__main__":
	main()