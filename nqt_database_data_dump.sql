-- ============================================================
-- NQT GYM SYSTEM - COMPLETE DATABASE DATA EXPORT DUMP
-- Exported on: 2026-06-02 11:07:05
-- Database: nqtam_project4
-- Hướng dẫn khôi phục:
--   1. Chạy các file schema trong thư mục database/ để tạo cấu trúc bảng.
--   2. Chạy file nqt_database_data_dump.sql này để khôi phục dữ liệu.
-- ============================================================

USE [nqtam_project4];
GO

-- 1. Vô hiệu hóa tất cả foreign key constraints để tránh lỗi phụ thuộc
EXEC sp_MSforeachtable "ALTER TABLE ? NOCHECK CONSTRAINT all";
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6BaiViet]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6BaiViet] ON;
GO

INSERT INTO [G6BaiViet] ([g6_ma_bai_viet], [g6_ma_danh_muc], [g6_tieu_de], [g6_slug], [g6_mo_ta_ngan], [g6_noi_dung], [g6_hinh_dai_dien], [g6_tac_gia], [g6_trang_thai], [g6_luot_xem], [g6_tu_khoa_seo], [g6_san_pham_lien_quan], [g6_ngay_xuat_ban], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1, 1, N'Cách tập Squat đúng cách', N'cach-tap-squat-dung-cach', NULL, N'Nội dung hướng dẫn chi tiết...', NULL, 1, N'da_xuat_ban', 0, NULL, NULL, NULL, N'2026-05-12 09:03:02.277000', N'2026-05-12 09:03:02.277000');
GO

SET IDENTITY_INSERT [G6BaiViet] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6Banner]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6Banner] ON;
GO

INSERT INTO [G6Banner] ([g6_ma_banner], [g6_tieu_de], [g6_hinh_anh], [g6_duong_dan], [g6_vi_tri], [g6_thu_tu], [g6_ngay_bat_dau], [g6_ngay_ket_thuc], [g6_la_hoat_dong]) VALUES (1, N'Test Banner', N'https://example.com/image.jpg', N'https://example.com', N'', 1, NULL, NULL, 1);
INSERT INTO [G6Banner] ([g6_ma_banner], [g6_tieu_de], [g6_hinh_anh], [g6_duong_dan], [g6_vi_tri], [g6_thu_tu], [g6_ngay_bat_dau], [g6_ngay_ket_thuc], [g6_la_hoat_dong]) VALUES (2, N'Test Banner', N'https://placehold.co/600x400', N'https://google.com', N'slider', 0, NULL, NULL, 1);
GO

SET IDENTITY_INSERT [G6Banner] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6BienTheSanPham]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6BienTheSanPham] ON;
GO

INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (1, 1, N'WHEY-G-01', N'Hộp 2kg - Socola', NULL, NULL, NULL, NULL, 1200000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (20, 20, N'JAC-JACKE-700', N'Mặc định', NULL, NULL, NULL, NULL, 1450000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (21, 21, N'PER-PERFE-366', N'Mặc định', NULL, NULL, NULL, NULL, 3390000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (22, 22, N'DYM-DYMAT-328', N'Mặc định', NULL, NULL, NULL, NULL, 3800000, 3850000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (23, 23, N'BEY-BEYON-322', N'Mặc định', NULL, NULL, NULL, NULL, 3000000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (24, 24, N'PRE-PREMI-675', N'Mặc định', NULL, NULL, NULL, NULL, 1190000, 1550000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (25, 25, N'PER-PERFE-874', N'Mặc định', NULL, NULL, NULL, NULL, 1490000, 1990000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (26, 26, N'AXE-AXE-S-200', N'Mặc định', NULL, NULL, NULL, NULL, 1050000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (27, 27, N'NUT-NUTRA-718', N'Mặc định', NULL, NULL, NULL, NULL, 1150000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (28, 28, N'ELI-ELITE-767', N'Mặc định', NULL, NULL, NULL, NULL, 2900000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (29, 29, N'PVL-PVL-I-237', N'Mặc định', NULL, NULL, NULL, NULL, 2850000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (30, 30, N'NUT-NUTRA-326', N'Mặc định', NULL, NULL, NULL, NULL, 3290000, 3350000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (31, 31, N'NUT-NUTRA-563', N'Mặc định', NULL, NULL, NULL, NULL, 2490000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (32, 32, N'LAB-LABRA-862', N'Mặc định', NULL, NULL, NULL, NULL, 1950000, 2150000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (33, 33, N'MUT-MUTAN-894', N'Mặc định', NULL, NULL, NULL, NULL, 2300000, 2450000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (34, 34, N'OPT-ON-SE-421', N'Mặc định', NULL, NULL, NULL, NULL, 2380000, 2490000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (35, 35, N'BIO-BIOTE-380', N'Mặc định', NULL, NULL, NULL, NULL, 1750000, 1790000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (36, 36, N'MUT-MUTAN-865', N'Mặc định', NULL, NULL, NULL, NULL, 1720000, 1750000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (37, 37, N'RUL-SỮA-T-620', N'Mặc định', NULL, NULL, NULL, NULL, 1650000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (38, 38, N'OPT-ON-SE-542', N'Mặc định', NULL, NULL, NULL, NULL, 1320000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (39, 39, N'MUT-MUTAN-102', N'Mặc định', NULL, NULL, NULL, NULL, 950000, 1000000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (40, 40, N'GEN-TÁCH--950', N'Mặc định', NULL, NULL, NULL, NULL, 360000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (41, 41, N'ELI-ELITE-732', N'Mặc định', NULL, NULL, NULL, NULL, 1160000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (42, 42, N'NUT-NUTRE-839', N'Mặc định', NULL, NULL, NULL, NULL, 1760000, 1950000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (43, 43, N'APP-SỮA-T-130', N'Mặc định', NULL, NULL, NULL, NULL, 2200000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (44, 44, N'GEN-GĂNG--310', N'Mặc định', NULL, NULL, NULL, NULL, 180000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (45, 45, N'HAR-GĂNG--339', N'Mặc định', NULL, NULL, NULL, NULL, 430000, 450000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (46, 46, N'HAR-GĂNG--515', N'Mặc định', NULL, NULL, NULL, NULL, 430000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (47, 47, N'HAR-HARBI-319', N'Mặc định', NULL, NULL, NULL, NULL, 480000, 510000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (48, 48, N'HAR-HARBI-647', N'Mặc định', NULL, NULL, NULL, NULL, 510000, 550000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (49, 49, N'HAR-HARBI-609', N'Mặc định', NULL, NULL, NULL, NULL, 520000, 550000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (50, 50, N'HAR-HARBI-720', N'Mặc định', NULL, NULL, NULL, NULL, 600000, 680000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (51, 51, N'HAR-HARBI-303', N'Mặc định', NULL, NULL, NULL, NULL, 600000, 680000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (52, 52, N'HAR-HARBI-141', N'Mặc định', NULL, NULL, NULL, NULL, 610000, 660000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (53, 53, N'HAR-HARBI-852', N'Mặc định', NULL, NULL, NULL, NULL, 650000, 730000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (54, 54, N'HAR-HARBI-794', N'Mặc định', NULL, NULL, NULL, NULL, 700000, NULL, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (55, 55, N'HAR-HARBI-572', N'Mặc định', NULL, NULL, NULL, NULL, 700000, 750000, NULL, 1, 1, 0);
INSERT INTO [G6BienTheSanPham] ([g6_ma_bien_the], [g6_ma_san_pham], [g6_sku], [g6_ten_bien_the], [g6_trong_luong], [g6_trong_luong_gram], [g6_so_luot_dung], [g6_huong_vi], [g6_gia], [g6_gia_so_sanh], [g6_hinh_anh], [g6_la_mac_dinh], [g6_la_hoat_dong], [g6_thu_tu]) VALUES (1002, 1002, N'test-default', N'Mặc định', NULL, NULL, NULL, NULL, 11000, NULL, NULL, 1, 1, 0);
GO

SET IDENTITY_INSERT [G6BienTheSanPham] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6BuoiTapPT]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6BuoiTapPT] ON;
GO

INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (1, 2, 10, 1, 1, N'2026-05-19 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-19 13:45:05.267000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (2, 2, 10, 1, 1, N'2026-05-19 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-19 13:45:07.157000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (3, 2, 10, 1, 1, N'2026-05-19 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-19 13:45:07.770000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (4, 2, 10, 1, 1, N'2026-05-19 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-19 13:45:07.950000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (5, 2, 10, 1, 1, N'2026-05-19 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-19 13:45:08.113000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (6, 2, 10, 1, 1, N'2026-05-19 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-19 13:45:08.260000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (7, 2, 10, 1, 1, N'2026-05-19 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-19 13:45:08.420000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (8, 2, 10, 1, 1, N'2026-05-19 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-19 13:56:44.740000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (9, 3, 10, 1, 1, N'2026-05-20 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-20 08:29:54.953000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (10, 3, 10, 1, 1, N'2026-05-20 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-20 08:29:56.543000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (11, 3, 10, 1, 1, N'2026-05-20 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-20 08:29:56.717000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (12, 3, 10, 1, 1, N'2026-05-20 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-20 08:29:56.887000');
INSERT INTO [G6BuoiTapPT] ([g6_ma_buoi_tap], [g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_hlv], [g6_ma_chi_nhanh], [g6_ngay_tap], [g6_thoi_luong], [g6_trang_thai], [g6_noi_dung_buoi_tap], [g6_nhan_xet_hlv], [g6_danh_gia_hoi_vien], [g6_ngay_tao]) VALUES (13, 3, 10, 1, 1, N'2026-05-20 00:00:00', 60, N'cho_xac_nhan', NULL, NULL, NULL, N'2026-05-20 08:29:57.033000');
GO

SET IDENTITY_INSERT [G6BuoiTapPT] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6CauHinh]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6CauHinh] ON;
GO

INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (1, N'g6_ten_website', N'G6 Gym', N'string', N'website', N'Tên website', N'2026-05-12 11:18:15.683000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (2, N'g6_jwt_het_han_phut', N'1440', N'int', N'security', N'JWT expiration (mins)', N'2026-05-12 09:03:02.013000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (3, N'g6_phi_ship_mac_dinh', N'30000', N'int', N'shipping', N'Default shipping fee', N'2026-05-12 09:03:02.013000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (4, N'g6_mo_ta_website', N'Đây là project 4 của sinh viên năm 3 trường Đại học Nguyễn Trãi. 
Thành viên: Nguyễn Quang Tâm - Đoàn Anh Quân - Nguyễn Xuân Vinh - Nguyễn Hoài Nam', N'string', N'website', NULL, N'2026-05-12 11:18:15.690000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (5, N'g6_logo_url', N'/static/uploads/66f31dfadb3742c78c82c13e13c6cbc8.jpg', N'string', N'website', NULL, N'2026-05-19 10:49:58.607000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (6, N'g6_favicon_url', N'/static/uploads/c74e11d3dff442deb3b8d3c332af5a07.jpg', N'string', N'website', NULL, N'2026-05-19 10:49:58.627000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (7, N'g6_email_lien_he', N'nguyenquangtam179@gmail.com', N'string', N'website', NULL, N'2026-05-12 11:18:15.700000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (8, N'g6_so_dien_thoai_hotline', N'096 1138 440', N'string', N'website', NULL, N'2026-05-12 11:18:15.703000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (9, N'g6_dia_chi_tru_so', N'Xã Đại Thanh, Hà Nội', N'string', N'website', NULL, N'2026-05-12 11:18:15.707000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (10, N'g6_facebook_url', N'https://facebook.com/', N'string', N'website', NULL, N'2026-05-12 11:18:15.710000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (11, N'g6_zalo_url', N'https://zalo.me/', N'string', N'website', NULL, N'2026-05-12 11:18:15.710000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (12, N'g6_gio_mo_cua', N'05:00', N'string', N'business', NULL, N'2026-05-12 11:18:37.790000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (13, N'g6_gio_dong_cua', N'23:00', N'string', N'business', NULL, N'2026-05-12 11:18:37.800000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (14, N'g6_so_luot_checkin_ngay_mac_dinh', N'2', N'string', N'business', NULL, N'2026-05-12 11:18:37.803000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (15, N'g6_cho_phep_checkin_truoc_phut', N'30', N'string', N'business', NULL, N'2026-05-12 11:18:37.807000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (16, N'g6_suc_chua_mac_dinh', N'100', N'string', N'business', NULL, N'2026-05-12 11:18:37.810000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (17, N'g6_so_ngay_nhac_het_han', N'7', N'string', N'business', NULL, N'2026-05-12 11:18:37.813000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (18, N'g6_so_ngay_nhac_lan_2', N'5', N'string', N'business', NULL, N'2026-05-12 11:18:37.817000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (19, N'g6_smtp_host', N'smtp.gmail.com', N'string', N'email', NULL, N'2026-05-12 11:19:13.603000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (20, N'g6_smtp_port', N'587', N'string', N'email', NULL, N'2026-05-12 11:19:13.607000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (21, N'g6_smtp_bao_mat', N'tls', N'string', N'email', NULL, N'2026-05-12 11:19:13.610000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (22, N'g6_smtp_email', N'nguyenquangtam6666@gmail.com', N'string', N'email', NULL, N'2026-05-12 11:19:13.613000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (23, N'g6_smtp_mat_khau', N'lxki pknn uocd wwjt', N'string', N'email', NULL, N'2026-05-12 11:19:13.617000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (24, N'g6_email_gui_tu', N'nguyenquangtam6666@gmail.com', N'string', N'email', NULL, N'2026-05-12 11:19:13.620000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (25, N'g6_ten_nguoi_gui_email', N'G6 Gym', N'string', N'email', NULL, N'2026-05-12 11:19:13.623000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (26, N'g6_tien_te', N'VND', N'string', N'payment', NULL, N'2026-05-12 11:19:25.173000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (27, N'g6_thue_vat_phan_tram', N'7', N'string', N'payment', NULL, N'2026-05-12 11:19:25.177000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (28, N'g6_phi_giao_hang_mac_dinh', N'50000', N'string', N'payment', NULL, N'2026-05-12 11:19:25.180000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (29, N'g6_mien_phi_giao_hang_tu', N'200000', N'string', N'payment', NULL, N'2026-05-12 11:19:25.183000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (30, N'g6_jwt_expiry_giay', N'86400000', N'string', N'security', NULL, N'2026-05-12 11:20:42.740000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (31, N'g6_so_lan_sai_mat_khau', N'3', N'string', N'security', NULL, N'2026-05-12 11:20:42.747000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (32, N'g6_thoi_gian_khoa_phut', N'5', N'string', N'security', NULL, N'2026-05-12 11:20:42.750000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (33, N'g6_otp_het_han_phut', N'5', N'string', N'security', NULL, N'2026-05-12 11:20:42.753000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (34, N'g6_diem_tren_moi_1000_dong', N'1', N'string', N'loyalty', NULL, N'2026-05-12 11:20:49.573000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (35, N'g6_1_diem_bang_dong', N'1', N'string', N'loyalty', NULL, N'2026-05-12 11:20:49.577000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (36, N'g6_mau_chu_dao', N'#00aaff', N'string', N'theme', NULL, N'2026-05-12 13:16:14.547000');
INSERT INTO [G6CauHinh] ([g6_ma_cau_hinh], [g6_khoa], [g6_gia_tri], [g6_kieu_du_lieu], [g6_nhom], [g6_mo_ta], [g6_ngay_cap_nhat]) VALUES (37, N'g6_mau_phu', N'#5ef00f', N'string', N'theme', NULL, N'2026-05-20 10:45:07.337000');
GO

SET IDENTITY_INSERT [G6CauHinh] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6ChiNhanh]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6ChiNhanh] ON;
GO

INSERT INTO [G6ChiNhanh] ([g6_ma_chi_nhanh], [g6_ten_chi_nhanh], [g6_dia_chi], [g6_thanh_pho], [g6_tinh], [g6_hotline], [g6_email], [g6_gio_mo_cua], [g6_gio_dong_cua], [g6_gio_mo_lich], [g6_vi_do], [g6_kinh_do], [g6_google_maps_url], [g6_hinh_anh], [g6_suc_chua_toi_da], [g6_co_sauna], [g6_co_ho_boi], [g6_la_hoat_dong], [g6_ngay_tao]) VALUES (1, N'IronCore Cầu Giấy', N'123 Xuân Thủy, Cầu Giấy, Hà Nội', N'Hà Nội', NULL, N'0987654321', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 200, 0, 0, 1, N'2026-05-12 09:03:02.030000');
INSERT INTO [G6ChiNhanh] ([g6_ma_chi_nhanh], [g6_ten_chi_nhanh], [g6_dia_chi], [g6_thanh_pho], [g6_tinh], [g6_hotline], [g6_email], [g6_gio_mo_cua], [g6_gio_dong_cua], [g6_gio_mo_lich], [g6_vi_do], [g6_kinh_do], [g6_google_maps_url], [g6_hinh_anh], [g6_suc_chua_toi_da], [g6_co_sauna], [g6_co_ho_boi], [g6_la_hoat_dong], [g6_ngay_tao]) VALUES (2, N'Đại Thanh', N'Xã Đại Thanh, Hà Nội', N'Hà Nội', N'', N'0000000000', N'nguyenquangtam179@gmail.com', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 100, 1, 1, 1, N'2026-05-12 12:32:14.737000');
GO

SET IDENTITY_INSERT [G6ChiNhanh] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6ChiSoCoThe]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6ChiSoCoThe] ON;
GO

INSERT INTO [G6ChiSoCoThe] ([g6_ma_chi_so], [g6_ma_nguoi_dung], [g6_ngay_do], [g6_can_nang], [g6_chieu_cao], [g6_chi_so_bmi], [g6_ti_le_mo], [g6_ti_le_co], [g6_ti_le_nuoc], [g6_khoi_luong_co], [g6_vong_nguc], [g6_vong_eo], [g6_vong_hong], [g6_vong_tay_trai], [g6_vong_dui_trai], [g6_nguoi_do], [g6_ghi_chu], [g6_ngay_tao]) VALUES (1, 4, N'2026-05-12', 75.50, 175.00, 24.60, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, N'2026-05-12 09:03:02.253000');
GO

SET IDENTITY_INSERT [G6ChiSoCoThe] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6ChiTietDonHang]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6ChiTietDonHang] ON;
GO

INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1, 1, 1, N'Sản phẩm mẫu', NULL, 1, 1200000, 1200000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (2, 2, 55, N'Harbinger Gloves Pro WristWrap Style 140', NULL, 2, 0, 0);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1004, 1004, 55, N'Harbinger Gloves Pro WristWrap Style 140', N'HAR-HARBI-572', 1, 700000, 700000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1005, 1005, 40, N'(Tách Lẻ) Sữa Tăng Cân Mass Gainer, 1KG', N'GEN-TÁCH--950', 1, 360000, 360000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1006, 1006, 55, N'Harbinger Gloves Pro WristWrap Style 140', N'HAR-HARBI-572', 1, 700000, 700000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1007, 1007, 54, N'Harbinger 1260 Men''s Training Grip Gloves, Blue/Black', N'HAR-HARBI-794', 1, 700000, 700000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1008, 1008, 1002, N'test', N'test-default', 1, 11000, 11000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1009, 1009, 1002, N'test', N'test-default', 1, 11000, 11000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1010, 1010, 55, N'Harbinger Gloves Pro WristWrap Style 140', N'HAR-HARBI-572', 1, 700000, 700000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1011, 1010, 1002, N'test', N'test-default', 1, 11000, 11000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1012, 1011, 36, N'Mutant Mass Extreme 2500, 12Lbs (5.45 Kg)', N'MUT-MUTAN-865', 1, 1720000, 1720000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1013, 1012, 1002, N'test', N'test-default', 1, 11000, 11000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1014, 1013, 55, N'Harbinger Gloves Pro WristWrap Style 140', N'HAR-HARBI-572', 1, 700000, 700000);
INSERT INTO [G6ChiTietDonHang] ([g6_ma_chi_tiet], [g6_ma_don_hang], [g6_ma_bien_the], [g6_ten_san_pham], [g6_sku], [g6_so_luong], [g6_don_gia], [g6_thanh_tien]) VALUES (1015, 1014, 1002, N'test', N'test-default', 1, 11000, 11000);
GO

SET IDENTITY_INSERT [G6ChiTietDonHang] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6ChiTietGioHang]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6ChiTietGioHang] ON;
GO

-- (Bảng [G6ChiTietGioHang] rỗng)

SET IDENTITY_INSERT [G6ChiTietGioHang] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6ChungNhanSanPham]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6ChungNhanSanPham] ON;
GO

-- (Bảng [G6ChungNhanSanPham] rỗng)

SET IDENTITY_INSERT [G6ChungNhanSanPham] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DangKyGoiPT]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DangKyGoiPT] ON;
GO

INSERT INTO [G6DangKyGoiPT] ([g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_goi_pt], [g6_ma_hlv], [g6_ngay_mua], [g6_ngay_het_han], [g6_so_buoi_con_lai], [g6_gia_thuc_te], [g6_ma_thanh_toan], [g6_trang_thai], [g6_ngay_tao]) VALUES (2, 10, 1, 1, N'2026-05-19', N'2026-08-17', 12, 3600000, NULL, N'dang_dung', N'2026-05-19 13:45:01.230000');
INSERT INTO [G6DangKyGoiPT] ([g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_goi_pt], [g6_ma_hlv], [g6_ngay_mua], [g6_ngay_het_han], [g6_so_buoi_con_lai], [g6_gia_thuc_te], [g6_ma_thanh_toan], [g6_trang_thai], [g6_ngay_tao]) VALUES (3, 10, 1, 1, N'2026-05-19', N'2026-08-17', 12, 3600000, NULL, N'dang_dung', N'2026-05-19 14:00:50.480000');
INSERT INTO [G6DangKyGoiPT] ([g6_ma_dang_ky_pt], [g6_ma_nguoi_dung], [g6_ma_goi_pt], [g6_ma_hlv], [g6_ngay_mua], [g6_ngay_het_han], [g6_so_buoi_con_lai], [g6_gia_thuc_te], [g6_ma_thanh_toan], [g6_trang_thai], [g6_ngay_tao]) VALUES (4, 10, 2, 2, N'2026-05-20', N'2026-06-19', 10, 450000, NULL, N'dang_dung', N'2026-05-20 08:50:31.407000');
GO

SET IDENTITY_INSERT [G6DangKyGoiPT] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DangKyGoiTap]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DangKyGoiTap] ON;
GO

INSERT INTO [G6DangKyGoiTap] ([g6_ma_dang_ky], [g6_ma_nguoi_dung], [g6_ma_goi_tap], [g6_ma_chi_nhanh], [g6_ngay_bat_dau], [g6_ngay_het_han], [g6_gia_thuc_te], [g6_ma_thanh_toan], [g6_trang_thai], [g6_ly_do_tam_dung], [g6_ngay_tam_dung], [g6_ngay_tiep_tuc], [g6_tu_dong_gia_han], [g6_ghi_chu], [g6_nguoi_tao], [g6_ngay_tao]) VALUES (1, 4, 1, 1, N'2026-05-12', N'2026-06-11', 500000, NULL, N'dang_hoat_dong', NULL, NULL, NULL, 0, NULL, NULL, N'2026-05-12 09:03:02.257000');
INSERT INTO [G6DangKyGoiTap] ([g6_ma_dang_ky], [g6_ma_nguoi_dung], [g6_ma_goi_tap], [g6_ma_chi_nhanh], [g6_ngay_bat_dau], [g6_ngay_het_han], [g6_gia_thuc_te], [g6_ma_thanh_toan], [g6_trang_thai], [g6_ly_do_tam_dung], [g6_ngay_tam_dung], [g6_ngay_tiep_tuc], [g6_tu_dong_gia_han], [g6_ghi_chu], [g6_nguoi_tao], [g6_ngay_tao]) VALUES (2, 10, 2, 1, N'2026-05-19', N'2026-11-15', 2500000, NULL, N'dang_hoat_dong', NULL, NULL, NULL, 0, NULL, NULL, N'2026-05-19 13:44:50.637000');
GO

SET IDENTITY_INSERT [G6DangKyGoiTap] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DanhGiaSanPham]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DanhGiaSanPham] ON;
GO

-- (Bảng [G6DanhGiaSanPham] rỗng)

SET IDENTITY_INSERT [G6DanhGiaSanPham] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DanhMucBaiViet]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DanhMucBaiViet] ON;
GO

INSERT INTO [G6DanhMucBaiViet] ([g6_ma_danh_muc], [g6_ten], [g6_slug], [g6_ma_cha], [g6_thu_tu], [g6_la_hoat_dong]) VALUES (1, N'Kiến thức tập luyện', N'kien-thuc-tap-luyen', NULL, 0, 1);
GO

SET IDENTITY_INSERT [G6DanhMucBaiViet] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DanhMucSanPham]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DanhMucSanPham] ON;
GO

INSERT INTO [G6DanhMucSanPham] ([g6_ma_danh_muc], [g6_ma_danh_muc_cha], [g6_ten_danh_muc], [g6_slug], [g6_mo_ta], [g6_hinh_anh], [g6_thu_tu_hien_thi], [g6_la_hien_thi_menu], [g6_la_hoat_dong]) VALUES (1, NULL, N'Thực phẩm bổ sung', N'thuc-pham-bo-sung', NULL, NULL, 0, 1, 1);
INSERT INTO [G6DanhMucSanPham] ([g6_ma_danh_muc], [g6_ma_danh_muc_cha], [g6_ten_danh_muc], [g6_slug], [g6_mo_ta], [g6_hinh_anh], [g6_thu_tu_hien_thi], [g6_la_hien_thi_menu], [g6_la_hoat_dong]) VALUES (8, NULL, N'Whey Protein', N'whey-protein', NULL, NULL, 0, 1, 1);
INSERT INTO [G6DanhMucSanPham] ([g6_ma_danh_muc], [g6_ma_danh_muc_cha], [g6_ten_danh_muc], [g6_slug], [g6_mo_ta], [g6_hinh_anh], [g6_thu_tu_hien_thi], [g6_la_hien_thi_menu], [g6_la_hoat_dong]) VALUES (9, NULL, N'Sữa tăng cân', N'sua-tang-can', NULL, NULL, 0, 1, 1);
INSERT INTO [G6DanhMucSanPham] ([g6_ma_danh_muc], [g6_ma_danh_muc_cha], [g6_ten_danh_muc], [g6_slug], [g6_mo_ta], [g6_hinh_anh], [g6_thu_tu_hien_thi], [g6_la_hien_thi_menu], [g6_la_hoat_dong]) VALUES (10, NULL, N'Găng tay & Phụ kiện', N'gang-tay-phu-kien', NULL, NULL, 0, 1, 1);
GO

SET IDENTITY_INSERT [G6DanhMucSanPham] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DatChoLopHoc]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DatChoLopHoc] ON;
GO

INSERT INTO [G6DatChoLopHoc] ([g6_ma_dat_cho], [g6_ma_lich_lop], [g6_ma_nguoi_dung], [g6_ngay_tap], [g6_trang_thai], [g6_thoi_gian_dat], [g6_thoi_gian_huy], [g6_ly_do_huy]) VALUES (1, 1, 2, N'2026-05-12', N'dat_cho', N'2026-05-12 09:03:02.297000', NULL, NULL);
INSERT INTO [G6DatChoLopHoc] ([g6_ma_dat_cho], [g6_ma_lich_lop], [g6_ma_nguoi_dung], [g6_ngay_tap], [g6_trang_thai], [g6_thoi_gian_dat], [g6_thoi_gian_huy], [g6_ly_do_huy]) VALUES (2, 1, 10, N'2026-05-19', N'da_huy', N'2026-05-19 12:29:07.180000', N'2026-05-19 13:16:54.907000', NULL);
INSERT INTO [G6DatChoLopHoc] ([g6_ma_dat_cho], [g6_ma_lich_lop], [g6_ma_nguoi_dung], [g6_ngay_tap], [g6_trang_thai], [g6_thoi_gian_dat], [g6_thoi_gian_huy], [g6_ly_do_huy]) VALUES (3, 1, 10, N'2026-05-19', N'dat_cho', N'2026-05-19 13:17:16.327000', NULL, NULL);
INSERT INTO [G6DatChoLopHoc] ([g6_ma_dat_cho], [g6_ma_lich_lop], [g6_ma_nguoi_dung], [g6_ngay_tap], [g6_trang_thai], [g6_thoi_gian_dat], [g6_thoi_gian_huy], [g6_ly_do_huy]) VALUES (4, 1, 10, N'2026-05-20', N'dat_cho', N'2026-05-20 08:30:05.213000', NULL, NULL);
INSERT INTO [G6DatChoLopHoc] ([g6_ma_dat_cho], [g6_ma_lich_lop], [g6_ma_nguoi_dung], [g6_ngay_tap], [g6_trang_thai], [g6_thoi_gian_dat], [g6_thoi_gian_huy], [g6_ly_do_huy]) VALUES (1002, 1, 10, N'2026-05-23', N'dat_cho', N'2026-05-23 03:58:16.367000', NULL, NULL);
INSERT INTO [G6DatChoLopHoc] ([g6_ma_dat_cho], [g6_ma_lich_lop], [g6_ma_nguoi_dung], [g6_ngay_tap], [g6_trang_thai], [g6_thoi_gian_dat], [g6_thoi_gian_huy], [g6_ly_do_huy]) VALUES (1003, 1, 10, N'2026-05-24', N'dat_cho', N'2026-05-24 10:28:16.977000', NULL, NULL);
GO

SET IDENTITY_INSERT [G6DatChoLopHoc] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DatDichVu]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DatDichVu] ON;
GO

-- (Bảng [G6DatDichVu] rỗng)

SET IDENTITY_INSERT [G6DatDichVu] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DiaChiGiaoHang]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DiaChiGiaoHang] ON;
GO

-- (Bảng [G6DiaChiGiaoHang] rỗng)

SET IDENTITY_INSERT [G6DiaChiGiaoHang] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DichVuPhu]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DichVuPhu] ON;
GO

INSERT INTO [G6DichVuPhu] ([g6_ma_dich_vu], [g6_ma_chi_nhanh], [g6_ten_dich_vu], [g6_loai_dich_vu], [g6_mo_ta], [g6_gia_theo_luot], [g6_thoi_luong_phut], [g6_suc_chua], [g6_la_mien_phi_goi], [g6_la_hoat_dong]) VALUES (1, 1, N'Sauna & Steam', N'relaxation', NULL, 50000, 60, NULL, 0, 1);
GO

SET IDENTITY_INSERT [G6DichVuPhu] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DiemDanh]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DiemDanh] ON;
GO

INSERT INTO [G6DiemDanh] ([g6_ma_diem_danh], [g6_ma_dang_ky], [g6_ma_nguoi_dung], [g6_ma_chi_nhanh], [g6_thoi_gian_vao], [g6_thoi_gian_ra], [g6_phuong_thuc], [g6_nguoi_xac_nhan], [g6_ghi_chu]) VALUES (1, 2, 10, 1, N'2026-05-23 03:48:21.303000', N'2026-05-23 04:02:41.773000', N'qr', NULL, NULL);
INSERT INTO [G6DiemDanh] ([g6_ma_diem_danh], [g6_ma_dang_ky], [g6_ma_nguoi_dung], [g6_ma_chi_nhanh], [g6_thoi_gian_vao], [g6_thoi_gian_ra], [g6_phuong_thuc], [g6_nguoi_xac_nhan], [g6_ghi_chu]) VALUES (2, 2, 10, 1, N'2026-05-23 03:48:53.033000', N'2026-05-23 04:02:28.243000', N'qr', NULL, NULL);
INSERT INTO [G6DiemDanh] ([g6_ma_diem_danh], [g6_ma_dang_ky], [g6_ma_nguoi_dung], [g6_ma_chi_nhanh], [g6_thoi_gian_vao], [g6_thoi_gian_ra], [g6_phuong_thuc], [g6_nguoi_xac_nhan], [g6_ghi_chu]) VALUES (3, 2, 10, 1, N'2026-05-23 03:57:18.293000', N'2026-05-23 04:02:22.970000', N'qr', NULL, NULL);
INSERT INTO [G6DiemDanh] ([g6_ma_diem_danh], [g6_ma_dang_ky], [g6_ma_nguoi_dung], [g6_ma_chi_nhanh], [g6_thoi_gian_vao], [g6_thoi_gian_ra], [g6_phuong_thuc], [g6_nguoi_xac_nhan], [g6_ghi_chu]) VALUES (4, 2, 10, 1, N'2026-05-23 04:02:51.613000', N'2026-05-23 04:02:59.790000', N'qr', NULL, NULL);
INSERT INTO [G6DiemDanh] ([g6_ma_diem_danh], [g6_ma_dang_ky], [g6_ma_nguoi_dung], [g6_ma_chi_nhanh], [g6_thoi_gian_vao], [g6_thoi_gian_ra], [g6_phuong_thuc], [g6_nguoi_xac_nhan], [g6_ghi_chu]) VALUES (5, 2, 10, 1, N'2026-05-24 00:59:11.727000', N'2026-05-24 01:02:07.847000', N'qr', NULL, NULL);
GO

SET IDENTITY_INSERT [G6DiemDanh] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DiemKhachHang]
-- ------------------------------------------------------------
INSERT INTO [G6DiemKhachHang] ([g6_ma_nguoi_dung], [g6_tong_diem], [g6_diem_kha_dung], [g6_ma_hang], [g6_ngay_cap_nhat]) VALUES (9, 0, 0, 1, N'2026-05-12 11:29:14.270000');
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DonHang]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DonHang] ON;
GO

INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1, 4, NULL, NULL, NULL, N'Nguyễn Xuân Vinh', N'0912345678', N'123 ABC, Ha Noi', 1200000, 0, 0, 0, 0, 1200000, N'cho_xac_nhan', N'cod', NULL, NULL, N'2026-05-12 09:03:02.327000', N'2026-05-12 09:03:02.327000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (2, NULL, NULL, NULL, NULL, N'Khách Test', N'0999888777', N'123 Đường Test, Hà Nội', 0, 0, 0, 0, 0, 0, N'cho_xac_nhan', N'tien_mat', N'', NULL, N'2026-05-20 09:44:45.487000', N'2026-05-20 09:44:45.487000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1004, 10, NULL, NULL, NULL, N'Khách Test', N'0999888777', N'123 Đường Test, Hà Nội', 700000, 0, 0, 0, 0, 700000, N'cho_xac_nhan', N'chuyen_khoan', N'Giao giờ hành chính', NULL, N'2026-05-23 04:24:10.983000', N'2026-05-23 04:24:10.983000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1005, 10, NULL, NULL, NULL, N'Nguyen Van A', N'0987654321', N'123 Nguyen Trai, Ho Chi Minh', 360000, 0, 0, 0, 0, 360000, N'cho_xac_nhan', N'tien_mat', N'Giao hang gio hanh chinh', NULL, N'2026-05-23 04:27:02.750000', N'2026-05-23 04:27:02.750000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1006, NULL, NULL, NULL, NULL, N'Khách vãng lai', N'43423', N'434234234, 34342', 700000, 0, 0, 0, 0, 700000, N'cho_xac_nhan', N'tien_mat', N'', NULL, N'2026-05-23 04:50:54.400000', N'2026-05-23 04:50:54.400000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1007, NULL, NULL, NULL, NULL, N'Khách vãng lai', N'0202000', N'địa chỉ, HN', 700000, 0, 0, 0, 0, 700000, N'cho_xac_nhan', N'chuyen_khoan', N'ghi chú nè', NULL, N'2026-05-23 04:51:54.697000', N'2026-05-23 04:51:54.697000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1008, NULL, NULL, NULL, NULL, N'Nguyen Van A', N'0987654321', N'123 Street, Hanoi', 11000, 0, 0, 0, 0, 11000, N'cho_xac_nhan', N'chuyen_khoan', N'', NULL, N'2026-05-23 04:56:05.640000', N'2026-05-23 04:56:05.640000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1009, 10, NULL, NULL, NULL, N'Test đăng ký', N'0961111101', N'Số nhà, HN', 11000, 0, 0, 0, 0, 11000, N'cho_xac_nhan', N'chuyen_khoan', N'ghi chú', NULL, N'2026-05-24 00:41:18.013000', N'2026-05-24 00:41:18.013000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1010, NULL, NULL, NULL, NULL, N'Kh', N'0999888777', N'123 Đường Test, Hà Nội', 711000, 0, 0, 0, 0, 711000, N'cho_xac_nhan', N'chuyen_khoan', N'', NULL, N'2026-05-24 00:45:54.573000', N'2026-05-24 00:45:54.573000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1011, 10, NULL, NULL, NULL, N'Khách', N'0999888777', N'123 Đường Test, Hà Nội', 1720000, 0, 0, 0, 0, 1720000, N'cho_xac_nhan', N'chuyen_khoan', N'Giao gio hanh chinh nhe', NULL, N'2026-05-24 00:52:37.813000', N'2026-05-24 00:52:37.813000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1012, 10, NULL, NULL, NULL, N'Nguyễn Quang Tâm', N'0961111101', N'111, 111', 11000, 0, 0, 0, 0, 11000, N'dang_xu_ly', N'chuyen_khoan', N'111', NULL, N'2026-05-24 13:53:44.867000', N'2026-05-24 13:58:02.550000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1013, 10, NULL, NULL, NULL, N'Nguyễn Quang Tâm', N'0961138440', N'Xã Đại Thanh, Hà Nội, Hà Nội', 700000, 0, 0, 0, 0, 700000, N'cho_xac_nhan', N'chuyen_khoan', N'giao cho tôi vào buổi sáng', NULL, N'2026-06-02 03:33:54.453000', N'2026-06-02 03:33:54.453000');
INSERT INTO [G6DonHang] ([g6_ma_don_hang], [g6_ma_nguoi_dung], [g6_ma_nguoi_xu_ly], [g6_ma_van_chuyen], [g6_ma_giam_gia], [g6_ho_ten_nguoi_nhan], [g6_so_dien_thoai], [g6_dia_chi_giao_hang], [g6_tong_tien_hang], [g6_phi_van_chuyen], [g6_so_tien_giam], [g6_diem_su_dung], [g6_tien_diem_tru], [g6_tong_thanh_toan], [g6_trang_thai], [g6_phuong_thuc_thanh_toan], [g6_ghi_chu_khach], [g6_ghi_chu_noi_bo], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1014, 10, NULL, NULL, NULL, N'Nguyễn Quang Tâm', N'0961111101', N'2323231, Xã Đại Thanh, Thành phố Hà Nội', 11000, 0, 0, 0, 0, 11000, N'cho_xac_nhan', N'tien_mat', N'3123', NULL, N'2026-06-02 04:04:12.023000', N'2026-06-02 04:04:12.023000');
GO

SET IDENTITY_INSERT [G6DonHang] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6DonViVanChuyen]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6DonViVanChuyen] ON;
GO

INSERT INTO [G6DonViVanChuyen] ([g6_ma_don_vi], [g6_ten], [g6_ma], [g6_logo], [g6_la_hoat_dong]) VALUES (1, N'Giao Hàng Nhanh', N'GHN', NULL, 1);
GO

SET IDENTITY_INSERT [G6DonViVanChuyen] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6GoiPT]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6GoiPT] ON;
GO

INSERT INTO [G6GoiPT] ([g6_ma_goi_pt], [g6_ma_hlv], [g6_ten_goi], [g6_so_buoi], [g6_thoi_luong_buoi], [g6_gia], [g6_gia_khuyen_mai], [g6_hieu_luc_ngay], [g6_la_hoat_dong], [g6_ngay_tao]) VALUES (1, 1, N'PT 1:1 12 Buổi', 12, 60, 3600000, NULL, 90, 1, N'2026-05-12 09:03:02.233000');
INSERT INTO [G6GoiPT] ([g6_ma_goi_pt], [g6_ma_hlv], [g6_ten_goi], [g6_so_buoi], [g6_thoi_luong_buoi], [g6_gia], [g6_gia_khuyen_mai], [g6_hieu_luc_ngay], [g6_la_hoat_dong], [g6_ngay_tao]) VALUES (2, 2, N'Gói tập 1-1', 10, 60, 500000, 450000, 30, 1, N'2026-05-20 08:50:22.170000');
GO

SET IDENTITY_INSERT [G6GoiPT] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6GoiTap]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6GoiTap] ON;
GO

INSERT INTO [G6GoiTap] ([g6_ma_goi_tap], [g6_ma_chi_nhanh], [g6_ten_goi], [g6_mo_ta], [g6_so_ngay], [g6_gia], [g6_gia_khuyen_mai], [g6_so_luot_checkin_ngay], [g6_duoc_dua_khach], [g6_so_khach_duoc_dua], [g6_co_pt], [g6_so_buoi_pt], [g6_co_sauna], [g6_mau_hien_thi], [g6_la_noi_bat], [g6_thu_tu_hien_thi], [g6_la_hoat_dong], [g6_ngay_tao]) VALUES (1, NULL, N'Gói Classic 1 Tháng', NULL, 30, 500000, NULL, 1, 0, 0, 0, 0, 0, NULL, 0, 0, 1, N'2026-05-12 09:03:02.243000');
INSERT INTO [G6GoiTap] ([g6_ma_goi_tap], [g6_ma_chi_nhanh], [g6_ten_goi], [g6_mo_ta], [g6_so_ngay], [g6_gia], [g6_gia_khuyen_mai], [g6_so_luot_checkin_ngay], [g6_duoc_dua_khach], [g6_so_khach_duoc_dua], [g6_co_pt], [g6_so_buoi_pt], [g6_co_sauna], [g6_mau_hien_thi], [g6_la_noi_bat], [g6_thu_tu_hien_thi], [g6_la_hoat_dong], [g6_ngay_tao]) VALUES (2, NULL, N'Gói Silver 6 Tháng', NULL, 180, 2500000, NULL, 1, 0, 0, 0, 0, 0, NULL, 0, 0, 1, N'2026-05-12 09:03:02.243000');
INSERT INTO [G6GoiTap] ([g6_ma_goi_tap], [g6_ma_chi_nhanh], [g6_ten_goi], [g6_mo_ta], [g6_so_ngay], [g6_gia], [g6_gia_khuyen_mai], [g6_so_luot_checkin_ngay], [g6_duoc_dua_khach], [g6_so_khach_duoc_dua], [g6_co_pt], [g6_so_buoi_pt], [g6_co_sauna], [g6_mau_hien_thi], [g6_la_noi_bat], [g6_thu_tu_hien_thi], [g6_la_hoat_dong], [g6_ngay_tao]) VALUES (3, NULL, N'Gói Gold 12 Tháng', NULL, 365, 4500000, NULL, 1, 0, 0, 0, 0, 0, NULL, 0, 0, 1, N'2026-05-12 09:03:02.243000');
GO

SET IDENTITY_INSERT [G6GoiTap] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6GiaoDichDiem]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6GiaoDichDiem] ON;
GO

-- (Bảng [G6GiaoDichDiem] rỗng)

SET IDENTITY_INSERT [G6GiaoDichDiem] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6GioHang]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6GioHang] ON;
GO

