
# Used once a user is logged in and will specifies what it can do as that role

#
def userController(result):

	role = result["role"]

	if role == "D":
		print "You are logged in as a doctor\n"
		hcno = raw_input("Please enter the patient's health care number: ")

		print "Please select an action you wish to perform..."
		print "	[0] List all charts for this patient"
		print "	[1] Add a symptom"
		print "	[2] Add a diagnosis"
		print "	[3] Add a medication"
		action = raw_input("action: ")

		#check for hcno found
	elif role == "N":
		print "You are logged in as a nurse\n"
		hcno = raw_input("Please enter the patient's health care number: ")
		#check
	else:
		print "You are logged in as an administrator\n"
