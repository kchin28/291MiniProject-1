import sqlite3
import hashlib
import sys
from userInfo import *

def openConnection():
	conn = sqlite3.connect('hospital.db') 
	conn.text_factory = str
	c = conn.cursor()
	c.execute('PRAGMA foreign_keys=ON;')
	
	scriptFile = open('p1-tables.sql', 'r')
	script = scriptFile.read()
	scriptFile.close()
	c.executescript(script)

	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	return conn, c


def closeConnection(conn):
	conn.commit()
	conn.close()

def main():
	conn, c = openConnection()
	closeConnection(conn)

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
	role = promptForUserRole()
	name = promptForName()
	user, pw = promptForLoginInfo()

	addUserSQL(role, name, user, pw)

	sys.stdout.write(user + "\n")
	sys.stdout.write(pw + "\n")


def addUserSQL(role, name, user, pw):
	conn, c = openConnection()

	c.execute("SELECT COUNT(*) FROM staff;")
	# count = c.fetchall()
	count = c.fetchone()[0]
	sys.stdout.write("Count of staff: " + str(count) + "\n");

	insert = [count, role, name, user, pw]
	c.execute("INSERT INTO staff VALUES (?, ?, ?, ?, ?)", insert)
	conn.commit()



	c.execute("SELECT * FROM staff;")
	
	print
	row = c.fetchone()
	print row
	print "Column names of staff table:", row.keys()
	print

	result = c.fetchall()
	for r in result: #staff_id, role, name, login, password
	    print "ID: ", row["staff_id"], "Role: ", row["role"], "Name: ", row["name"], "Login: ", row["login"]
	print

	closeConnection(conn)

if __name__ == "__main__":
	main()