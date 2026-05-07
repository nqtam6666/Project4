-- ============================================================
-- NXV SCHEMA PART 5 - Đánh giá, Chương trình tập, Bảo trì, Sự kiện
-- ============================================================

-- Đánh giá HLV
CREATE TABLE NxvDanhGiaHLV (
    nxv_ma_danh_gia     INT IDENTITY(1,1) PRIMARY KEY,
    nxv_ma_hlv          INT NOT NULL FOREIGN KEY REFERENCES G6HuanLuyenVien(g6_ma_hlv) ON DELETE CASCADE,
    nxv_ma_hoi_vien     INT NULL FOREIGN KEY REFERENCES G6HoiVien(g6_ma_hoi_vien) ON DELETE SET NULL,
    nxv_ma_dang_ky_pt   INT NULL FOREIGN KEY REFERENCES G6DangKyGoiPT(g6_ma_dang_ky_pt) ON DELETE SET NULL,
    nxv_sao             SMALLINT NOT NULL CHECK (nxv_sao BETWEEN 1 AND 5),
    nxv_noi_dung        NVARCHAR(MAX) NULL,
    nxv_phan_hoi_hlv    NVARCHAR(MAX) NULL,
    nxv_trang_thai      NVARCHAR(20) NOT NULL DEFAULT 'cho_duyet',
    nxv_ngay_tao        DATETIME2 NOT NULL DEFAULT GETDATE(),
    g6_deleted_at       DATETIME2 NULL DEFAULT NULL
);

-- Đánh giá lớp học
CREATE TABLE NxvDanhGiaLopHoc (
    nxv_ma_danh_gia     INT IDENTITY(1,1) PRIMARY KEY,
    nxv_ma_lop_hoc      INT NOT NULL FOREIGN KEY REFERENCES G6LopHoc(g6_ma_lop_hoc) ON DELETE CASCADE,
    nxv_ma_hoi_vien     INT NULL FOREIGN KEY REFERENCES G6HoiVien(g6_ma_hoi_vien) ON DELETE SET NULL,
    nxv_ma_dat_cho      INT NULL FOREIGN KEY REFERENCES G6DatChoLopHoc(g6_ma_dat_cho) ON DELETE SET NULL,
    nxv_sao             SMALLINT NOT NULL CHECK (nxv_sao BETWEEN 1 AND 5),
    nxv_noi_dung        NVARCHAR(MAX) NULL,
    nxv_phan_hoi_hlv    NVARCHAR(MAX) NULL,
    nxv_trang_thai      NVARCHAR(20) NOT NULL DEFAULT 'cho_duyet',
    nxv_ngay_tao        DATETIME2 NOT NULL DEFAULT GETDATE(),
    g6_deleted_at       DATETIME2 NULL DEFAULT NULL
);

-- Chương trình tập luyện
CREATE TABLE NxvChuongTrinhTapLuyen (
    nxv_ma_chuong_trinh INT IDENTITY(1,1) PRIMARY KEY,
    nxv_ma_hoi_vien     INT NOT NULL FOREIGN KEY REFERENCES G6HoiVien(g6_ma_hoi_vien) ON DELETE CASCADE,
    nxv_ma_hlv          INT NULL FOREIGN KEY REFERENCES G6HuanLuyenVien(g6_ma_hlv) ON DELETE SET NULL,
    nxv_ten             NVARCHAR(200) NOT NULL,
    nxv_muc_tieu        NVARCHAR(100) NULL,
    nxv_so_tuan         INT NOT NULL DEFAULT 4,
    nxv_ngay_bat_dau    DATE NOT NULL,
    nxv_ngay_ket_thuc   DATE NULL,
    nxv_ghi_chu         NVARCHAR(MAX) NULL,
    nxv_trang_thai      NVARCHAR(20) NOT NULL DEFAULT 'dang_thuc_hien',
    nxv_ngay_tao        DATETIME2 NOT NULL DEFAULT GETDATE(),
    g6_deleted_at       DATETIME2 NULL DEFAULT NULL
);

-- Bài tập trong ngày
CREATE TABLE NxvBaiTapTrongNgay (
    nxv_ma_bai_tap          INT IDENTITY(1,1) PRIMARY KEY,
    nxv_ma_chuong_trinh     INT NOT NULL FOREIGN KEY REFERENCES NxvChuongTrinhTapLuyen(nxv_ma_chuong_trinh) ON DELETE CASCADE,
    nxv_tuan                INT NOT NULL,
    nxv_ngay_trong_tuan     INT NOT NULL CHECK (nxv_ngay_trong_tuan BETWEEN 1 AND 7),
    nxv_ten_bai_tap         NVARCHAR(200) NOT NULL,
    nxv_nhom_co             NVARCHAR(100) NULL,
    nxv_so_hieu             INT NULL,
    nxv_so_set              INT NULL,
    nxv_so_rep              INT NULL,
    nxv_trong_luong_kg      DECIMAL(6,2) NULL,
    nxv_thoi_gian_nghi_giay INT NULL,
    nxv_ghi_chu             NVARCHAR(MAX) NULL,
    nxv_la_hoan_thanh       BIT NOT NULL DEFAULT 0,
    g6_deleted_at           DATETIME2 NULL DEFAULT NULL
);

