USE SUSUSHISHI
GO 

---------------------------------------- TRIGGER CHO BẢNG ACCOUNT ----------------------------------------
CREATE OR ALTER TRIGGER TRG_ACCOUNT_VALIDITY
ON ACCOUNT
FOR INSERT, UPDATE
AS
BEGIN
    -- Kiểm tra cả EMPLOYEE_ID và CUSTOMER_ID không được đồng thời cùng Có giá trị
    IF EXISTS (
        SELECT *
        FROM INSERTED
        WHERE EMPLOYEE_ID IS NOT NULL AND CUSTOMER_ID IS NOT NULL
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'EMPLOYEE_ID và CUSTOMER_ID không thể cùng tồn tại.', 16, 1)
    END

    -- Xác định ROLE dựa trên các điều kiện
    UPDATE ACCOUNT
    SET ROLE = 
        CASE 
            WHEN I.CUSTOMER_ID IS NOT NULL THEN N'Khách hàng'
            WHEN I.EMPLOYEE_ID IS NOT NULL THEN 
                CASE 
                    WHEN D.DEPARTMENT_NAME = N'Quản lý chi nhánh' THEN N'Quản lý chi nhánh'
                    ELSE N'Nhân viên'
                END
            ELSE N'Quản lý công ty'
        END
    FROM INSERTED I
    LEFT JOIN EMPLOYEE E ON I.EMPLOYEE_ID = E.EMPLOYEE_ID
    LEFT JOIN DEPARTMENT D ON E.DEPARTMENT_ID = D.DEPARTMENT_ID
    WHERE ACCOUNT.ACCOUNT_ID = I.ACCOUNT_ID
END
GO

