import sqlite3

def createReport(startDate, endDate, cursor):
	#startDate and endDate are strings

	sql = ''' 
				select s.name, m.drug_name, sum(m.amount) as total
				from staff s, medications m
				where (julianday(?) <= julianday(m.mdate))
				and (julianday(m.mdate) <= julianday(?))
				and s.staff_id = m.staff_id
				group by s.name, m.drug_name;
			'''
	cursor.execute(sql,(startDate,endDate))
	result = cursor.fetchall()
	print
	print "report of total drugs prescribed"
	prevDoctorHeader = None
	for row in result:
		if prevDoctorHeader != row["name"]:
			print "Doctor", row["name"]
			prevDoctorHeader = row["name"]
		print " drug:", row["drug_name"], "total:", row["total"]

	print

def drugCategoryTotal(startDate, endDate, category, cursor):
	drugTotal = '''
			select d.drug_name, sum(m.amount) as drugTotal
			from drugs d, medications m
			where d.category = ?
			and d.drug_name = m.drug_name
			and (julianday(?) <= julianday(m.mdate))
			and (julianday(m.mdate) <= julianday(?))
			group by d.drug_name
			'''
	cursor.execute(drugTotal, (category, startDate, endDate))
	resultDrugTotal = cursor.fetchall()
	categoryTotal = '''
					select d.category, sum(m.amount) as categoryTotal
					from drugs d, medications m
					where d.category = ?
					and d.drug_name = m.drug_name
					and (julianday(?) <= julianday(m.mdate))
					and (julianday(m.mdate) <= julianday(?))
					group by d.category
					'''
	cursor.execute(categoryTotal, (category, startDate, endDate))
	resultCategoryTotal = cursor.fetchall()
	print
	print "Total of each drug in a category and total in category"
	for row in resultCategoryTotal:
		print "Category:", row["category"], "Total:", row["categoryTotal"]
	for row in resultDrugTotal:
		print " Drug name:", row["drug_name"], "Total:", row["drugTotal"]
	print

def medicationsAfterDiagnoses(diagnoses, cursor):
	sql = '''
			select m.drug_name
			from medications m, diagnoses dia
			where dia.diagnosis = ?
			and (julianday(dia.ddate) < julianday(m.mdate))
			group by m.drug_name
			order by count(*) desc
			'''
	print
	print "list of medications prescribed after the diagnoses"
	cursor.execute(sql, [diagnoses])
	result = cursor.fetchall()
	for row in result:
		print "Drug name:", row["drug_name"]
	print

def diagnosesBeforeDrug(drug_name, cursor):
	sql = '''
			select dia.diagnosis
			from diagnoses dia, medications m
			where m.drug_name = ?
			and (julianday(dia.ddate) < julianday(m.mdate))
			group by dia.diagnosis
			order by avg(m.amount) desc
			'''
	cursor.execute(sql, [drug_name])
	result = cursor.fetchall()
	print
	print "List of diagnoses before prescription of drug "
	for row in result:
		print "Diagnoses:", row['diagnosis']

def testCreateReport(cursor):
	startDate = '2016-10-25'
	endDate = '2016-11-01'
	createReport(startDate, endDate, cursor)

def testDrugCategoryTotal(cursor):
	startDate = '2016-10-25'
	endDate = '2016-11-01'
	category = 'pain relief'
	drugCategoryTotal(startDate, endDate, category, cursor)

def testMedicationsAfterDiagnoses(cursor):
	diagnoses = 'diagnoses1'
	medicationsAfterDiagnoses(diagnoses,cursor)

def testDiagnosesBeforeDrug(cursor):
	drug = 'moltrin'
	diagnosesBeforeDrug(drug, cursor)

conn = sqlite3.connect('hospital.db') 
conn.text_factory = str
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute('PRAGMA foreign_keys=ON;')

testCreateReport(c)
testDrugCategoryTotal(c)
testMedicationsAfterDiagnoses(c)
testDiagnosesBeforeDrug(c)