-- (Bảng [G6GioHang] rỗng)

SET IDENTITY_INSERT [G6GioHang] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6HangThanhVien]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6HangThanhVien] ON;
GO

INSERT INTO [G6HangThanhVien] ([g6_ma_hang], [g6_ten_hang], [g6_diem_toi_thieu], [g6_he_so_tich_diem], [g6_mau_hien_thi], [g6_icon]) VALUES (1, N'Đồng', 0, 1.00, NULL, NULL);
INSERT INTO [G6HangThanhVien] ([g6_ma_hang], [g6_ten_hang], [g6_diem_toi_thieu], [g6_he_so_tich_diem], [g6_mau_hien_thi], [g6_icon]) VALUES (2, N'Bạc', 1000, 1.10, NULL, NULL);
GO

SET IDENTITY_INSERT [G6HangThanhVien] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6HinhAnhSanPham]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6HinhAnhSanPham] ON;
GO

INSERT INTO [G6HinhAnhSanPham] ([g6_ma_hinh_anh], [g6_ma_san_pham], [g6_ma_bien_the], [g6_duong_dan], [g6_alt_text], [g6_thu_tu], [g6_la_anh_chinh]) VALUES (1, 55, NULL, N'/static/uploads/06f8c5b123e94d5fbd647ce1ff05bfe1.png', NULL, 0, 0);
INSERT INTO [G6HinhAnhSanPham] ([g6_ma_hinh_anh], [g6_ma_san_pham], [g6_ma_bien_the], [g6_duong_dan], [g6_alt_text], [g6_thu_tu], [g6_la_anh_chinh]) VALUES (2, 55, NULL, N'/static/uploads/7b842d1a99fd4852b2bdebcbeb8ae338.webp', NULL, 0, 0);
INSERT INTO [G6HinhAnhSanPham] ([g6_ma_hinh_anh], [g6_ma_san_pham], [g6_ma_bien_the], [g6_duong_dan], [g6_alt_text], [g6_thu_tu], [g6_la_anh_chinh]) VALUES (3, 55, NULL, N'/static/uploads/bf5ce524d23941858723f686b0db99aa.webp', NULL, 0, 0);
INSERT INTO [G6HinhAnhSanPham] ([g6_ma_hinh_anh], [g6_ma_san_pham], [g6_ma_bien_the], [g6_duong_dan], [g6_alt_text], [g6_thu_tu], [g6_la_anh_chinh]) VALUES (4, 1002, NULL, N'/static/uploads/e120cc6708ef4760b49a0f2383c939fd.png', NULL, 0, 0);
INSERT INTO [G6HinhAnhSanPham] ([g6_ma_hinh_anh], [g6_ma_san_pham], [g6_ma_bien_the], [g6_duong_dan], [g6_alt_text], [g6_thu_tu], [g6_la_anh_chinh]) VALUES (5, 1002, NULL, N'/static/uploads/90778d31719147dbbc3234c54afbed5a.png', NULL, 0, 0);
INSERT INTO [G6HinhAnhSanPham] ([g6_ma_hinh_anh], [g6_ma_san_pham], [g6_ma_bien_the], [g6_duong_dan], [g6_alt_text], [g6_thu_tu], [g6_la_anh_chinh]) VALUES (6, 1002, NULL, N'/static/uploads/9455cf339bd14863a9678282a751d9c7.png', NULL, 0, 1);
INSERT INTO [G6HinhAnhSanPham] ([g6_ma_hinh_anh], [g6_ma_san_pham], [g6_ma_bien_the], [g6_duong_dan], [g6_alt_text], [g6_thu_tu], [g6_la_anh_chinh]) VALUES (7, 55, NULL, N'/static/uploads/92e8eda5816f422eb3f806b9a0a0a616.webp', NULL, 0, 1);
GO

SET IDENTITY_INSERT [G6HinhAnhSanPham] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6HoaDon]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6HoaDon] ON;
GO

