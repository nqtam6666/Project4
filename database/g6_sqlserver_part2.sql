-- ============================================================
-- G6 GYM MANAGEMENT + SUPPLEMENT STORE
-- SQL Server Schema - Part 2: Group 6-10
-- GROUP 6: HUẤN LUYỆN VIÊN | GROUP 7: LỚP HỌC NHÓM
-- GROUP 8: DỊCH VỤ PHỤ | GROUP 9: DANH MỤC SP | GROUP 10: SẢN PHẨM
-- ============================================================

-- ============================================================
-- GROUP 6: HUẤN LUYỆN VIÊN (PT)
-- ============================================================

CREATE TABLE G6HuanLuyenVien (
    g6_ma_hlv              INT             NOT NULL IDENTITY(1,1),
    g6_ma_nhan_vien        INT             NOT NULL,
    g6_ma_chi_nhanh        INT             NOT NULL,
    g6_chuyen_mon          NVARCHAR(MAX)   NULL,        -- JSON: ["tang_co","giam_mo","yoga","boxing"]
    g6_cap_chung_chi       NVARCHAR(50)    NULL,        -- 'ACE','NASM','REPs','ISSA'
    g6_so_nam_kinh_nghiem  INT             NOT NULL DEFAULT 0,
    g6_tieu_su             NVARCHAR(MAX)   NULL,
    g6_gia_theo_buoi       DECIMAL(15,0)   NULL,
    g6_hinh_anh            NVARCHAR(500)   NULL,
    g6_thu_hang            TINYINT         NOT NULL DEFAULT 5, -- 1-5 sao
    g6_so_hoi_vien_hien_tai INT            NOT NULL DEFAULT 0,
    g6_toi_da_hoi_vien     INT             NOT NULL DEFAULT 20,
    g6_la_hien_thi_web     BIT             NOT NULL DEFAULT 1,
    CONSTRAINT PK_G6HuanLuyenVien PRIMARY KEY (g6_ma_hlv),
    CONSTRAINT FK_G6HLV_NhanVien FOREIGN KEY (g6_ma_nhan_vien) REFERENCES G6NhanVien (g6_ma_nhan_vien),
    CONSTRAINT FK_G6HLV_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
);

CREATE TABLE G6GoiPT (
    g6_ma_goi_pt       INT             NOT NULL IDENTITY(1,1),
    g6_ma_hlv          INT             NOT NULL,
    g6_ten_goi         NVARCHAR(100)   NOT NULL,
    g6_so_buoi         INT             NOT NULL,        -- 10, 20, 30 buổi
    g6_thoi_luong_buoi INT             NOT NULL,        -- Phút/buổi
    g6_gia             DECIMAL(15,0)   NOT NULL,
    g6_gia_khuyen_mai  DECIMAL(15,0)   NULL,
    g6_hieu_luc_ngay   INT             NOT NULL DEFAULT 90, -- Hết hạn sau X ngày
    g6_la_hoat_dong    BIT             NOT NULL DEFAULT 1,
    g6_ngay_tao        DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6GoiPT PRIMARY KEY (g6_ma_goi_pt),
    CONSTRAINT FK_G6GoiPT_HLV FOREIGN KEY (g6_ma_hlv) REFERENCES G6HuanLuyenVien (g6_ma_hlv)
);

CREATE TABLE G6DangKyGoiPT (
    g6_ma_dang_ky_pt   INT             NOT NULL IDENTITY(1,1),
    g6_ma_hoi_vien     INT             NOT NULL,
    g6_ma_goi_pt       INT             NOT NULL,
    g6_ma_hlv          INT             NOT NULL,
    g6_ngay_mua        DATE            NOT NULL,
    g6_ngay_het_han    DATE            NOT NULL,
    g6_so_buoi_con_lai INT             NOT NULL,
    g6_gia_thuc_te     DECIMAL(15,0)   NOT NULL,
    g6_ma_thanh_toan   INT             NULL,
    g6_trang_thai      NVARCHAR(20)    NOT NULL DEFAULT 'dang_dung', -- 'dang_dung','het_buoi','het_han','huy'
    g6_ngay_tao        DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6DangKyGoiPT PRIMARY KEY (g6_ma_dang_ky_pt),
    CONSTRAINT FK_G6DKPT_HoiVien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien),
    CONSTRAINT FK_G6DKPT_GoiPT FOREIGN KEY (g6_ma_goi_pt) REFERENCES G6GoiPT (g6_ma_goi_pt),
    CONSTRAINT FK_G6DKPT_HLV FOREIGN KEY (g6_ma_hlv) REFERENCES G6HuanLuyenVien (g6_ma_hlv)
);

