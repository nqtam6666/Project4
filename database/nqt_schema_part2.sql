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

CREATE TABLE NxvHuanLuyenVien (
    nxv_ma_hlv              INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_nhan_vien        INT             NOT NULL,
    nxv_ma_chi_nhanh        INT             NOT NULL,
    nxv_chuyen_mon          JSON            NULL COMMENT '["tang_co","giam_mo","yoga","boxing"]',
    nxv_cap_chung_chi       VARCHAR(50)     NULL COMMENT '''ACE'',''NASM'',''REPs'',''ISSA''',
    nxv_so_nam_kinh_nghiem  INT             NOT NULL DEFAULT 0,
    nxv_tieu_su             TEXT            NULL,
    nxv_gia_theo_buoi       DECIMAL(15,0)   NULL,
    nxv_hinh_anh            VARCHAR(500)    NULL,
    nxv_thu_hang            TINYINT         NOT NULL DEFAULT 5 COMMENT '1-5 sao',
    nxv_so_hoi_vien_hien_tai INT            NOT NULL DEFAULT 0,
    nxv_toi_da_hoi_vien     INT             NOT NULL DEFAULT 20,
    nxv_la_hien_thi_web     TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nxv_ma_hlv),
    KEY idx_nxv_hlv_nhanvien  (nxv_ma_nhan_vien),
    KEY idx_nxv_hlv_chinhanh  (nxv_ma_chi_nhanh),
    CONSTRAINT fk_nxv_hlv_nhanvien FOREIGN KEY (nxv_ma_nhan_vien) REFERENCES NqtNhanVien (nxv_ma_nhan_vien),
    CONSTRAINT fk_nxv_hlv_chinhanh FOREIGN KEY (nxv_ma_chi_nhanh) REFERENCES NqtChiNhanh (nxv_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvGoiPT (
    nxv_ma_goi_pt       INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_hlv          INT             NOT NULL,
    nxv_ten_goi         VARCHAR(100)    NOT NULL,
    nxv_so_buoi         INT             NOT NULL COMMENT '10, 20, 30 buổi',
    nxv_thoi_luong_buoi INT             NOT NULL COMMENT 'Phút/buổi',
    nxv_gia             DECIMAL(15,0)   NOT NULL,
    nxv_gia_khuyen_mai  DECIMAL(15,0)   NULL,
    nxv_hieu_luc_ngay   INT             NOT NULL DEFAULT 90 COMMENT 'Hết hạn sau X ngày từ ngày mua',
    nxv_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    nxv_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nxv_ma_goi_pt),
    KEY idx_nxv_goipt_hlv (nxv_ma_hlv),
    CONSTRAINT fk_nxv_goipt_hlv FOREIGN KEY (nxv_ma_hlv) REFERENCES NxvHuanLuyenVien (nxv_ma_hlv)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvDangKyGoiPT (
    nxv_ma_dang_ky_pt   INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_hoi_vien     INT             NOT NULL,
    nxv_ma_goi_pt       INT             NOT NULL,
    nxv_ma_hlv          INT             NOT NULL,
    nxv_ngay_mua        DATE            NOT NULL,
    nxv_ngay_het_han    DATE            NOT NULL,
    nxv_so_buoi_con_lai INT             NOT NULL,
    nxv_gia_thuc_te     DECIMAL(15,0)   NOT NULL,
    nxv_ma_thanh_toan   INT             NULL,
    nxv_trang_thai      VARCHAR(20)     NOT NULL DEFAULT 'dang_dung' COMMENT '''dang_dung'',''het_buoi'',''het_han'',''huy''',
    nxv_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nxv_ma_dang_ky_pt),
    KEY idx_nxv_dkgoipt_hoivien (nxv_ma_hoi_vien),
    KEY idx_nxv_dkgoipt_hlv     (nxv_ma_hlv),
    CONSTRAINT fk_nxv_dkgoipt_hoivien FOREIGN KEY (nxv_ma_hoi_vien) REFERENCES NqtHoiVien (nxv_ma_hoi_vien),
    CONSTRAINT fk_nxv_dkgoipt_goipt   FOREIGN KEY (nxv_ma_goi_pt)   REFERENCES NxvGoiPT (nxv_ma_goi_pt),
    CONSTRAINT fk_nxv_dkgoipt_hlv     FOREIGN KEY (nxv_ma_hlv)      REFERENCES NxvHuanLuyenVien (nxv_ma_hlv)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvBuoiTapPT (
    nxv_ma_buoi_tap         INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_dang_ky_pt       INT             NOT NULL,
    nxv_ma_hoi_vien         INT             NOT NULL,
    nxv_ma_hlv              INT             NOT NULL,
    nxv_ma_chi_nhanh        INT             NOT NULL,
    nxv_ngay_tap            DATETIME        NOT NULL,
    nxv_thoi_luong          INT             NULL COMMENT 'Phút thực tế',
    nxv_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'cho_xac_nhan' COMMENT '''da_tap'',''vang_mat'',''huy'',''cho_xac_nhan''',
    nxv_noi_dung_buoi_tap   TEXT            NULL,
    nxv_nhan_xet_hlv        TEXT            NULL,
    nxv_danh_gia_hoi_vien   TINYINT         NULL COMMENT '1-5 sao',
    nxv_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nxv_ma_buoi_tap),
    KEY idx_nxv_buoitap_dangky  (nxv_ma_dang_ky_pt),
    KEY idx_nxv_buoitap_hoivien (nxv_ma_hoi_vien),
    KEY idx_nxv_buoitap_ngaytap (nxv_ngay_tap),
    CONSTRAINT fk_nxv_buoitap_dangky   FOREIGN KEY (nxv_ma_dang_ky_pt) REFERENCES NxvDangKyGoiPT (nxv_ma_dang_ky_pt),
    CONSTRAINT fk_nxv_buoitap_hoivien  FOREIGN KEY (nxv_ma_hoi_vien)   REFERENCES NqtHoiVien (nxv_ma_hoi_vien),
    CONSTRAINT fk_nxv_buoitap_hlv      FOREIGN KEY (nxv_ma_hlv)        REFERENCES NxvHuanLuyenVien (nxv_ma_hlv),
    CONSTRAINT fk_nxv_buoitap_chinhanh FOREIGN KEY (nxv_ma_chi_nhanh)  REFERENCES NqtChiNhanh (nxv_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 7: LỚP HỌC NHÓM
-- ============================================================

CREATE TABLE NxvLopHoc (
    nxv_ma_lop_hoc      INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_chi_nhanh    INT             NOT NULL,
    nxv_ten_lop         VARCHAR(100)    NOT NULL,
    nxv_loai_lop        VARCHAR(50)     NOT NULL COMMENT '''yoga'',''spinning'',''boxing'',''zumba'',''aerobic''',
    nxv_mo_ta           TEXT            NULL,
    nxv_hinh_anh        VARCHAR(500)    NULL,
    nxv_do_kho          VARCHAR(20)     NOT NULL DEFAULT 'co_ban' COMMENT '''co_ban'',''trung_binh'',''nang_cao''',
    nxv_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nxv_ma_lop_hoc),
    KEY idx_nxv_lophoc_chinhanh (nxv_ma_chi_nhanh),
    CONSTRAINT fk_nxv_lophoc_chinhanh FOREIGN KEY (nxv_ma_chi_nhanh) REFERENCES NqtChiNhanh (nxv_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvLichLopHoc (
    nxv_ma_lich_lop         INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_lop_hoc          INT             NOT NULL,
    nxv_ma_hlv              INT             NOT NULL,
    nxv_thu_trong_tuan      TINYINT         NOT NULL COMMENT '1=T2 ... 7=CN',
    nxv_gio_bat_dau         TIME            NOT NULL,
    nxv_thoi_luong          INT             NOT NULL COMMENT 'Phút',
    nxv_suc_chua_toi_da     INT             NOT NULL DEFAULT 20,
    nxv_phong_tap           VARCHAR(50)     NULL,
    nxv_ngay_ap_dung_tu     DATE            NOT NULL,
    nxv_ngay_ap_dung_den    DATE            NULL,
    nxv_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nxv_ma_lich_lop),
    KEY idx_nxv_lichlop_lophoc (nxv_ma_lop_hoc),
    KEY idx_nxv_lichlop_hlv    (nxv_ma_hlv),
    CONSTRAINT fk_nxv_lichlop_lophoc FOREIGN KEY (nxv_ma_lop_hoc) REFERENCES NxvLopHoc (nxv_ma_lop_hoc) ON DELETE CASCADE,
    CONSTRAINT fk_nxv_lichlop_hlv    FOREIGN KEY (nxv_ma_hlv)     REFERENCES NxvHuanLuyenVien (nxv_ma_hlv)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvDatChoLopHoc (
    nxv_ma_dat_cho      INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_lich_lop     INT             NOT NULL,
    nxv_ma_hoi_vien     INT             NOT NULL,
    nxv_ngay_tap        DATE            NOT NULL,
    nxv_trang_thai      VARCHAR(20)     NOT NULL DEFAULT 'dat_cho' COMMENT '''dat_cho'',''da_den'',''vang_mat'',''da_huy''',
    nxv_thoi_gian_dat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nxv_thoi_gian_huy   DATETIME        NULL,
    nxv_ly_do_huy       VARCHAR(255)    NULL,
    PRIMARY KEY (nxv_ma_dat_cho),
    UNIQUE KEY uk_nxv_datcholop (nxv_ma_lich_lop, nxv_ma_hoi_vien, nxv_ngay_tap),
    KEY idx_nxv_datcholop_hoivien (nxv_ma_hoi_vien),
    KEY idx_nxv_datcholop_ngaytap (nxv_ngay_tap),
    CONSTRAINT fk_nxv_datcholop_lichlop FOREIGN KEY (nxv_ma_lich_lop) REFERENCES NxvLichLopHoc (nxv_ma_lich_lop),
    CONSTRAINT fk_nxv_datcholop_hoivien FOREIGN KEY (nxv_ma_hoi_vien) REFERENCES NqtHoiVien (nxv_ma_hoi_vien)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 8: DỊCH VỤ PHỤ (Sauna, Hồ bơi, Massage...)
-- ============================================================

CREATE TABLE NxvDichVuPhu (
    nxv_ma_dich_vu      INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_chi_nhanh    INT             NOT NULL,
    nxv_ten_dich_vu     VARCHAR(100)    NOT NULL COMMENT '''Sauna'',''Hồ bơi'',''Massage''',
    nxv_loai_dich_vu    VARCHAR(50)     NOT NULL,
    nxv_mo_ta           TEXT            NULL,
    nxv_gia_theo_luot   DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nxv_thoi_luong_phut INT             NOT NULL DEFAULT 60,
    nxv_suc_chua        INT             NULL,
    nxv_la_mien_phi_goi TINYINT(1)      NOT NULL DEFAULT 0 COMMENT 'Miễn phí theo gói tập không',
    nxv_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nxv_ma_dich_vu),
    KEY idx_nxv_dichvuphu_chinhanh (nxv_ma_chi_nhanh),
    CONSTRAINT fk_nxv_dichvuphu_chinhanh FOREIGN KEY (nxv_ma_chi_nhanh) REFERENCES NqtChiNhanh (nxv_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvDatDichVu (
    nxv_ma_dat_dich_vu      INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_dich_vu          INT             NOT NULL,
    nxv_ma_hoi_vien         INT             NOT NULL,
    nxv_thoi_gian_bat_dau   DATETIME        NOT NULL,
    nxv_thoi_gian_ket_thuc  DATETIME        NOT NULL,
    nxv_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'da_dat' COMMENT '''da_dat'',''da_dung'',''da_huy''',
    nxv_la_mien_phi         TINYINT(1)      NOT NULL DEFAULT 0,
    nxv_ma_thanh_toan       INT             NULL,
    nxv_ghi_chu             VARCHAR(255)    NULL,
    nxv_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nxv_ma_dat_dich_vu),
    KEY idx_nxv_datdichvu_dichvu  (nxv_ma_dich_vu),
    KEY idx_nxv_datdichvu_hoivien (nxv_ma_hoi_vien),
    KEY idx_nxv_datdichvu_thoigian(nxv_thoi_gian_bat_dau),
    CONSTRAINT fk_nxv_datdichvu_dichvu  FOREIGN KEY (nxv_ma_dich_vu)  REFERENCES NxvDichVuPhu (nxv_ma_dich_vu),
    CONSTRAINT fk_nxv_datdichvu_hoivien FOREIGN KEY (nxv_ma_hoi_vien) REFERENCES NqtHoiVien (nxv_ma_hoi_vien)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 9: DANH MỤC SẢN PHẨM (TPCN)
-- ============================================================

CREATE TABLE NxvDanhMucSanPham (
    nxv_ma_danh_muc         INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_danh_muc_cha     INT             NULL COMMENT 'Self-join - NULL = danh mục gốc',
    nxv_ten_danh_muc        VARCHAR(100)    NOT NULL,
    nxv_slug                VARCHAR(100)    NOT NULL,
    nxv_mo_ta               TEXT            NULL,
    nxv_hinh_anh            VARCHAR(500)    NULL,
    nxv_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    nxv_la_hien_thi_menu    TINYINT(1)      NOT NULL DEFAULT 1,
    nxv_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nxv_ma_danh_muc),
    UNIQUE KEY uk_nxv_danhmuc_slug (nxv_slug),
    KEY idx_nxv_danhmuc_cha (nxv_ma_danh_muc_cha),
    CONSTRAINT fk_nxv_danhmuc_cha FOREIGN KEY (nxv_ma_danh_muc_cha) REFERENCES NxvDanhMucSanPham (nxv_ma_danh_muc) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed danh mục (cấp 1)
INSERT INTO NxvDanhMucSanPham (nxv_ten_danh_muc, nxv_slug, nxv_thu_tu_hien_thi) VALUES
('Whey Protein',            'whey-protein',         1),
('Tăng Sức Mạnh',           'tang-suc-manh',        2),
('Hỗ Trợ Giảm Mỡ',         'ho-tro-giam-mo',       3),
('Vitamin & Khoáng Chất',   'vitamin-khoang-chat',  4),
('Sức Khỏe Toàn Diện',      'suc-khoe-toan-dien',   5),
('Thảo Mộc',                'thao-moc',             6),
('Phụ Kiện Thể Thao',       'phu-kien-the-thao',    7);

-- Seed danh mục (cấp 2) - Whey Protein
INSERT INTO NxvDanhMucSanPham (nxv_ma_danh_muc_cha, nxv_ten_danh_muc, nxv_slug, nxv_thu_tu_hien_thi) VALUES
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

CREATE TABLE NxvMucTieuSucKhoe (
    nxv_ma_muc_tieu     INT             NOT NULL AUTO_INCREMENT,
    nxv_ten_muc_tieu    VARCHAR(50)     NOT NULL,
    nxv_slug            VARCHAR(50)     NOT NULL,
    nxv_bieu_tuong      VARCHAR(20)     NULL COMMENT 'Icon/emoji code',
    PRIMARY KEY (nxv_ma_muc_tieu),
    UNIQUE KEY uk_nxv_muctieu_slug (nxv_slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO NxvMucTieuSucKhoe (nxv_ten_muc_tieu, nxv_slug, nxv_bieu_tuong) VALUES
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

CREATE TABLE NxvThuongHieu (
    nxv_ma_thuong_hieu      INT             NOT NULL AUTO_INCREMENT,
    nxv_ten_thuong_hieu     VARCHAR(100)    NOT NULL,
    nxv_slug                VARCHAR(100)    NOT NULL,
    nxv_nuoc_xuat_xu        VARCHAR(50)     NULL,
    nxv_logo                VARCHAR(500)    NULL,
    nxv_mo_ta               TEXT            NULL,
    nxv_website             VARCHAR(255)    NULL,
    nxv_la_noi_bat          TINYINT(1)      NOT NULL DEFAULT 0,
    nxv_loai_tru_ma_giam    TINYINT(1)      NOT NULL DEFAULT 0 COMMENT 'Loại trừ khỏi coupon',
    nxv_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    nxv_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    PRIMARY KEY (nxv_ma_thuong_hieu),
    UNIQUE KEY uk_nxv_thuonghieu_slug (nxv_slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 10: SẢN PHẨM
-- ============================================================

CREATE TABLE NxvSanPham (
    nxv_ma_san_pham     INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_danh_muc     INT             NOT NULL,
    nxv_ma_thuong_hieu  INT             NOT NULL,
    nxv_ten_san_pham    VARCHAR(255)    NOT NULL,
    nxv_slug            VARCHAR(255)    NOT NULL,
    nxv_mo_ta_ngan      VARCHAR(500)    NULL,
    nxv_mo_ta_day_du    LONGTEXT        NULL,
    nxv_cach_dung       TEXT            NULL,
    nxv_nuoc_xuat_xu    VARCHAR(50)     NULL,
    nxv_doi_tuong_dung  VARCHAR(100)    NULL COMMENT '''nam'',''nu'',''nam_va_nu''',
    nxv_da_ban          INT             NOT NULL DEFAULT 0,
    nxv_luot_xem        INT             NOT NULL DEFAULT 0,
    nxv_thu_tu_hien_thi INT             NOT NULL DEFAULT 0,
    nxv_la_noi_bat      TINYINT(1)      NOT NULL DEFAULT 0,
    nxv_la_ban_chay     TINYINT(1)      NOT NULL DEFAULT 0,
    nxv_la_hang_moi     TINYINT(1)      NOT NULL DEFAULT 0,
    nxv_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    nxv_seo_title       VARCHAR(255)    NULL,
    nxv_seo_mo_ta       VARCHAR(500)    NULL,
    nxv_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nxv_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (nxv_ma_san_pham),
    UNIQUE KEY uk_nxv_sanpham_slug (nxv_slug),
    KEY idx_nxv_sanpham_danhmuc   (nxv_ma_danh_muc),
    KEY idx_nxv_sanpham_thuonghieu(nxv_ma_thuong_hieu),
    KEY idx_nxv_sanpham_noibat    (nxv_la_noi_bat),
    KEY idx_nxv_sanpham_banchay   (nxv_la_ban_chay),
    CONSTRAINT fk_nxv_sanpham_danhmuc    FOREIGN KEY (nxv_ma_danh_muc)   REFERENCES NxvDanhMucSanPham (nxv_ma_danh_muc),
    CONSTRAINT fk_nxv_sanpham_thuonghieu FOREIGN KEY (nxv_ma_thuong_hieu) REFERENCES NxvThuongHieu (nxv_ma_thuong_hieu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvBienTheSanPham (
    nxv_ma_bien_the     INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_san_pham     INT             NOT NULL,
    nxv_sku             VARCHAR(100)    NOT NULL,
    nxv_ten_bien_the    VARCHAR(100)    NOT NULL COMMENT '"5Lbs - Chocolate"',
    nxv_trong_luong     VARCHAR(30)     NULL COMMENT '"5Lbs","2Lbs","500g"',
    nxv_trong_luong_gram INT            NULL COMMENT 'Quy đổi ra gram',
    nxv_so_luot_dung    INT             NULL COMMENT 'Số servings',
    nxv_huong_vi        VARCHAR(50)     NULL COMMENT '"Chocolate","Vanilla","Unflavored"',
    nxv_gia             DECIMAL(15,0)   NOT NULL,
    nxv_gia_so_sanh     DECIMAL(15,0)   NULL COMMENT 'Giá gốc để gạch ngang',
    nxv_hinh_anh        VARCHAR(500)    NULL,
    nxv_la_mac_dinh     TINYINT(1)      NOT NULL DEFAULT 0,
    nxv_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    nxv_thu_tu          INT             NOT NULL DEFAULT 0,
    PRIMARY KEY (nxv_ma_bien_the),
    UNIQUE KEY uk_nxv_bienthe_sku (nxv_sku),
    KEY idx_nxv_bienthe_sanpham (nxv_ma_san_pham),
    CONSTRAINT fk_nxv_bienthe_sanpham FOREIGN KEY (nxv_ma_san_pham) REFERENCES NxvSanPham (nxv_ma_san_pham) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvHinhAnhSanPham (
    nxv_ma_hinh_anh     INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_san_pham     INT             NOT NULL,
    nxv_ma_bien_the     INT             NULL COMMENT 'NULL = ảnh chung của sản phẩm',
    nxv_duong_dan       VARCHAR(500)    NOT NULL,
    nxv_alt_text        VARCHAR(255)    NULL,
    nxv_thu_tu          INT             NOT NULL DEFAULT 0,
    nxv_la_anh_chinh    TINYINT(1)      NOT NULL DEFAULT 0,
    PRIMARY KEY (nxv_ma_hinh_anh),
    KEY idx_nxv_hinhanh_sanpham (nxv_ma_san_pham),
    CONSTRAINT fk_nxv_hinhanh_sanpham FOREIGN KEY (nxv_ma_san_pham) REFERENCES NxvSanPham (nxv_ma_san_pham) ON DELETE CASCADE,
    CONSTRAINT fk_nxv_hinhanh_bienthe FOREIGN KEY (nxv_ma_bien_the) REFERENCES NxvBienTheSanPham (nxv_ma_bien_the) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvThanhPhanDinhDuong (
    nxv_ma_dinh_duong   INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_bien_the     INT             NOT NULL,
    nxv_khau_phan       INT             NULL COMMENT 'gram/serving',
    nxv_calo            INT             NULL,
    nxv_protein         DECIMAL(6,2)    NULL COMMENT 'gram',
    nxv_tinh_bot        DECIMAL(6,2)    NULL,
    nxv_chat_beo        DECIMAL(6,2)    NULL,
    nxv_duong           DECIMAL(6,2)    NULL,
    nxv_chat_xo         DECIMAL(6,2)    NULL,
    nxv_bcaa            DECIMAL(6,2)    NULL,
    nxv_glutamine       DECIMAL(6,2)    NULL,
    nxv_creatine        DECIMAL(6,2)    NULL,
    nxv_caffeine        DECIMAL(6,2)    NULL COMMENT 'mg',
    nxv_thanh_phan_khac JSON            NULL COMMENT 'Các vi chất khác',
    PRIMARY KEY (nxv_ma_dinh_duong),
    UNIQUE KEY uk_nxv_dinhduong_bienthe (nxv_ma_bien_the),
    CONSTRAINT fk_nxv_dinhduong_bienthe FOREIGN KEY (nxv_ma_bien_the) REFERENCES NxvBienTheSanPham (nxv_ma_bien_the) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvChungNhanSanPham (
    nxv_ma_chung_nhan   INT             NOT NULL AUTO_INCREMENT,
    nxv_ma_san_pham     INT             NOT NULL,
    nxv_loai            VARCHAR(30)     NOT NULL COMMENT '''GMP'',''Halal'',''Kosher'',''FDA'',''DĐVN''',
    nxv_so_chung_nhan   VARCHAR(100)    NULL,
    nxv_ngay_cap        DATE            NULL,
    nxv_hinh_anh        VARCHAR(500)    NULL,
    PRIMARY KEY (nxv_ma_chung_nhan),
    KEY idx_nxv_chungnhan_sanpham (nxv_ma_san_pham),
    CONSTRAINT fk_nxv_chungnhan_sanpham FOREIGN KEY (nxv_ma_san_pham) REFERENCES NxvSanPham (nxv_ma_san_pham) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NxvSanPhamMucTieu (
    nxv_ma_san_pham     INT             NOT NULL,
    nxv_ma_muc_tieu     INT             NOT NULL,
    PRIMARY KEY (nxv_ma_san_pham, nxv_ma_muc_tieu),
    CONSTRAINT fk_nxv_spmuctieu_sanpham FOREIGN KEY (nxv_ma_san_pham) REFERENCES NxvSanPham (nxv_ma_san_pham) ON DELETE CASCADE,
    CONSTRAINT fk_nxv_spmuctieu_muctieu FOREIGN KEY (nxv_ma_muc_tieu) REFERENCES NxvMucTieuSucKhoe (nxv_ma_muc_tieu) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
