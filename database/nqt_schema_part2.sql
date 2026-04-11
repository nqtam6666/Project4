-- ============================================================
-- NQT GYM MANAGEMENT + SUPPLEMENT STORE
-- MySQL Schema - Part 2: Group 6-10
-- GROUP 6: HUẤN LUYỆN VIÊN | GROUP 7: LỚP HỌC NHÓM
-- GROUP 8: DỊCH VỤ PHỤ | GROUP 9: DANH MỤC SP | GROUP 10: SẢN PHẨM
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- GROUP 6: HUẤN LUYỆN VIÊN (PT)
-- ============================================================

CREATE TABLE NqtHuanLuyenVien (
    nqt_ma_hlv              INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_nhan_vien        INT             NOT NULL,
    nqt_ma_chi_nhanh        INT             NOT NULL,
    nqt_chuyen_mon          JSON            NULL COMMENT '["tang_co","giam_mo","yoga","boxing"]',
    nqt_cap_chung_chi       VARCHAR(50)     NULL COMMENT '''ACE'',''NASM'',''REPs'',''ISSA''',
    nqt_so_nam_kinh_nghiem  INT             NOT NULL DEFAULT 0,
    nqt_tieu_su             TEXT            NULL,
    nqt_gia_theo_buoi       DECIMAL(15,0)   NULL,
    nqt_hinh_anh            VARCHAR(500)    NULL,
    nqt_thu_hang            TINYINT         NOT NULL DEFAULT 5 COMMENT '1-5 sao',
    nqt_so_hoi_vien_hien_tai INT            NOT NULL DEFAULT 0,
    nqt_toi_da_hoi_vien     INT             NOT NULL DEFAULT 20,
    nqt_la_hien_thi_web     TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nqt_ma_hlv),
    KEY idx_nqt_hlv_nhanvien  (nqt_ma_nhan_vien),
    KEY idx_nqt_hlv_chinhanh  (nqt_ma_chi_nhanh),
    CONSTRAINT fk_nqt_hlv_nhanvien FOREIGN KEY (nqt_ma_nhan_vien) REFERENCES NqtNhanVien (nqt_ma_nhan_vien),
    CONSTRAINT fk_nqt_hlv_chinhanh FOREIGN KEY (nqt_ma_chi_nhanh) REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtGoiPT (
    nqt_ma_goi_pt       INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_hlv          INT             NOT NULL,
    nqt_ten_goi         VARCHAR(100)    NOT NULL,
    nqt_so_buoi         INT             NOT NULL COMMENT '10, 20, 30 buổi',
    nqt_thoi_luong_buoi INT             NOT NULL COMMENT 'Phút/buổi',
    nqt_gia             DECIMAL(15,0)   NOT NULL,
    nqt_gia_khuyen_mai  DECIMAL(15,0)   NULL,
    nqt_hieu_luc_ngay   INT             NOT NULL DEFAULT 90 COMMENT 'Hết hạn sau X ngày từ ngày mua',
    nqt_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_goi_pt),
    KEY idx_nqt_goipt_hlv (nqt_ma_hlv),
    CONSTRAINT fk_nqt_goipt_hlv FOREIGN KEY (nqt_ma_hlv) REFERENCES NqtHuanLuyenVien (nqt_ma_hlv)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtDangKyGoiPT (
    nqt_ma_dang_ky_pt   INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_hoi_vien     INT             NOT NULL,
    nqt_ma_goi_pt       INT             NOT NULL,
    nqt_ma_hlv          INT             NOT NULL,
    nqt_ngay_mua        DATE            NOT NULL,
    nqt_ngay_het_han    DATE            NOT NULL,
    nqt_so_buoi_con_lai INT             NOT NULL,
    nqt_gia_thuc_te     DECIMAL(15,0)   NOT NULL,
    nqt_ma_thanh_toan   INT             NULL,
    nqt_trang_thai      VARCHAR(20)     NOT NULL DEFAULT 'dang_dung' COMMENT '''dang_dung'',''het_buoi'',''het_han'',''huy''',
    nqt_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_dang_ky_pt),
    KEY idx_nqt_dkgoipt_hoivien (nqt_ma_hoi_vien),
    KEY idx_nqt_dkgoipt_hlv     (nqt_ma_hlv),
    CONSTRAINT fk_nqt_dkgoipt_hoivien FOREIGN KEY (nqt_ma_hoi_vien) REFERENCES NqtHoiVien (nqt_ma_hoi_vien),
    CONSTRAINT fk_nqt_dkgoipt_goipt   FOREIGN KEY (nqt_ma_goi_pt)   REFERENCES NqtGoiPT (nqt_ma_goi_pt),
    CONSTRAINT fk_nqt_dkgoipt_hlv     FOREIGN KEY (nqt_ma_hlv)      REFERENCES NqtHuanLuyenVien (nqt_ma_hlv)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtBuoiTapPT (
    nqt_ma_buoi_tap         INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_dang_ky_pt       INT             NOT NULL,
    nqt_ma_hoi_vien         INT             NOT NULL,
    nqt_ma_hlv              INT             NOT NULL,
    nqt_ma_chi_nhanh        INT             NOT NULL,
    nqt_ngay_tap            DATETIME        NOT NULL,
    nqt_thoi_luong          INT             NULL COMMENT 'Phút thực tế',
    nqt_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'cho_xac_nhan' COMMENT '''da_tap'',''vang_mat'',''huy'',''cho_xac_nhan''',
    nqt_noi_dung_buoi_tap   TEXT            NULL,
    nqt_nhan_xet_hlv        TEXT            NULL,
    nqt_danh_gia_hoi_vien   TINYINT         NULL COMMENT '1-5 sao',
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_buoi_tap),
    KEY idx_nqt_buoitap_dangky  (nqt_ma_dang_ky_pt),
    KEY idx_nqt_buoitap_hoivien (nqt_ma_hoi_vien),
    KEY idx_nqt_buoitap_ngaytap (nqt_ngay_tap),
    CONSTRAINT fk_nqt_buoitap_dangky   FOREIGN KEY (nqt_ma_dang_ky_pt) REFERENCES NqtDangKyGoiPT (nqt_ma_dang_ky_pt),
    CONSTRAINT fk_nqt_buoitap_hoivien  FOREIGN KEY (nqt_ma_hoi_vien)   REFERENCES NqtHoiVien (nqt_ma_hoi_vien),
    CONSTRAINT fk_nqt_buoitap_hlv      FOREIGN KEY (nqt_ma_hlv)        REFERENCES NqtHuanLuyenVien (nqt_ma_hlv),
    CONSTRAINT fk_nqt_buoitap_chinhanh FOREIGN KEY (nqt_ma_chi_nhanh)  REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 7: LỚP HỌC NHÓM