CREATE TABLE G6BuoiTapPT (
    g6_ma_buoi_tap         INT             NOT NULL IDENTITY(1,1),
    g6_ma_dang_ky_pt       INT             NOT NULL,
    g6_ma_hoi_vien         INT             NOT NULL,
    g6_ma_hlv              INT             NOT NULL,
    g6_ma_chi_nhanh        INT             NOT NULL,
    g6_ngay_tap            DATETIME2       NOT NULL,
    g6_thoi_luong          INT             NULL,        -- Phút thực tế
    g6_trang_thai          NVARCHAR(20)    NOT NULL DEFAULT 'cho_xac_nhan', -- 'da_tap','vang_mat','huy','cho_xac_nhan'
    g6_noi_dung_buoi_tap   NVARCHAR(MAX)   NULL,
    g6_nhan_xet_hlv        NVARCHAR(MAX)   NULL,
    g6_danh_gia_hoi_vien   TINYINT         NULL,        -- 1-5 sao
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6BuoiTapPT PRIMARY KEY (g6_ma_buoi_tap),
    CONSTRAINT FK_G6BuoiTap_DangKy FOREIGN KEY (g6_ma_dang_ky_pt) REFERENCES G6DangKyGoiPT (g6_ma_dang_ky_pt),
    CONSTRAINT FK_G6BuoiTap_HoiVien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien),
    CONSTRAINT FK_G6BuoiTap_HLV FOREIGN KEY (g6_ma_hlv) REFERENCES G6HuanLuyenVien (g6_ma_hlv),
    CONSTRAINT FK_G6BuoiTap_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
);

-- ============================================================
-- GROUP 7: LỚP HỌC NHÓM
-- ============================================================

CREATE TABLE G6LopHoc (
    g6_ma_lop_hoc      INT             NOT NULL IDENTITY(1,1),
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_ten_lop         NVARCHAR(100)   NOT NULL,
    g6_loai_lop        NVARCHAR(50)    NOT NULL,        -- 'yoga','spinning','boxing','zumba','aerobic'
    g6_mo_ta           NVARCHAR(MAX)   NULL,
    g6_hinh_anh        NVARCHAR(500)   NULL,
    g6_do_kho          NVARCHAR(20)    NOT NULL DEFAULT 'co_ban', -- 'co_ban','trung_binh','nang_cao'
    g6_la_hoat_dong    BIT             NOT NULL DEFAULT 1,
    CONSTRAINT PK_G6LopHoc PRIMARY KEY (g6_ma_lop_hoc),
    CONSTRAINT FK_G6LopHoc_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
);

CREATE TABLE G6LichLopHoc (
    g6_ma_lich_lop         INT             NOT NULL IDENTITY(1,1),
    g6_ma_lop_hoc          INT             NOT NULL,
    g6_ma_hlv              INT             NOT NULL,
    g6_thu_trong_tuan      TINYINT         NOT NULL,    -- 1=T2 ... 7=CN
    g6_gio_bat_dau         TIME            NOT NULL,
    g6_thoi_luong          INT             NOT NULL,    -- Phút
    g6_suc_chua_toi_da     INT             NOT NULL DEFAULT 20,
    g6_phong_tap           NVARCHAR(50)    NULL,
    g6_ngay_ap_dung_tu     DATE            NOT NULL,
    g6_ngay_ap_dung_den    DATE            NULL,
    g6_la_hoat_dong        BIT             NOT NULL DEFAULT 1,
    CONSTRAINT PK_G6LichLopHoc PRIMARY KEY (g6_ma_lich_lop),
    CONSTRAINT FK_G6LichLop_LopHoc FOREIGN KEY (g6_ma_lop_hoc) REFERENCES G6LopHoc (g6_ma_lop_hoc) ON DELETE CASCADE,
    CONSTRAINT FK_G6LichLop_HLV FOREIGN KEY (g6_ma_hlv) REFERENCES G6HuanLuyenVien (g6_ma_hlv)
);

