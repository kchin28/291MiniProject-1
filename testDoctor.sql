INSERT INTO patients VALUES ('34wsa','Sammy Ab','25-30','fakeaddress','780-123-4566','780-123-4566'); 

INSERT INTO charts VALUES  ('abcdh','34wsa','1999-03-01','1999-03-07');
INSERT INTO charts VALUES  ('abcdt','34wsa','1995-03-01','1995-05-07');
INSERT INTO charts (chart_id,hcno,adate) VALUES  ('abcd4','34wsa','2010-03-02');

INSERT INTO drugs VALUES ('Tylenol', "pain");
INSERT INTO drugs VALUES ('A', "B");


INSERT INTO staff VALUES ('qwed2','D','jelly','kgchin','5006bab5782456808d60bddfa64db2d13d90b2c5550ba1ff2b2acad7');

INSERT INTO medications VALUES  ('34wsa','abcd4','qwed2','2010-03-07','2010-03-07','2010-03-09',200,'drug132');

INSERT INTO symptoms VALUES  ('34wsa','abcd4','qwed2','2010-03-07','excessive coughing');

INSERT INTO diagnoses VALUES  ('34wsa','abcd4','qwed2','2010-03-07','common cold');

INSERT INTO dosage VALUES  ('Tylenol','25-30',100);
INSERT INTO dosage VALUES  ('Advil','40-45',200);
INSERT INTO dosage VALUeS ('A', "25-30", 400);


INSERT INTO reportedallergies VALUES ('34wsa','Tylenol');
INSERT INTO inferredallergies VALUES ('Tylenol','Advil');
INSERT INTO inferredallergies VALUES ('Tylenol','A');
INSERT INTO inferredallergies VALUES ('A','Tylenol');
