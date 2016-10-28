
import sqlite3
from sqlConnection import *
from Admin import *

def testDoctorActions():
	conn, c = openConnection()
	scriptFile = open('p1-tables.sql', 'r')
	script = scriptFile.read()
	scriptFile.close()
	c.executescript(script)
	conn.commit()

	scriptFile = open('chartsTestData.sql', 'r')
	script = scriptFile.read()
	scriptFile.close()
	c.executescript(script)
	
	hcno = "34wsa"
	selectAllPatientCharts(hcno)

def isChartOpen(chartID, hcno):
	conn, c = openConnection()
	
	# check if chart is open before proceeding	
	c.execute( '''SELECT *
				FROM charts
				WHERE charts.chart_id = ? 
				AND charts.hcno = ?'''
			 ,(chartID, hcno))
	results = c.fetchone()

	if results["edate"] is not None:
		print "Chart: " +  str(chartID) +  " not active. Nothing done" 
		return False
	
	return True
	
# ----------------------------------- Doctor & Nurse actions -----------------------------------
def selectAllPatientCharts(hcno):
	conn, c = openConnection()

	c.execute( '''SELECT *
				FROM charts
				WHERE charts.hcno = ? 
				ORDER BY adate'''
			 ,(hcno,))
	results = c.fetchall()
	
	print results[0].keys()

	for i in results:
		chartStatus = i[3]
		
		if chartStatus is None: #open
			print i['chart_id'],i['hcno'],i['adate'],i['edate']," open"
		else: #closed
		 	print i['chart_id'],i['hcno'],i['adate'],i['edate']," closed"

	closeConnection(conn)

def pickChart(hcno):
	conn, c = openConnection()
	chartID = raw_input("To view a chart in more detail, enter its id. (ie. First Column)\n")

	#enter error checking here
	# not yet tested w data, only forming sql query
	c.execute(''' 
			SELECT * FROM 
			 ( SELECT staff_id as StaffID,obs_date as Date ,symptom as Description 
  			  FROM symptoms
			  WHERE chart_id=?
			 UNION
			 SELECT staff_id as StaffID ,ddate as Date,diagnosis as Description
			  FROM diagnoses
			  WHERE chart_id=? 
			 UNION 
		     SELECT staff_id as StaffID,mdate as Date,drug_name as Description
			  FROM medications
			  WHERE chart_id=? 
			 ) 
			 ORDER BY Date
			  '''
		,(chartID,chartID,chartID) )
	results = c.fetchall()

	for i in results:
		print i['StaffID'],i['Date'],i['Description']

	closeConnection(conn)

def addSymptom(hcno, chartID, staff_id, sym):
	conn, c = openConnection()
	
	if not isChartOpen(chartID, hcno):
		return

	c.execute("SELECT datetime('now')")
	date = c.fetchone()[0]

	c.execute('''
			  INSERT INTO symptoms
			  VALUES (?,?,?,?,?)
			   '''
		,(hcno,chartID,staff_id,date,sym))

	#check proper insert
	print("Symptom added successfully.")

	closeConnection(conn)

# ----------------------------------- Doctor actions -----------------------------------
def addDiagnosis(hcno, chartID, staff_id, diag):
	conn, c = openConnection()

	if not isChartOpen(chartID, hcno):
		return

	c.execute("SELECT datetime('now')")
	date = c.fetchone()[0]

	c.execute('''
			  INSERT INTO diagnoses
			  VALUES (?,?,?,?,?)
			  '''
		,(hcno,chartID,staff_id,date,diag))

	#check proper insert
	print("Diagnosis added successfully.")
	closeConnection(conn)


def addMedication(hcno, chartID, staffID, medication, dose):
	conn,c = openConnection()

	if not isChartOpen(chartID, hcno):
		return

	c.execute("SELECT datetime('now')")
	date = c.fetchone()[0]

	okAmt = checkAmt(hcno, dose, medication) #(1) check prescribed amt against sug amt inside 'dosage'
	okDrug = checkAllergies(hcno, medication) #(2) 
	
	#add medication entry
	startDate = raw_input("Enter date to start medication (YYYY-MM-DD HH:MM:SS): ")
	endDate = raw_input("Enter date to end medication (YYYY-MM-DD HH:MM:SS): ")

	print str(hcno), str(chartID), str(staffID), str(okDrug)
	c.execute('''
		  INSERT INTO medications
		  VALUES (?,?,?,?,?,?,?,?)
		  '''
	,(hcno,chartID,staffID,date,startDate,endDate,okAmt,okDrug))

	print(" Medication added successfully.")
	closeConnection(conn)