CREATE TABLE G6DatChoLopHoc (
    g6_ma_dat_cho      INT             NOT NULL IDENTITY(1,1),
    g6_ma_lich_lop     INT             NOT NULL,
    g6_ma_hoi_vien     INT             NOT NULL,
    g6_ngay_tap        DATE            NOT NULL,
    g6_trang_thai      NVARCHAR(20)    NOT NULL DEFAULT 'dat_cho', -- 'dat_cho','da_den','vang_mat','da_huy'
    g6_thoi_gian_dat   DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_thoi_gian_huy   DATETIME2       NULL,
    g6_ly_do_huy       NVARCHAR(255)   NULL,
    CONSTRAINT PK_G6DatChoLopHoc PRIMARY KEY (g6_ma_dat_cho),
    CONSTRAINT UK_G6DatChoLop UNIQUE (g6_ma_lich_lop, g6_ma_hoi_vien, g6_ngay_tap),
    CONSTRAINT FK_G6DatCho_LichLop FOREIGN KEY (g6_ma_lich_lop) REFERENCES G6LichLopHoc (g6_ma_lich_lop),
    CONSTRAINT FK_G6DatCho_HoiVien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien)
);

-- ============================================================
-- GROUP 8: DỊCH VỤ PHỤ (Sauna, Hồ bơi, Massage...)
-- ============================================================

CREATE TABLE G6DichVuPhu (
    g6_ma_dich_vu      INT             NOT NULL IDENTITY(1,1),
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_ten_dich_vu     NVARCHAR(100)   NOT NULL,        -- 'Sauna','Hồ bơi','Massage'
    g6_loai_dich_vu    NVARCHAR(50)    NOT NULL,
    g6_mo_ta           NVARCHAR(MAX)   NULL,
    g6_gia_theo_luot   DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_thoi_luong_phut INT             NOT NULL DEFAULT 60,
    g6_suc_chua        INT             NULL,
    g6_la_mien_phi_goi BIT             NOT NULL DEFAULT 0, -- Miễn phí theo gói tập
    g6_la_hoat_dong    BIT             NOT NULL DEFAULT 1,
    CONSTRAINT PK_G6DichVuPhu PRIMARY KEY (g6_ma_dich_vu),
    CONSTRAINT FK_G6DichVu_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
);

CREATE TABLE G6DatDichVu (
    g6_ma_dat_dich_vu      INT             NOT NULL IDENTITY(1,1),
    g6_ma_dich_vu          INT             NOT NULL,
    g6_ma_hoi_vien         INT             NOT NULL,
    g6_thoi_gian_bat_dau   DATETIME2       NOT NULL,
    g6_thoi_gian_ket_thuc  DATETIME2       NOT NULL,
    g6_trang_thai          NVARCHAR(20)    NOT NULL DEFAULT 'da_dat', -- 'da_dat','da_dung','da_huy'
    g6_la_mien_phi         BIT             NOT NULL DEFAULT 0,
    g6_ma_thanh_toan       INT             NULL,
    g6_ghi_chu             NVARCHAR(255)   NULL,
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6DatDichVu PRIMARY KEY (g6_ma_dat_dich_vu),
    CONSTRAINT FK_G6DatDV_DichVu FOREIGN KEY (g6_ma_dich_vu) REFERENCES G6DichVuPhu (g6_ma_dich_vu),
    CONSTRAINT FK_G6DatDV_HoiVien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien)
);

-- ============================================================
-- GROUP 9: DANH MỤC SẢN PHẨM (TPCN)
-- ============================================================

