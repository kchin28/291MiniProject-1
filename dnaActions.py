
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
			print i['hcno'],i['adate'],i['edate']," open"
		else:
		 	print i['hcno'],i['adate'],i['edate']," closed"

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
def openChart():
	conn,c = openConnection()
	closeConnection(conn)

def closeChart():
	conn,c = openConnection()
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
