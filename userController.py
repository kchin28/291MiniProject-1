from doctorActions import *
from sqlConnection import *

# Used once a user is logged in and will specifies what it can do as that role

def verfiyPatient(hcno): # check if patient is in database
	conn, c = openConnection()
	c.execute( '''SELECT *
				FROM patients
				WHERE patients.hcno = ?''',(hcno,))
	results = c.fetchall()

	if results:
		return True

	return False

def userController(result):

	role = result["role"]

	if role == "D":
		print "You are logged in as a doctor\n"

		while(1):
			hcno = raw_input("Please enter the patient's health care number: ")

			if not verfiyPatient(hcno):
				print "Patient not found, please try again"
				continue

			print "Please select an action you wish to perform..."
			print "	[0] List all charts for this patient"
			print "	[1] Add a symptom"
			print "	[2] Add a diagnosis"
			print "	[3] Add a medication"
			action = raw_input("action: ")
			doctorController(action, hcno)

	#check for hcno found
	elif role == "N":
		print "You are logged in as a nurse\n"
		hcno = raw_input("Please enter the patient's health care number: ")
		#check
	else:
		print "You are logged in as an administrator\n"


def doctorController(action, hcno):

	conn, c = openConnection()

	if action == str(0):
		selectAllPatientCharts(hcno)
	elif action == str(1):
		action = raw_input("		symptom: ")
	elif action == str(2):
		action = raw_input("		diagnosis: ")
	elif action == str(3):
		action = raw_input("		medication: ")

	closeConnection(conn)


