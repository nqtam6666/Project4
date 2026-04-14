-- ============================================================
-- G6 GYM MANAGEMENT + SUPPLEMENT STORE
-- SQL Server Schema - DROP ALL TABLES
-- Chạy file này trước khi tạo lại schema
-- ============================================================

-- Tắt kiểm tra FK
EXEC sp_MSforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL';

-- Drop tất cả bảng Nqt* và Nxv* cũ (nếu còn)
DECLARE @sql NVARCHAR(MAX) = N'';

SELECT @sql += 'DROP TABLE IF EXISTS [' + TABLE_NAME + '];' + CHAR(13)
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
  AND (TABLE_NAME LIKE 'Nqt%' OR TABLE_NAME LIKE 'Nxv%' OR TABLE_NAME LIKE 'G6%');

EXEC sp_executesql @sql;

PRINT 'Đã xóa tất cả bảng cũ!';
GO