INSERT INTO [G6HoaDon] ([g6_ma_hoa_don], [g6_ma_thanh_toan], [g6_so_hoa_don], [g6_tien_truoc_thue], [g6_tien_thue], [g6_tong_cong], [g6_thong_tin_mst], [g6_ngay_xuat]) VALUES (1, 1, N'HD2026051218741', 1200000, 84000, 1284000, NULL, N'2026-05-12 12:53:25.550000');
INSERT INTO [G6HoaDon] ([g6_ma_hoa_don], [g6_ma_thanh_toan], [g6_so_hoa_don], [g6_tien_truoc_thue], [g6_tien_thue], [g6_tong_cong], [g6_thong_tin_mst], [g6_ngay_xuat]) VALUES (2, 2, N'HD2026052417740', 11000, 770, 11770, NULL, N'2026-05-24 13:58:02.563000');
GO

SET IDENTITY_INSERT [G6HoaDon] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6HuanLuyenVien]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6HuanLuyenVien] ON;
GO

INSERT INTO [G6HuanLuyenVien] ([g6_ma_hlv], [g6_ma_nhan_vien], [g6_ma_chi_nhanh], [g6_chuyen_mon], [g6_cap_chung_chi], [g6_so_nam_kinh_nghiem], [g6_tieu_su], [g6_gia_theo_buoi], [g6_hinh_anh], [g6_thu_hang], [g6_so_hoi_vien_hien_tai], [g6_toi_da_hoi_vien], [g6_la_hien_thi_web]) VALUES (1, 3, 1, N'Gym, Bodybuilding, Fitness', NULL, 5, N'Chuyên gia hình thể với 5 năm kinh nghiệm.', NULL, NULL, 5, 2, 20, 1);
INSERT INTO [G6HuanLuyenVien] ([g6_ma_hlv], [g6_ma_nhan_vien], [g6_ma_chi_nhanh], [g6_chuyen_mon], [g6_cap_chung_chi], [g6_so_nam_kinh_nghiem], [g6_tieu_su], [g6_gia_theo_buoi], [g6_hinh_anh], [g6_thu_hang], [g6_so_hoi_vien_hien_tai], [g6_toi_da_hoi_vien], [g6_la_hien_thi_web]) VALUES (2, 5, 1, N'Fitness, LL, PP', NULL, 3, N'mô tả Nguyễn Quang Tâm - HLV', 300000, NULL, 5, 1, 20, 1);
INSERT INTO [G6HuanLuyenVien] ([g6_ma_hlv], [g6_ma_nhan_vien], [g6_ma_chi_nhanh], [g6_chuyen_mon], [g6_cap_chung_chi], [g6_so_nam_kinh_nghiem], [g6_tieu_su], [g6_gia_theo_buoi], [g6_hinh_anh], [g6_thu_hang], [g6_so_hoi_vien_hien_tai], [g6_toi_da_hoi_vien], [g6_la_hien_thi_web]) VALUES (3, 1, 1, N'Master Trainer, Gym, Fitness', N'IRONCORE Elite', 10, N'Admin / Master Trainer of the system.', 1000000, NULL, 5, 0, 50, 1);
GO

SET IDENTITY_INSERT [G6HuanLuyenVien] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6KhuyenMaiMuaKem]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6KhuyenMaiMuaKem] ON;
GO

INSERT INTO [G6KhuyenMaiMuaKem] ([g6_ma_khuyen_mai], [g6_ten], [g6_ma_san_pham_chinh], [g6_so_luong_mua], [g6_ma_san_pham_tang], [g6_so_luong_tang], [g6_phan_tram_giam], [g6_ngay_bat_dau], [g6_ngay_ket_thuc], [g6_la_hoat_dong]) VALUES (2, N'Test Mua Kem', 1, 1, NULL, 1, 50.00, N'2026-05-19 17:54:00', N'2026-06-08 17:54:00', 1);
GO

SET IDENTITY_INSERT [G6KhuyenMaiMuaKem] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6LichGuiThongBao]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6LichGuiThongBao] ON;
GO

-- (Bảng [G6LichGuiThongBao] rỗng)

SET IDENTITY_INSERT [G6LichGuiThongBao] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6LichLamViec]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6LichLamViec] ON;
GO

-- (Bảng [G6LichLamViec] rỗng)

SET IDENTITY_INSERT [G6LichLamViec] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6LichLopHoc]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6LichLopHoc] ON;
GO

INSERT INTO [G6LichLopHoc] ([g6_ma_lich_lop], [g6_ma_lop_hoc], [g6_ma_hlv], [g6_thu_trong_tuan], [g6_gio_bat_dau], [g6_thoi_luong], [g6_suc_chua_toi_da], [g6_phong_tap], [g6_ngay_ap_dung_tu], [g6_ngay_ap_dung_den], [g6_la_hoat_dong]) VALUES (1, 1, 1, 1, N'08:00:00', 60, 20, NULL, N'2026-05-12', NULL, 1);
GO

SET IDENTITY_INSERT [G6LichLopHoc] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6LichSuDonHang]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6LichSuDonHang] ON;
GO

INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (1, 2, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-05-20 09:44:45.503000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (2, 1004, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-05-23 04:24:11');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (3, 1005, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-05-23 04:27:02.773000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (4, 1006, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-05-23 04:50:54.423000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (5, 1007, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-05-23 04:51:54.727000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (6, 1008, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-05-23 04:56:05.657000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (7, 1009, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-05-24 00:41:18.023000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (8, 1010, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-05-24 00:45:54.587000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (9, 1011, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-05-24 00:52:37.827000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (10, 1012, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-05-24 13:53:44.883000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (11, 1012, NULL, N'dang_xu_ly', N'Xác nhận thanh toán tự động qua MBBank (Job ngầm), mã GD: FT26145915489130', NULL, N'2026-05-24 13:58:02.557000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (12, 1013, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-06-02 03:33:54.470000');
INSERT INTO [G6LichSuDonHang] ([g6_ma_lich_su], [g6_ma_don_hang], [g6_trang_thai_cu], [g6_trang_thai_moi], [g6_ghi_chu], [g6_nguoi_thay_doi], [g6_ngay_tao]) VALUES (13, 1014, NULL, N'cho_xac_nhan', N'Đơn hàng mới', NULL, N'2026-06-02 04:04:12.033000');
GO

SET IDENTITY_INSERT [G6LichSuDonHang] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6LichSuTonKho]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6LichSuTonKho] ON;
GO

-- (Bảng [G6LichSuTonKho] rỗng)

SET IDENTITY_INSERT [G6LichSuTonKho] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6LopHoc]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6LopHoc] ON;
GO

INSERT INTO [G6LopHoc] ([g6_ma_lop_hoc], [g6_ma_chi_nhanh], [g6_ten_lop], [g6_loai_lop], [g6_mo_ta], [g6_hinh_anh], [g6_do_kho], [g6_la_hoat_dong]) VALUES (1, 1, N'Yoga Flow', N'yoga', NULL, NULL, N'co_ban', 1);
GO

SET IDENTITY_INSERT [G6LopHoc] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6MaGiamGia]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6MaGiamGia] ON;
GO

INSERT INTO [G6MaGiamGia] ([g6_ma_ma_giam_gia], [g6_ma], [g6_loai], [g6_gia_tri], [g6_gia_tri_toi_da], [g6_don_hang_toi_thieu], [g6_so_luong_tong], [g6_so_luong_da_dung], [g6_so_lan_moi_kh], [g6_ngay_bat_dau], [g6_ngay_ket_thuc], [g6_yeu_cau_hang], [g6_la_hoat_dong], [g6_ngay_tao]) VALUES (1, N'SALE20', N'phan_tram', 20, NULL, 0, 1000, 0, 1, N'2025-01-01 00:00:00', N'2025-05-15 00:00:00', NULL, 1, N'2026-05-12 11:30:45.440000');
GO

SET IDENTITY_INSERT [G6MaGiamGia] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6MucTieuSucKhoe]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6MucTieuSucKhoe] ON;
GO

-- (Bảng [G6MucTieuSucKhoe] rỗng)

SET IDENTITY_INSERT [G6MucTieuSucKhoe] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6NguoiDung]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6NguoiDung] ON;
GO

INSERT INTO [G6NguoiDung] ([g6_ma_nguoi_dung], [g6_ten_dang_nhap], [g6_mat_khau], [g6_ho_ten], [g6_email], [g6_so_dien_thoai], [g6_ngay_sinh], [g6_gioi_tinh], [g6_dia_chi], [g6_so_cccd], [g6_anh_the], [g6_anh_dai_dien], [g6_la_nhan_vien], [g6_la_hoi_vien], [g6_la_khach_hang], [g6_ma_chi_nhanh], [g6_ngay_dang_ky], [g6_ma_qr], [g6_nguon_gioi_thieu], [g6_ma_gioi_thieu], [g6_ghi_chu], [g6_google_id], [g6_la_xac_thuc_otp], [g6_la_hoat_dong], [g6_lan_dang_nhap_sai], [g6_khoa_den], [g6_reset_token], [g6_reset_token_het_han], [g6_ngay_tao], [g6_ngay_cap_nhat], [g6_totp_secret]) VALUES (1, N'quangtam', N'$2b$12$JiFxMM0Gn7a/RDWCpBKxuu0qm5KG1DGUChnBgwY.fjIqomtNeQn22', N'Nguyễn Quang Tâm', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, 0, 1, NULL, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, NULL, NULL, NULL, N'2026-05-12 09:03:02.210000', N'2026-05-12 09:03:02.210000', NULL);
INSERT INTO [G6NguoiDung] ([g6_ma_nguoi_dung], [g6_ten_dang_nhap], [g6_mat_khau], [g6_ho_ten], [g6_email], [g6_so_dien_thoai], [g6_ngay_sinh], [g6_gioi_tinh], [g6_dia_chi], [g6_so_cccd], [g6_anh_the], [g6_anh_dai_dien], [g6_la_nhan_vien], [g6_la_hoi_vien], [g6_la_khach_hang], [g6_ma_chi_nhanh], [g6_ngay_dang_ky], [g6_ma_qr], [g6_nguon_gioi_thieu], [g6_ma_gioi_thieu], [g6_ghi_chu], [g6_google_id], [g6_la_xac_thuc_otp], [g6_la_hoat_dong], [g6_lan_dang_nhap_sai], [g6_khoa_den], [g6_reset_token], [g6_reset_token_het_han], [g6_ngay_tao], [g6_ngay_cap_nhat], [g6_totp_secret]) VALUES (2, N'hoainam', N'$2b$12$JiFxMM0Gn7a/RDWCpBKxuu0qm5KG1DGUChnBgwY.fjIqomtNeQn22', N'Nguyễn Hoài Nam', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, 0, 1, NULL, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, NULL, NULL, NULL, N'2026-05-12 09:03:02.220000', N'2026-05-12 09:03:02.220000', NULL);
INSERT INTO [G6NguoiDung] ([g6_ma_nguoi_dung], [g6_ten_dang_nhap], [g6_mat_khau], [g6_ho_ten], [g6_email], [g6_so_dien_thoai], [g6_ngay_sinh], [g6_gioi_tinh], [g6_dia_chi], [g6_so_cccd], [g6_anh_the], [g6_anh_dai_dien], [g6_la_nhan_vien], [g6_la_hoi_vien], [g6_la_khach_hang], [g6_ma_chi_nhanh], [g6_ngay_dang_ky], [g6_ma_qr], [g6_nguon_gioi_thieu], [g6_ma_gioi_thieu], [g6_ghi_chu], [g6_google_id], [g6_la_xac_thuc_otp], [g6_la_hoat_dong], [g6_lan_dang_nhap_sai], [g6_khoa_den], [g6_reset_token], [g6_reset_token_het_han], [g6_ngay_tao], [g6_ngay_cap_nhat], [g6_totp_secret]) VALUES (3, N'doanquan', N'$2b$12$JiFxMM0Gn7a/RDWCpBKxuu0qm5KG1DGUChnBgwY.fjIqomtNeQn22', N'Đoàn Anh Quân', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, 0, 1, NULL, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, NULL, NULL, NULL, N'2026-05-12 09:03:02.223000', N'2026-05-12 09:03:02.223000', NULL);
INSERT INTO [G6NguoiDung] ([g6_ma_nguoi_dung], [g6_ten_dang_nhap], [g6_mat_khau], [g6_ho_ten], [g6_email], [g6_so_dien_thoai], [g6_ngay_sinh], [g6_gioi_tinh], [g6_dia_chi], [g6_so_cccd], [g6_anh_the], [g6_anh_dai_dien], [g6_la_nhan_vien], [g6_la_hoi_vien], [g6_la_khach_hang], [g6_ma_chi_nhanh], [g6_ngay_dang_ky], [g6_ma_qr], [g6_nguon_gioi_thieu], [g6_ma_gioi_thieu], [g6_ghi_chu], [g6_google_id], [g6_la_xac_thuc_otp], [g6_la_hoat_dong], [g6_lan_dang_nhap_sai], [g6_khoa_den], [g6_reset_token], [g6_reset_token_het_han], [g6_ngay_tao], [g6_ngay_cap_nhat], [g6_totp_secret]) VALUES (4, N'xuanvinh', N'$2b$12$JiFxMM0Gn7a/RDWCpBKxuu0qm5KG1DGUChnBgwY.fjIqomtNeQn22', N'Nguyễn Xuân Vinh', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, 0, 1, NULL, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, NULL, NULL, NULL, N'2026-05-12 09:03:02.233000', N'2026-05-12 09:03:02.233000', NULL);
INSERT INTO [G6NguoiDung] ([g6_ma_nguoi_dung], [g6_ten_dang_nhap], [g6_mat_khau], [g6_ho_ten], [g6_email], [g6_so_dien_thoai], [g6_ngay_sinh], [g6_gioi_tinh], [g6_dia_chi], [g6_so_cccd], [g6_anh_the], [g6_anh_dai_dien], [g6_la_nhan_vien], [g6_la_hoi_vien], [g6_la_khach_hang], [g6_ma_chi_nhanh], [g6_ngay_dang_ky], [g6_ma_qr], [g6_nguon_gioi_thieu], [g6_ma_gioi_thieu], [g6_ghi_chu], [g6_google_id], [g6_la_xac_thuc_otp], [g6_la_hoat_dong], [g6_lan_dang_nhap_sai], [g6_khoa_den], [g6_reset_token], [g6_reset_token_het_han], [g6_ngay_tao], [g6_ngay_cap_nhat], [g6_totp_secret]) VALUES (5, NULL, NULL, N'Hội viên 1', N'1221@gmail.com', N'0000000000', N'2005-02-22', N'nam', N'Địa chỉ Hội viên 1', NULL, NULL, NULL, 0, 1, 0, 1, N'2026-05-12', N'83f88812-6aa5-45d5-89f1-740e0fd29bda', NULL, NULL, NULL, NULL, 0, 1, 0, N'2026-05-13 08:49:21.470000', NULL, NULL, N'2026-05-12 11:01:55.787000', N'2026-05-13 08:19:21.473000', NULL);
INSERT INTO [G6NguoiDung] ([g6_ma_nguoi_dung], [g6_ten_dang_nhap], [g6_mat_khau], [g6_ho_ten], [g6_email], [g6_so_dien_thoai], [g6_ngay_sinh], [g6_gioi_tinh], [g6_dia_chi], [g6_so_cccd], [g6_anh_the], [g6_anh_dai_dien], [g6_la_nhan_vien], [g6_la_hoi_vien], [g6_la_khach_hang], [g6_ma_chi_nhanh], [g6_ngay_dang_ky], [g6_ma_qr], [g6_nguon_gioi_thieu], [g6_ma_gioi_thieu], [g6_ghi_chu], [g6_google_id], [g6_la_xac_thuc_otp], [g6_la_hoat_dong], [g6_lan_dang_nhap_sai], [g6_khoa_den], [g6_reset_token], [g6_reset_token_het_han], [g6_ngay_tao], [g6_ngay_cap_nhat], [g6_totp_secret]) VALUES (8, NULL, NULL, N'Hội viên 2', N'eqwe@gmail.com', N'0000000001', N'2024-11-11', N'nam', N'địa chỉ Hội viên 2', NULL, NULL, NULL, 0, 1, 0, 1, N'2026-05-12', N'f8bb72cf-cbd3-484f-a1c9-dd77590c2af5', NULL, NULL, NULL, NULL, 0, 1, 0, NULL, NULL, NULL, N'2026-05-12 11:27:52.850000', N'2026-05-12 11:27:52.850000', NULL);
INSERT INTO [G6NguoiDung] ([g6_ma_nguoi_dung], [g6_ten_dang_nhap], [g6_mat_khau], [g6_ho_ten], [g6_email], [g6_so_dien_thoai], [g6_ngay_sinh], [g6_gioi_tinh], [g6_dia_chi], [g6_so_cccd], [g6_anh_the], [g6_anh_dai_dien], [g6_la_nhan_vien], [g6_la_hoi_vien], [g6_la_khach_hang], [g6_ma_chi_nhanh], [g6_ngay_dang_ky], [g6_ma_qr], [g6_nguon_gioi_thieu], [g6_ma_gioi_thieu], [g6_ghi_chu], [g6_google_id], [g6_la_xac_thuc_otp], [g6_la_hoat_dong], [g6_lan_dang_nhap_sai], [g6_khoa_den], [g6_reset_token], [g6_reset_token_het_han], [g6_ngay_tao], [g6_ngay_cap_nhat], [g6_totp_secret]) VALUES (9, NULL, N'$2b$12$OyZqUTQr4NE8/EDPsIY5SOQP2JJE5yD7IYAHSKoXjsfEbgaNZoKY6', N'mHp63jsMJF2S - KH', N'mHp63jsMJF2S@gmail.com', N'0000000000', NULL, NULL, NULL, NULL, NULL, NULL, 0, 0, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, NULL, NULL, NULL, N'2026-05-12 11:29:14.260000', N'2026-05-12 11:29:14.260000', NULL);
INSERT INTO [G6NguoiDung] ([g6_ma_nguoi_dung], [g6_ten_dang_nhap], [g6_mat_khau], [g6_ho_ten], [g6_email], [g6_so_dien_thoai], [g6_ngay_sinh], [g6_gioi_tinh], [g6_dia_chi], [g6_so_cccd], [g6_anh_the], [g6_anh_dai_dien], [g6_la_nhan_vien], [g6_la_hoi_vien], [g6_la_khach_hang], [g6_ma_chi_nhanh], [g6_ngay_dang_ky], [g6_ma_qr], [g6_nguon_gioi_thieu], [g6_ma_gioi_thieu], [g6_ghi_chu], [g6_google_id], [g6_la_xac_thuc_otp], [g6_la_hoat_dong], [g6_lan_dang_nhap_sai], [g6_khoa_den], [g6_reset_token], [g6_reset_token_het_han], [g6_ngay_tao], [g6_ngay_cap_nhat], [g6_totp_secret]) VALUES (10, N'testmember', N'$2b$12$IdTQyzxWA/QJNVHNzSsTneeS9nIes.E6s/fvSdppY1JykV2cJGjq2', N'Nguyễn Quang Tâm', N'nguyenquangtam6666@gmail.com', N'0961111101', N'2026-05-24', N'nam', N'HN', NULL, N'/static/uploads/8b19f5b0a0bc4179812eac6c4ec8b6cb.png', NULL, 0, 1, 0, 1, N'2026-05-12', N'E28BFD5D-3D5', NULL, NULL, NULL, NULL, 0, 1, 0, NULL, N'803542', N'2026-05-25 02:06:52.960000', N'2026-05-12 12:08:28.870000', N'2026-05-31 12:31:46.080000', N'C2U6W5YL3SNI6MREC5FIXQIDIOM4F75K');
INSERT INTO [G6NguoiDung] ([g6_ma_nguoi_dung], [g6_ten_dang_nhap], [g6_mat_khau], [g6_ho_ten], [g6_email], [g6_so_dien_thoai], [g6_ngay_sinh], [g6_gioi_tinh], [g6_dia_chi], [g6_so_cccd], [g6_anh_the], [g6_anh_dai_dien], [g6_la_nhan_vien], [g6_la_hoi_vien], [g6_la_khach_hang], [g6_ma_chi_nhanh], [g6_ngay_dang_ky], [g6_ma_qr], [g6_nguon_gioi_thieu], [g6_ma_gioi_thieu], [g6_ghi_chu], [g6_google_id], [g6_la_xac_thuc_otp], [g6_la_hoat_dong], [g6_lan_dang_nhap_sai], [g6_khoa_den], [g6_reset_token], [g6_reset_token_het_han], [g6_ngay_tao], [g6_ngay_cap_nhat], [g6_totp_secret]) VALUES (11, NULL, N'$2b$12$OTTKfcwJNWzHobzSMdFVROQhf4FfbVBAlswYomDcvwAWGA6qz04e6', N'Test Member', N'test@example.com', N'0912345678', NULL, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, 1, N'2026-05-13', N'1EA4533D-6BA', NULL, NULL, NULL, NULL, 0, 1, 0, NULL, NULL, NULL, N'2026-05-13 09:08:52.920000', N'2026-05-13 09:08:52.920000', NULL);
INSERT INTO [G6NguoiDung] ([g6_ma_nguoi_dung], [g6_ten_dang_nhap], [g6_mat_khau], [g6_ho_ten], [g6_email], [g6_so_dien_thoai], [g6_ngay_sinh], [g6_gioi_tinh], [g6_dia_chi], [g6_so_cccd], [g6_anh_the], [g6_anh_dai_dien], [g6_la_nhan_vien], [g6_la_hoi_vien], [g6_la_khach_hang], [g6_ma_chi_nhanh], [g6_ngay_dang_ky], [g6_ma_qr], [g6_nguon_gioi_thieu], [g6_ma_gioi_thieu], [g6_ghi_chu], [g6_google_id], [g6_la_xac_thuc_otp], [g6_la_hoat_dong], [g6_lan_dang_nhap_sai], [g6_khoa_den], [g6_reset_token], [g6_reset_token_het_han], [g6_ngay_tao], [g6_ngay_cap_nhat], [g6_totp_secret]) VALUES (1008, NULL, N'$2b$12$vksBQrEBTl96LbbLKWber.saPJTa9MeEPT8Sl/DkNuE5N3jsyRBZS', N'Nguyễn Quang Tâm', N'nguyenquangtam179@gmail.com', N'0036386328', N'2026-04-30', N'nam', N'Hà Nội', NULL, NULL, N'https://lh3.googleusercontent.com/a/ACg8ocIdaEGE6ppPYd_0Kn-CFn-3Z91W6Okys6qQoqj-7XapkkffemFw=s96-c', 0, 1, 0, NULL, N'2026-05-25', N'52D6ED9F-143', NULL, NULL, NULL, N'109117830608901779412', 0, 1, 0, NULL, NULL, NULL, N'2026-05-25 01:38:42.170000', N'2026-05-25 02:01:35.260000', NULL);
GO

