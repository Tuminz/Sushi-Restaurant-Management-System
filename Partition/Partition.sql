GO
USE SUSUSHISHI
GO
----------------------INVOICE-----------------------------------
-- File groups
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Invoice_FG_1997_2000;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Invoice_FG_2001_2004;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Invoice_FG_2005_2008;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Invoice_FG_2009_2012;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Invoice_FG_2013_2016;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Invoice_FG_2017_2020;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Invoice_FG_2021_2024;
GO

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Invoice_1997_2000',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_INVOICE\Invoice_1997_2000.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Invoice_FG_1997_2000;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Invoice_2001_2004',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_INVOICE\Invoice_2001_2004.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Invoice_FG_2001_2004;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Invoice_2005_2008',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_INVOICE\Invoice_2005_2008.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Invoice_FG_2005_2008;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Invoice_2009_2012',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_INVOICE\Invoice_2009_2012.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Invoice_FG_2009_2012;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Invoice_2013_2016',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_INVOICE\Invoice_2013_2016.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Invoice_FG_2013_2016;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Invoice_2017_2020',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_INVOICE\Invoice_2017_2020.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Invoice_FG_2017_2020;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Invoice_2021_2024',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_INVOICE\Invoice_2021_2024.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Invoice_FG_2021_2024;

-- Partition function
CREATE PARTITION FUNCTION pfInvoiceByYear(DATETIME)
AS RANGE RIGHT FOR VALUES 
(
    '2001-01-01',
    '2005-01-01',
    '2009-01-01',
    '2013-01-01',
    '2017-01-01',
    '2021-01-01',
    '2025-01-01'
);
GO

-- Partition scheme
CREATE PARTITION SCHEME psInvoiceByYear
AS PARTITION pfInvoiceByYear
TO (Invoice_FG_1997_2000, 
	Invoice_FG_2001_2004, 
	Invoice_FG_2005_2008, 
	Invoice_FG_2009_2012, 
	Invoice_FG_2013_2016, 
	Invoice_FG_2017_2020, 
	Invoice_FG_2021_2024, 
	[PRIMARY]
);
GO

-- Gỡ khóa ngoại
ALTER TABLE BRANCH_RATING DROP CONSTRAINT FK_BranchRating_Invoice;
GO
-- Gỡ khóa chính
ALTER TABLE INVOICE DROP CONSTRAINT PK_INVOICE;
GO
-- Đặt non clus idx cho khóa chính 
ALTER TABLE INVOICE ADD PRIMARY KEY NONCLUSTERED (INVOICE_ID ASC) ON [PRIMARY];
GO
-- Tạo clus idx cho ISSUE_DATE
CREATE CLUSTERED INDEX ix_issue_date ON INVOICE 
(
	ISSUE_DATE
) ON psInvoiceByYear(ISSUE_DATE);
GO

