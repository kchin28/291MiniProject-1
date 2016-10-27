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
			doctorController(action, hcno, result["staff_id"])

	#check for hcno found
	elif role == "N":
		print "You are logged in as a nurse\n"
		hcno = raw_input("Please enter the patient's health care number: ")
		#check
	else:
		print "You are logged in as an administrator\n"


def doctorController(action, hcno, staff_id):

	conn, c = openConnection()

	if action == str(0):
		selectAllPatientCharts(hcno)

	elif action == str(1): # hcno, chart_id, staff_id, symptom, obs_date
		chartID = raw_input("	Please enter chart ID: ")
		sym = raw_input("	symptom: ")
		addSymptom(hcno, chartID, staff_id, sym)

	elif action == str(2): # hcno, chart_id, staff_id, diagnosis
		chartID = raw_input("	Please enter chart ID: ")
		diag = raw_input("	diagnosis: ")
		addDiagnosis(hcno, chartID, staff_id, diag)

	elif action == str(3): # hcno,chart_id,staff_id,mdate,drug_name
		chartID = raw_input("	Please enter chart ID: ")
		medication = raw_input("	medication: ")
		dose = raw_input("	dose:")

		# has to give warning: dose (Y/N) and allergies
		addMedication(hcno, chartID, staff_id, medication, dose) 

	closeConnection(conn)


