import sys
import hashlib
# basic login functions and verifications

def promptForLoginInfo():
	validUsernameLen = False
	while not validUsernameLen:
		username = raw_input("Please enter your username: ")
		
		if len(username) > 0:
			validUsernameLen = True

	validPWLen = False
	while not validPWLen:
		password = raw_input("Please enter your password: ")
		if len(password)  > 0:
			validPWLen = True

	password = hashlib.sha224(password).hexdigest()
	return username, password

def verifyLoginInfo(c, username, password):
	c.execute("SELECT * FROM staff WHERE login = ? AND password = ?;", (username, password))

	result = c.fetchone()
	if result:
		return True

	print "...Invalid log in, please try again"
	return False

def roleStr(role):
	if(role == "D"):
		return "Doctor"
	elif(role == "N"):
		return "Nurse"
	else:
		return "Admin"

# when adding a new user D, N, A: staff_id, role, name, login, password
def promptForUserRole():
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
		sys.stdout.write("Creating new doctor user...\n\n")
	elif userRole == "N":
		sys.stdout.write("Creating new nurse user...\n\n")
	else:
		sys.stdout.write("Creating new administrator user...\n\n")

	return userRole

def promptForName():
	return raw_input("Please enter your name: ") 