CREATE TABLE G6DanhMucSanPham (
    g6_ma_danh_muc         INT             NOT NULL IDENTITY(1,1),
    g6_ma_danh_muc_cha     INT             NULL,        -- Self-join, NULL = danh mục gốc
    g6_ten_danh_muc        NVARCHAR(100)   NOT NULL,
    g6_slug                NVARCHAR(100)   NOT NULL,
    g6_mo_ta               NVARCHAR(MAX)   NULL,
    g6_hinh_anh            NVARCHAR(500)   NULL,
    g6_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    g6_la_hien_thi_menu    BIT             NOT NULL DEFAULT 1,
    g6_la_hoat_dong        BIT             NOT NULL DEFAULT 1,
    CONSTRAINT PK_G6DanhMucSP PRIMARY KEY (g6_ma_danh_muc),
    CONSTRAINT UK_G6DanhMuc_Slug UNIQUE (g6_slug),
    -- Rule 3: Self-referencing FK — KHÔNG có ON DELETE
    CONSTRAINT FK_G6DanhMuc_Cha FOREIGN KEY (g6_ma_danh_muc_cha) REFERENCES G6DanhMucSanPham (g6_ma_danh_muc)
);

-- Seed danh mục (cấp 1)
INSERT INTO G6DanhMucSanPham (g6_ten_danh_muc, g6_slug, g6_thu_tu_hien_thi) VALUES
(N'Whey Protein',            'whey-protein',         1),
(N'Tăng Sức Mạnh',           'tang-suc-manh',        2),
(N'Hỗ Trợ Giảm Mỡ',         'ho-tro-giam-mo',       3),
(N'Vitamin & Khoáng Chất',   'vitamin-khoang-chat',  4),
(N'Sức Khỏe Toàn Diện',      'suc-khoe-toan-dien',   5),
(N'Thảo Mộc',                'thao-moc',             6),
(N'Phụ Kiện Thể Thao',       'phu-kien-the-thao',    7);

-- Seed danh mục (cấp 2) - Whey Protein
INSERT INTO G6DanhMucSanPham (g6_ma_danh_muc_cha, g6_ten_danh_muc, g6_slug, g6_thu_tu_hien_thi) VALUES
(1, N'Whey Isolate',         'whey-isolate',             1),
(1, N'Whey Hydrolyzed',      'whey-hydrolyzed',          2),
(1, N'Whey Blend',           'whey-blend',               3),
(1, N'Casein',               'casein',                   4),
(1, N'Vegan Protein',        'vegan-protein',            5),
(1, N'Protein Bar',          'protein-bar',              6),
(1, N'Mass Gainer',          'mass-gainer',              7),
-- Tăng Sức Mạnh
(2, N'Creatine',             'creatine',                 1),
(2, N'Pre-Workout',          'pre-workout',              2),
(2, N'BCAA',                 'bcaa',                     3),
(2, N'EAA',                  'eaa',                      4),
(2, N'Glutamine',            'glutamine',                5),
-- Giảm Mỡ
(3, N'Fat Burner',           'fat-burner',               1),
(3, N'L-Carnitine',          'l-carnitine',              2),
(3, N'CLA',                  'cla',                      3),
(3, N'Yohimbine',            'yohimbine',                4),
-- Vitamin
(4, N'Vitamin D3 + K2',      'vitamin-d3-k2',            1),
(4, N'Omega-3 Fish Oil',     'omega-3-fish-oil',         2),
(4, N'Multivitamin',         'multivitamin',             3),
(4, N'Zinc & ZMA',           'zinc-zma',                 4),
-- Sức Khỏe Toàn Diện
(5, N'Collagen',             'collagen',                 1),
(5, N'Probiotic',            'probiotic',                2),
(5, N'Glucosamine',          'glucosamine',              3),
(5, N'Melatonin',            'melatonin',                4),
-- Thảo Mộc
(6, N'Ashwagandha',          'ashwagandha',              1),
(6, N'Curcumin',             'curcumin',                 2),
(6, N'Ginkgo Biloba',        'ginkgo-biloba',            3),
-- Phụ Kiện
(7, N'Shaker & Bình Lắc',    'shaker-binh-lac',          1),
(7, N'Găng Tay Tập',         'gang-tay-tap',             2),
(7, N'Đai Lưng',             'dai-lung',                 3),
(7, N'Quần Áo Tập',          'quan-ao-tap',              4);

