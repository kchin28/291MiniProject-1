
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