def checkAmt(hcno, amt, drugName):
	conn, c = openConnection()

	c.execute('''SELECT sug_amount,dosage.age_group
			  FROM dosage,patients
			  WHERE patients.hcno = ?
			  AND dosage.drug_name= ?
			  AND dosage.age_group=patients.age_group
			  '''
	,(hcno,drugName))

	results = c.fetchall()

	sug_amt = results[0][0]
	patientsAge = results[0][1]

	if int(amt) > int(sug_amt):
		print "The amount, "+ str(amt) +" you are prescribing for a patient aged between "+ patientsAge + " is over the recommended amount of "+str(sug_amt)+	"."

		patterns = ['change','keep']
		matches = set(patterns)
		validChoice = False
		choice = "dummy string"

		while not(validChoice):
			choice = raw_input("Do you wish to [change] or [keep] the prescribed amount? \n")
			choice = choice.lower().strip()

			if choice in matches: 
				validChoice = True
			
		if choice == 'change':
			changedAmt=raw_input("Please enter the new amount:   ")
			amt = changedAmt
			checkAmt(hcno, amt, drugName)

	closeConnection(conn)
	return amt;

def checkAllergies(hcno, prescribedDrug):
	conn, c = openConnection()
	c.execute(
	''' SELECT *
		FROM reportedallergies,inferredallergies
		WHERE reportedallergies.hcno= ?
		AND reportedallergies.drug_name=inferredallergies.alg
	'''
	,(hcno,))

	results2 = c.fetchall();

	for r in results2:
		# print r 
		if r['drug_name'] == prescribedDrug:
			print "This patient has a reported allergy to the drug, " + prescribedDrug + " with inferred " + r["canbe_alg"]
		if r['canbe_alg'] == prescribedDrug:
			print "This patient is at risk of an allergy reaction to the drug, " + r['canbe_alg'] + " beacause of its similarties to " + r['alg']
	
	closeConnection(conn)
	return prescribedDrug

# ----------------------------------- Nurse actions -----------------------------------
def promptNewPatient():
	name = raw_input("Name:")
	age = raw_input("Age:")
	addr = raw_input("Address:")
	phone = raw_input("Phone:")
	ephone = raw_input("Emergency Phone:")

	return name, age, addr, phone, ephone

def createNewPatient(hcno, name, age, addr, phone, ephone):
	conn, c = openConnection()

	insert = [hcno, name, age, addr, phone, ephone]
	c.execute("INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?)", insert)
	print "Patient added to database\n"
	closeConnection(conn)

def promptToAskClose(chartID):
	print "Chart '" + chartID +  "' is currently open"
	answ = raw_input("Would you like to close this chart [y/n]? ")

	validAns = False
	while not validAns:
		if answ == "y":
			return True

		elif answ == "n":
			return False

def openChart(hcno):
	conn,c = openConnection()
	# check if patient exists, if not make one
	c.execute("SELECT * from patients WHERE hcno = ?", (hcno,) )
	result = c.fetchone()

	if not result: # no patient
		print "\nPatient is not found. Creating new patient..."

		name, age, addr, phone, ePhone = promptNewPatient()
		createNewPatient(hcno, name, age, addr, phone, ePhone)

	else: #check if they have a chart open
		c.execute("SELECT * FROM charts WHERE charts.hcno = ?",(hcno,))
		results = c.fetchall()
	
		for i in results:
			chartStatus = i[3]
			if chartStatus is None: #open
				if promptToAskClose(i["chart_id"]):
					closeChart(i["chart_id"], hcno)
				else:
					print "No chart was created"
					return

	# code to create chart
	chartID = raw_input("Please enter a unique chart id: ")
	c.execute("SELECT datetime('now')")
	result = c.fetchone()[0]
	insert = [chartID, hcno, str(result), None]
	c.execute("INSERT into charts VALUES (?,?,?,?)", insert)
	print "Chart has is now open"

	closeConnection(conn)

def closeChart(chartID, hcno):
	conn,c = openConnection()
	
	c.execute("SELECT datetime('now')")
	endDate = c.fetchone()[0]
	c.execute("UPDATE charts SET edate = ? WHERE hcno = ?", (endDate,hcno))
	print "Chart has been closed\n"

	closeConnection(conn)

# ----------------------------------- Admin actions -----------------------------------
def createDoctorPrescriptionsReport(starDate, endDate): # dont know if we need to get a period
	conn,c = openConnection()
	createReport(starDate, endDate, c)
	closeConnection(conn)

def listPrescriptionsForDrug(starDate, endDate, category):
	conn,c = openConnection()
	drugCategoryTotal(starDate, endDate, category, c)
	closeConnection(conn)

def listMedicationsForDiagnosis(diagnoses): # must do checks before a lot of them
	conn,c = openConnection()
	medicationsAfterDiagnoses(diagnoses, c)
	closeConnection(conn)

def listDiagnosisesPriorToDrug(drug_name): 
	conn,c = openConnection()
	diagnosesBeforeDrug(drug_name, c)
	closeConnection(conn)
