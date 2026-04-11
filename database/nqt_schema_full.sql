-- ============================================================
-- NQT GYM MANAGEMENT + SUPPLEMENT STORE
-- MySQL Schema - FULL (Master file)
-- Chạy file này để tạo toàn bộ schema theo đúng thứ tự phụ thuộc
--
-- Cấu trúc 60 bảng / 20 nhóm:
--   Part 1  (Group 01-05): Cấu hình, Người dùng, Nhân sự, Hội viên, Gói tập
--   Part 2  (Group 06-10): PT, Lớp học, Dịch vụ phụ, Sản phẩm
--   Part 3  (Group 11-16): Kho hàng, Khách hàng, Tích điểm, Giỏ hàng, Khuyến mãi, Thanh toán
--   Part 4  (Group 17-20): Vận chuyển, Blog, Thông báo, OTP / Audit log
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- PART 1: GROUP 01-05
-- ============================================================
SOURCE nqt_schema_part1.sql;

-- ============================================================
-- PART 2: GROUP 06-10
-- ============================================================
SOURCE nqt_schema_part2.sql;

-- ============================================================
-- PART 3: GROUP 11-16
-- ============================================================
SOURCE nqt_schema_part3.sql;

-- ============================================================
-- PART 4: GROUP 17-20
-- ============================================================
SOURCE nqt_schema_part4.sql;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- DONE - Kiểm tra số bảng đã tạo:
-- SELECT COUNT(*) AS nqt_so_bang FROM information_schema.TABLES
-- WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME LIKE 'Nqt%';
-- ============================================================