SET IDENTITY_INSERT [G6NguoiDung] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6NguoiDungVaiTro]
-- ------------------------------------------------------------
INSERT INTO [G6NguoiDungVaiTro] ([g6_ma_nguoi_dung], [g6_ma_vai_tro]) VALUES (1, 1);
INSERT INTO [G6NguoiDungVaiTro] ([g6_ma_nguoi_dung], [g6_ma_vai_tro]) VALUES (2, 2);
INSERT INTO [G6NguoiDungVaiTro] ([g6_ma_nguoi_dung], [g6_ma_vai_tro]) VALUES (3, 4);
INSERT INTO [G6NguoiDungVaiTro] ([g6_ma_nguoi_dung], [g6_ma_vai_tro]) VALUES (4, 3);
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6NhanVien]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6NhanVien] ON;
GO

INSERT INTO [G6NhanVien] ([g6_ma_nhan_vien], [g6_ma_nguoi_dung], [g6_ma_chi_nhanh], [g6_ho_ten], [g6_ngay_sinh], [g6_gioi_tinh], [g6_so_dien_thoai], [g6_email], [g6_dia_chi], [g6_so_cccd], [g6_ngay_vao_lam], [g6_ngay_nghi_viec], [g6_luong_co_ban], [g6_trang_thai], [g6_hinh_anh], [g6_ngay_tao]) VALUES (1, 1, 1, N'Nguyễn Quang Tâm', NULL, NULL, NULL, NULL, NULL, NULL, N'2026-05-12', NULL, 15000000, N'dang_lam', NULL, N'2026-05-12 09:03:02.217000');
INSERT INTO [G6NhanVien] ([g6_ma_nhan_vien], [g6_ma_nguoi_dung], [g6_ma_chi_nhanh], [g6_ho_ten], [g6_ngay_sinh], [g6_gioi_tinh], [g6_so_dien_thoai], [g6_email], [g6_dia_chi], [g6_so_cccd], [g6_ngay_vao_lam], [g6_ngay_nghi_viec], [g6_luong_co_ban], [g6_trang_thai], [g6_hinh_anh], [g6_ngay_tao]) VALUES (2, 2, 1, N'Nguyễn Hoài Nam', NULL, NULL, NULL, NULL, NULL, NULL, N'2026-05-12', NULL, 15000000, N'dang_lam', NULL, N'2026-05-12 09:03:02.223000');
INSERT INTO [G6NhanVien] ([g6_ma_nhan_vien], [g6_ma_nguoi_dung], [g6_ma_chi_nhanh], [g6_ho_ten], [g6_ngay_sinh], [g6_gioi_tinh], [g6_so_dien_thoai], [g6_email], [g6_dia_chi], [g6_so_cccd], [g6_ngay_vao_lam], [g6_ngay_nghi_viec], [g6_luong_co_ban], [g6_trang_thai], [g6_hinh_anh], [g6_ngay_tao]) VALUES (3, 3, 1, N'Đoàn Anh Quân', NULL, NULL, NULL, NULL, NULL, NULL, N'2026-05-12', NULL, 15000000, N'dang_lam', NULL, N'2026-05-12 09:03:02.230000');
INSERT INTO [G6NhanVien] ([g6_ma_nhan_vien], [g6_ma_nguoi_dung], [g6_ma_chi_nhanh], [g6_ho_ten], [g6_ngay_sinh], [g6_gioi_tinh], [g6_so_dien_thoai], [g6_email], [g6_dia_chi], [g6_so_cccd], [g6_ngay_vao_lam], [g6_ngay_nghi_viec], [g6_luong_co_ban], [g6_trang_thai], [g6_hinh_anh], [g6_ngay_tao]) VALUES (4, 4, 1, N'Nguyễn Xuân Vinh', NULL, NULL, NULL, NULL, NULL, NULL, N'2026-05-12', NULL, 15000000, N'dang_lam', NULL, N'2026-05-12 09:03:02.237000');
INSERT INTO [G6NhanVien] ([g6_ma_nhan_vien], [g6_ma_nguoi_dung], [g6_ma_chi_nhanh], [g6_ho_ten], [g6_ngay_sinh], [g6_gioi_tinh], [g6_so_dien_thoai], [g6_email], [g6_dia_chi], [g6_so_cccd], [g6_ngay_vao_lam], [g6_ngay_nghi_viec], [g6_luong_co_ban], [g6_trang_thai], [g6_hinh_anh], [g6_ngay_tao]) VALUES (5, NULL, 1, N'Nguyễn Quang Tâm - HLV', NULL, NULL, N'0961138440', NULL, NULL, NULL, N'2026-05-12', NULL, 0, N'dang_lam', NULL, N'2026-05-12 11:29:51.820000');
GO

SET IDENTITY_INSERT [G6NhanVien] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6NhatKyHoatDong]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6NhatKyHoatDong] ON;
GO

INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 09:06:28.603000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (2, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 11:18:15.713000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (3, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 11:18:37.820000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (4, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 11:19:13.627000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (5, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 11:19:25.187000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (6, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 11:20:42.753000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (7, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 11:20:49.577000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (8, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 11:20:55.797000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (9, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 11:21:41.080000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (10, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 12:00:31.163000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (11, N'G6QuanTri', 1, N'Thêm lịch bảo trì', N'NxvLichSuBaoTri', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 12:33:35.903000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (12, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-12 13:16:14.557000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (13, N'G6NhanVien', 3, N'Đăng nhập hệ thống', N'G6NguoiDung', 3, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 08:20:26.817000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (14, N'G6NhanVien', 3, N'Đăng nhập hệ thống', N'G6NguoiDung', 3, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 08:53:04.410000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (15, N'G6NhanVien', 4, N'Đăng nhập hệ thống', N'G6NguoiDung', 4, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 08:53:38.183000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (16, N'G6NhanVien', 4, N'Đăng nhập hệ thống', N'G6NguoiDung', 4, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 08:57:29.953000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (17, N'G6NhanVien', 4, N'Đăng nhập hệ thống', N'G6NguoiDung', 4, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 08:59:26.957000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (18, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 11:02:01.347000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (19, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 11:57:44.987000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (20, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 12:01:18.837000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (21, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 13:23:02.897000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (22, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 13:54:47.830000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (23, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 13:54:57.750000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (24, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 14:04:02.857000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (25, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 14:20:10.053000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (26, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 14:20:11.567000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (27, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 14:20:11.757000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (28, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 14:20:12.030000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (29, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 14:23:50.113000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (30, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 14:23:51.043000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (31, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 14:23:51.353000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (32, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-13 14:23:57');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (33, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:27:16.263000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (34, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:27:36.820000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (35, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:29:36.160000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (36, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:29:41.877000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (37, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:29:48.147000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (38, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:32:44.593000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (39, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:36:59.307000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (40, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:37:07.543000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (41, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:41:13.960000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (42, N'G6NhanVien', 2, N'Đăng nhập hệ thống', N'G6NguoiDung', 2, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:41:30.550000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (43, N'G6NhanVien', 4, N'Đăng nhập hệ thống', N'G6NguoiDung', 4, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:41:45.130000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (44, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 10:49:58.643000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (45, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 11:56:07.837000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (46, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 12:29:14.413000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (47, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 13:17:05.780000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (48, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 13:55:51.287000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (49, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-19 14:33:38');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (50, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-20 08:26:44.593000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (51, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-20 08:44:30.347000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (52, N'G6QuanTri', 1, N'Tạo đơn hàng', N'G6DonHang', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-20 09:44:45.563000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (53, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-20 10:05:52.830000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (54, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-20 10:06:26.620000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (55, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-20 10:45:00.803000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (56, N'G6QuanTri', 1, N'Cập nhật cấu hình', N'G6CauHinh', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-20 10:45:07.337000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (57, N'G6QuanTri', 1, N'Cập nhật sản phẩm', N'G6SanPham', 55, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-21 04:02:32.780000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1002, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-23 03:32:23.343000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1003, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-23 03:39:04.550000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1006, N'G6QuanTri', 1, N'Cập nhật sản phẩm', N'G6SanPham', 55, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-23 04:53:45.220000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1007, N'G6QuanTri', 1, N'Cập nhật sản phẩm', N'G6SanPham', 55, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-23 04:53:51.917000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1008, N'G6QuanTri', 1, N'Thêm sản phẩm', N'G6SanPham', NULL, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-23 04:54:24.003000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1009, N'G6QuanTri', 1, N'Cập nhật sản phẩm', N'G6SanPham', 1002, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-23 04:58:48.253000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1012, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-24 10:38:21.517000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1013, N'G6QuanTri', 1, N'Cập nhật sản phẩm', N'G6SanPham', 1002, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-24 10:38:44.937000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1015, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-24 13:59:14.403000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1016, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-25 01:42:02.303000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1017, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-25 01:42:09.980000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1018, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-25 01:43:42.717000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1019, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-05-31 12:18:23.633000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1020, N'G6QuanTri', 1, N'Đăng nhập hệ thống', N'G6NguoiDung', 1, NULL, NULL, N'127.0.0.1', NULL, N'2026-06-02 03:31:58.493000');
INSERT INTO [G6NhatKyHoatDong] ([g6_ma_nhat_ky], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_hanh_dong], [g6_ten_bang], [g6_ma_ban_ghi], [g6_du_lieu_cu], [g6_du_lieu_moi], [g6_dia_chi_ip], [g6_thiet_bi], [g6_ngay_tao]) VALUES (1021, N'G6QuanTri', 1, N'Cập nhật sản phẩm', N'G6SanPham', 55, NULL, NULL, N'127.0.0.1', NULL, N'2026-06-02 03:32:13.090000');
GO

SET IDENTITY_INSERT [G6NhatKyHoatDong] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6OtpXacThuc]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6OtpXacThuc] ON;
GO

-- (Bảng [G6OtpXacThuc] rỗng)

SET IDENTITY_INSERT [G6OtpXacThuc] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6PhienDangNhap]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6PhienDangNhap] ON;
GO

INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (1, N'G6QuanTri', 1, N'6e9c109d84cc6aeda5da9c8c999c3f0dd8297b57c249e335835d321d16f15c90', NULL, N'127.0.0.1', N'2026-05-19 09:06:28.597000', 0, N'2026-05-12 09:06:28.597000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (2, N'G6QuanTri', 1, N'ee824aa7660b36f6f10111d4b7b8c63b1bd0944bfa87b1314df17900588989ee', NULL, N'127.0.0.1', N'2026-05-19 12:00:31.150000', 0, N'2026-05-12 12:00:31.153000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (3, N'G6NhanVien', 3, N'd6308443804af295d4a011c6300aa1ce9e0925965f2c336e50f3dff574bb28e1', NULL, N'127.0.0.1', N'2026-05-20 08:20:26.793000', 0, N'2026-05-13 08:20:26.797000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (4, N'G6NhanVien', 3, N'cef659a8ae4b70b197f3e0b5344eb3b6944f981275762648dddeaad6aa1ac25e', NULL, N'127.0.0.1', N'2026-05-20 08:53:04.403000', 0, N'2026-05-13 08:53:04.407000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (5, N'G6NhanVien', 4, N'23bf0e6cb93e745a071a1a143db0ec35362d9c298297cfd3090239d62df252c3', NULL, N'127.0.0.1', N'2026-05-20 08:53:38.183000', 0, N'2026-05-13 08:53:38.183000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (6, N'G6NhanVien', 4, N'234b187e870880b1b4d04e5666975ede1346f0ba21730ca9d0c5893f56f52dab', NULL, N'127.0.0.1', N'2026-05-20 08:57:29.947000', 0, N'2026-05-13 08:57:29.947000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (7, N'G6NhanVien', 4, N'0c2fb734f1632a76d81f1bcbb2e392b11daf31255bc1e130d255b7bd1018b790', NULL, N'127.0.0.1', N'2026-05-20 08:59:26.950000', 0, N'2026-05-13 08:59:26.950000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (8, N'G6QuanTri', 1, N'f210d73ac54fe279e0e0d3439acce70e6e408e163b0a1405a9a40612eeb34038', NULL, N'127.0.0.1', N'2026-05-20 11:02:01.337000', 0, N'2026-05-13 11:02:01.337000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (9, N'G6QuanTri', 1, N'8051b1eab1af1c2f2590ba7b9ef64ea08e93b573619467ebe499ba3d854abd25', NULL, N'127.0.0.1', N'2026-05-20 11:57:44.980000', 0, N'2026-05-13 11:57:44.983000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (10, N'G6QuanTri', 1, N'24aaef3d9faa747b2b46954a0d266e050ba9b074e3f55278d474aaa2bbca67ea', NULL, N'127.0.0.1', N'2026-05-20 12:01:18.810000', 0, N'2026-05-13 12:01:18.810000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (11, N'G6QuanTri', 1, N'45d091d5c4cf15207080ca9ca221a1a8a562458d4cfa9ae6ecf17cbaa299b719', NULL, N'127.0.0.1', N'2026-05-20 13:23:02.890000', 0, N'2026-05-13 13:23:02.893000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (12, N'G6QuanTri', 1, N'bf2aea0d7c607c6532de6f84365136af82b4aaf3cb352c07ceecbcc7dc5d1648', NULL, N'127.0.0.1', N'2026-05-20 13:54:47.823000', 0, N'2026-05-13 13:54:47.827000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (13, N'G6QuanTri', 1, N'7b6a77ad3b23478bb8baa2c251daa1e7c6eb4f196d1b66d90d1e7f604eade378', NULL, N'127.0.0.1', N'2026-05-20 13:54:57.747000', 0, N'2026-05-13 13:54:57.747000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (14, N'G6QuanTri', 1, N'9f7f5717f6e48257ba16f4cb4cea3687aa82ab8d553af08f3ce1ed7fc1d8272c', NULL, N'127.0.0.1', N'2026-05-20 14:04:02.850000', 0, N'2026-05-13 14:04:02.853000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (15, N'G6QuanTri', 1, N'f77d35fe8d4a3cdb651e1acb6085a1b6011b828a56d106835e63d1f880d35732', NULL, N'127.0.0.1', N'2026-05-20 14:20:10.047000', 0, N'2026-05-13 14:20:10.047000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (16, N'G6QuanTri', 1, N'f254ba129d884cb0250e09e6cdebb4c932f3acd88b73120691a7efce40a98570', NULL, N'127.0.0.1', N'2026-05-20 14:20:11.563000', 0, N'2026-05-13 14:20:11.563000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (17, N'G6QuanTri', 1, N'b77a5a6951ece9e51769216135320ced3dd8686048f9a8515402d7a1c0227385', NULL, N'127.0.0.1', N'2026-05-20 14:20:11.757000', 0, N'2026-05-13 14:20:11.757000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (18, N'G6QuanTri', 1, N'b9ef6e70ef01c5a5288486a1606f79c6c00c4c7236faf42553e2db594b84f7c0', NULL, N'127.0.0.1', N'2026-05-20 14:20:12.027000', 0, N'2026-05-13 14:20:12.027000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (19, N'G6QuanTri', 1, N'd22d3e2fcd7ae1d22483d78cee184b48f8e7dc518d643293074186ccad00d643', NULL, N'127.0.0.1', N'2026-05-20 14:23:50.107000', 0, N'2026-05-13 14:23:50.107000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (20, N'G6QuanTri', 1, N'5e6a4ce3d8c545dbfc840a158014c2a67e0ad5525e0daee0d648c84f534e08fc', NULL, N'127.0.0.1', N'2026-05-20 14:23:51.040000', 0, N'2026-05-13 14:23:51.040000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (21, N'G6QuanTri', 1, N'ead753c171ea88ad46534d9e87de1885ffc9ae35a6428df2199b9d806c7c2885', NULL, N'127.0.0.1', N'2026-05-20 14:23:51.350000', 0, N'2026-05-13 14:23:51.350000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (22, N'G6QuanTri', 1, N'27408018ed10b68322cb45a6fec0b154ce3889d4cf14d2336953de6405466621', NULL, N'127.0.0.1', N'2026-05-20 14:23:56.993000', 0, N'2026-05-13 14:23:56.997000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (23, N'G6QuanTri', 1, N'6c8ee8b3ee02b387d289f8f83405235e51593ba6bbb6682c316f55c35b99e751', NULL, N'127.0.0.1', N'2026-05-26 10:27:16.243000', 0, N'2026-05-19 10:27:16.247000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (24, N'G6QuanTri', 1, N'2abdaf91bbeb7efd3f102a60255e1343db3003b8eb661cec695db1634f3210f2', NULL, N'127.0.0.1', N'2026-05-26 10:27:36.817000', 0, N'2026-05-19 10:27:36.817000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (25, N'G6QuanTri', 1, N'60d6155d4073a4173f101b4a0f60808871604763865e1b49dcaf8c74bc2b2c5c', NULL, N'127.0.0.1', N'2026-05-26 10:29:36.153000', 0, N'2026-05-19 10:29:36.153000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (26, N'G6QuanTri', 1, N'5605e1f879f3e696be54d10054296edaabec09e1070db4b1bfc93d446c5ca83d', NULL, N'127.0.0.1', N'2026-05-26 10:29:41.877000', 0, N'2026-05-19 10:29:41.877000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (27, N'G6QuanTri', 1, N'6880de8455f7263cfba67da10fae02ad3811056cab99b7980643f6c7838be684', NULL, N'127.0.0.1', N'2026-05-26 10:29:48.143000', 0, N'2026-05-19 10:29:48.143000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (28, N'G6QuanTri', 1, N'a7eac287daeb830ef622477c83e919a3777ff4e4f46e7edb18970edc09be7665', NULL, N'127.0.0.1', N'2026-05-26 10:32:44.580000', 0, N'2026-05-19 10:32:44.583000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (29, N'G6QuanTri', 1, N'0cac1cd4cfc7cc2034b66457f99866ec3a6fb3d3d43a264dd431557262402cda', NULL, N'127.0.0.1', N'2026-05-26 10:36:59.297000', 0, N'2026-05-19 10:36:59.297000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (30, N'G6QuanTri', 1, N'7340adefaad394ab211f230e2c05fa75f2b34f0f06d809f41479cfd2c02e51bb', NULL, N'127.0.0.1', N'2026-05-26 10:37:07.540000', 0, N'2026-05-19 10:37:07.540000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (31, N'G6QuanTri', 1, N'f0df74e0710a6bc940686d286f7418c337cf3f8ee037eb76567964a6ac93e368', NULL, N'127.0.0.1', N'2026-05-26 10:41:13.950000', 0, N'2026-05-19 10:41:13.950000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (32, N'G6NhanVien', 2, N'911bcfbe1ff87c5142b5a9e73fda50939c474006337f9f62984770a1bd9749cf', NULL, N'127.0.0.1', N'2026-05-26 10:41:30.543000', 0, N'2026-05-19 10:41:30.543000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (33, N'G6NhanVien', 4, N'8e59f77c474cc4b6b12e22673213f0652e7d3fd196bd0154b321ccafa0d21d51', NULL, N'127.0.0.1', N'2026-05-26 10:41:45.130000', 0, N'2026-05-19 10:41:45.130000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (34, N'G6QuanTri', 1, N'6dac93e1bc70f1a547fe1e46e0e4ddc1d6d0e2ecaaec2ad95b6fa79988fc3761', NULL, N'127.0.0.1', N'2026-05-26 11:56:07.823000', 0, N'2026-05-19 11:56:07.827000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (35, N'G6QuanTri', 1, N'127a85187e7e71a7332aea9c875268b1bdddf56693d8d8d109fcde60a169b527', NULL, N'127.0.0.1', N'2026-05-26 12:29:14.407000', 0, N'2026-05-19 12:29:14.410000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (36, N'G6QuanTri', 1, N'4687bc5d53be684cdae6ab0fb1120cdfe5863a7e58019f3d317691a1a9aa7e41', NULL, N'127.0.0.1', N'2026-05-26 13:17:05.770000', 0, N'2026-05-19 13:17:05.770000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (37, N'G6QuanTri', 1, N'72118961ca1199f5f9a53f1e5b654139273fb9c103e94d069f236e906d00eb94', NULL, N'127.0.0.1', N'2026-05-26 13:55:51.277000', 0, N'2026-05-19 13:55:51.277000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (38, N'G6QuanTri', 1, N'8e6969c99cab5c4254fba988750b7527e00e9d4120a94c94f585f1ec096dcb17', NULL, N'127.0.0.1', N'2026-05-26 14:33:37.990000', 0, N'2026-05-19 14:33:37.993000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (39, N'G6QuanTri', 1, N'7e0eeb7df411e91dc77347a1b5d3432a52dc53a68781d96bd89e67fe833d63cb', NULL, N'127.0.0.1', N'2026-05-27 08:26:44.583000', 0, N'2026-05-20 08:26:44.583000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (40, N'G6QuanTri', 1, N'ccfa4b6b460a7eb0d287eccfe95cbf9ba3dc2b0e17a9d7b8b467437ca4a6c4c7', NULL, N'127.0.0.1', N'2026-05-27 08:44:30.337000', 0, N'2026-05-20 08:44:30.340000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (41, N'G6QuanTri', 1, N'3c2ded655028d8ae1b83ca4144c31875136fdcd9e8e2a1bd29b15081f78a7df0', NULL, N'127.0.0.1', N'2026-05-27 10:05:52.820000', 0, N'2026-05-20 10:05:52.820000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (42, N'G6QuanTri', 1, N'df9099b40db441301cf77e157510407d9847c924079b1f91db350b0eb07a89b0', NULL, N'127.0.0.1', N'2026-05-27 10:06:26.617000', 0, N'2026-05-20 10:06:26.617000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (1002, N'G6QuanTri', 1, N'08a357b62dfe72b0db006acb219e804d1715339c5dbe5fc7e8a703f58deeaf9e', NULL, N'127.0.0.1', N'2026-05-30 03:32:23.337000', 0, N'2026-05-23 03:32:23.337000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (1003, N'G6QuanTri', 1, N'daf6111224712889dadc63e9d5a37ff917cee72e7ed43ac3ddee4630dc224343', NULL, N'127.0.0.1', N'2026-05-30 03:39:04.547000', 0, N'2026-05-23 03:39:04.547000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (1004, N'G6QuanTri', 1, N'9c8af6faa854ddbe24b542209d3b84c98042bb6b1e5dc82261c4378ab0659ffb', NULL, N'127.0.0.1', N'2026-05-31 10:38:21.510000', 0, N'2026-05-24 10:38:21.510000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (1005, N'G6QuanTri', 1, N'd40ba82b8c157464c3f73a59d018b9ea3d43c2572b6ecec38a84a5ed2fff12be', NULL, N'127.0.0.1', N'2026-05-31 13:59:14.390000', 0, N'2026-05-24 13:59:14.390000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (1006, N'G6QuanTri', 1, N'e1dbb8e7a82a7b0339c713c7037953fa9e9cd92768e0fdbe0ca1f7f5bed06a75', NULL, N'127.0.0.1', N'2026-06-01 01:42:02.293000', 0, N'2026-05-25 01:42:02.297000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (1007, N'G6QuanTri', 1, N'7acfca5311a74269768be15c325e69e6e49e365193d988742f48e2e0a6555be2', NULL, N'127.0.0.1', N'2026-06-01 01:42:09.977000', 0, N'2026-05-25 01:42:09.977000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (1008, N'G6QuanTri', 1, N'1c806250ec7d0aa1f3fc5fd73af218f3175eec4d2a7dc93d1769236c5e738520', NULL, N'127.0.0.1', N'2026-06-01 01:43:42.707000', 0, N'2026-05-25 01:43:42.707000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (1009, N'G6QuanTri', 1, N'0e239238cbc3415b3e996950a6bde8bd4dd1f010132937996bc20afd360198a9', NULL, N'127.0.0.1', N'2026-06-07 12:18:23.613000', 0, N'2026-05-31 12:18:23.617000');
INSERT INTO [G6PhienDangNhap] ([g6_ma_phien], [g6_loai_nguoi_dung], [g6_ma_nguoi_dung], [g6_ma_refresh_token_hash], [g6_thiet_bi], [g6_dia_chi_ip], [g6_het_han_luc], [g6_la_thu_hoi], [g6_ngay_tao]) VALUES (1010, N'G6QuanTri', 1, N'2ba74a5ab7f7ca452660a5dd9da256ef258702a0f680730f7b663974cc4f0796', NULL, N'127.0.0.1', N'2026-06-09 03:31:58.480000', 0, N'2026-06-02 03:31:58.483000');
GO

SET IDENTITY_INSERT [G6PhienDangNhap] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6QuyenHan]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6QuyenHan] ON;
GO

INSERT INTO [G6QuyenHan] ([g6_ma_quyen], [g6_ten_quyen], [g6_nhom_quyen]) VALUES (1, N'XEM_BAO_CAO', N'Thống kê');
INSERT INTO [G6QuyenHan] ([g6_ma_quyen], [g6_ten_quyen], [g6_nhom_quyen]) VALUES (2, N'QL_NHAN_VIEN', N'Quản lý nhân sự');
INSERT INTO [G6QuyenHan] ([g6_ma_quyen], [g6_ten_quyen], [g6_nhom_quyen]) VALUES (3, N'QL_KHO', N'Quản lý kho hàng');
INSERT INTO [G6QuyenHan] ([g6_ma_quyen], [g6_ten_quyen], [g6_nhom_quyen]) VALUES (4, N'QL_HOI_VIEN', N'Quản lý hội viên');
INSERT INTO [G6QuyenHan] ([g6_ma_quyen], [g6_ten_quyen], [g6_nhom_quyen]) VALUES (5, N'g6_xem_hoi_vien', N'Hội viên');
INSERT INTO [G6QuyenHan] ([g6_ma_quyen], [g6_ten_quyen], [g6_nhom_quyen]) VALUES (6, N'g6_checkin_hoi_vien', N'Hội viên');
INSERT INTO [G6QuyenHan] ([g6_ma_quyen], [g6_ten_quyen], [g6_nhom_quyen]) VALUES (7, N'g6_xem_cau_hinh', N'Hệ thống');
INSERT INTO [G6QuyenHan] ([g6_ma_quyen], [g6_ten_quyen], [g6_nhom_quyen]) VALUES (8, N'g6_xem_goi_tap', N'Gói tập');
INSERT INTO [G6QuyenHan] ([g6_ma_quyen], [g6_ten_quyen], [g6_nhom_quyen]) VALUES (9, N'g6_xem_nhan_vien', N'Nhân sự');
GO

SET IDENTITY_INSERT [G6QuyenHan] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6SanPham]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6SanPham] ON;
GO

INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1, 1, 1, N'Whey Protein Gold', N'whey-protein-gold', N'Sản phẩm tăng cơ chất lượng cao.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 09:03:02.263000', N'2026-05-12 09:03:02.263000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (20, 8, 38, N'Jacked Factory Authentic ISO Whey Protein, 25 Servings', N'jacked-factory-authentic-iso-whey-protein-25-servings', N'Jacked Factory Authentic ISO Whey Protein, 25 Servings chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.107000', N'2026-05-12 13:22:35.107000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (21, 8, 39, N'Perfect Diesel Whey Isolate New Zealand, 5 Lbs (75 Servings)', N'perfect-diesel-whey-isolate-new-zealand-5-lbs-75-servings', N'Perfect Diesel Whey Isolate New Zealand, 5 Lbs (75 Servings) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.110000', N'2026-05-12 13:22:35.110000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (22, 8, 40, N'Dymatize ISO 100 Hydrolyzed, 100% Whey Protein Isolate, 5 Lbs (2.27 kg)', N'dymatize-iso-100-hydrolyzed-100-whey-protein-isolate-5-lbs-227-kg', N'Dymatize ISO 100 Hydrolyzed, 100% Whey Protein Isolate, 5 Lbs (2.27 kg) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.113000', N'2026-05-12 13:22:35.113000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (23, 8, 41, N'Beyond Isolate - Ultra Premium Whey Protein Isolate, 5 Lbs (75 Servings)', N'beyond-isolate---ultra-premium-whey-protein-isolate-5-lbs-75-servings', N'Beyond Isolate - Ultra Premium Whey Protein Isolate, 5 Lbs (75 Servings) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.117000', N'2026-05-12 13:22:35.117000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (24, 8, 42, N'Premier Protein 100% Whey Protein Powder, 3Lbs (35 Servings)', N'premier-protein-100-whey-protein-powder-3lbs-35-servings', N'Premier Protein 100% Whey Protein Powder, 3Lbs (35 Servings) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.117000', N'2026-05-12 13:22:35.117000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (25, 8, 39, N'Perfect Sport Ultra Fuel 100% Grass-Fed Whey Protein, 4 Lb (45 Servings)', N'perfect-sport-ultra-fuel-100-grass-fed-whey-protein-4-lb-45-servings', N'Perfect Sport Ultra Fuel 100% Grass-Fed Whey Protein, 4 Lb (45 Servings) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.120000', N'2026-05-12 13:22:35.120000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (26, 8, 43, N'Axe & Sledge 100% Whey Isolate Farm Fed, 2Lbs (28 Servings)', N'axe-sledge-100-whey-isolate-farm-fed-2lbs-28-servings', N'Axe & Sledge 100% Whey Isolate Farm Fed, 2Lbs (28 Servings) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.123000', N'2026-05-12 13:22:35.123000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (27, 8, 44, N'NutraBio Clear Whey Protein Isolate, 20 Servings', N'nutrabio-clear-whey-protein-isolate-20-servings', N'NutraBio Clear Whey Protein Isolate, 20 Servings chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.123000', N'2026-05-12 13:22:35.123000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (28, 8, 45, N'Elite Labs USA 100% True Whey 5Lbs (50 Servings)', N'elite-labs-usa-100-true-whey-5lbs-50-servings', N'Elite Labs USA 100% True Whey 5Lbs (50 Servings) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.127000', N'2026-05-12 13:22:35.127000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (29, 8, 46, N'PVL ISO Gold - Premium Whey Protein With Probiotic, 5 Lbs (2.27kg)', N'pvl-iso-gold---premium-whey-protein-with-probiotic-5-lbs-227kg', N'PVL ISO Gold - Premium Whey Protein With Probiotic, 5 Lbs (2.27kg) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.127000', N'2026-05-12 13:22:35.127000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (30, 8, 44, N'NutraBio Whey Protein Isolate, 5Lbs (2.27kg)', N'nutrabio-whey-protein-isolate-5lbs-227kg', N'NutraBio Whey Protein Isolate, 5Lbs (2.27kg) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.130000', N'2026-05-12 13:22:35.130000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (31, 8, 44, N'Nutrabio Classic Whey Protein - Premium Quality Protein, 5 Lbs (2,268 Kg)', N'nutrabio-classic-whey-protein---premium-quality-protein-5-lbs-2268-kg', N'Nutrabio Classic Whey Protein - Premium Quality Protein, 5 Lbs (2,268 Kg) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.133000', N'2026-05-12 13:22:35.133000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (32, 9, 47, N'Labrada Muscle Mass Gainer 12 Lbs (5443g)', N'labrada-muscle-mass-gainer-12-lbs-5443g', N'Labrada Muscle Mass Gainer 12 Lbs (5443g) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.133000', N'2026-05-12 13:22:35.133000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (33, 9, 48, N'Mutant Mass 15 Lbs (6.8 kg)', N'mutant-mass-15-lbs-68-kg', N'Mutant Mass 15 Lbs (6.8 kg) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.137000', N'2026-05-12 13:22:35.137000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (34, 9, 49, N'ON Serious Mass 12 Lbs (5.4 KG)', N'on-serious-mass-12-lbs-54-kg', N'ON Serious Mass 12 Lbs (5.4 KG) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.140000', N'2026-05-12 13:22:35.140000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (35, 9, 50, N'BioTechUSA Hyper Mass', N'biotechusa-hyper-mass', N'BioTechUSA Hyper Mass chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.143000', N'2026-05-12 13:22:35.143000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (36, 9, 48, N'Mutant Mass Extreme 2500, 12Lbs (5.45 Kg)', N'mutant-mass-extreme-2500-12lbs-545-kg', N'Mutant Mass Extreme 2500, 12Lbs (5.45 Kg) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.147000', N'2026-05-12 13:22:35.147000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (37, 9, 51, N'Sữa tăng cân Rule 1 Mass Gainer, 12 Lbs (16 Servings)', N'sữa-tăng-cân-rule-1-mass-gainer-12-lbs-16-servings', N'Sữa tăng cân Rule 1 Mass Gainer, 12 Lbs (16 Servings) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.147000', N'2026-05-12 13:22:35.147000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (38, 9, 49, N'ON Serious Mass 6 Lbs (2.72 KG)', N'on-serious-mass-6-lbs-272-kg', N'ON Serious Mass 6 Lbs (2.72 KG) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.150000', N'2026-05-12 13:22:35.150000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (39, 9, 48, N'Mutant Mass 5 Lbs (2,27 Kg)', N'mutant-mass-5-lbs-227-kg', N'Mutant Mass 5 Lbs (2,27 Kg) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.153000', N'2026-05-12 13:22:35.153000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (40, 9, 55, N'(Tách Lẻ) Sữa Tăng Cân Mass Gainer, 1KG', N'tách-lẻ-sữa-tăng-cân-mass-gainer-1kg', N'(Tách Lẻ) Sữa Tăng Cân Mass Gainer, 1KG chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.157000', N'2026-05-12 13:22:35.157000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (41, 9, 45, N'Elite Labs USA Mass Muscle Gainer, 5 Lbs (2.3 kg)', N'elite-labs-usa-mass-muscle-gainer-5-lbs-23-kg', N'Elite Labs USA Mass Muscle Gainer, 5 Lbs (2.3 kg) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.160000', N'2026-05-12 13:22:35.160000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (42, 9, 52, N'Nutrex Mass Infusion, 12 Lbs (5.45 Kg)', N'nutrex-mass-infusion-12-lbs-545-kg', N'Nutrex Mass Infusion, 12 Lbs (5.45 Kg) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.163000', N'2026-05-12 13:22:35.163000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (43, 9, 53, N'Sữa Tăng Cân Applied Nutrition Critical Mass, 6KG (40 Servings)', N'sữa-tăng-cân-applied-nutrition-critical-mass-6kg-40-servings', N'Sữa Tăng Cân Applied Nutrition Critical Mass, 6KG (40 Servings) chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.167000', N'2026-05-12 13:22:35.167000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (44, 10, 55, N'Găng tay cao cấp Premium Glove', N'găng-tay-cao-cấp-premium-glove', N'Găng tay cao cấp Premium Glove chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.173000', N'2026-05-12 13:22:35.173000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (45, 10, 54, N'Găng tay nữ - Harbinger Women''s Power Glove #1', N'găng-tay-nữ---harbinger-womens-power-glove-1', N'Găng tay nữ - Harbinger Women''s Power Glove #1 chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.177000', N'2026-05-12 13:22:35.177000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (46, 10, 54, N'Găng tay nam - Harbinger Gloves Power StretchBack Style 155', N'găng-tay-nam---harbinger-gloves-power-stretchback-style-155', N'Găng tay nam - Harbinger Gloves Power StretchBack Style 155 chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.180000', N'2026-05-12 13:22:35.180000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (47, 10, 54, N'Harbinger Gloves Pro FlexClosure Style 143', N'harbinger-gloves-pro-flexclosure-style-143', N'Harbinger Gloves Pro FlexClosure Style 143 chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.183000', N'2026-05-12 13:22:35.183000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (48, 10, 54, N'Harbinger Women''s FlexFit AntiMicrobial Gloves, White', N'harbinger-womens-flexfit-antimicrobial-gloves-white', N'Harbinger Women''s FlexFit AntiMicrobial Gloves, White chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.187000', N'2026-05-12 13:22:35.187000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (49, 10, 54, N'Harbinger Women''s FlexFit AntiMicrobial Gloves, Purple', N'harbinger-womens-flexfit-antimicrobial-gloves-purple', N'Harbinger Women''s FlexFit AntiMicrobial Gloves, Purple chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.193000', N'2026-05-12 13:22:35.193000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (50, 10, 54, N'Harbinger Women''s Pro Glove, Black/Pink', N'harbinger-womens-pro-glove-blackpink', N'Harbinger Women''s Pro Glove, Black/Pink chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.197000', N'2026-05-12 13:22:35.197000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (51, 10, 54, N'Harbinger Women''s Pro Glove, Black/Gray', N'harbinger-womens-pro-glove-blackgray', N'Harbinger Women''s Pro Glove, Black/Gray chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.197000', N'2026-05-12 13:22:35.197000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (52, 10, 54, N'Harbinger Palm Grips, Black', N'harbinger-palm-grips-black', N'Harbinger Palm Grips, Black chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.200000', N'2026-05-12 13:22:35.200000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (53, 10, 54, N'Harbinger Pro Gloves, Black/Grey', N'harbinger-pro-gloves-blackgrey', N'Harbinger Pro Gloves, Black/Grey chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.203000', N'2026-05-12 13:22:35.203000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (54, 10, 54, N'Harbinger 1260 Men''s Training Grip Gloves, Blue/Black', N'harbinger-1260-mens-training-grip-gloves-blueblack', N'Harbinger 1260 Men''s Training Grip Gloves, Blue/Black chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.207000', N'2026-05-12 13:22:35.207000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (55, 10, 54, N'Harbinger Gloves Pro WristWrap Style 140', N'harbinger-gloves-pro-wristwrap-style-140', N'Harbinger Gloves Pro WristWrap Style 140 chính hãng, hỗ trợ tập luyện hiệu quả.', NULL, NULL, NULL, NULL, 0, 1, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-12 13:22:35.210000', N'2026-05-23 12:04:40.213000');
INSERT INTO [G6SanPham] ([g6_ma_san_pham], [g6_ma_danh_muc], [g6_ma_thuong_hieu], [g6_ten_san_pham], [g6_slug], [g6_mo_ta_ngan], [g6_mo_ta_day_du], [g6_cach_dung], [g6_nuoc_xuat_xu], [g6_doi_tuong_dung], [g6_da_ban], [g6_luot_xem], [g6_thu_tu_hien_thi], [g6_la_noi_bat], [g6_la_ban_chay], [g6_la_hang_moi], [g6_la_hoat_dong], [g6_seo_title], [g6_seo_mo_ta], [g6_ngay_tao], [g6_ngay_cap_nhat]) VALUES (1002, 1, 1, N'test', N'test', N'mô tả sản phẩm', NULL, NULL, NULL, NULL, 0, 2, 0, 0, 0, 0, 1, NULL, NULL, N'2026-05-23 04:54:23.993000', N'2026-06-02 04:05:13.237000');
GO

SET IDENTITY_INSERT [G6SanPham] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6SanPhamMucTieu]
-- ------------------------------------------------------------
-- (Bảng [G6SanPhamMucTieu] rỗng)

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6TonKho]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6TonKho] ON;
GO

INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (18, 20, 1, 73, 0, 10, N'2026-05-12 13:22:35.110000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (19, 21, 1, 27, 0, 10, N'2026-05-12 13:22:35.113000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (20, 22, 1, 26, 0, 10, N'2026-05-12 13:22:35.113000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (21, 23, 1, 34, 0, 10, N'2026-05-12 13:22:35.117000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (22, 24, 1, 98, 0, 10, N'2026-05-12 13:22:35.120000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (23, 25, 1, 20, 0, 10, N'2026-05-12 13:22:35.120000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (24, 26, 1, 92, 0, 10, N'2026-05-12 13:22:35.123000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (25, 27, 1, 68, 0, 10, N'2026-05-12 13:22:35.127000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (26, 28, 1, 100, 0, 10, N'2026-05-12 13:22:35.127000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (27, 29, 1, 71, 0, 10, N'2026-05-12 13:22:35.130000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (28, 30, 1, 74, 0, 10, N'2026-05-12 13:22:35.130000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (29, 31, 1, 88, 0, 10, N'2026-05-12 13:22:35.133000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (30, 32, 1, 20, 0, 10, N'2026-05-12 13:22:35.137000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (31, 33, 1, 92, 0, 10, N'2026-05-12 13:22:35.140000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (32, 34, 1, 65, 0, 10, N'2026-05-12 13:22:35.143000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (33, 35, 1, 79, 0, 10, N'2026-05-12 13:22:35.143000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (34, 36, 1, 92, 0, 10, N'2026-05-12 13:22:35.147000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (35, 37, 1, 23, 0, 10, N'2026-05-12 13:22:35.150000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (36, 38, 1, 62, 0, 10, N'2026-05-12 13:22:35.153000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (37, 39, 1, 23, 0, 10, N'2026-05-12 13:22:35.153000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (38, 40, 1, 97, 0, 10, N'2026-05-12 13:22:35.160000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (39, 41, 1, 80, 0, 10, N'2026-05-12 13:22:35.163000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (40, 42, 1, 70, 0, 10, N'2026-05-12 13:22:35.167000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (41, 43, 1, 70, 0, 10, N'2026-05-12 13:22:35.170000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (42, 44, 1, 49, 0, 10, N'2026-05-12 13:22:35.177000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (43, 45, 1, 39, 0, 10, N'2026-05-12 13:22:35.180000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (44, 46, 1, 25, 0, 10, N'2026-05-12 13:22:35.183000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (45, 47, 1, 98, 0, 10, N'2026-05-12 13:22:35.187000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (46, 48, 1, 36, 0, 10, N'2026-05-12 13:22:35.190000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (47, 49, 1, 99, 0, 10, N'2026-05-12 13:22:35.193000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (48, 50, 1, 92, 0, 10, N'2026-05-12 13:22:35.197000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (49, 51, 1, 93, 0, 10, N'2026-05-12 13:22:35.200000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (50, 52, 1, 58, 0, 10, N'2026-05-12 13:22:35.203000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (51, 53, 1, 70, 0, 10, N'2026-05-12 13:22:35.207000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (52, 54, 1, 69, 0, 10, N'2026-05-12 13:22:35.210000');
INSERT INTO [G6TonKho] ([g6_ma_ton_kho], [g6_ma_bien_the], [g6_ma_chi_nhanh], [g6_so_luong], [g6_so_luong_dat_truoc], [g6_nguong_canh_bao], [g6_ngay_cap_nhat]) VALUES (53, 55, 1, 46, 0, 10, N'2026-05-12 13:22:35.210000');
GO

SET IDENTITY_INSERT [G6TonKho] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6ThanhPhanDinhDuong]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6ThanhPhanDinhDuong] ON;
GO

-- (Bảng [G6ThanhPhanDinhDuong] rỗng)

SET IDENTITY_INSERT [G6ThanhPhanDinhDuong] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6ThanhToan]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6ThanhToan] ON;
GO

INSERT INTO [G6ThanhToan] ([g6_ma_thanh_toan], [g6_ma_nguoi_dung], [g6_loai_giao_dich], [g6_so_tien], [g6_phuong_thuc], [g6_trang_thai], [g6_ma_giao_dich_cong], [g6_du_lieu_tra_ve], [g6_ngay_thanh_toan], [g6_ghi_chu], [g6_ngay_tao]) VALUES (1, 4, N'thanh_toan_don_hang', 1200000, N'cod', N'thanh_cong', NULL, NULL, N'2026-05-12 12:53:25.540000', NULL, N'2026-05-12 09:03:02.333000');
INSERT INTO [G6ThanhToan] ([g6_ma_thanh_toan], [g6_ma_nguoi_dung], [g6_loai_giao_dich], [g6_so_tien], [g6_phuong_thuc], [g6_trang_thai], [g6_ma_giao_dich_cong], [g6_du_lieu_tra_ve], [g6_ngay_thanh_toan], [g6_ghi_chu], [g6_ngay_tao]) VALUES (2, 10, N'don_hang', 11000, N'bank_transfer', N'thanh_cong', N'FT26145915489130', N'{"transaction_id": "FT26145915489130", "transaction_date": "2026-05-24 20:54:04", "account_number": "188806789", "bank": "MB", "amount": 11000, "description": "NGUYEN QUANG TAM MBVCB.14368484461.133660.DH1012.CT tu 1038957518 NGUYEN QUANG TAM toi 188806789 NGUYEN QUANG TAM tai MB- Ma GD ACSP/ gs133660", "type": "IN"}', N'2026-05-24 13:58:02.550000', N'Tự động tạo từ đơn hàng #1012', N'2026-05-24 13:58:02.553000');
GO

SET IDENTITY_INSERT [G6ThanhToan] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6ThietBi]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6ThietBi] ON;
GO

INSERT INTO [G6ThietBi] ([g6_ma_thiet_bi], [g6_ma_chi_nhanh], [g6_ten_thiet_bi], [g6_thuong_hieu], [g6_model], [g6_so_serie], [g6_ngay_mua], [g6_ngay_bao_hanh_het], [g6_ngay_bao_tri_cuoi], [g6_ngay_bao_tri_tiep], [g6_trang_thai], [g6_hinh_anh], [g6_ghi_chu]) VALUES (1, 1, N'Máy chạy bộ Matrix T7', N'Matrix', NULL, NULL, NULL, NULL, NULL, NULL, N'hoat_dong', NULL, NULL);
INSERT INTO [G6ThietBi] ([g6_ma_thiet_bi], [g6_ma_chi_nhanh], [g6_ten_thiet_bi], [g6_thuong_hieu], [g6_model], [g6_so_serie], [g6_ngay_mua], [g6_ngay_bao_hanh_het], [g6_ngay_bao_tri_cuoi], [g6_ngay_bao_tri_tiep], [g6_trang_thai], [g6_hinh_anh], [g6_ghi_chu]) VALUES (2, 1, N'thiết bị 1', N'thương hiệu 1', NULL, NULL, NULL, NULL, NULL, NULL, N'hoat_dong', NULL, NULL);
INSERT INTO [G6ThietBi] ([g6_ma_thiet_bi], [g6_ma_chi_nhanh], [g6_ten_thiet_bi], [g6_thuong_hieu], [g6_model], [g6_so_serie], [g6_ngay_mua], [g6_ngay_bao_hanh_het], [g6_ngay_bao_tri_cuoi], [g6_ngay_bao_tri_tiep], [g6_trang_thai], [g6_hinh_anh], [g6_ghi_chu]) VALUES (3, 1, N'thiết bị 2', N'thương hiệu 2', NULL, NULL, NULL, NULL, NULL, NULL, N'hoat_dong', NULL, NULL);
INSERT INTO [G6ThietBi] ([g6_ma_thiet_bi], [g6_ma_chi_nhanh], [g6_ten_thiet_bi], [g6_thuong_hieu], [g6_model], [g6_so_serie], [g6_ngay_mua], [g6_ngay_bao_hanh_het], [g6_ngay_bao_tri_cuoi], [g6_ngay_bao_tri_tiep], [g6_trang_thai], [g6_hinh_anh], [g6_ghi_chu]) VALUES (4, 1, N'Máy tạ', N'Technogym', NULL, NULL, NULL, NULL, NULL, NULL, N'hoat_dong', NULL, NULL);
GO

SET IDENTITY_INSERT [G6ThietBi] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6ThongBao]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6ThongBao] ON;
GO

INSERT INTO [G6ThongBao] ([g6_ma_thong_bao], [g6_tieu_de], [g6_noi_dung], [g6_loai], [g6_la_quang_ba], [g6_ma_nguoi_nhan], [g6_loai_nguoi_nhan], [g6_la_da_doc], [g6_du_lieu_them], [g6_ngay_tao]) VALUES (1, N'Chào mừng', N'Chào mừng bạn đến với hệ thống!', N'in_app', 0, 1, NULL, 0, NULL, N'2026-05-12 09:03:02.340000');
GO

SET IDENTITY_INSERT [G6ThongBao] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6ThuongHieu]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6ThuongHieu] ON;
GO

INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (1, N'IronMax', N'ironmax', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (38, N'Jacked Factory', N'jacked-factory', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (39, N'Perfect Sports', N'perfect-sports', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (40, N'Dymatize', N'dymatize', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (41, N'Beyond Yourself', N'beyond-yourself', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (42, N'Premier Protein', N'premier-protein', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (43, N'Axe & Sledge', N'axe-sledge', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (44, N'NutraBio', N'nutrabio', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (45, N'Elite Labs USA', N'elite-labs-usa', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (46, N'PVL', N'pvl', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (47, N'Labrada', N'labrada', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (48, N'Mutant', N'mutant', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (49, N'Optimum Nutrition', N'optimum-nutrition', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (50, N'BioTechUSA', N'biotechusa', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (51, N'Rule 1', N'rule-1', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (52, N'Nutrex', N'nutrex', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (53, N'Applied Nutrition', N'applied-nutrition', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (54, N'Harbinger', N'harbinger', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
INSERT INTO [G6ThuongHieu] ([g6_ma_thuong_hieu], [g6_ten_thuong_hieu], [g6_slug], [g6_nuoc_xuat_xu], [g6_logo], [g6_mo_ta], [g6_website], [g6_la_noi_bat], [g6_loai_tru_ma_giam], [g6_la_hoat_dong], [g6_thu_tu_hien_thi]) VALUES (55, N'Generic', N'generic', NULL, NULL, NULL, NULL, 0, 0, 1, 0);
GO

SET IDENTITY_INSERT [G6ThuongHieu] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6VaiTro]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6VaiTro] ON;
GO

INSERT INTO [G6VaiTro] ([g6_ma_vai_tro], [g6_ten_vai_tro], [g6_mo_ta]) VALUES (1, N'G6QuanTri', N'Quản trị hệ thống');
INSERT INTO [G6VaiTro] ([g6_ma_vai_tro], [g6_ten_vai_tro], [g6_mo_ta]) VALUES (2, N'G6QuanLy', N'Quản lý chi nhánh');
INSERT INTO [G6VaiTro] ([g6_ma_vai_tro], [g6_ten_vai_tro], [g6_mo_ta]) VALUES (3, N'G6NhanVien', N'Nhân viên bán hàng');
INSERT INTO [G6VaiTro] ([g6_ma_vai_tro], [g6_ten_vai_tro], [g6_mo_ta]) VALUES (4, N'G6PT', N'Huấn luyện viên (PT)');
INSERT INTO [G6VaiTro] ([g6_ma_vai_tro], [g6_ten_vai_tro], [g6_mo_ta]) VALUES (5, N'G6HoiVien', N'Hội viên');
INSERT INTO [G6VaiTro] ([g6_ma_vai_tro], [g6_ten_vai_tro], [g6_mo_ta]) VALUES (6, N'G6KhachHang', N'Khách hàng online');
GO

SET IDENTITY_INSERT [G6VaiTro] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6VaiTroQuyen]
-- ------------------------------------------------------------
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (1, 1);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (1, 2);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (1, 3);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (1, 4);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (1, 5);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (1, 7);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (1, 8);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (2, 1);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (2, 2);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (2, 3);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (2, 4);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (2, 5);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (2, 6);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (2, 7);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (2, 8);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (2, 9);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (3, 1);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (3, 2);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (3, 3);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (3, 4);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (3, 5);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (3, 7);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (3, 8);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (4, 1);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (4, 3);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (4, 4);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (4, 5);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (4, 6);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (4, 7);
INSERT INTO [G6VaiTroQuyen] ([g6_ma_vai_tro], [g6_ma_quyen]) VALUES (4, 8);
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [G6VungVanChuyen]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [G6VungVanChuyen] ON;
GO

-- (Bảng [G6VungVanChuyen] rỗng)

SET IDENTITY_INSERT [G6VungVanChuyen] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [NxvBaiTapTrongNgay]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [NxvBaiTapTrongNgay] ON;
GO

-- (Bảng [NxvBaiTapTrongNgay] rỗng)

SET IDENTITY_INSERT [NxvBaiTapTrongNgay] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [NxvChuongTrinhTapLuyen]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [NxvChuongTrinhTapLuyen] ON;
GO

-- (Bảng [NxvChuongTrinhTapLuyen] rỗng)

SET IDENTITY_INSERT [NxvChuongTrinhTapLuyen] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [NxvDangKySuKien]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [NxvDangKySuKien] ON;
GO

-- (Bảng [NxvDangKySuKien] rỗng)

SET IDENTITY_INSERT [NxvDangKySuKien] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [NxvDanhGiaHLV]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [NxvDanhGiaHLV] ON;
GO

-- (Bảng [NxvDanhGiaHLV] rỗng)

SET IDENTITY_INSERT [NxvDanhGiaHLV] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [NxvDanhGiaLopHoc]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [NxvDanhGiaLopHoc] ON;
GO

-- (Bảng [NxvDanhGiaLopHoc] rỗng)

SET IDENTITY_INSERT [NxvDanhGiaLopHoc] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [NxvLichSuBaoTri]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [NxvLichSuBaoTri] ON;
GO

INSERT INTO [NxvLichSuBaoTri] ([nxv_ma_bao_tri], [nxv_ma_thiet_bi], [nxv_ma_chi_nhanh], [nxv_loai], [nxv_ngay_bao_tri], [nxv_ngay_hoan_thanh], [nxv_nguoi_thuc_hien], [nxv_noi_dung], [nxv_chi_phi], [nxv_ket_qua], [nxv_ghi_chu], [nxv_ngay_bao_tri_tiep_theo], [nxv_ngay_tao], [g6_deleted_at]) VALUES (1, 3, NULL, N'dinh_ky', N'2026-05-12', NULL, NULL, N'mô tả 1', 0, N'cho_xu_ly', NULL, NULL, N'2026-05-12 12:33:35.893000', NULL);
GO

SET IDENTITY_INSERT [NxvLichSuBaoTri] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [NxvPhieuSuaChua]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [NxvPhieuSuaChua] ON;
GO

-- (Bảng [NxvPhieuSuaChua] rỗng)

SET IDENTITY_INSERT [NxvPhieuSuaChua] OFF;
GO

-- ------------------------------------------------------------
-- Dữ liệu bảng: [NxvSuKien]
-- ------------------------------------------------------------
SET IDENTITY_INSERT [NxvSuKien] ON;
GO

INSERT INTO [NxvSuKien] ([nxv_ma_su_kien], [nxv_ma_chi_nhanh], [nxv_ten], [nxv_mo_ta], [nxv_loai], [nxv_hinh_anh], [nxv_ngay_bat_dau], [nxv_ngay_ket_thuc], [nxv_dia_diem], [nxv_suc_chua], [nxv_gia_ve], [nxv_gia_giam], [nxv_ma_goi_ap_dung], [nxv_la_hoat_dong], [nxv_ngay_tao], [g6_deleted_at]) VALUES (1, 1, N'Thử thách 7 ngày Squat', N'Tham gia thử thách để nhận quà hấp dẫn.', N'su_kien', NULL, N'2026-05-12 16:03:02.273000', N'2026-05-19 16:03:02.273000', NULL, NULL, 0, NULL, NULL, 1, N'2026-05-12 09:03:02.277000', NULL);
INSERT INTO [NxvSuKien] ([nxv_ma_su_kien], [nxv_ma_chi_nhanh], [nxv_ten], [nxv_mo_ta], [nxv_loai], [nxv_hinh_anh], [nxv_ngay_bat_dau], [nxv_ngay_ket_thuc], [nxv_dia_diem], [nxv_suc_chua], [nxv_gia_ve], [nxv_gia_giam], [nxv_ma_goi_ap_dung], [nxv_la_hoat_dong], [nxv_ngay_tao], [g6_deleted_at]) VALUES (2, NULL, N'Giải vô địch Gym 2026', N'mô tả Giải vô địch Gym 2026', N'su_kien', NULL, N'2026-05-12 18:30:00', N'2026-05-16 18:30:00', N'Hội trường tầng 2', 100, 0, NULL, NULL, 1, N'2026-05-12 11:31:08.083000', NULL);
GO

SET IDENTITY_INSERT [NxvSuKien] OFF;
GO

-- 2. Kích hoạt lại toàn bộ foreign key constraints
EXEC sp_MSforeachtable "ALTER TABLE ? WITH CHECK CHECK CONSTRAINT all";
GO
