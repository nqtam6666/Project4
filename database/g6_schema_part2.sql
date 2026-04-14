-- ============================================================
-- G6 GYM MANAGEMENT + SUPPLEMENT STORE
-- MySQL Schema - Part 2: Group 6-10
-- GROUP 6: HUẤN LUYỆN VIÊN | GROUP 7: LỚP HỌC NHÓM
-- GROUP 8: DỊCH VỤ PHỤ | GROUP 9: DANH MỤC SP | GROUP 10: SẢN PHẨM
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- GROUP 6: HUẤN LUYỆN VIÊN (PT)
-- ============================================================

CREATE TABLE G6HuanLuyenVien (
    g6_ma_hlv              INT             NOT NULL AUTO_INCREMENT,
    g6_ma_nhan_vien        INT             NOT NULL,
    g6_ma_chi_nhanh        INT             NOT NULL,
    g6_chuyen_mon          JSON            NULL COMMENT '["tang_co","giam_mo","yoga","boxing"]',
    g6_cap_chung_chi       VARCHAR(50)     NULL COMMENT '''ACE'',''NASM'',''REPs'',''ISSA''',
    g6_so_nam_kinh_nghiem  INT             NOT NULL DEFAULT 0,
    g6_tieu_su             TEXT            NULL,
    g6_gia_theo_buoi       DECIMAL(15,0)   NULL,
    g6_hinh_anh            VARCHAR(500)    NULL,
    g6_thu_hang            TINYINT         NOT NULL DEFAULT 5 COMMENT '1-5 sao',
    g6_so_hoi_vien_hien_tai INT            NOT NULL DEFAULT 0,
    g6_toi_da_hoi_vien     INT             NOT NULL DEFAULT 20,
    g6_la_hien_thi_web     TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (g6_ma_hlv),
    KEY idx_g6_hlv_nhanvien  (g6_ma_nhan_vien),
    KEY idx_g6_hlv_chinhanh  (g6_ma_chi_nhanh),
    CONSTRAINT fk_g6_hlv_nhanvien FOREIGN KEY (g6_ma_nhan_vien) REFERENCES G6NhanVien (g6_ma_nhan_vien),
    CONSTRAINT fk_g6_hlv_chinhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6GoiPT (
    g6_ma_goi_pt       INT             NOT NULL AUTO_INCREMENT,
    g6_ma_hlv          INT             NOT NULL,
    g6_ten_goi         VARCHAR(100)    NOT NULL,
    g6_so_buoi         INT             NOT NULL COMMENT '10, 20, 30 buổi',
    g6_thoi_luong_buoi INT             NOT NULL COMMENT 'Phút/buổi',
    g6_gia             DECIMAL(15,0)   NOT NULL,
    g6_gia_khuyen_mai  DECIMAL(15,0)   NULL,
    g6_hieu_luc_ngay   INT             NOT NULL DEFAULT 90 COMMENT 'Hết hạn sau X ngày từ ngày mua',
    g6_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    g6_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_goi_pt),
    KEY idx_g6_goipt_hlv (g6_ma_hlv),
    CONSTRAINT fk_g6_goipt_hlv FOREIGN KEY (g6_ma_hlv) REFERENCES G6HuanLuyenVien (g6_ma_hlv)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6DangKyGoiPT (
    g6_ma_dang_ky_pt   INT             NOT NULL AUTO_INCREMENT,
    g6_ma_hoi_vien     INT             NOT NULL,
    g6_ma_goi_pt       INT             NOT NULL,
    g6_ma_hlv          INT             NOT NULL,
    g6_ngay_mua        DATE            NOT NULL,
    g6_ngay_het_han    DATE            NOT NULL,
    g6_so_buoi_con_lai INT             NOT NULL,
    g6_gia_thuc_te     DECIMAL(15,0)   NOT NULL,
    g6_ma_thanh_toan   INT             NULL,
    g6_trang_thai      VARCHAR(20)     NOT NULL DEFAULT 'dang_dung' COMMENT '''dang_dung'',''het_buoi'',''het_han'',''huy''',
    g6_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_dang_ky_pt),
    KEY idx_g6_dkgoipt_hoivien (g6_ma_hoi_vien),
    KEY idx_g6_dkgoipt_hlv     (g6_ma_hlv),
    CONSTRAINT fk_g6_dkgoipt_hoivien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien),
    CONSTRAINT fk_g6_dkgoipt_goipt   FOREIGN KEY (g6_ma_goi_pt)   REFERENCES G6GoiPT (g6_ma_goi_pt),
    CONSTRAINT fk_g6_dkgoipt_hlv     FOREIGN KEY (g6_ma_hlv)      REFERENCES G6HuanLuyenVien (g6_ma_hlv)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6BuoiTapPT (
    g6_ma_buoi_tap         INT             NOT NULL AUTO_INCREMENT,
    g6_ma_dang_ky_pt       INT             NOT NULL,
    g6_ma_hoi_vien         INT             NOT NULL,
    g6_ma_hlv              INT             NOT NULL,
    g6_ma_chi_nhanh        INT             NOT NULL,
    g6_ngay_tap            DATETIME        NOT NULL,
    g6_thoi_luong          INT             NULL COMMENT 'Phút thực tế',
    g6_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'cho_xac_nhan' COMMENT '''da_tap'',''vang_mat'',''huy'',''cho_xac_nhan''',
    g6_noi_dung_buoi_tap   TEXT            NULL,
    g6_nhan_xet_hlv        TEXT            NULL,
    g6_danh_gia_hoi_vien   TINYINT         NULL COMMENT '1-5 sao',
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_buoi_tap),
    KEY idx_g6_buoitap_dangky  (g6_ma_dang_ky_pt),
    KEY idx_g6_buoitap_hoivien (g6_ma_hoi_vien),
    KEY idx_g6_buoitap_ngaytap (g6_ngay_tap),
    CONSTRAINT fk_g6_buoitap_dangky   FOREIGN KEY (g6_ma_dang_ky_pt) REFERENCES G6DangKyGoiPT (g6_ma_dang_ky_pt),
    CONSTRAINT fk_g6_buoitap_hoivien  FOREIGN KEY (g6_ma_hoi_vien)   REFERENCES G6HoiVien (g6_ma_hoi_vien),
    CONSTRAINT fk_g6_buoitap_hlv      FOREIGN KEY (g6_ma_hlv)        REFERENCES G6HuanLuyenVien (g6_ma_hlv),
    CONSTRAINT fk_g6_buoitap_chinhanh FOREIGN KEY (g6_ma_chi_nhanh)  REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 7: LỚP HỌC NHÓM
