import sqlite3, sys
from userInfo import *
<<<<<<< HEAD
from userController import *
=======
from doctorActions import *
>>>>>>> db2d0efa3fd7fe5c2127afa15d78fbabd728e178

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
<<<<<<< HEAD
	sys.stdout.write("Welcome!\n\n")
=======
	closeConnection(conn)

	sys.stdout.write("Welcome!\n")
>>>>>>> db2d0efa3fd7fe5c2127afa15d78fbabd728e178

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
<<<<<<< HEAD
			return choice
=======
			validChoice = True

	if choice == "login":
		user, pw = promptForLoginInfo() # login info from the user

		if verifyLoginInfo(user, pw):
			sys.stdout.write("You are logged in as: " + user + "\n");
	else:
		sys.stdout.write("your choice was add users!\n")
		addUsers()
>>>>>>> db2d0efa3fd7fe5c2127afa15d78fbabd728e178

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
<<<<<<< HEAD
	main()
=======
	
def testDoctorActions():
	conn, c = openConnection()
	scriptFile = open('chartsTestData.sql', 'r')
	script = scriptFile.read()
	scriptFile.close()
	c.executescript(script)
	
	x = "34wsa"
	
	c.execute( '''SELECT *
				FROM charts
				WHERE charts.hcno = ? 
				ORDER BY adate'''
			 ,(x,))
	results = c.fetchall()
	
	for i in results:
		chartStatus = i[3]
		
		print "chartStatus:",chartStatus," | "
		if chartStatus is None: #open
			print i['hcno'],i['adate'],i['edate']," open"
		else:
		 	print i['hcno'],i['adate'],i['edate']," closed"
>>>>>>> db2d0efa3fd7fe5c2127afa15d78fbabd728e178

if __name__ == "__main__":
	#main()
	testDoctorActions()