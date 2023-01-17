CREATE TABLE rockwell
(
    L3EmpCreditingHierarchy text, 
	Concat TEXT, 
	Metric1 text,
	Metric2 text,
	Metric3 text,
	TransactionType text,
	
	SourceTransactionID text,
	PBIIndex text,
	Date TEXT,
	
	TransactionAmount text, 
	DeltaDate text    
)
WITH (
  OIDS=FALSE

);


---COPY rockwell FROM 'C:\tmp\CALC_ Employee Transactions (1).txt' 

---select* from rockwell limit 5

--delete from rockwell
--where concat = 'Concat';

CREATE TABLE rockwell2
(
    L3EmpCreditingHierarchy text, 
	Concat TEXT, 
	Metric1 text,
	Metric2 text,
	Metric3 text,
	TransactionType text,
	
	SourceTransactionID text,
	PBIIndex text,
	Date TEXT,
	
	TransactionAmount text, 
	DeltaDate text    
)
WITH (
  OIDS=FALSE

);

---COPY rockwell2 FROM 'C:\tmp\SIP Employee Transactions 12-10-2022.txt'

select* from rockwell2 limit 5

--delete from rockwell2
--where concat = 'Concat';



--ALTER TABLE rockwell2  
--DROP COLUMN concat,
--DROP COLUMN metric1,
--DROP COLUMN metric2,
---DROP COLUMN metric3,
--DROP COLUMN transactiontype,
--DROP COLUMN pbiindex,
--DROP COLUMN date,
--DROP COLUMN transactionamount,
--DROP COLUMN deltadate;



create table rockwell3
as 
select rockwell.L3EmpCreditingHierarchy , 
	rockwell.Concat , 
	rockwell.Metric1 ,
	rockwell.Metric2 ,
	rockwell.Metric3 ,
	rockwell.TransactionType ,
	
	rockwell.SourceTransactionID ,
	rockwell.PBIIndex ,
	rockwell.Date,
	
	rockwell.TransactionAmount , 
	rockwell.DeltaDate, 
	rockwell2.L3EmpCreditingHierarchy as L3EmpCreditingHierarchy2, 
	rockwell2.SourceTransactionID as SourceTransactionID2   
	from rockwell left JOIN  rockwell2 on rockwell.l3empcreditinghierarchy = rockwell2.l3empcreditinghierarchy;
	
	

--delete from rockwell3
--where l3empcreditinghierarchy2 IS NOT NULL;

--ALTER TABLE rockwell3  
--DROP COLUMN l3empcreditinghierarchy2, DROP COLUMN sourcetransactionid2;

--select * from rockwell3 where sourcetransactionid = 'C12224980'

COPY rockwell3 TO 'C:\tmp\missingdata.txt' CSV HEADER;	
	
	