-- Lịch sử bảo trì thiết bị
CREATE TABLE NxvLichSuBaoTri (
    nxv_ma_bao_tri              INT IDENTITY(1,1) PRIMARY KEY,
    nxv_ma_thiet_bi             INT NOT NULL FOREIGN KEY REFERENCES G6ThietBi(g6_ma_thiet_bi) ON DELETE CASCADE,
    nxv_ma_chi_nhanh            INT NULL FOREIGN KEY REFERENCES G6ChiNhanh(g6_ma_chi_nhanh) ON DELETE SET NULL,
    nxv_loai                    NVARCHAR(30) NOT NULL DEFAULT 'dinh_ky',
    nxv_ngay_bao_tri            DATE NOT NULL,
    nxv_ngay_hoan_thanh         DATE NULL,
    nxv_nguoi_thuc_hien         NVARCHAR(100) NULL,
    nxv_noi_dung                NVARCHAR(MAX) NOT NULL,
    nxv_chi_phi                 DECIMAL(15,0) NOT NULL DEFAULT 0,
    nxv_ket_qua                 NVARCHAR(30) NOT NULL DEFAULT 'cho_xu_ly',
    nxv_ghi_chu                 NVARCHAR(MAX) NULL,
    nxv_ngay_bao_tri_tiep_theo  DATE NULL,
    nxv_ngay_tao                DATETIME2 NOT NULL DEFAULT GETDATE(),
    g6_deleted_at               DATETIME2 NULL DEFAULT NULL
);

-- Phiếu sửa chữa thiết bị
CREATE TABLE NxvPhieuSuaChua (
    nxv_ma_phieu        INT IDENTITY(1,1) PRIMARY KEY,
    nxv_ma_thiet_bi     INT NOT NULL FOREIGN KEY REFERENCES G6ThietBi(g6_ma_thiet_bi) ON DELETE CASCADE,
    nxv_ma_chi_nhanh    INT NULL FOREIGN KEY REFERENCES G6ChiNhanh(g6_ma_chi_nhanh) ON DELETE SET NULL,
    nxv_so_phieu        NVARCHAR(30) NOT NULL UNIQUE,
    nxv_ngay_tao_phieu  DATE NOT NULL,
    nxv_mo_ta_su_co     NVARCHAR(MAX) NOT NULL,
    nxv_don_vi_sua_chua NVARCHAR(200) NULL,
    nxv_chi_phi_du_kien DECIMAL(15,0) NULL,
    nxv_chi_phi_thuc_te DECIMAL(15,0) NULL,
    nxv_ngay_gui_sua    DATE NULL,
    nxv_ngay_nhan_lai   DATE NULL,
    nxv_trang_thai      NVARCHAR(30) NOT NULL DEFAULT 'cho_xu_ly',
    nxv_ket_qua_sua_chua NVARCHAR(MAX) NULL,
    nxv_ngay_tao        DATETIME2 NOT NULL DEFAULT GETDATE(),
    g6_deleted_at       DATETIME2 NULL DEFAULT NULL
);

-- Sự kiện / Flash sale
CREATE TABLE NxvSuKien (
    nxv_ma_su_kien      INT IDENTITY(1,1) PRIMARY KEY,
    nxv_ma_chi_nhanh    INT NULL FOREIGN KEY REFERENCES G6ChiNhanh(g6_ma_chi_nhanh) ON DELETE SET NULL,
    nxv_ten             NVARCHAR(200) NOT NULL,
    nxv_mo_ta           NVARCHAR(MAX) NULL,
    nxv_loai            NVARCHAR(30) NOT NULL DEFAULT 'su_kien',
    nxv_hinh_anh        NVARCHAR(500) NULL,
    nxv_ngay_bat_dau    DATETIME2 NOT NULL,
    nxv_ngay_ket_thuc   DATETIME2 NOT NULL,
    nxv_dia_diem        NVARCHAR(255) NULL,
    nxv_suc_chua        INT NULL,
    nxv_gia_ve          DECIMAL(15,0) NOT NULL DEFAULT 0,
    nxv_gia_giam        DECIMAL(15,0) NULL,
    nxv_ma_goi_ap_dung  INT NULL FOREIGN KEY REFERENCES G6GoiTap(g6_ma_goi_tap) ON DELETE SET NULL,
    nxv_la_hoat_dong    BIT NOT NULL DEFAULT 1,
    nxv_ngay_tao        DATETIME2 NOT NULL DEFAULT GETDATE(),
    g6_deleted_at       DATETIME2 NULL DEFAULT NULL
);

-- Đăng ký sự kiện
CREATE TABLE NxvDangKySuKien (
    nxv_ma_dang_ky      INT IDENTITY(1,1) PRIMARY KEY,
    nxv_ma_su_kien      INT NOT NULL FOREIGN KEY REFERENCES NxvSuKien(nxv_ma_su_kien) ON DELETE CASCADE,
    nxv_ma_hoi_vien     INT NULL FOREIGN KEY REFERENCES G6HoiVien(g6_ma_hoi_vien) ON DELETE SET NULL,
    nxv_ma_khach_hang   INT NULL FOREIGN KEY REFERENCES G6KhachHang(g6_ma_khach_hang) ON DELETE SET NULL,
    nxv_ho_ten          NVARCHAR(100) NOT NULL,
    nxv_so_dien_thoai   NVARCHAR(15) NULL,
    nxv_email           NVARCHAR(100) NULL,
    nxv_so_ve           INT NOT NULL DEFAULT 1,
    nxv_tong_tien       DECIMAL(15,0) NOT NULL DEFAULT 0,
    nxv_trang_thai      NVARCHAR(20) NOT NULL DEFAULT 'cho_xac_nhan',
    nxv_ma_qr           NVARCHAR(100) NULL UNIQUE,
    nxv_ngay_tao        DATETIME2 NOT NULL DEFAULT GETDATE(),
    g6_deleted_at       DATETIME2 NULL DEFAULT NULL
);
