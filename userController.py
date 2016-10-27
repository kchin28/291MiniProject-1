import sys
from dnaActions import *
from sqlConnection import *
from Admin import *

# Used once a user is logged in and will specifies what it can do as that role
def userController(result):
	role = result["role"]

	if role == "D":
		print "You are logged in as a doctor"

		while(1):
			print "\nPlease select an action you wish to perform..."
			print "	[0] List all charts for a given patient"
			print "	[1] Add a symptom"
			print "	[2] Add a diagnosis"
			print "	[3] Add a medication"
			print "	[q] Quit program"
			action = raw_input("action: ")
			doctorController(action, result["staff_id"])

	#check for hcno found
	elif role == "N":
		print "You are logged in as a nurse"

		while(1):
			print "\nPlease select an action you wish to perform..."
			print "	[0] List all charts for a given patient"
			print "	[1] Add a symptom"
			print "	[2] Create a new chart"
			print "	[3] Close an open chart"
			print "	[q] Quit program"
			action = raw_input("action: ")
			nurseController(action, result["staff_id"])
	else:
		print "You are logged in as an administrator"

		while(1):
			print "\nPlease select an action you wish to perform..."
			print "	[0] Create report for all doctor prescriptions"
			print "	[1] List all perscriptions for specific drug"
			print "	[2] List all possible medications for a specific diagnosis"
			print "	[3] List all the diagnoses made prior to prescribing specific drug"
			print "	[q] Quit program"
			action = raw_input("action: ")
			adminController(action, result["staff_id"])


def doctorController(action, staff_id):
	if action == "q":
		sys.exit(0)

	conn, c = openConnection()
	hcno = raw_input("Please enter patient hcno: ")

	if action == str(0):
		selectAllPatientCharts(hcno)
		pickChart()

	elif action == str(1): # hcno, chart_id, staff_id, symptom, obs_date
		chartID = raw_input("Please enter chart ID: ")
		sym = raw_input("symptom: ")
		addSymptom(hcno, chartID, staff_id, sym)

	elif action == str(2): # hcno, chart_id, staff_id, diagnosis
		chartID = raw_input("Please enter chart ID: ")
		diag = raw_input("diagnosis: ")
		addDiagnosis(hcno, chartID, staff_id, diag)

	elif action == str(3): # hcno,chart_id,staff_id,mdate,drug_name
		chartID = raw_input("Please enter chart ID: ")
		medication = raw_input("medication: ")
		dose = raw_input("dose: ")

		# has to give warning: dose (Y/N) and allergies
		addMedication(hcno, chartID, staff_id, medication, dose)

	closeConnection(conn)

def nurseController(action, staff_id):
	if action == "q":
		sys.exit(0)
	
	conn, c = openConnection()

	hcno = raw_input("Please enter patient hcno: ")

	if action == str(0):
		selectAllPatientCharts(hcno)
		pickChart()

	elif action == str(1): # hcno, chart_id, staff_id, symptom, obs_date
		chartID = raw_input("Please enter chart ID: ")
		sym = raw_input("symptom: ")
		addSymptom(hcno, chartID, staff_id, sym)

	elif action == str(2):
		openChart(hcno)

	elif action == str(3):
		chartID = raw_input("Please enter chart ID: ")
		closeChart(chartID, hcno) 

	closeConnection(conn)

def adminController(action, staff_id):
	if action == "q":
		sys.exit(0)

	conn, c = openConnection()

	if action == str(0): # ------------------------- IMPORTANT ------------------------
		startDate = raw_input("Please enter start date: ")
		endDate = raw_input("Please enter end date: ")
		createDoctorPrescriptionsReport(startDate, endDate)
		

	elif action == str(1):
		startDate = raw_input("Please enter start date: ")
		endDate = raw_input("Please enter end date: ")
		category = raw_input("Please enter a drug category to search: ")
		listPrescriptionsForDrug(startDate, endDate, category)

	elif action == str(2):
		diagnoses = raw_input("Please enter the diagnoses you would like to loop up: ")
		listMedicationsForDiagnosis(diagnoses) # must do checks before a lot of them

	elif action == str(3):
		drug_name = raw_input("Please enter the drug you would like to look up: ")
		listDiagnosisesPriorToDrug(drug_name) 

	closeConnection(conn)