-- ============================================================

CREATE TABLE NqtLopHoc (
    nqt_ma_lop_hoc      INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_chi_nhanh    INT             NOT NULL,
    nqt_ten_lop         VARCHAR(100)    NOT NULL,
    nqt_loai_lop        VARCHAR(50)     NOT NULL COMMENT '''yoga'',''spinning'',''boxing'',''zumba'',''aerobic''',
    nqt_mo_ta           TEXT            NULL,
    nqt_hinh_anh        VARCHAR(500)    NULL,
    nqt_do_kho          VARCHAR(20)     NOT NULL DEFAULT 'co_ban' COMMENT '''co_ban'',''trung_binh'',''nang_cao''',
    nqt_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nqt_ma_lop_hoc),
    KEY idx_nqt_lophoc_chinhanh (nqt_ma_chi_nhanh),
    CONSTRAINT fk_nqt_lophoc_chinhanh FOREIGN KEY (nqt_ma_chi_nhanh) REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtLichLopHoc (
    nqt_ma_lich_lop         INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_lop_hoc          INT             NOT NULL,
    nqt_ma_hlv              INT             NOT NULL,
    nqt_thu_trong_tuan      TINYINT         NOT NULL COMMENT '1=T2 ... 7=CN',
    nqt_gio_bat_dau         TIME            NOT NULL,
    nqt_thoi_luong          INT             NOT NULL COMMENT 'Phút',
    nqt_suc_chua_toi_da     INT             NOT NULL DEFAULT 20,
    nqt_phong_tap           VARCHAR(50)     NULL,
    nqt_ngay_ap_dung_tu     DATE            NOT NULL,
    nqt_ngay_ap_dung_den    DATE            NULL,
    nqt_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nqt_ma_lich_lop),
    KEY idx_nqt_lichlop_lophoc (nqt_ma_lop_hoc),
    KEY idx_nqt_lichlop_hlv    (nqt_ma_hlv),
    CONSTRAINT fk_nqt_lichlop_lophoc FOREIGN KEY (nqt_ma_lop_hoc) REFERENCES NqtLopHoc (nqt_ma_lop_hoc) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_lichlop_hlv    FOREIGN KEY (nqt_ma_hlv)     REFERENCES NqtHuanLuyenVien (nqt_ma_hlv)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtDatChoLopHoc (
    nqt_ma_dat_cho      INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_lich_lop     INT             NOT NULL,
    nqt_ma_hoi_vien     INT             NOT NULL,
    nqt_ngay_tap        DATE            NOT NULL,
    nqt_trang_thai      VARCHAR(20)     NOT NULL DEFAULT 'dat_cho' COMMENT '''dat_cho'',''da_den'',''vang_mat'',''da_huy''',
    nqt_thoi_gian_dat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_thoi_gian_huy   DATETIME        NULL,
    nqt_ly_do_huy       VARCHAR(255)    NULL,
    PRIMARY KEY (nqt_ma_dat_cho),
    UNIQUE KEY uk_nqt_datcholop (nqt_ma_lich_lop, nqt_ma_hoi_vien, nqt_ngay_tap),
    KEY idx_nqt_datcholop_hoivien (nqt_ma_hoi_vien),
    KEY idx_nqt_datcholop_ngaytap (nqt_ngay_tap),
    CONSTRAINT fk_nqt_datcholop_lichlop FOREIGN KEY (nqt_ma_lich_lop) REFERENCES NqtLichLopHoc (nqt_ma_lich_lop),
    CONSTRAINT fk_nqt_datcholop_hoivien FOREIGN KEY (nqt_ma_hoi_vien) REFERENCES NqtHoiVien (nqt_ma_hoi_vien)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 8: DỊCH VỤ PHỤ (Sauna, Hồ bơi, Massage...)
-- ============================================================

CREATE TABLE NqtDichVuPhu (
    nqt_ma_dich_vu      INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_chi_nhanh    INT             NOT NULL,
    nqt_ten_dich_vu     VARCHAR(100)    NOT NULL COMMENT '''Sauna'',''Hồ bơi'',''Massage''',
    nqt_loai_dich_vu    VARCHAR(50)     NOT NULL,
    nqt_mo_ta           TEXT            NULL,
    nqt_gia_theo_luot   DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_thoi_luong_phut INT             NOT NULL DEFAULT 60,
    nqt_suc_chua        INT             NULL,
    nqt_la_mien_phi_goi TINYINT(1)      NOT NULL DEFAULT 0 COMMENT 'Miễn phí theo gói tập không',
    nqt_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nqt_ma_dich_vu),
    KEY idx_nqt_dichvuphu_chinhanh (nqt_ma_chi_nhanh),
    CONSTRAINT fk_nqt_dichvuphu_chinhanh FOREIGN KEY (nqt_ma_chi_nhanh) REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtDatDichVu (
    nqt_ma_dat_dich_vu      INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_dich_vu          INT             NOT NULL,
    nqt_ma_hoi_vien         INT             NOT NULL,
    nqt_thoi_gian_bat_dau   DATETIME        NOT NULL,
    nqt_thoi_gian_ket_thuc  DATETIME        NOT NULL,
    nqt_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'da_dat' COMMENT '''da_dat'',''da_dung'',''da_huy''',
    nqt_la_mien_phi         TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_ma_thanh_toan       INT             NULL,
    nqt_ghi_chu             VARCHAR(255)    NULL,
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_dat_dich_vu),
    KEY idx_nqt_datdichvu_dichvu  (nqt_ma_dich_vu),
    KEY idx_nqt_datdichvu_hoivien (nqt_ma_hoi_vien),
    KEY idx_nqt_datdichvu_thoigian(nqt_thoi_gian_bat_dau),
    CONSTRAINT fk_nqt_datdichvu_dichvu  FOREIGN KEY (nqt_ma_dich_vu)  REFERENCES NqtDichVuPhu (nqt_ma_dich_vu),
    CONSTRAINT fk_nqt_datdichvu_hoivien FOREIGN KEY (nqt_ma_hoi_vien) REFERENCES NqtHoiVien (nqt_ma_hoi_vien)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 9: DANH MỤC SẢN PHẨM (TPCN)
-- ============================================================

CREATE TABLE NqtDanhMucSanPham (
    nqt_ma_danh_muc         INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_danh_muc_cha     INT             NULL COMMENT 'Self-join - NULL = danh mục gốc',
    nqt_ten_danh_muc        VARCHAR(100)    NOT NULL,
    nqt_slug                VARCHAR(100)    NOT NULL,
    nqt_mo_ta               TEXT            NULL,
    nqt_hinh_anh            VARCHAR(500)    NULL,
    nqt_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    nqt_la_hien_thi_menu    TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nqt_ma_danh_muc),
    UNIQUE KEY uk_nqt_danhmuc_slug (nqt_slug),
    KEY idx_nqt_danhmuc_cha (nqt_ma_danh_muc_cha),
    CONSTRAINT fk_nqt_danhmuc_cha FOREIGN KEY (nqt_ma_danh_muc_cha) REFERENCES NqtDanhMucSanPham (nqt_ma_danh_muc) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed danh mục (cấp 1)
INSERT INTO NqtDanhMucSanPham (nqt_ten_danh_muc, nqt_slug, nqt_thu_tu_hien_thi) VALUES
('Whey Protein',            'whey-protein',         1),
('Tăng Sức Mạnh',           'tang-suc-manh',        2),
('Hỗ Trợ Giảm Mỡ',         'ho-tro-giam-mo',       3),
('Vitamin & Khoáng Chất',   'vitamin-khoang-chat',  4),
('Sức Khỏe Toàn Diện',      'suc-khoe-toan-dien',   5),
('Thảo Mộc',                'thao-moc',             6),
('Phụ Kiện Thể Thao',       'phu-kien-the-thao',    7);

-- Seed danh mục (cấp 2) - Whey Protein
INSERT INTO NqtDanhMucSanPham (nqt_ma_danh_muc_cha, nqt_ten_danh_muc, nqt_slug, nqt_thu_tu_hien_thi) VALUES
(1, 'Whey Isolate',         'whey-isolate',             1),
(1, 'Whey Hydrolyzed',      'whey-hydrolyzed',          2),
(1, 'Whey Blend',           'whey-blend',               3),
(1, 'Casein',               'casein',                   4),
(1, 'Vegan Protein',        'vegan-protein',            5),
(1, 'Protein Bar',          'protein-bar',              6),
(1, 'Mass Gainer',          'mass-gainer',              7),
-- Tăng Sức Mạnh
(2, 'Creatine',             'creatine',                 1),
(2, 'Pre-Workout',          'pre-workout',              2),
(2, 'BCAA',                 'bcaa',                     3),
(2, 'EAA',                  'eaa',                      4),
(2, 'Glutamine',            'glutamine',                5),
-- Giảm Mỡ
(3, 'Fat Burner',           'fat-burner',               1),
(3, 'L-Carnitine',          'l-carnitine',              2),
(3, 'CLA',                  'cla',                      3),
(3, 'Yohimbine',            'yohimbine',                4),
-- Vitamin
(4, 'Vitamin D3 + K2',      'vitamin-d3-k2',            1),
(4, 'Omega-3 Fish Oil',     'omega-3-fish-oil',         2),
(4, 'Multivitamin',         'multivitamin',             3),
(4, 'Zinc & ZMA',           'zinc-zma',                 4),
-- Sức Khỏe Toàn Diện
(5, 'Collagen',             'collagen',                 1),
(5, 'Probiotic',            'probiotic',                2),
(5, 'Glucosamine',          'glucosamine',              3),
(5, 'Melatonin',            'melatonin',                4),
-- Thảo Mộc
(6, 'Ashwagandha',          'ashwagandha',              1),
(6, 'Curcumin',             'curcumin',                 2),
(6, 'Ginkgo Biloba',        'ginkgo-biloba',            3),
-- Phụ Kiện
(7, 'Shaker & Bình Lắc',    'shaker-binh-lac',          1),
(7, 'Găng Tay Tập',         'gang-tay-tap',             2),
(7, 'Đai Lưng',             'dai-lung',                 3),
(7, 'Quần Áo Tập',          'quan-ao-tap',              4);

CREATE TABLE NqtMucTieuSucKhoe (
    nqt_ma_muc_tieu     INT             NOT NULL AUTO_INCREMENT,
    nqt_ten_muc_tieu    VARCHAR(50)     NOT NULL,
    nqt_slug            VARCHAR(50)     NOT NULL,
    nqt_bieu_tuong      VARCHAR(20)     NULL COMMENT 'Icon/emoji code',
    PRIMARY KEY (nqt_ma_muc_tieu),
    UNIQUE KEY uk_nqt_muctieu_slug (nqt_slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO NqtMucTieuSucKhoe (nqt_ten_muc_tieu, nqt_slug, nqt_bieu_tuong) VALUES
('Tăng Cơ',             'tang-co',          '💪'),
('Giảm Mỡ',             'giam-mo',          '🔥'),
('Tăng Cân',            'tang-can',         '⬆️'),
('Xương Khớp',          'xuong-khop',       '🦴'),
('Da Tóc Móng',         'da-toc-mong',      '✨'),
('Bảo Vệ Gan',          'bao-ve-gan',       '🫀'),
('Giấc Ngủ',            'giac-ngu',         '😴'),
('Tim Mạch',            'tim-mach',         '❤️'),
('Tiêu Hóa',            'tieu-hoa',         '🌿'),
('Chống Lão Hóa',       'chong-lao-hoa',    '⏳'),
('Giảm Căng Thẳng',     'giam-cang-thang',  '🧘');

CREATE TABLE NqtThuongHieu (
    nqt_ma_thuong_hieu      INT             NOT NULL AUTO_INCREMENT,
    nqt_ten_thuong_hieu     VARCHAR(100)    NOT NULL,
    nqt_slug                VARCHAR(100)    NOT NULL,
    nqt_nuoc_xuat_xu        VARCHAR(50)     NULL,
    nqt_logo                VARCHAR(500)    NULL,
    nqt_mo_ta               TEXT            NULL,
    nqt_website             VARCHAR(255)    NULL,
    nqt_la_noi_bat          TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_loai_tru_ma_giam    TINYINT(1)      NOT NULL DEFAULT 0 COMMENT 'Loại trừ khỏi coupon',
    nqt_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    PRIMARY KEY (nqt_ma_thuong_hieu),
    UNIQUE KEY uk_nqt_thuonghieu_slug (nqt_slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 10: SẢN PHẨM
-- ============================================================

CREATE TABLE NqtSanPham (
    nqt_ma_san_pham     INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_danh_muc     INT             NOT NULL,
    nqt_ma_thuong_hieu  INT             NOT NULL,
    nqt_ten_san_pham    VARCHAR(255)    NOT NULL,
    nqt_slug            VARCHAR(255)    NOT NULL,
    nqt_mo_ta_ngan      VARCHAR(500)    NULL,
    nqt_mo_ta_day_du    LONGTEXT        NULL,
    nqt_cach_dung       TEXT            NULL,
    nqt_nuoc_xuat_xu    VARCHAR(50)     NULL,
    nqt_doi_tuong_dung  VARCHAR(100)    NULL COMMENT '''nam'',''nu'',''nam_va_nu''',
    nqt_da_ban          INT             NOT NULL DEFAULT 0,
    nqt_luot_xem        INT             NOT NULL DEFAULT 0,
    nqt_thu_tu_hien_thi INT             NOT NULL DEFAULT 0,
    nqt_la_noi_bat      TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_la_ban_chay     TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_la_hang_moi     TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_seo_title       VARCHAR(255)    NULL,
    nqt_seo_mo_ta       VARCHAR(500)    NULL,
    nqt_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_san_pham),
    UNIQUE KEY uk_nqt_sanpham_slug (nqt_slug),
    KEY idx_nqt_sanpham_danhmuc   (nqt_ma_danh_muc),
    KEY idx_nqt_sanpham_thuonghieu(nqt_ma_thuong_hieu),
    KEY idx_nqt_sanpham_noibat    (nqt_la_noi_bat),
    KEY idx_nqt_sanpham_banchay   (nqt_la_ban_chay),
    CONSTRAINT fk_nqt_sanpham_danhmuc    FOREIGN KEY (nqt_ma_danh_muc)   REFERENCES NqtDanhMucSanPham (nqt_ma_danh_muc),
    CONSTRAINT fk_nqt_sanpham_thuonghieu FOREIGN KEY (nqt_ma_thuong_hieu) REFERENCES NqtThuongHieu (nqt_ma_thuong_hieu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtBienTheSanPham (
    nqt_ma_bien_the     INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_san_pham     INT             NOT NULL,
    nqt_sku             VARCHAR(100)    NOT NULL,
    nqt_ten_bien_the    VARCHAR(100)    NOT NULL COMMENT '"5Lbs - Chocolate"',
    nqt_trong_luong     VARCHAR(30)     NULL COMMENT '"5Lbs","2Lbs","500g"',
    nqt_trong_luong_gram INT            NULL COMMENT 'Quy đổi ra gram',
    nqt_so_luot_dung    INT             NULL COMMENT 'Số servings',
    nqt_huong_vi        VARCHAR(50)     NULL COMMENT '"Chocolate","Vanilla","Unflavored"',
    nqt_gia             DECIMAL(15,0)   NOT NULL,
    nqt_gia_so_sanh     DECIMAL(15,0)   NULL COMMENT 'Giá gốc để gạch ngang',
    nqt_hinh_anh        VARCHAR(500)    NULL,
    nqt_la_mac_dinh     TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_thu_tu          INT             NOT NULL DEFAULT 0,
    PRIMARY KEY (nqt_ma_bien_the),
    UNIQUE KEY uk_nqt_bienthe_sku (nqt_sku),
    KEY idx_nqt_bienthe_sanpham (nqt_ma_san_pham),
    CONSTRAINT fk_nqt_bienthe_sanpham FOREIGN KEY (nqt_ma_san_pham) REFERENCES NqtSanPham (nqt_ma_san_pham) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtHinhAnhSanPham (
    nqt_ma_hinh_anh     INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_san_pham     INT             NOT NULL,
    nqt_ma_bien_the     INT             NULL COMMENT 'NULL = ảnh chung của sản phẩm',
    nqt_duong_dan       VARCHAR(500)    NOT NULL,
    nqt_alt_text        VARCHAR(255)    NULL,
    nqt_thu_tu          INT             NOT NULL DEFAULT 0,
    nqt_la_anh_chinh    TINYINT(1)      NOT NULL DEFAULT 0,
    PRIMARY KEY (nqt_ma_hinh_anh),
    KEY idx_nqt_hinhanh_sanpham (nqt_ma_san_pham),
    CONSTRAINT fk_nqt_hinhanh_sanpham FOREIGN KEY (nqt_ma_san_pham) REFERENCES NqtSanPham (nqt_ma_san_pham) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_hinhanh_bienthe FOREIGN KEY (nqt_ma_bien_the) REFERENCES NqtBienTheSanPham (nqt_ma_bien_the) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtThanhPhanDinhDuong (
    nqt_ma_dinh_duong   INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_bien_the     INT             NOT NULL,
    nqt_khau_phan       INT             NULL COMMENT 'gram/serving',
    nqt_calo            INT             NULL,
    nqt_protein         DECIMAL(6,2)    NULL COMMENT 'gram',
    nqt_tinh_bot        DECIMAL(6,2)    NULL,
    nqt_chat_beo        DECIMAL(6,2)    NULL,
    nqt_duong           DECIMAL(6,2)    NULL,
    nqt_chat_xo         DECIMAL(6,2)    NULL,
    nqt_bcaa            DECIMAL(6,2)    NULL,
    nqt_glutamine       DECIMAL(6,2)    NULL,
    nqt_creatine        DECIMAL(6,2)    NULL,
    nqt_caffeine        DECIMAL(6,2)    NULL COMMENT 'mg',
    nqt_thanh_phan_khac JSON            NULL COMMENT 'Các vi chất khác',
    PRIMARY KEY (nqt_ma_dinh_duong),
    UNIQUE KEY uk_nqt_dinhduong_bienthe (nqt_ma_bien_the),
    CONSTRAINT fk_nqt_dinhduong_bienthe FOREIGN KEY (nqt_ma_bien_the) REFERENCES NqtBienTheSanPham (nqt_ma_bien_the) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtChungNhanSanPham (
    nqt_ma_chung_nhan   INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_san_pham     INT             NOT NULL,
    nqt_loai            VARCHAR(30)     NOT NULL COMMENT '''GMP'',''Halal'',''Kosher'',''FDA'',''DĐVN''',
    nqt_so_chung_nhan   VARCHAR(100)    NULL,
    nqt_ngay_cap        DATE            NULL,
    nqt_hinh_anh        VARCHAR(500)    NULL,
    PRIMARY KEY (nqt_ma_chung_nhan),
    KEY idx_nqt_chungnhan_sanpham (nqt_ma_san_pham),
    CONSTRAINT fk_nqt_chungnhan_sanpham FOREIGN KEY (nqt_ma_san_pham) REFERENCES NqtSanPham (nqt_ma_san_pham) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtSanPhamMucTieu (
    nqt_ma_san_pham     INT             NOT NULL,
    nqt_ma_muc_tieu     INT             NOT NULL,
    PRIMARY KEY (nqt_ma_san_pham, nqt_ma_muc_tieu),
    CONSTRAINT fk_nqt_spmuctieu_sanpham FOREIGN KEY (nqt_ma_san_pham) REFERENCES NqtSanPham (nqt_ma_san_pham) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_spmuctieu_muctieu FOREIGN KEY (nqt_ma_muc_tieu) REFERENCES NqtMucTieuSucKhoe (nqt_ma_muc_tieu) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