-- ============================================================

CREATE TABLE G6LopHoc (
    g6_ma_lop_hoc      INT             NOT NULL AUTO_INCREMENT,
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_ten_lop         VARCHAR(100)    NOT NULL,
    g6_loai_lop        VARCHAR(50)     NOT NULL COMMENT '''yoga'',''spinning'',''boxing'',''zumba'',''aerobic''',
    g6_mo_ta           TEXT            NULL,
    g6_hinh_anh        VARCHAR(500)    NULL,
    g6_do_kho          VARCHAR(20)     NOT NULL DEFAULT 'co_ban' COMMENT '''co_ban'',''trung_binh'',''nang_cao''',
    g6_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (g6_ma_lop_hoc),
    KEY idx_g6_lophoc_chinhanh (g6_ma_chi_nhanh),
    CONSTRAINT fk_g6_lophoc_chinhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6LichLopHoc (
    g6_ma_lich_lop         INT             NOT NULL AUTO_INCREMENT,
    g6_ma_lop_hoc          INT             NOT NULL,
    g6_ma_hlv              INT             NOT NULL,
    g6_thu_trong_tuan      TINYINT         NOT NULL COMMENT '1=T2 ... 7=CN',
    g6_gio_bat_dau         TIME            NOT NULL,
    g6_thoi_luong          INT             NOT NULL COMMENT 'Phút',
    g6_suc_chua_toi_da     INT             NOT NULL DEFAULT 20,
    g6_phong_tap           VARCHAR(50)     NULL,
    g6_ngay_ap_dung_tu     DATE            NOT NULL,
    g6_ngay_ap_dung_den    DATE            NULL,
    g6_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (g6_ma_lich_lop),
    KEY idx_g6_lichlop_lophoc (g6_ma_lop_hoc),
    KEY idx_g6_lichlop_hlv    (g6_ma_hlv),
    CONSTRAINT fk_g6_lichlop_lophoc FOREIGN KEY (g6_ma_lop_hoc) REFERENCES G6LopHoc (g6_ma_lop_hoc) ON DELETE CASCADE,
    CONSTRAINT fk_g6_lichlop_hlv    FOREIGN KEY (g6_ma_hlv)     REFERENCES G6HuanLuyenVien (g6_ma_hlv)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6DatChoLopHoc (
    g6_ma_dat_cho      INT             NOT NULL AUTO_INCREMENT,
    g6_ma_lich_lop     INT             NOT NULL,
    g6_ma_hoi_vien     INT             NOT NULL,
    g6_ngay_tap        DATE            NOT NULL,
    g6_trang_thai      VARCHAR(20)     NOT NULL DEFAULT 'dat_cho' COMMENT '''dat_cho'',''da_den'',''vang_mat'',''da_huy''',
    g6_thoi_gian_dat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_thoi_gian_huy   DATETIME        NULL,
    g6_ly_do_huy       VARCHAR(255)    NULL,
    PRIMARY KEY (g6_ma_dat_cho),
    UNIQUE KEY uk_g6_datcholop (g6_ma_lich_lop, g6_ma_hoi_vien, g6_ngay_tap),
    KEY idx_g6_datcholop_hoivien (g6_ma_hoi_vien),
    KEY idx_g6_datcholop_ngaytap (g6_ngay_tap),
    CONSTRAINT fk_g6_datcholop_lichlop FOREIGN KEY (g6_ma_lich_lop) REFERENCES G6LichLopHoc (g6_ma_lich_lop),
    CONSTRAINT fk_g6_datcholop_hoivien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 8: DỊCH VỤ PHỤ (Sauna, Hồ bơi, Massage...)
-- ============================================================

CREATE TABLE G6DichVuPhu (
    g6_ma_dich_vu      INT             NOT NULL AUTO_INCREMENT,
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_ten_dich_vu     VARCHAR(100)    NOT NULL COMMENT '''Sauna'',''Hồ bơi'',''Massage''',
    g6_loai_dich_vu    VARCHAR(50)     NOT NULL,
    g6_mo_ta           TEXT            NULL,
    g6_gia_theo_luot   DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_thoi_luong_phut INT             NOT NULL DEFAULT 60,
    g6_suc_chua        INT             NULL,
    g6_la_mien_phi_goi TINYINT(1)      NOT NULL DEFAULT 0 COMMENT 'Miễn phí theo gói tập không',
    g6_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (g6_ma_dich_vu),
    KEY idx_g6_dichvuphu_chinhanh (g6_ma_chi_nhanh),
    CONSTRAINT fk_g6_dichvuphu_chinhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6DatDichVu (
    g6_ma_dat_dich_vu      INT             NOT NULL AUTO_INCREMENT,
    g6_ma_dich_vu          INT             NOT NULL,
    g6_ma_hoi_vien         INT             NOT NULL,
    g6_thoi_gian_bat_dau   DATETIME        NOT NULL,
    g6_thoi_gian_ket_thuc  DATETIME        NOT NULL,
    g6_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'da_dat' COMMENT '''da_dat'',''da_dung'',''da_huy''',
    g6_la_mien_phi         TINYINT(1)      NOT NULL DEFAULT 0,
    g6_ma_thanh_toan       INT             NULL,
    g6_ghi_chu             VARCHAR(255)    NULL,
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_dat_dich_vu),
    KEY idx_g6_datdichvu_dichvu  (g6_ma_dich_vu),
    KEY idx_g6_datdichvu_hoivien (g6_ma_hoi_vien),
    KEY idx_g6_datdichvu_thoigian(g6_thoi_gian_bat_dau),
    CONSTRAINT fk_g6_datdichvu_dichvu  FOREIGN KEY (g6_ma_dich_vu)  REFERENCES G6DichVuPhu (g6_ma_dich_vu),
    CONSTRAINT fk_g6_datdichvu_hoivien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 9: DANH MỤC SẢN PHẨM (TPCN)
-- ============================================================

CREATE TABLE G6DanhMucSanPham (
    g6_ma_danh_muc         INT             NOT NULL AUTO_INCREMENT,
    g6_ma_danh_muc_cha     INT             NULL COMMENT 'Self-join - NULL = danh mục gốc',
    g6_ten_danh_muc        VARCHAR(100)    NOT NULL,
    g6_slug                VARCHAR(100)    NOT NULL,
    g6_mo_ta               TEXT            NULL,
    g6_hinh_anh            VARCHAR(500)    NULL,
    g6_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    g6_la_hien_thi_menu    TINYINT(1)      NOT NULL DEFAULT 1,
    g6_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (g6_ma_danh_muc),
    UNIQUE KEY uk_g6_danhmuc_slug (g6_slug),
    KEY idx_g6_danhmuc_cha (g6_ma_danh_muc_cha),
    CONSTRAINT fk_g6_danhmuc_cha FOREIGN KEY (g6_ma_danh_muc_cha) REFERENCES G6DanhMucSanPham (g6_ma_danh_muc) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed danh mục (cấp 1)
INSERT INTO G6DanhMucSanPham (g6_ten_danh_muc, g6_slug, g6_thu_tu_hien_thi) VALUES
('Whey Protein',            'whey-protein',         1),
('Tăng Sức Mạnh',           'tang-suc-manh',        2),
('Hỗ Trợ Giảm Mỡ',         'ho-tro-giam-mo',       3),
('Vitamin & Khoáng Chất',   'vitamin-khoang-chat',  4),
('Sức Khỏe Toàn Diện',      'suc-khoe-toan-dien',   5),
('Thảo Mộc',                'thao-moc',             6),
('Phụ Kiện Thể Thao',       'phu-kien-the-thao',    7);

-- Seed danh mục (cấp 2) - Whey Protein
INSERT INTO G6DanhMucSanPham (g6_ma_danh_muc_cha, g6_ten_danh_muc, g6_slug, g6_thu_tu_hien_thi) VALUES
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

CREATE TABLE G6MucTieuSucKhoe (
    g6_ma_muc_tieu     INT             NOT NULL AUTO_INCREMENT,
    g6_ten_muc_tieu    VARCHAR(50)     NOT NULL,
    g6_slug            VARCHAR(50)     NOT NULL,
    g6_bieu_tuong      VARCHAR(20)     NULL COMMENT 'Icon/emoji code',
    PRIMARY KEY (g6_ma_muc_tieu),
    UNIQUE KEY uk_g6_muctieu_slug (g6_slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO G6MucTieuSucKhoe (g6_ten_muc_tieu, g6_slug, g6_bieu_tuong) VALUES
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

CREATE TABLE G6ThuongHieu (
    g6_ma_thuong_hieu      INT             NOT NULL AUTO_INCREMENT,
    g6_ten_thuong_hieu     VARCHAR(100)    NOT NULL,
    g6_slug                VARCHAR(100)    NOT NULL,
    g6_nuoc_xuat_xu        VARCHAR(50)     NULL,
    g6_logo                VARCHAR(500)    NULL,
    g6_mo_ta               TEXT            NULL,
    g6_website             VARCHAR(255)    NULL,
    g6_la_noi_bat          TINYINT(1)      NOT NULL DEFAULT 0,
    g6_loai_tru_ma_giam    TINYINT(1)      NOT NULL DEFAULT 0 COMMENT 'Loại trừ khỏi coupon',
    g6_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    g6_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    PRIMARY KEY (g6_ma_thuong_hieu),
    UNIQUE KEY uk_g6_thuonghieu_slug (g6_slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 10: SẢN PHẨM
-- ============================================================

CREATE TABLE G6SanPham (
    g6_ma_san_pham     INT             NOT NULL AUTO_INCREMENT,
    g6_ma_danh_muc     INT             NOT NULL,
    g6_ma_thuong_hieu  INT             NOT NULL,
    g6_ten_san_pham    VARCHAR(255)    NOT NULL,
    g6_slug            VARCHAR(255)    NOT NULL,
    g6_mo_ta_ngan      VARCHAR(500)    NULL,
    g6_mo_ta_day_du    LONGTEXT        NULL,
    g6_cach_dung       TEXT            NULL,
    g6_nuoc_xuat_xu    VARCHAR(50)     NULL,
    g6_doi_tuong_dung  VARCHAR(100)    NULL COMMENT '''nam'',''nu'',''nam_va_nu''',
    g6_da_ban          INT             NOT NULL DEFAULT 0,
    g6_luot_xem        INT             NOT NULL DEFAULT 0,
    g6_thu_tu_hien_thi INT             NOT NULL DEFAULT 0,
    g6_la_noi_bat      TINYINT(1)      NOT NULL DEFAULT 0,
    g6_la_ban_chay     TINYINT(1)      NOT NULL DEFAULT 0,
    g6_la_hang_moi     TINYINT(1)      NOT NULL DEFAULT 0,
    g6_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    g6_seo_title       VARCHAR(255)    NULL,
    g6_seo_mo_ta       VARCHAR(500)    NULL,
    g6_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_san_pham),
    UNIQUE KEY uk_g6_sanpham_slug (g6_slug),
    KEY idx_g6_sanpham_danhmuc   (g6_ma_danh_muc),
    KEY idx_g6_sanpham_thuonghieu(g6_ma_thuong_hieu),
    KEY idx_g6_sanpham_noibat    (g6_la_noi_bat),
    KEY idx_g6_sanpham_banchay   (g6_la_ban_chay),
    CONSTRAINT fk_g6_sanpham_danhmuc    FOREIGN KEY (g6_ma_danh_muc)   REFERENCES G6DanhMucSanPham (g6_ma_danh_muc),
    CONSTRAINT fk_g6_sanpham_thuonghieu FOREIGN KEY (g6_ma_thuong_hieu) REFERENCES G6ThuongHieu (g6_ma_thuong_hieu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6BienTheSanPham (
    g6_ma_bien_the     INT             NOT NULL AUTO_INCREMENT,
    g6_ma_san_pham     INT             NOT NULL,
    g6_sku             VARCHAR(100)    NOT NULL,
    g6_ten_bien_the    VARCHAR(100)    NOT NULL COMMENT '"5Lbs - Chocolate"',
    g6_trong_luong     VARCHAR(30)     NULL COMMENT '"5Lbs","2Lbs","500g"',
    g6_trong_luong_gram INT            NULL COMMENT 'Quy đổi ra gram',
    g6_so_luot_dung    INT             NULL COMMENT 'Số servings',
    g6_huong_vi        VARCHAR(50)     NULL COMMENT '"Chocolate","Vanilla","Unflavored"',
    g6_gia             DECIMAL(15,0)   NOT NULL,
    g6_gia_so_sanh     DECIMAL(15,0)   NULL COMMENT 'Giá gốc để gạch ngang',
    g6_hinh_anh        VARCHAR(500)    NULL,
    g6_la_mac_dinh     TINYINT(1)      NOT NULL DEFAULT 0,
    g6_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    g6_thu_tu          INT             NOT NULL DEFAULT 0,
    PRIMARY KEY (g6_ma_bien_the),
    UNIQUE KEY uk_g6_bienthe_sku (g6_sku),
    KEY idx_g6_bienthe_sanpham (g6_ma_san_pham),
    CONSTRAINT fk_g6_bienthe_sanpham FOREIGN KEY (g6_ma_san_pham) REFERENCES G6SanPham (g6_ma_san_pham) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6HinhAnhSanPham (
    g6_ma_hinh_anh     INT             NOT NULL AUTO_INCREMENT,
    g6_ma_san_pham     INT             NOT NULL,
    g6_ma_bien_the     INT             NULL COMMENT 'NULL = ảnh chung của sản phẩm',
    g6_duong_dan       VARCHAR(500)    NOT NULL,
    g6_alt_text        VARCHAR(255)    NULL,
    g6_thu_tu          INT             NOT NULL DEFAULT 0,
    g6_la_anh_chinh    TINYINT(1)      NOT NULL DEFAULT 0,
    PRIMARY KEY (g6_ma_hinh_anh),
    KEY idx_g6_hinhanh_sanpham (g6_ma_san_pham),
    CONSTRAINT fk_g6_hinhanh_sanpham FOREIGN KEY (g6_ma_san_pham) REFERENCES G6SanPham (g6_ma_san_pham) ON DELETE CASCADE,
    CONSTRAINT fk_g6_hinhanh_bienthe FOREIGN KEY (g6_ma_bien_the) REFERENCES G6BienTheSanPham (g6_ma_bien_the) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6ThanhPhanDinhDuong (
    g6_ma_dinh_duong   INT             NOT NULL AUTO_INCREMENT,
    g6_ma_bien_the     INT             NOT NULL,
    g6_khau_phan       INT             NULL COMMENT 'gram/serving',
    g6_calo            INT             NULL,
    g6_protein         DECIMAL(6,2)    NULL COMMENT 'gram',
    g6_tinh_bot        DECIMAL(6,2)    NULL,
    g6_chat_beo        DECIMAL(6,2)    NULL,
    g6_duong           DECIMAL(6,2)    NULL,
    g6_chat_xo         DECIMAL(6,2)    NULL,
    g6_bcaa            DECIMAL(6,2)    NULL,
    g6_glutamine       DECIMAL(6,2)    NULL,
    g6_creatine        DECIMAL(6,2)    NULL,
    g6_caffeine        DECIMAL(6,2)    NULL COMMENT 'mg',
    g6_thanh_phan_khac JSON            NULL COMMENT 'Các vi chất khác',
    PRIMARY KEY (g6_ma_dinh_duong),
    UNIQUE KEY uk_g6_dinhduong_bienthe (g6_ma_bien_the),
    CONSTRAINT fk_g6_dinhduong_bienthe FOREIGN KEY (g6_ma_bien_the) REFERENCES G6BienTheSanPham (g6_ma_bien_the) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6ChungNhanSanPham (
    g6_ma_chung_nhan   INT             NOT NULL AUTO_INCREMENT,
    g6_ma_san_pham     INT             NOT NULL,
    g6_loai            VARCHAR(30)     NOT NULL COMMENT '''GMP'',''Halal'',''Kosher'',''FDA'',''DĐVN''',
    g6_so_chung_nhan   VARCHAR(100)    NULL,
    g6_ngay_cap        DATE            NULL,
    g6_hinh_anh        VARCHAR(500)    NULL,
    PRIMARY KEY (g6_ma_chung_nhan),
    KEY idx_g6_chungnhan_sanpham (g6_ma_san_pham),
    CONSTRAINT fk_g6_chungnhan_sanpham FOREIGN KEY (g6_ma_san_pham) REFERENCES G6SanPham (g6_ma_san_pham) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6SanPhamMucTieu (
    g6_ma_san_pham     INT             NOT NULL,
    g6_ma_muc_tieu     INT             NOT NULL,
    PRIMARY KEY (g6_ma_san_pham, g6_ma_muc_tieu),
    CONSTRAINT fk_g6_spmuctieu_sanpham FOREIGN KEY (g6_ma_san_pham) REFERENCES G6SanPham (g6_ma_san_pham) ON DELETE CASCADE,
    CONSTRAINT fk_g6_spmuctieu_muctieu FOREIGN KEY (g6_ma_muc_tieu) REFERENCES G6MucTieuSucKhoe (g6_ma_muc_tieu) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
