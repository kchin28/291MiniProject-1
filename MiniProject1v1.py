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

	patterns = ['login','add users']
	matches = set(patterns)

	validChoice = False
	choice = "dummy string"

	while not(validChoice):
		choice = raw_input("Do you wish to LOGIN or ADD USERS?")
		if choice.lower().strip() in matches: 
			validChoice = True

	if choice.lower().strip() =="login":
		sys.stdout.write("your choice was login!\n")
	else:
		sys.stdout.write("your choice was add users!\n")
		addUsers()

def addUsers():
	file_name = raw_input("Please write the name of the sql containing your users.\n")
	
	conn = sqlite3.connect('hospital.db')   
	c = conn.cursor()
	c.execute('PRAGMA foreign_keys=ON;')
	
	scriptFile = open(file_name.strip(), 'r')
	script = scriptFile.read()
	scriptFile.close()
	
	c.executescript(script)
	conn.commit()
	conn.close()
	
	getLoginInfo()
	
# def getLoginInfo():
# needs body or else main will fail
	


if __name__ == "__main__":
	main()