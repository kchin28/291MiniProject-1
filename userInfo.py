import sys
# basic login functions and verifications

def promptForLoginInfo():
	validUserName = False;
	while not(validUserName):
		username = raw_input("Please enter your username: ")
		# check valid username
		
		validUserName = True
		validPassword = False

		while not(validPassword):
			password = raw_input("Please enter your password: ")
			# check valid password
			validPassword = True

	return username, password

def verifyLoginInfo(username, password):
	# if login info is in staff
	i = 0

	return True


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