-- Thêm lại khóa ngoại
ALTER TABLE BRANCH_RATING
WITH CHECK ADD CONSTRAINT FK_BranchRating_Invoice
FOREIGN KEY (INVOICE_ID)
REFERENCES INVOICE (INVOICE_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;
GO


-- Chi tiết partition 
SELECT p.partition_number AS partition_number,
       f.name AS file_group,
       p.rows AS row_count
FROM sys.partitions p
JOIN sys.destination_data_spaces dds 
    ON p.partition_number = dds.destination_id
JOIN sys.filegroups f 
    ON dds.data_space_id = f.data_space_id
JOIN sys.indexes i 
    ON i.object_id = p.object_id AND i.index_id = p.index_id
WHERE OBJECT_NAME(i.OBJECT_ID) = 'INVOICE' 
  AND i.type = 1
  AND f.name LIKE 'Invoice%'
ORDER BY partition_number;

--------------------------------MEBERSHIP_CARD-------------------------------

-- File groups
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Card_FG_1997_2000;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Card_FG_2001_2004;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Card_FG_2005_2008;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Card_FG_2009_2012;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Card_FG_2013_2016;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Card_FG_2017_2020;
ALTER DATABASE SUSUSHISHI ADD FILEGROUP Card_FG_2021_2024;
GO

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Card_1997_2000',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_MEMCARD\Card_1997_2000.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Card_FG_1997_2000;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Card_2001_2004',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_MEMCARD\Card_2001_2004.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Card_FG_2001_2004;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Card_2005_2008',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_MEMCARD\Card_2005_2008.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Card_FG_2005_2008;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Card_2009_2012',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_MEMCARD\Card_2009_2012.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Card_FG_2009_2012;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Card_2013_2016',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_MEMCARD\Card_2013_2016.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Card_FG_2013_2016;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Card_2017_2020',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_MEMCARD\Card_2017_2020.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Card_FG_2017_2020;

ALTER DATABASE SUSUSHISHI ADD FILE 
(
    NAME = 'Card_2021_2024',
    FILENAME = 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\Partition\FG_MEMCARD\Card_2021_2024.ndf',
    SIZE = 5MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
) TO FILEGROUP Card_FG_2021_2024;
GO


-- Partition function
CREATE PARTITION FUNCTION pfMembershipCardByYear (DATE)
AS RANGE RIGHT FOR VALUES 
(
    '2001-01-01', 
    '2005-01-01', 
    '2009-01-01', 
    '2013-01-01',
    '2017-01-01', 
    '2021-01-01', 
    '2025-01-01'  
);

-- Partition scheme
CREATE PARTITION SCHEME psMembershipCardByYear
AS PARTITION pfMembershipCardByYear
TO (
    Card_FG_1997_2000, 
	Card_FG_2001_2004, 
	Card_FG_2005_2008,
    Card_FG_2009_2012, 
	Card_FG_2013_2016,
	Card_FG_2017_2020, 
	Card_FG_2021_2024,
	[PRIMARY]
);

-- Gỡ khóa ngoại
ALTER TABLE MEMBERSHIP_CARD DROP CONSTRAINT FK_MembershipCard_Customer;
GO
ALTER TABLE MEMBERSHIP_CARD DROP CONSTRAINT FK_MembershipCard_Employee;
GO
-- Gỡ khóa chính
ALTER TABLE MEMBERSHIP_CARD DROP CONSTRAINT PK_MEMBERSHIP_CARD;
GO
-- Đặt non clus idx cho khóa chính 
ALTER TABLE MEMBERSHIP_CARD ADD PRIMARY KEY NONCLUSTERED (CARD_ID ASC) ON [PRIMARY];
GO
-- Tạo clus idx cho DATE_ISSUED
CREATE CLUSTERED INDEX ix_date_issued ON MEMBERSHIP_CARD
(
	DATE_ISSUED
) ON psMembershipCardByYear(DATE_ISSUED);
GO

-- Thêm lại khóa ngoại
ALTER TABLE MEMBERSHIP_CARD
WITH CHECK ADD CONSTRAINT FK_MembershipCard_Customer
FOREIGN KEY (CUSTOMER_ID)
REFERENCES CUSTOMER (CUSTOMER_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;
GO

ALTER TABLE MEMBERSHIP_CARD
WITH CHECK ADD CONSTRAINT FK_MembershipCard_Employee
FOREIGN KEY (EMPLOYEE_ID)
REFERENCES EMPLOYEE (EMPLOYEE_ID)
ON UPDATE CASCADE
ON DELETE CASCADE;
GO

-- Chi tiết partition 
SELECT p.partition_number AS partition_number,
       f.name AS file_group,
       p.rows AS row_count
FROM sys.partitions p
JOIN sys.destination_data_spaces dds 
    ON p.partition_number = dds.destination_id
JOIN sys.filegroups f 
    ON dds.data_space_id = f.data_space_id
JOIN sys.indexes i 
    ON i.object_id = p.object_id AND i.index_id = p.index_id
WHERE OBJECT_NAME(i.OBJECT_ID) = 'MEMBERSHIP_CARD' 
  AND i.type = 1
  AND f.name LIKE 'Card%'
ORDER BY partition_number;

----------------Testing---------------------------
/*
SELECT COUNT(*)
FROM INVOICE


SELECT SUM(p.rows)
FROM sys.partitions p
JOIN sys.destination_data_spaces dds 
    ON p.partition_number = dds.destination_id
JOIN sys.filegroups f 
    ON dds.data_space_id = f.data_space_id
JOIN sys.indexes i 
    ON i.object_id = p.object_id AND i.index_id = p.index_id
WHERE OBJECT_NAME(i.OBJECT_ID) = 'MEMBERSHIP_CARD' 
  AND i.type = 1
  AND f.name LIKE 'Card%'


SELECT COUNT(*)
FROM MEMBERSHIP_CARD
*/