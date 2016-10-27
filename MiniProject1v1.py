import sqlite3, sys
from userInfo import *
from userController import *

def openConnection():
	conn = sqlite3.connect('hospital.db') 
	conn.text_factory = str
	c = conn.cursor()
	c.execute('PRAGMA foreign_keys=ON;')
	
	c.execute("SELECT name FROM sqlite_master WHERE type='table';")
	result = c.fetchone()

	if not result: #tables haven't been created
		print "Reading tables..."
		scriptFile = open('p1-tables.sql', 'r')
		script = scriptFile.read()
		scriptFile.close()
		c.executescript(script)
		conn.commit()

	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	return conn, c

def closeConnection(conn):
	conn.commit()
	conn.close()

def main():
	conn, c = openConnection()
	sys.stdout.write("Welcome!\n\n")

	choice = promptForInitialAction()

	if choice == "login":
		validLogin = False
		user = ""
		pw = ""

		result = False
		while not validLogin:
			user, pw = promptForLoginInfo()
			result = verifyLoginInfo(c, user, pw)
			if result:
				validLogin = True
		
		# valid login! now branch to what you can do as that user
		userController(result)
	else:
		addUsers()

	closeConnection(conn)

def promptForInitialAction():
	patterns = ['login','add']
	matches = set(patterns)

	validChoice = False
	choice = "dummy string"

	while not(validChoice):
		choice = raw_input("Do you wish to Login [login] or Add a user [add]? ")
		choice = choice.lower().strip()

		if choice in matches: 
			return choice

def addUsers():
	role = promptForUserRole()
	name = promptForName()
	user, pw = promptForLoginInfo()

	addUserSQL(role, name, user, pw)


def addUserSQL(role, name, user, pw):
	# count will be the user id!
	c.execute("SELECT COUNT(*) FROM staff;")

	count = c.fetchone()[0]
	insert = [count, role, name, user, pw]
	c.execute("INSERT INTO staff VALUES (?, ?, ?, ?, ?)", insert)
	conn.commit()

	c.execute("SELECT * FROM staff;")
	
	result = c.fetchall()
	for row in result: #staff_id, role, name, login, password
		role = roleStr(row["role"])
		print "	Successfully added", role, row["name"], "| username:", row["login"]
	print

	closeConnection(conn)
	main()

if __name__ == "__main__":
	main()