CREATE TABLE G6MucTieuSucKhoe (
    g6_ma_muc_tieu     INT             NOT NULL IDENTITY(1,1),
    g6_ten_muc_tieu    NVARCHAR(50)    NOT NULL,
    g6_slug            NVARCHAR(50)    NOT NULL,
    g6_bieu_tuong      NVARCHAR(20)    NULL,            -- Icon/emoji code
    CONSTRAINT PK_G6MucTieuSK PRIMARY KEY (g6_ma_muc_tieu),
    CONSTRAINT UK_G6MucTieu_Slug UNIQUE (g6_slug)
);

INSERT INTO G6MucTieuSucKhoe (g6_ten_muc_tieu, g6_slug, g6_bieu_tuong) VALUES
(N'Tăng Cơ',             'tang-co',          N'💪'),
(N'Giảm Mỡ',             'giam-mo',          N'🔥'),
(N'Tăng Cân',            'tang-can',         N'⬆️'),
(N'Xương Khớp',          'xuong-khop',       N'🦴'),
(N'Da Tóc Móng',         'da-toc-mong',      N'✨'),
(N'Bảo Vệ Gan',          'bao-ve-gan',       N'🫀'),
(N'Giấc Ngủ',            'giac-ngu',         N'😴'),
(N'Tim Mạch',            'tim-mach',         N'❤️'),
(N'Tiêu Hóa',            'tieu-hoa',         N'🌿'),
(N'Chống Lão Hóa',       'chong-lao-hoa',    N'⏳'),
(N'Giảm Căng Thẳng',     'giam-cang-thang',  N'🧘');

CREATE TABLE G6ThuongHieu (
    g6_ma_thuong_hieu      INT             NOT NULL IDENTITY(1,1),
    g6_ten_thuong_hieu     NVARCHAR(100)   NOT NULL,
    g6_slug                NVARCHAR(100)   NOT NULL,
    g6_nuoc_xuat_xu        NVARCHAR(50)    NULL,
    g6_logo                NVARCHAR(500)   NULL,
    g6_mo_ta               NVARCHAR(MAX)   NULL,
    g6_website             NVARCHAR(255)   NULL,
    g6_la_noi_bat          BIT             NOT NULL DEFAULT 0,
    g6_loai_tru_ma_giam    BIT             NOT NULL DEFAULT 0, -- Loại trừ khỏi coupon
    g6_la_hoat_dong        BIT             NOT NULL DEFAULT 1,
    g6_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    CONSTRAINT PK_G6ThuongHieu PRIMARY KEY (g6_ma_thuong_hieu),
    CONSTRAINT UK_G6ThuongHieu_Slug UNIQUE (g6_slug)
);

-- ============================================================
-- GROUP 10: SẢN PHẨM
-- ============================================================

CREATE TABLE G6SanPham (
    g6_ma_san_pham     INT             NOT NULL IDENTITY(1,1),
    g6_ma_danh_muc     INT             NOT NULL,
    g6_ma_thuong_hieu  INT             NOT NULL,
    g6_ten_san_pham    NVARCHAR(255)   NOT NULL,
    g6_slug            NVARCHAR(255)   NOT NULL,
    g6_mo_ta_ngan      NVARCHAR(500)   NULL,
    g6_mo_ta_day_du    NVARCHAR(MAX)   NULL,
    g6_cach_dung       NVARCHAR(MAX)   NULL,
    g6_nuoc_xuat_xu    NVARCHAR(50)    NULL,
    g6_doi_tuong_dung  NVARCHAR(100)   NULL,            -- 'nam','nu','nam_va_nu'
    g6_da_ban          INT             NOT NULL DEFAULT 0,
    g6_luot_xem        INT             NOT NULL DEFAULT 0,
    g6_thu_tu_hien_thi INT             NOT NULL DEFAULT 0,
    g6_la_noi_bat      BIT             NOT NULL DEFAULT 0,
    g6_la_ban_chay     BIT             NOT NULL DEFAULT 0,
    g6_la_hang_moi     BIT             NOT NULL DEFAULT 0,
    g6_la_hoat_dong    BIT             NOT NULL DEFAULT 1,
    g6_seo_title       NVARCHAR(255)   NULL,
    g6_seo_mo_ta       NVARCHAR(500)   NULL,
    g6_ngay_tao        DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_cap_nhat   DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6SanPham PRIMARY KEY (g6_ma_san_pham),
    CONSTRAINT UK_G6SanPham_Slug UNIQUE (g6_slug),
    CONSTRAINT FK_G6SP_DanhMuc FOREIGN KEY (g6_ma_danh_muc) REFERENCES G6DanhMucSanPham (g6_ma_danh_muc),
    CONSTRAINT FK_G6SP_ThuongHieu FOREIGN KEY (g6_ma_thuong_hieu) REFERENCES G6ThuongHieu (g6_ma_thuong_hieu)
);

