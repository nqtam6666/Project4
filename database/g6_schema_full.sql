-- ============================================================
-- G6 GYM MANAGEMENT + SUPPLEMENT STORE
-- SQL Server Schema - FULL (Master file)
-- Chạy file này để tạo toàn bộ schema theo đúng thứ tự phụ thuộc
--
-- Cấu trúc ~60 bảng / 20 nhóm:
--   Part 1  (Group 01-05): Cấu hình, Người dùng, Nhân sự, Hội viên, Gói tập
--   Part 2  (Group 06-10): PT, Lớp học, Dịch vụ phụ, Sản phẩm
--   Part 3  (Group 11-16): Kho hàng, Khách hàng, Tích điểm, Giỏ hàng, Khuyến mãi, Thanh toán
--   Part 4  (Group 17-20): Vận chuyển, Blog, Thông báo, OTP / Audit log
--
-- Hướng dẫn chạy trên SQL Server:
--   1. Chạy g6_drop_all.sql trước (nếu cần xóa schema cũ)
--   2. Chạy lần lượt từng file part hoặc dùng SSMS mở file này
--      và chạy từng phần thủ công (SQL Server không hỗ trợ SOURCE)
-- ============================================================

-- ============================================================
-- PART 1: GROUP 01-05
-- Cấu hình, Vai trò, Quyền, Chi nhánh, Người dùng, Nhân viên, Hội viên, Gói tập
-- ============================================================
-- :r g6_sqlserver_part1.sql

-- ============================================================
-- PART 2: GROUP 06-10
-- HLV, Gói PT, Lớp học, Dịch vụ phụ, Danh mục SP, Sản phẩm, Biến thể
-- ============================================================
-- :r g6_sqlserver_part2.sql

-- ============================================================
-- PART 3: GROUP 11-16
-- Kho hàng, Khách hàng, Tích điểm, Giỏ hàng, Đơn hàng, Mã giảm giá, Thanh toán
-- ============================================================
-- :r g6_sqlserver_part3.sql

-- ============================================================
-- PART 4: GROUP 17-20
-- Vận chuyển, Blog, Đánh giá SP, Thông báo, OTP, Phiên đăng nhập, Nhật ký
-- ============================================================
-- :r g6_sqlserver_part4.sql

-- ============================================================
-- DONE - Kiểm tra số bảng đã tạo:
-- SELECT COUNT(*) AS g6_so_bang FROM INFORMATION_SCHEMA.TABLES
-- WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'G6%';
-- ============================================================

PRINT N'Schema đã tạo hoàn tất! Kiểm tra số bảng:';
SELECT COUNT(*) AS g6_so_bang FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME LIKE 'G6%';
GO
