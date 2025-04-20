USE SUSUSHISHI_NoIndex
-------------------------------------- IMPORT DATA---------------------------------
-- CUSTOMER --
BULK INSERT CUSTOMER
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\customer_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- ONLINE_ACCESS_HISTORY --
BULK INSERT ONLINE_ACCESS_HISTORY
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\online_access_history_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- RESTAURANT_BRANCH --
BULK INSERT RESTAURANT_BRANCH
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\restaurant_branch_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- TABLE_ --
BULK INSERT TABLE_
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\table_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- DEPARTMENT -- 
BULK INSERT DEPARTMENT
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\department_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- EMPLOYEE --
BULK INSERT EMPLOYEE
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\employee_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- WORK_HISTORY --
BULK INSERT WORK_HISTORY
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\work_history_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- ACCOUNT -- 
BULK INSERT ACCOUNT
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\account_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- ORDER --
BULK INSERT ORDER_
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\order_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- OFFLINE_ORDER --
BULK INSERT OFFLINE_ORDER
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\offline_order_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- DELIVERY_ORDER --
BULK INSERT DELIVERY_ORDER
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\delivery_order_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- ONLINE_ORDER --
BULK INSERT ONLINE_ORDER
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\online_order_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- DISH --
BULK INSERT DISH
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\dish_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- DISH_AVAILABLE --
BULK INSERT DISH_AVAILABLE
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\dish_available_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- ORDER_DISH --
BULK INSERT ORDER_DISH
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\order_dish_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);

-- INVOICE --
BULK INSERT INVOICE
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\invoice_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- BRANCH_RATING --
BULK INSERT BRANCH_RATING
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\branch_rating_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO

-- MEMBERSHIP_CARD --
BULK INSERT MEMBERSHIP_CARD
FROM 'D:\KHTN\NAM3\1st_Semester\CSDLNC\NewSSRes\Sushi_Restaurant\CreateDB_ImportData\DATA\membership_data.csv'
WITH
(
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
	FIRSTROW = 2,
    CODEPAGE = '65001' -- UTF-8
);
GO