CREATE TABLE G6BienTheSanPham (
    g6_ma_bien_the     INT             NOT NULL IDENTITY(1,1),
    g6_ma_san_pham     INT             NOT NULL,
    g6_sku             NVARCHAR(100)   NOT NULL,
    g6_ten_bien_the    NVARCHAR(100)   NOT NULL,        -- "5Lbs - Chocolate"
    g6_trong_luong     NVARCHAR(30)    NULL,             -- "5Lbs","2Lbs","500g"
    g6_trong_luong_gram INT            NULL,             -- Quy đổi ra gram
    g6_so_luot_dung    INT             NULL,             -- Số servings
    g6_huong_vi        NVARCHAR(50)    NULL,             -- "Chocolate","Vanilla"
    g6_gia             DECIMAL(15,0)   NOT NULL,
    g6_gia_so_sanh     DECIMAL(15,0)   NULL,             -- Giá gốc để gạch ngang
    g6_hinh_anh        NVARCHAR(500)   NULL,
    g6_la_mac_dinh     BIT             NOT NULL DEFAULT 0,
    g6_la_hoat_dong    BIT             NOT NULL DEFAULT 1,
    g6_thu_tu          INT             NOT NULL DEFAULT 0,
    CONSTRAINT PK_G6BienThe PRIMARY KEY (g6_ma_bien_the),
    CONSTRAINT UK_G6BienThe_SKU UNIQUE (g6_sku),
    CONSTRAINT FK_G6BienThe_SP FOREIGN KEY (g6_ma_san_pham) REFERENCES G6SanPham (g6_ma_san_pham) ON DELETE CASCADE
);

CREATE TABLE G6HinhAnhSanPham (
    g6_ma_hinh_anh     INT             NOT NULL IDENTITY(1,1),
    g6_ma_san_pham     INT             NOT NULL,
    g6_ma_bien_the     INT             NULL,             -- NULL = ảnh chung của sản phẩm
    g6_duong_dan       NVARCHAR(500)   NOT NULL,
    g6_alt_text        NVARCHAR(255)   NULL,
    g6_thu_tu          INT             NOT NULL DEFAULT 0,
    g6_la_anh_chinh    BIT             NOT NULL DEFAULT 0,
    CONSTRAINT PK_G6HinhAnhSP PRIMARY KEY (g6_ma_hinh_anh),
    CONSTRAINT FK_G6HinhAnh_SP FOREIGN KEY (g6_ma_san_pham) REFERENCES G6SanPham (g6_ma_san_pham) ON DELETE CASCADE,
    CONSTRAINT FK_G6HinhAnh_BienThe FOREIGN KEY (g6_ma_bien_the) REFERENCES G6BienTheSanPham (g6_ma_bien_the) ON DELETE SET NULL
);

