import sqlite3, sys
from sqlConnection import *
from userInfo import *
from userController import *

def main():
	conn, c = openConnection()
	sys.stdout.write("Welcome!\n\n")
	choice = promptForInitialAction()

	if choice == "login":
		validLogin = False
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

# initial action splits up the action as login or adding a user
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

	conn, c = openConnection()
	c.execute("SELECT COUNT(*) FROM staff;")

	count = c.fetchone()[0] # count will be the user id!
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
	# conn, c = openConnection()
	# testDoctorActions(c, conn)