import sqlite3
import hashlib
import sys
import datetime

def openConnection():
	conn = sqlite3.connect('hospital.db') 
	conn.text_factory = str
	c = conn.cursor()
	# c.execute('PRAGMA foreign_keys=ON;')
	
	scriptFile = open('p1-tables.sql', 'r')
	script = scriptFile.read()
	scriptFile.close()
	c.executescript(script)

	conn.row_factory = sqlite3.Row
	c = conn.cursor()

	return conn, c


def closeConnection(conn):
	conn.commit()
	conn.close()

def main():
	conn, c = openConnection()
	closeConnection(conn)

	sys.stdout.write("Welcome!\n")

	patterns = ['login','add']
	matches = set(patterns)

	validChoice = False
	choice = "dummy string"

	while not(validChoice):
		choice = raw_input("Do you wish to Login [login] or Add a user [add]? ")
		choice = choice.lower().strip()

		if choice in matches: 
			validChoice = True

	if choice == "login":
		user, pw = promptForLoginInfo() # login info from the user

		if verifyLoginInfo(user, pw):
			sys.stdout.write("You are logged in as: " + user + "\n");
	else:
		sys.stdout.write("your choice was add users!\n")
		addUsers()

def addUsers():
	role = promptForUserRole()
	name = promptForName()
	user, pw = promptForLoginInfo()

	addUserSQL(role, name, user, pw)

	sys.stdout.write(user + "\n")
	sys.stdout.write(pw + "\n")


def addUserSQL(role, name, user, pw):
	conn, c = openConnection()

	c.execute("SELECT COUNT(*) FROM staff;")
	# count = c.fetchall()
	count = c.fetchone()[0]
	sys.stdout.write("Count of staff: " + str(count) + "\n");

	insert = [count, role, name, user, pw]
	c.execute("INSERT INTO staff VALUES (?, ?, ?, ?, ?)", insert)
	conn.commit()



	c.execute("SELECT * FROM staff;")
	
	print
	row = c.fetchone()
	print row
	print "Column names of staff table:", row.keys()
	print

	result = c.fetchall()
	for r in result: #staff_id, role, name, login, password
	    print "ID: ", row["staff_id"], "Role: ", row["role"], "Name: ", row["name"], "Login: ", row["login"]
	print

	closeConnection(conn)
	
def testDoctorActions():
	conn, c = openConnection()
	scriptFile = open('chartsTestData.sql', 'r')
	script = scriptFile.read()
	scriptFile.close()
	c.executescript(script)

	# x = "34wsa"
	searchChartsByPatient(c)
	# pickChart(c)
	addSymptom(c)l

	closeConnection(conn)

def searchChartsByPatient(c):

	# Doctor #1
	# Assume the user is a doctor and their user profile has been verified as such
	patientHCNO = raw_input("To view all charts associated with a patient, please provide the patient's health care number.\n")
	
	#add error checking here

	c.execute( '''SELECT *
				FROM charts
				WHERE charts.hcno = ? 
				ORDER BY adate'''
			 ,(patientHCNO,))
	results = c.fetchall()
	
	print results[0].keys()

	for i in results:
		chartStatus = i[3]
		
		if chartStatus is None: #open
			print i['chart_id'],i['hcno'],i['adate'],i['edate']," open"
		else: #closed
		 	print i['chart_id'],i['hcno'],i['adate'],i['edate']," closed"


def pickChart(c):
	chartID = raw_input("To view a chart in more detail, enter its id. (ie. First Column)\n")
	
	# check if chart is open before proceeding	
	c.execute( '''SELECT *
				FROM charts
				WHERE charts.chart_id = ? 
				ORDER BY adate'''
			 ,(chartID,))
	results = c.fetchone()

	if results[3] is not None:
		print "Chart: " +  str(chartID) +  " not active. " 
		return;  #goes back to 'main menu'

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

	print i.keys()
	for i in results:
		print i['StaffID'],i['Date'],i['Description']

def addSymptom(hcno, chartID, staff_id, sym):

	now = datetime.datetime.now()
	newObs_date = now.strftime("%Y-%m-%d %H:%M:%S")

	c.execute('''
			  INSERT INTO symptoms
			  VALUES (?,?,?,?,?)
			   '''
		,(hcno,chartID,staff_id,newObs_date,sym))

	#check proper insert
	print("Symptom added successfully.")

def addDiagnosis(hcno, chartID, staff_id, diag):

	now = datetime.datetime.now()
	new_ddate = now.strftime("%Y-%m-%d %H:%M:%S")

	c.execute('''
			  INSERT INTO diagnosis
			  VALUES (?,?,?,?,?)
			  '''
		,(hcno,chartID,staff_id,new_ddate,diag))

	#check proper insert
	print("Diagnosis added successfully.")

if __name__ == "__main__":
	#main()
	testDoctorActions()