---------------------------------------- TRIGGER CHO BẢNG EMPLOYEE ----------------------------------------
CREATE OR ALTER TRIGGER TRG_EMPLOYEE_VALIDITY
ON EMPLOYEE
FOR INSERT, UPDATE
AS
BEGIN
    -- Kiểm tra tuổi của nhân viên (>= 18 và <= 55)
    IF EXISTS (
        SELECT *
        FROM INSERTED
        WHERE DATEDIFF(YEAR, DATE_OF_BIRTH, GETDATE()) < 18
           OR DATEDIFF(YEAR, DATE_OF_BIRTH, GETDATE()) > 55
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Tuổi của nhân viên phải từ 18 đến 55!', 16, 1)
    END

    -- Kiểm tra start_date >= 18 năm từ date_of_birth
    IF EXISTS (
        SELECT *
        FROM INSERTED
        WHERE DATEDIFF(YEAR, DATE_OF_BIRTH, START_DATE_WORK) < 18
           OR DATEDIFF(YEAR, DATE_OF_BIRTH, START_DATE_WORK) > 55
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Ngày bắt đầu làm việc phải >= 18 và <= 55 năm từ ngày sinh!', 16, 1)
    END

    -- Kiểm tra termination_date hợp lệ
    IF EXISTS (
        SELECT *
        FROM INSERTED
        WHERE TERMINATION_DATE IS NOT NULL 
          AND (TERMINATION_DATE <= START_DATE_WORK 
          OR DATEDIFF(YEAR, DATE_OF_BIRTH, COALESCE(TERMINATION_DATE, GETDATE())) > 55)
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Ngày kết thúc làm việc không hợp lệ!', 16, 1)
    END

	-- Kiểm tra salary của nhân viên phải ít nhất là 10 triệu
	IF EXISTS (
		SELECT * 
		FROM INSERTED I 
		WHERE I.SALARY < 10000000 )
	BEGIN
		ROLLBACK
        RAISERROR(N'Lương của nhân viên phải ít nhất là 10 triệu!', 16, 1)
	END 

    -- Kiểm tra salary cho department_name "Quản lý chi nhánh" phải lớn nhất
    IF EXISTS (
        SELECT *
        FROM INSERTED I
        JOIN DEPARTMENT D ON I.DEPARTMENT_ID = D.DEPARTMENT_ID
        WHERE D.DEPARTMENT_NAME = N'Quản lý chi nhánh'
          AND I.SALARY < (SELECT MAX(SALARY) FROM EMPLOYEE)
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Lương của nhân viên thuộc "Quản lý chi nhánh" phải cao nhất!', 16, 1)
    END
END
GO
---------------------------------------- TRIGGER CHO BẢNG CUSTOMER ----------------------------------------
CREATE OR ALTER TRIGGER TRG_CUSTOMER_VALIDITY
ON CUSTOMER
FOR INSERT, UPDATE
AS
BEGIN
    -- Kiểm tra EMAIL đúng định dạng
    IF EXISTS (
        SELECT *
        FROM INSERTED
        WHERE EMAIL NOT LIKE '%@gmail.com'
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'EMAIL không đúng định dạng đuôi @gmail.com.', 16, 1)
    END
END
GO

---------------------------------------- TRIGGER CHO BẢNG MEMBERSHIP_CARD ----------------------------------------
CREATE OR ALTER TRIGGER TRG_MEMBERSHIP_CARD
ON MEMBERSHIP_CARD
FOR INSERT, UPDATE
AS
BEGIN
    -- Kiểm tra giá trị points không phù hợp với card_type
    IF EXISTS (
        SELECT *
        FROM INSERTED I
        WHERE (I.CARD_TYPE = N'Thẻ thành viên' AND I.POINTS NOT BETWEEN 0 AND 99) 
           OR (I.CARD_TYPE = N'Thẻ Silver' AND I.POINTS NOT BETWEEN 100 AND 199) 
           OR (I.CARD_TYPE = N'Thẻ Gold' AND I.POINTS NOT BETWEEN 200 AND 400)
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Giá trị POINTS không phù hợp với card_type.', 16, 1)
    END

    -- Kiểm tra date_issued
    IF EXISTS (
        SELECT *
        FROM INSERTED I
        JOIN ORDER_ O ON I.CUSTOMER_ID = O.CUSTOMER_ID
        WHERE I.DATE_ISSUED > O.ORDER_DATE AND I.CARD_TYPE = N'Thẻ thành viên'
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Giá trị DATE_ISSUED không hợp lệ. DATE_ISSUED phải nhỏ hơn ORDER_DATE của CUSTOMER.', 16, 1)
    END

    -- Kiểm tra employee_id làm việc tại thời điểm thẻ có hiệu lực
    IF EXISTS (
        SELECT *
        FROM INSERTED I
        JOIN EMPLOYEE E ON I.EMPLOYEE_ID = E.EMPLOYEE_ID
        WHERE I.DATE_ISSUED NOT BETWEEN E.START_DATE_WORK AND E.TERMINATION_DATE
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Giá trị EMPLOYEE_ID không hợp lệ. EMPLOYEE_ID phải làm việc tại thời điểm thẻ có hiệu lực.', 16, 1)
    END

    -- Cập nhật discount_amount
    UPDATE MEMBERSHIP_CARD
    SET DISCOUNT_AMOUNT = 
        CASE
            WHEN I.CARD_TYPE = N'Thẻ thành viên' THEN 50000
            WHEN I.CARD_TYPE = N'Thẻ Silver' THEN 100000
            WHEN I.CARD_TYPE = N'Thẻ Gold' THEN 200000
        END
    FROM INSERTED I
    WHERE MEMBERSHIP_CARD.CARD_ID = I.CARD_ID
END
GO

---------------------------------------- TRIGGER CHO BẢNG WORK_HISTORY ----------------------------------------
CREATE OR ALTER TRIGGER TRG_WORK_HISTORY
ON WORK_HISTORY
FOR INSERT, UPDATE
AS
BEGIN
    -- Kiểm tra branch_start_date và branch_end_date
    IF EXISTS (
        SELECT *
        FROM INSERTED I
        WHERE I.BRANCH_START_DATE > I.BRANCH_END_DATE
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Ngày không hợp lệ. BRANCH_START_DATE phải nhỏ hơn BRANCH_END_DATE.', 16, 1)
    END

    -- Kiểm tra branch_end_date với termination_date và start_date_work
    IF EXISTS (
        SELECT *
        FROM INSERTED I
        JOIN EMPLOYEE E ON I.EMPLOYEE_ID = E.EMPLOYEE_ID
        WHERE I.BRANCH_END_DATE < E.START_DATE_WORK 
           OR (E.TERMINATION_DATE IS NOT NULL AND I.BRANCH_END_DATE > E.TERMINATION_DATE)
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Ngày không hợp lệ.', 16, 1)
    END
END
GO

---------------------------------------- TRIGGER CHO BẢNG ORDER_ ----------------------------------------
CREATE OR ALTER TRIGGER TRG_ORDER
ON ORDER_
FOR INSERT, UPDATE
AS
BEGIN
    -- Kiểm tra thời gian đặt hàng với thời gian mở cửa chi nhánh
    IF EXISTS (
        SELECT *
        FROM INSERTED I
        JOIN RESTAURANT_BRANCH RB ON I.BRANCH_ID = RB.BRANCH_ID
        WHERE I.ORDER_TIME NOT BETWEEN RB.OPEN_TIME AND RB.CLOSE_TIME
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Thời gian đặt hàng không hợp lệ.', 16, 1)
    END

    -- Kiểm tra ngày đặt hàng với ngày phát hành thẻ thành viên
    IF EXISTS (
        SELECT *
        FROM INSERTED I
        JOIN MEMBERSHIP_CARD MC ON I.CUSTOMER_ID = MC.CUSTOMER_ID
        WHERE I.ORDER_DATE < MC.DATE_ISSUED AND MC.CARD_TYPE = N'Thẻ thành viên'
    )
    BEGIN
        ROLLBACK
        RAISERROR(N'Ngày đặt hàng không hợp lệ.', 16, 1)
    END

	-- Kiểm tra nếu BRANCH_ID thay đổi làm món ăn không còn hợp lệ với chi nhánh mới
    IF NOT EXISTS (
        SELECT *
        FROM INSERTED i, ORDER_DISH od,DISH_AVAILABLE da 
		WHERE i.ORDER_ID = od.ORDER_ID AND  od.DISH_ID = da.DISH_ID
        AND i.BRANCH_ID = da.BRANCH_ID AND da.IS_AVAILABLE = 1
    )
    BEGIN
		ROLLBACK
        RAISERROR (N'BRANCH_ID thay đổi làm món ăn không còn hợp lệ với chi nhánh mới', 16, 1)
    END

	-- Kiểm tra điều kiện để chặn việc cập nhật loại đơn hàng
    IF EXISTS (
        SELECT *
        FROM INSERTED i, ORDER_DISH od,DISH_AVAILABLE d
        WHERE i.ORDER_ID = od.ORDER_ID AND od.DISH_ID = d.DISH_ID AND i.BRANCH_ID = d.BRANCH_ID AND i.ORDER_TYPE = 'Delivery' 
		AND (d.IS_AVAILABLE = 0 OR d.IS_DELIVERABLE = 0)
    )
    BEGIN
	    ROLLBACK
        RAISERROR (N'Không thể thay đổi loại đơn hàng thành "Delivery" nếu nó chứa món ăn không khả dụng hoặc không hỗ trợ giao hàng!', 16, 1)
    END
END

GO
CREATE OR ALTER TRIGGER TRG_DELETE_ORDER
ON ORDER_
FOR DELETE
AS
BEGIN
    -- Kiểm tra nếu đơn hàng muốn xóa vẫn còn món ăn trong ORDER_DISH
    IF EXISTS (
        SELECT *
        FROM DELETED d, ORDER_DISH od 
		WHERE d.ORDER_ID = od.ORDER_ID
    )
    BEGIN
		ROLLBACK
        RAISERROR (N'Không thể xóa vì đã tạo ORDER_DISH!', 16, 1)
    END
END
---------------------------------------- TRIGGER CHO BẢNG RESTAURANT_BRANCH ----------------------------------------
GO
CREATE OR ALTER TRIGGER TRG_RESTAURANT_BRANCH
ON RESTAURANT_BRANCH
FOR INSERT, UPDATE
AS
BEGIN
    -- Kiểm tra điều kiện thời gian nằm trong khoảng 00:00 đến 23:59
    IF EXISTS (
        SELECT *
        FROM inserted
        WHERE 
            OPEN_TIME NOT BETWEEN '00:00:00' AND '23:59:59'
            OR CLOSE_TIME NOT BETWEEN '00:00:00' AND '23:59:59'
    )
    BEGIN
		ROLLBACK
        RAISERROR (N'Thời gian mở cửa và đóng cửa không hợp lệ ! Thời gian mở cửa và đóng cửa phải nằm trong khoảng 00:00 đến 23:59 !', 16, 1)
    END

	-- Kiểm tra điều kiện OPEN_TIME phải nhỏ hơn CLOSE_TIME
	IF EXISTS (
        SELECT *
        FROM inserted
        WHERE OPEN_TIME >= CLOSE_TIME
    )
    BEGIN
		ROLLBACK
        RAISERROR (N'Thời gian mở cửa và đóng cửa không hợp lệ. OPEN_TIME phải nhỏ hơn CLOSE_TIME!', 16, 1)
    END

	-- Kiểm tra điều kiện: có bất kỳ đơn hàng nào trong ONLINE_ORDER với ARRIVAL_DATE >= hôm nay -> Ko cho update open time và close time
    IF EXISTS (
        SELECT *
        FROM ONLINE_ORDER o, INSERTED i
        WHERE o.BRANCH_ID = i.BRANCH_ID 
          AND o.ARRIVAL_DATE >= CAST(GETDATE() AS DATE)
    )
    BEGIN
        ROLLBACK
        RAISERROR (N'Không thể update open time và close time!', 16, 1)
    END
END
GO

---------------------------------------- TRIGGER CHO BẢNG ORDER_DISH ----------------------------------------
CREATE OR ALTER TRIGGER TRG_ORDER_DISH
ON ORDER_DISH
FOR INSERT, UPDATE
AS
BEGIN
    -- Kiểm tra xem món ăn có tồn tại trong thực đơn của chi nhánh và có IS_AVAILABLE = 1 không
    IF NOT EXISTS (
        SELECT *
        FROM INSERTED i, ORDER_ o, DISH_AVAILABLE da
        WHERE i.ORDER_ID = o.ORDER_ID AND i.DISH_ID = da.DISH_ID AND  o.BRANCH_ID = da.BRANCH_ID AND da.IS_AVAILABLE = 1
    )
    BEGIN
        -- Ngăn chặn insert nếu món ăn không có trong thực đơn hoặc không có sẵn
		ROLLBACK
        RAISERROR ('Món ăn không tồn tại trong thực đơn của chi nhánh hoặc không có sẵn.', 16, 1)
    END

	-- Kiểm tra điều kiện để chặn việc thêm món ăn không hỗ trợ giao hàng với các order có type là Delivery
    IF EXISTS (
        SELECT *
        FROM INSERTED i, ORDER_ o, DISH_AVAILABLE d
        WHERE  i.ORDER_ID = o.ORDER_ID AND i.DISH_ID = d.DISH_ID AND o.BRANCH_ID = d.BRANCH_ID
		AND o.ORDER_TYPE = 'Delivery' AND d.IS_DELIVERABLE = 0
    )
    BEGIN
		ROLLBACK 
        RAISERROR (N'Món ăn phải hỗ trợ giao hàng với order có type là Delivery!', 16, 1)
    END
END

GO
CREATE OR ALTER TRIGGER TRG_DELETE_ORDER_DISH
ON ORDER_DISH
FOR DELETE
AS
BEGIN
    -- Kiểm tra nếu món ăn thuộc về một đơn hàng đã có hóa đơn
    IF EXISTS (
        SELECT *
        FROM DELETED d, INVOICE i
        WHERE d.ORDER_ID = i.ORDER_ID
    )
    BEGIN
        -- Ngăn chặn thao tác xóa và thông báo lỗi
		ROLLBACK
        RAISERROR (N'Không thể xóa món ăn từ đơn hàng đã tạo hóa đơn.', 16, 1)
    END
END

---------------------------------------- TRIGGER CHO BẢNG DISH_AVAILABLE ----------------------------------------
GO
CREATE OR ALTER TRIGGER TRG_DELETE_DA
ON DISH_AVAILABLE
FOR DELETE
AS
BEGIN
    -- Kiểm tra nếu món ăn bị xóa vẫn còn được sử dụng trong ORDER_DISH
    IF EXISTS (
        SELECT *
        FROM DELETED d, ORDER_DISH od, ORDER_ o
        WHERE d.DISH_ID = od.DISH_ID AND od.ORDER_ID = o.ORDER_ID AND o.BRANCH_ID = d.BRANCH_ID
    )
    BEGIN
		ROLLBACK 
        RAISERROR (N'Không thể xóa món ăn vì vẫn đang được sử dụng trong đơn hàng.', 16, 1)
    END
END

GO
CREATE OR ALTER TRIGGER TRG_DA
ON DISH_AVAILABLE
FOR UPDATE
AS
BEGIN
    -- Kiểm tra nếu IS_AVAILABLE được cập nhật thành 0 nhưng món ăn vẫn còn trong ORDER_DISH
    IF EXISTS (
        SELECT *
        FROM INSERTED i, ORDER_DISH od, ORDER_ o
        WHERE i.DISH_ID = od.DISH_ID AND od.ORDER_ID = o.ORDER_ID AND o.BRANCH_ID = i.BRANCH_ID AND i.IS_AVAILABLE = 0
    )
    BEGIN
		ROLLBACK
        RAISERROR (N'Không thể đánh dấu món ăn không khả dụng vì vẫn đang được sử dụng trong đơn hàng.', 16, 1)
    END

	-- Kiểm tra điều kiện để chặn việc cập nhật trạng thái món ăn thành không hỗ trợ giao hàng nếu món ăn đã thuộc đơn hàng "Delivery".
    IF EXISTS (
        SELECT *
        FROM INSERTED i, ORDER_DISH od, ORDER_ o
        WHERE i.DISH_ID = od.DISH_ID AND i.BRANCH_ID = od.ORDER_ID AND od.ORDER_ID = o.ORDER_ID 
		AND o.ORDER_TYPE = 'Delivery' AND i.IS_DELIVERABLE = 0
    )
    BEGIN
        ROLLBACK
        RAISERROR (N'Không thể cập nhật trạng thái món ăn thành không hỗ trợ giao hàng nếu món ăn đã thuộc đơn hàng Delivery !', 16, 1)
	END
END

GO
---------------------------------------- TRIGGER CHO BẢNG ONLINE_ORDER ----------------------------------------
CREATE OR ALTER TRIGGER TRG_ONLINE_ORDER
ON ONLINE_ORDER
FOR INSERT, UPDATE
AS
BEGIN
	-- Kiểm tra rằng OORDER_ID trong ONLINE_ORDER phải tồn tại trong ORDER_ với ORDER_TYPE = 'Online'
    IF EXISTS (
        SELECT *
        FROM INSERTED
        WHERE NOT EXISTS (
            SELECT 1
            FROM ORDER_
            WHERE ORDER_ID = INSERTED.OORDER_ID AND ORDER_TYPE = 'Online'
        )
    )
    BEGIN
		ROLLBACK
        RAISERROR (N'OORDER_ID phải tồn tại trong bảng ORDER_ với loại đơn hàng là "Online".', 16, 1)
    END

    -- Kiểm tra điều kiện: ARRIVAL_TIME phải >= OPEN_TIME và <= CLOSE_TIME
    IF EXISTS (
        SELECT *
        FROM INSERTED i
        WHERE EXISTS (
            SELECT 1
            FROM RESTAURANT_BRANCH rb
            WHERE rb.BRANCH_ID = i.BRANCH_ID
              AND (i.ARRIVAL_TIME < rb.OPEN_TIME OR i.ARRIVAL_TIME > rb.CLOSE_TIME)
        )
    )
    BEGIN
		ROLLBACK
        RAISERROR (N'Khách chỉ được đặt bàn trong giờ hoạt động của chi nhánh !', 16, 1)
    END

	-- Kiểm tra điều kiện: CUSTOMER_QUANTITY phải <= SEAT_AVAILABLE của bàn được chọn
    IF EXISTS (
        SELECT 1
        FROM INSERTED i
        WHERE EXISTS (
            SELECT *
            FROM TABLE_ t
            WHERE t.BRANCH_ID = i.BRANCH_ID
              AND t.TABLE_NUM = i.TABLE_NUMBER
              AND i.CUSTOMER_QUANTITY > t.SEAT_AVAILABLE
        )
    )
    BEGIN
        ROLLBACK
        RAISERROR (N'Số lượng khách đến tối đa phải bé hơn hoặc bằng quy định của bàn được chọn! ', 16, 1)
    END
END

---------------------------------------- TRIGGER CHO BẢNG TABLE_ ----------------------------------------
GO
CREATE OR ALTER TRIGGER TRG_TABLE
ON TABLE_
FOR UPDATE
AS
BEGIN
    -- Kiểm tra điều kiện: Không cho phép cập nhật SEAT_AVAILABLE nếu có đơn hàng với ARRIVAL_DATE >= hôm nay
    IF EXISTS (
        SELECT *
        FROM INSERTED i, ONLINE_ORDER o
        WHERE o.BRANCH_ID = i.BRANCH_ID
          AND o.TABLE_NUMBER = i.TABLE_NUM
          AND o.ARRIVAL_DATE >= CAST(GETDATE() AS DATE)
    )
    BEGIN
        ROLLBACK
        RAISERROR (N'Không thể cập nhật SEAT_AVAILABLE vì có đơn hàng sắp tới cho bảng này!', 16, 1)
    END
END
GO

---------------------------------------- TRIGGER CHO BẢNG OFFLINE_ORDER ----------------------------------------
CREATE OR ALTER TRIGGER TRG_OFFLINE_ORDER
ON OFFLINE_ORDER
FOR INSERT, UPDATE
AS
BEGIN
	-- Kiểm tra rằng OFORDER_ID trong OFFLINE_ORDER phải tồn tại trong ORDER_ với ORDER_TYPE = 'Offline'
    IF EXISTS (
        SELECT *
        FROM INSERTED
        WHERE NOT EXISTS (
            SELECT 1
            FROM ORDER_
            WHERE ORDER_ID = INSERTED.OFORDER_ID AND ORDER_TYPE = 'Offline'
        )
    )
    BEGIN
		ROLLBACK
        RAISERROR (N'OFORDER_ID phải tồn tại trong bảng ORDER_ với loại đơn hàng là "Offline".', 16, 1)
    END

    -- Kiểm tra điều kiện của nhân viên
    IF EXISTS (
        SELECT *
        FROM INSERTED i
        WHERE NOT EXISTS (
            SELECT *
            FROM WORK_HISTORY wh, ORDER_ o
            WHERE wh.EMPLOYEE_ID = i.EMPLOYEE_ID
              AND wh.BRANCH_ID = i.BRANCH_ID
              AND o.ORDER_ID = i.OFORDER_ID
              AND o.ORDER_DATE BETWEEN wh.BRANCH_START_DATE AND ISNULL(wh.BRANCH_END_DATE, CAST(GETDATE() AS DATE))
        )
    )
    BEGIN
		ROLLBACK
        RAISERROR (N'Đơn hàng offline phải được tạo bởi nhân viên đang làm tại chi nhánh đó tại thời điểm tạo đơn.', 16, 1)
    END
END
GO

---------------------------------------- TRIGGER CHO BẢNG DELIVERY_ORDER ----------------------------------------
CREATE OR ALTER TRIGGER TRG_DELIVERY_ORDER
ON DELIVERY_ORDER
FOR INSERT, UPDATE
AS
BEGIN
    -- Kiểm tra rằng DORDER_ID trong DELIVERY_ORDER phải tồn tại trong ORDER_ với ORDER_TYPE = 'Delivery'
    IF EXISTS (
        SELECT *
        FROM INSERTED
        WHERE NOT EXISTS (
            SELECT *
            FROM ORDER_
            WHERE ORDER_ID = INSERTED.DORDER_ID AND ORDER_TYPE = 'Delivery'
        )
    )
    BEGIN
		ROLLBACK
        RAISERROR (N'DORDER_ID phải tồn tại trong bảng ORDER_ với loại đơn hàng là "Delivery".', 16, 1)
    END
END