CREATE TABLE G6ThanhPhanDinhDuong (
    g6_ma_dinh_duong   INT             NOT NULL IDENTITY(1,1),
    g6_ma_bien_the     INT             NOT NULL,
    g6_khau_phan       INT             NULL,             -- gram/serving
    g6_calo            INT             NULL,
    g6_protein         DECIMAL(6,2)    NULL,             -- gram
    g6_tinh_bot        DECIMAL(6,2)    NULL,
    g6_chat_beo        DECIMAL(6,2)    NULL,
    g6_duong           DECIMAL(6,2)    NULL,
    g6_chat_xo         DECIMAL(6,2)    NULL,
    g6_bcaa            DECIMAL(6,2)    NULL,
    g6_glutamine       DECIMAL(6,2)    NULL,
    g6_creatine        DECIMAL(6,2)    NULL,
    g6_caffeine        DECIMAL(6,2)    NULL,             -- mg
    g6_thanh_phan_khac NVARCHAR(MAX)   NULL,             -- JSON: Các vi chất khác
    CONSTRAINT PK_G6DinhDuong PRIMARY KEY (g6_ma_dinh_duong),
    CONSTRAINT UK_G6DinhDuong_BienThe UNIQUE (g6_ma_bien_the),
    CONSTRAINT FK_G6DinhDuong_BienThe FOREIGN KEY (g6_ma_bien_the) REFERENCES G6BienTheSanPham (g6_ma_bien_the) ON DELETE CASCADE
);

CREATE TABLE G6ChungNhanSanPham (
    g6_ma_chung_nhan   INT             NOT NULL IDENTITY(1,1),
    g6_ma_san_pham     INT             NOT NULL,
    g6_loai            NVARCHAR(30)    NOT NULL,         -- 'GMP','Halal','Kosher','FDA','DĐVN'
    g6_so_chung_nhan   NVARCHAR(100)   NULL,
    g6_ngay_cap        DATE            NULL,
    g6_hinh_anh        NVARCHAR(500)   NULL,
    CONSTRAINT PK_G6ChungNhan PRIMARY KEY (g6_ma_chung_nhan),
    CONSTRAINT FK_G6ChungNhan_SP FOREIGN KEY (g6_ma_san_pham) REFERENCES G6SanPham (g6_ma_san_pham) ON DELETE CASCADE
);

CREATE TABLE G6SanPhamMucTieu (
    g6_ma_san_pham     INT             NOT NULL,
    g6_ma_muc_tieu     INT             NOT NULL,
    CONSTRAINT PK_G6SPMucTieu PRIMARY KEY (g6_ma_san_pham, g6_ma_muc_tieu),
    CONSTRAINT FK_G6SPMucTieu_SP FOREIGN KEY (g6_ma_san_pham) REFERENCES G6SanPham (g6_ma_san_pham) ON DELETE CASCADE,
    CONSTRAINT FK_G6SPMucTieu_MT FOREIGN KEY (g6_ma_muc_tieu) REFERENCES G6MucTieuSucKhoe (g6_ma_muc_tieu) ON DELETE CASCADE
);

-- Index
CREATE INDEX IX_G6HLV_NhanVien ON G6HuanLuyenVien (g6_ma_nhan_vien);
CREATE INDEX IX_G6HLV_ChiNhanh ON G6HuanLuyenVien (g6_ma_chi_nhanh);
CREATE INDEX IX_G6GoiPT_HLV ON G6GoiPT (g6_ma_hlv);
CREATE INDEX IX_G6DKPT_HoiVien ON G6DangKyGoiPT (g6_ma_hoi_vien);
CREATE INDEX IX_G6BuoiTap_DangKy ON G6BuoiTapPT (g6_ma_dang_ky_pt);
CREATE INDEX IX_G6BuoiTap_NgayTap ON G6BuoiTapPT (g6_ngay_tap);
CREATE INDEX IX_G6LopHoc_ChiNhanh ON G6LopHoc (g6_ma_chi_nhanh);
CREATE INDEX IX_G6DatCho_HoiVien ON G6DatChoLopHoc (g6_ma_hoi_vien);
CREATE INDEX IX_G6DanhMuc_Cha ON G6DanhMucSanPham (g6_ma_danh_muc_cha);
CREATE INDEX IX_G6SP_DanhMuc ON G6SanPham (g6_ma_danh_muc);
CREATE INDEX IX_G6SP_ThuongHieu ON G6SanPham (g6_ma_thuong_hieu);
CREATE INDEX IX_G6SP_NoiBat ON G6SanPham (g6_la_noi_bat);
CREATE INDEX IX_G6BienThe_SP ON G6BienTheSanPham (g6_ma_san_pham);
CREATE INDEX IX_G6HinhAnh_SP ON G6HinhAnhSanPham (g6_ma_san_pham);

PRINT N'Part 2 - Hoàn thành!';
GO
