
import sqlite3
from sqlConnection import *

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

# ----------------------------------- Doctor & Nurse actions -----------------------------------
def selectAllPatientCharts(hcno):
	conn, c = openConnection()
	c.execute( '''SELECT *
				FROM charts
				WHERE charts.hcno = ? 
				ORDER BY adate'''
			 ,(hcno,))
	results = c.fetchall()
	
	for i in results:
		chartStatus = i[3]
		
		print "chartStatus:",chartStatus," | "
		if chartStatus is None: #open
			print "	",i['hcno'],i['adate'],i['edate']," open"
		else:
		 	print "	",i['hcno'],i['adate'],i['edate']," closed"

	closeConnection(conn)

def addSymptom(hcno, chart_id, staff_id, sym):
	conn, c = openConnection()
	closeConnection(conn)

# ----------------------------------- Doctor actions -----------------------------------
def addDiagnosis(hcno, chartID, staff_id, diag):
	conn, c = openConnection()
	closeConnection(conn)


def addMedication(hcno, chartID, staff_id, medication, dose):
	#get age stuff too
	# check dose first
	#add to dosage chart
	conn,c = openConnection()
	closeConnection(conn)

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
def createDoctorPrescriptionsReport(): # dont know if we need to get a period
	conn,c = openConnection()
	closeConnection(conn)

def listPrescriptionsForDrug():
	conn,c = openConnection()
	closeConnection(conn)

def listMedicationsForDiagnosis(): # must do checks before a lot of them
	conn,c = openConnection()
	closeConnection(conn)

def listDiagnosisesPriorToDrug(): 
	conn,c = openConnection()
	closeConnection(conn)
