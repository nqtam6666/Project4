-- ============================================================
-- G6 GYM MANAGEMENT + SUPPLEMENT STORE
-- SQL Server Schema - Part 1: Group 1-5
-- GROUP 1: CẤU HÌNH | GROUP 2: NGƯỜI DÙNG & PHÂN QUYỀN
-- GROUP 3: CHI NHÁNH | GROUP 4: NHÂN VIÊN | GROUP 5: HỘI VIÊN
-- ============================================================

-- ============================================================
-- GROUP 1: CẤU HÌNH HỆ THỐNG
-- ============================================================

CREATE TABLE G6CauHinh (
    g6_ma_cau_hinh     INT             NOT NULL IDENTITY(1,1),
    g6_khoa            NVARCHAR(100)   NOT NULL,
    g6_gia_tri         NVARCHAR(MAX)   NULL,
    g6_kieu_du_lieu    NVARCHAR(20)    NOT NULL DEFAULT 'string',
    g6_nhom            NVARCHAR(50)    NOT NULL,
    g6_mo_ta           NVARCHAR(255)   NULL,
    g6_ngay_cap_nhat   DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6CauHinh PRIMARY KEY (g6_ma_cau_hinh),
    CONSTRAINT UK_G6CauHinh_Khoa UNIQUE (g6_khoa)
);

-- Seed data cấu hình mặc định
INSERT INTO G6CauHinh (g6_khoa, g6_gia_tri, g6_kieu_du_lieu, g6_nhom, g6_mo_ta) VALUES
(N'g6_ten_website', N'G6 Gym', 'string', 'website', N'Tên website'),
(N'g6_mo_ta_website', N'', 'string', 'website', N'Mô tả website'),
(N'g6_logo_url', N'', 'string', 'website', N'URL logo'),
(N'g6_favicon_url', N'', 'string', 'website', N'URL favicon'),
(N'g6_so_dien_thoai_hotline', N'', 'string', 'website', N'Hotline hiển thị'),
(N'g6_email_lien_he', N'', 'string', 'website', N'Email liên hệ'),
(N'g6_dia_chi_tru_so', N'', 'string', 'website', N'Địa chỉ trụ sở'),
(N'g6_facebook_url', N'', 'string', 'website', N'Facebook fanpage'),
(N'g6_zalo_url', N'', 'string', 'website', N'Zalo OA'),
(N'g6_instagram_url', N'', 'string', 'website', N'Instagram'),
(N'g6_youtube_url', N'', 'string', 'website', N'YouTube channel'),
(N'g6_footer_noi_dung', N'', 'string', 'website', N'Nội dung footer'),
-- Security
(N'g6_loai_ma_hoa_mat_khau', N'bcrypt', 'string', 'security', N'Thuật toán mã hóa: bcrypt|argon2|pbkdf2'),
(N'g6_jwt_het_han_phut', N'60', 'int', 'security', N'JWT access token hết hạn (phút)'),
(N'g6_jwt_refresh_ngay', N'7', 'int', 'security', N'JWT refresh token hết hạn (ngày)'),
(N'g6_so_lan_dang_nhap_sai', N'5', 'int', 'security', N'Số lần đăng nhập sai tối đa'),
(N'g6_khoa_tai_khoan_phut', N'30', 'int', 'security', N'Khóa tài khoản sau N phút'),
(N'g6_do_dai_mat_khau_toi_thieu', N'8', 'int', 'security', N'Độ dài mật khẩu tối thiểu'),
-- Email SMTP
(N'g6_smtp_host', N'', 'string', 'email', N'SMTP host'),
(N'g6_smtp_port', N'587', 'int', 'email', N'SMTP port'),
(N'g6_smtp_username', N'', 'string', 'email', N'SMTP username'),
(N'g6_smtp_mat_khau', N'', 'string', 'email', N'SMTP password'),
(N'g6_smtp_ma_hoa', N'TLS', 'string', 'email', N'SMTP encryption: TLS|SSL|None'),
(N'g6_email_gui_di', N'', 'string', 'email', N'From email address'),
(N'g6_ten_email_gui_di', N'', 'string', 'email', N'From email name'),
-- Payment
(N'g6_don_vi_tien_te', N'VND', 'string', 'payment', N'Đơn vị tiền tệ'),
(N'g6_vnpay_terminal_id', N'', 'string', 'payment', N'VNPay Terminal ID'),
(N'g6_vnpay_secret_key', N'', 'string', 'payment', N'VNPay Secret Key'),
(N'g6_momo_partner_code', N'', 'string', 'payment', N'MoMo Partner Code'),
(N'g6_momo_access_key', N'', 'string', 'payment', N'MoMo Access Key'),
(N'g6_momo_secret_key', N'', 'string', 'payment', N'MoMo Secret Key'),
(N'g6_thue_vat_phan_tram', N'0', 'int', 'payment', N'Thuế VAT %'),
-- Notification
(N'g6_so_ngay_nhac_het_han', N'7', 'int', 'business', N'Nhắc hội viên trước N ngày hết hạn'),
(N'g6_so_ngay_nhac_lan_2', N'3', 'int', 'business', N'Nhắc lần 2 trước N ngày hết hạn'),
-- Loyalty
(N'g6_diem_tren_moi_1000_dong', N'1', 'int', 'loyalty', N'1 điểm / N đồng chi tiêu'),
(N'g6_1_diem_bang_dong', N'100', 'int', 'loyalty', N'1 điểm = N đồng khi dùng'),
-- OTP
(N'g6_otp_het_han_phut', N'5', 'int', 'security', N'OTP hết hạn sau N phút'),
(N'g6_otp_so_lan_nhap_sai', N'3', 'int', 'security', N'OTP sai tối đa N lần'),
-- Theme
(N'g6_mau_chinh', N'#0d6efd', 'string', 'theme', N'Màu chủ đạo (hex)'),
(N'g6_mau_phu', N'#6c757d', 'string', 'theme', N'Màu phụ (hex)'),
(N'g6_che_do_toi', N'0', 'bool', 'theme', N'Bật chế độ tối mặc định');

-- ============================================================
-- GROUP 2: NGƯỜI DÙNG & PHÂN QUYỀN
-- ============================================================

CREATE TABLE G6VaiTro (
    g6_ma_vai_tro      INT             NOT NULL IDENTITY(1,1),
    g6_ten_vai_tro     NVARCHAR(50)    NOT NULL,
    g6_mo_ta           NVARCHAR(255)   NULL,
    CONSTRAINT PK_G6VaiTro PRIMARY KEY (g6_ma_vai_tro)
);

INSERT INTO G6VaiTro (g6_ten_vai_tro, g6_mo_ta) VALUES
(N'G6QuanTri', N'Quản trị hệ thống - toàn quyền'),
(N'G6QuanLy', N'Quản lý chi nhánh'),
(N'G6HuanLuyenVien', N'Huấn luyện viên PT'),
(N'G6LeTan', N'Lễ tân - check-in, đăng ký hội viên');

CREATE TABLE G6QuyenHan (
    g6_ma_quyen        INT             NOT NULL IDENTITY(1,1),
    g6_ten_quyen       NVARCHAR(100)   NOT NULL,
    g6_nhom_quyen      NVARCHAR(50)    NOT NULL,
    CONSTRAINT PK_G6QuyenHan PRIMARY KEY (g6_ma_quyen)
);

INSERT INTO G6QuyenHan (g6_ten_quyen, g6_nhom_quyen) VALUES
(N'g6_xem_hoi_vien', N'hoi_vien'),
(N'g6_tao_hoi_vien', N'hoi_vien'),
(N'g6_sua_hoi_vien', N'hoi_vien'),
(N'g6_xoa_hoi_vien', N'hoi_vien'),
(N'g6_xem_san_pham', N'san_pham'),
(N'g6_tao_san_pham', N'san_pham'),
(N'g6_sua_san_pham', N'san_pham'),
(N'g6_xoa_san_pham', N'san_pham'),
(N'g6_xem_don_hang', N'don_hang'),
(N'g6_cap_nhat_don_hang', N'don_hang'),
(N'g6_huy_don_hang', N'don_hang'),
(N'g6_xem_doanh_thu', N'bao_cao'),
(N'g6_xuat_bao_cao', N'bao_cao'),
(N'g6_xem_cau_hinh', N'cau_hinh'),
(N'g6_sua_cau_hinh', N'cau_hinh'),
(N'g6_quan_ly_nhan_vien', N'nhan_vien'),
(N'g6_xem_kho_hang', N'kho_hang'),
(N'g6_dieu_chinh_kho', N'kho_hang'),
(N'g6_checkin_hoi_vien', N'hoi_vien'),
(N'g6_xem_lich_lop_hoc', N'lop_hoc'),
(N'g6_quan_ly_lop_hoc', N'lop_hoc');

-- ============================================================
-- GROUP 3: CHI NHÁNH
-- ============================================================

CREATE TABLE G6ChiNhanh (
    g6_ma_chi_nhanh    INT             NOT NULL IDENTITY(1,1),
    g6_ten_chi_nhanh   NVARCHAR(100)   NOT NULL,
    g6_dia_chi         NVARCHAR(255)   NULL,
    g6_thanh_pho       NVARCHAR(50)    NULL,
    g6_tinh            NVARCHAR(50)    NULL,
    g6_hotline         NVARCHAR(15)    NULL,
    g6_email           NVARCHAR(100)   NULL,
    g6_gio_mo_cua      TIME            NULL,
    g6_gio_dong_cua    TIME            NULL,
    g6_gio_mo_lich     NVARCHAR(MAX)   NULL,
    g6_vi_do           DECIMAL(9,6)    NULL,
    g6_kinh_do         DECIMAL(9,6)    NULL,
    g6_google_maps_url NVARCHAR(500)   NULL,
    g6_hinh_anh        NVARCHAR(MAX)   NULL,
    g6_suc_chua_toi_da INT             NULL,
    g6_co_sauna        BIT             NOT NULL DEFAULT 0,
    g6_co_ho_boi       BIT             NOT NULL DEFAULT 0,
    g6_la_hoat_dong    BIT             NOT NULL DEFAULT 1,
    g6_ngay_tao        DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6ChiNhanh PRIMARY KEY (g6_ma_chi_nhanh)
);

CREATE TABLE G6NguoiDung (
    g6_ma_nguoi_dung   INT             NOT NULL IDENTITY(1,1),
    g6_ten_dang_nhap   NVARCHAR(50)    NOT NULL,
    g6_mat_khau        NVARCHAR(255)   NOT NULL,
    g6_ho_ten          NVARCHAR(100)   NOT NULL,
    g6_email           NVARCHAR(100)   NULL,
    g6_so_dien_thoai   NVARCHAR(15)    NULL,
    g6_ma_chi_nhanh    INT             NULL,
    g6_la_hoat_dong    BIT             NOT NULL DEFAULT 1,
    g6_lan_dang_nhap_sai INT           NOT NULL DEFAULT 0,
    g6_khoa_den        DATETIME2       NULL,
    g6_totp_secret     NVARCHAR(32)    NULL,
    g6_ngay_tao        DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_cap_nhat   DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6NguoiDung PRIMARY KEY (g6_ma_nguoi_dung),
    CONSTRAINT UK_G6NguoiDung_TenDangNhap UNIQUE (g6_ten_dang_nhap),
    CONSTRAINT UK_G6NguoiDung_Email UNIQUE (g6_email),
    CONSTRAINT FK_G6NguoiDung_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh) ON DELETE SET NULL
);

CREATE TABLE G6NguoiDungVaiTro (
    g6_ma_nguoi_dung   INT             NOT NULL,
    g6_ma_vai_tro      INT             NOT NULL,
    CONSTRAINT PK_G6NguoiDungVaiTro PRIMARY KEY (g6_ma_nguoi_dung, g6_ma_vai_tro),
    CONSTRAINT FK_G6NDVT_NguoiDung FOREIGN KEY (g6_ma_nguoi_dung) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE CASCADE,
    CONSTRAINT FK_G6NDVT_VaiTro FOREIGN KEY (g6_ma_vai_tro) REFERENCES G6VaiTro (g6_ma_vai_tro) ON DELETE CASCADE
);

CREATE TABLE G6VaiTroQuyen (
    g6_ma_vai_tro      INT             NOT NULL,
    g6_ma_quyen        INT             NOT NULL,
    CONSTRAINT PK_G6VaiTroQuyen PRIMARY KEY (g6_ma_vai_tro, g6_ma_quyen),
    CONSTRAINT FK_G6VTQ_VaiTro FOREIGN KEY (g6_ma_vai_tro) REFERENCES G6VaiTro (g6_ma_vai_tro) ON DELETE CASCADE,
    CONSTRAINT FK_G6VTQ_Quyen FOREIGN KEY (g6_ma_quyen) REFERENCES G6QuyenHan (g6_ma_quyen) ON DELETE CASCADE
);

CREATE TABLE G6ThietBi (
    g6_ma_thiet_bi         INT             NOT NULL IDENTITY(1,1),
    g6_ma_chi_nhanh        INT             NOT NULL,
    g6_ten_thiet_bi        NVARCHAR(100)   NOT NULL,
    g6_thuong_hieu         NVARCHAR(100)   NULL,
    g6_model               NVARCHAR(100)   NULL,
    g6_so_serie            NVARCHAR(100)   NULL,
    g6_ngay_mua            DATE            NULL,
    g6_ngay_bao_hanh_het   DATE            NULL,
    g6_ngay_bao_tri_cuoi   DATE            NULL,
    g6_ngay_bao_tri_tiep   DATE            NULL,
    g6_trang_thai          NVARCHAR(20)    NOT NULL DEFAULT 'hoat_dong',
    g6_hinh_anh            NVARCHAR(500)   NULL,
    g6_ghi_chu             NVARCHAR(MAX)   NULL,
    CONSTRAINT PK_G6ThietBi PRIMARY KEY (g6_ma_thiet_bi),
    CONSTRAINT FK_G6ThietBi_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh) ON DELETE CASCADE
);

-- ============================================================
-- GROUP 4: NHÂN VIÊN
-- ============================================================

CREATE TABLE G6NhanVien (
    g6_ma_nhan_vien    INT             NOT NULL IDENTITY(1,1),
    g6_ma_nguoi_dung   INT             NULL,
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_ho_ten          NVARCHAR(100)   NOT NULL,
    g6_ngay_sinh       DATE            NULL,
    g6_gioi_tinh       NVARCHAR(10)    NULL,
    g6_so_dien_thoai   NVARCHAR(15)    NULL,
    g6_email           NVARCHAR(100)   NULL,
    g6_dia_chi         NVARCHAR(255)   NULL,
    g6_so_cccd         NVARCHAR(20)    NULL,
    g6_ngay_vao_lam    DATE            NOT NULL,
    g6_ngay_nghi_viec  DATE            NULL,
    g6_luong_co_ban    DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_trang_thai      NVARCHAR(20)    NOT NULL DEFAULT 'dang_lam',
    g6_hinh_anh        NVARCHAR(500)   NULL,
    g6_ngay_tao        DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6NhanVien PRIMARY KEY (g6_ma_nhan_vien),
    CONSTRAINT FK_G6NhanVien_NguoiDung FOREIGN KEY (g6_ma_nguoi_dung) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL,
    CONSTRAINT FK_G6NhanVien_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
);

CREATE TABLE G6LichLamViec (
    g6_ma_lich         INT             NOT NULL IDENTITY(1,1),
    g6_ma_nhan_vien    INT             NOT NULL,
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_thu_trong_tuan  TINYINT         NOT NULL,
    g6_gio_bat_dau     TIME            NOT NULL,
    g6_gio_ket_thuc    TIME            NOT NULL,
    g6_tuan_hieu_luc   DATE            NULL,
    CONSTRAINT PK_G6LichLamViec PRIMARY KEY (g6_ma_lich),
    CONSTRAINT FK_G6LichLam_NhanVien FOREIGN KEY (g6_ma_nhan_vien) REFERENCES G6NhanVien (g6_ma_nhan_vien) ON DELETE CASCADE,
    CONSTRAINT FK_G6LichLam_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
);

-- ============================================================
-- GROUP 5: HỘI VIÊN
-- ============================================================

CREATE TABLE G6HoiVien (
    g6_ma_hoi_vien     INT             NOT NULL IDENTITY(1,1),
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_ho_ten          NVARCHAR(100)   NOT NULL,
    g6_ngay_sinh       DATE            NULL,
    g6_gioi_tinh       NVARCHAR(10)    NULL,
    g6_so_dien_thoai   NVARCHAR(15)    NOT NULL,
    g6_email           NVARCHAR(100)   NULL,
    g6_dia_chi         NVARCHAR(255)   NULL,
    g6_so_cccd         NVARCHAR(20)    NULL,
    g6_ngay_dang_ky    DATE            NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    g6_anh_the         NVARCHAR(500)   NULL,
    g6_ma_qr           NVARCHAR(100)   NOT NULL,
    g6_nguon_gioi_thieu NVARCHAR(100)  NULL,
    g6_ma_gioi_thieu   INT             NULL,
    g6_ghi_chu         NVARCHAR(MAX)   NULL,
    g6_la_hoat_dong    BIT             NOT NULL DEFAULT 1,
    g6_ngay_tao        DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_cap_nhat   DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6HoiVien PRIMARY KEY (g6_ma_hoi_vien),
    CONSTRAINT UK_G6HoiVien_SDT UNIQUE (g6_so_dien_thoai),
    CONSTRAINT UK_G6HoiVien_QR UNIQUE (g6_ma_qr),
    CONSTRAINT FK_G6HoiVien_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh),
    CONSTRAINT FK_G6HoiVien_GioiThieu FOREIGN KEY (g6_ma_gioi_thieu) REFERENCES G6HoiVien (g6_ma_hoi_vien)
);

CREATE TABLE G6GoiTap (
    g6_ma_goi_tap          INT             NOT NULL IDENTITY(1,1),
    g6_ma_chi_nhanh        INT             NULL,
    g6_ten_goi             NVARCHAR(100)   NOT NULL,
    g6_mo_ta               NVARCHAR(MAX)   NULL,
    g6_so_ngay             INT             NOT NULL,
    g6_gia                 DECIMAL(15,0)   NOT NULL,
    g6_gia_khuyen_mai      DECIMAL(15,0)   NULL,
    g6_so_luot_checkin_ngay INT            NOT NULL DEFAULT 1,
    g6_duoc_dua_khach      BIT             NOT NULL DEFAULT 0,
    g6_so_khach_duoc_dua   INT             NOT NULL DEFAULT 0,
    g6_co_pt               BIT             NOT NULL DEFAULT 0,
    g6_so_buoi_pt          INT             NOT NULL DEFAULT 0,
    g6_co_sauna            BIT             NOT NULL DEFAULT 0,
    g6_mau_hien_thi        NVARCHAR(20)    NULL,
    g6_la_noi_bat          BIT             NOT NULL DEFAULT 0,
    g6_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    g6_la_hoat_dong        BIT             NOT NULL DEFAULT 1,
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6GoiTap PRIMARY KEY (g6_ma_goi_tap),
    CONSTRAINT FK_G6GoiTap_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh) ON DELETE SET NULL
);

CREATE TABLE G6DangKyGoiTap (
    g6_ma_dang_ky      INT             NOT NULL IDENTITY(1,1),
    g6_ma_hoi_vien     INT             NOT NULL,
    g6_ma_goi_tap      INT             NOT NULL,
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_ngay_bat_dau    DATE            NOT NULL,
    g6_ngay_het_han    DATE            NOT NULL,
    g6_gia_thuc_te     DECIMAL(15,0)   NOT NULL,
    g6_ma_thanh_toan   INT             NULL,
    g6_trang_thai      NVARCHAR(20)    NOT NULL DEFAULT 'dang_hoat_dong',
    g6_ly_do_tam_dung  NVARCHAR(255)   NULL,
    g6_ngay_tam_dung   DATE            NULL,
    g6_ngay_tiep_tuc   DATE            NULL,
    g6_tu_dong_gia_han BIT             NOT NULL DEFAULT 0,
    g6_ghi_chu         NVARCHAR(MAX)   NULL,
    g6_nguoi_tao       INT             NULL,
    g6_ngay_tao        DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6DangKyGoiTap PRIMARY KEY (g6_ma_dang_ky),
    CONSTRAINT FK_G6DKGT_HoiVien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien),
    CONSTRAINT FK_G6DKGT_GoiTap FOREIGN KEY (g6_ma_goi_tap) REFERENCES G6GoiTap (g6_ma_goi_tap),
    CONSTRAINT FK_G6DKGT_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh),
    CONSTRAINT FK_G6DKGT_NguoiTao FOREIGN KEY (g6_nguoi_tao) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
);

CREATE TABLE G6DiemDanh (
    g6_ma_diem_danh    INT             NOT NULL IDENTITY(1,1),
    g6_ma_dang_ky      INT             NOT NULL,
    g6_ma_hoi_vien     INT             NOT NULL,
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_thoi_gian_vao   DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_thoi_gian_ra    DATETIME2       NULL,
    g6_phuong_thuc     NVARCHAR(20)    NOT NULL DEFAULT 'qr',
    g6_nguoi_xac_nhan  INT             NULL,
    g6_ghi_chu         NVARCHAR(255)   NULL,
    CONSTRAINT PK_G6DiemDanh PRIMARY KEY (g6_ma_diem_danh),
    CONSTRAINT FK_G6DD_DangKy FOREIGN KEY (g6_ma_dang_ky) REFERENCES G6DangKyGoiTap (g6_ma_dang_ky),
    CONSTRAINT FK_G6DD_HoiVien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien),
    CONSTRAINT FK_G6DD_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh),
    CONSTRAINT FK_G6DD_NguoiXN FOREIGN KEY (g6_nguoi_xac_nhan) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
);

CREATE TABLE G6ChiSoCoThe (
    g6_ma_chi_so       INT             NOT NULL IDENTITY(1,1),
    g6_ma_hoi_vien     INT             NOT NULL,
    g6_ngay_do         DATE            NOT NULL,
    g6_can_nang        DECIMAL(5,2)    NULL,
    g6_chieu_cao       DECIMAL(5,2)    NULL,
    g6_chi_so_bmi      DECIMAL(5,2)    NULL,
    g6_ti_le_mo        DECIMAL(5,2)    NULL,
    g6_ti_le_co        DECIMAL(5,2)    NULL,
    g6_ti_le_nuoc      DECIMAL(5,2)    NULL,
    g6_khoi_luong_co   DECIMAL(5,2)    NULL,
    g6_vong_nguc       DECIMAL(5,2)    NULL,
    g6_vong_eo         DECIMAL(5,2)    NULL,
    g6_vong_hong       DECIMAL(5,2)    NULL,
    g6_vong_tay_trai   DECIMAL(5,2)    NULL,
    g6_vong_dui_trai   DECIMAL(5,2)    NULL,
    g6_nguoi_do        INT             NULL,
    g6_ghi_chu         NVARCHAR(MAX)   NULL,
    g6_ngay_tao        DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6ChiSoCoThe PRIMARY KEY (g6_ma_chi_so),
    CONSTRAINT FK_G6CSCT_HoiVien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien) ON DELETE CASCADE,
    CONSTRAINT FK_G6CSCT_NguoiDo FOREIGN KEY (g6_nguoi_do) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
);

-- Index
CREATE INDEX IX_G6NguoiDung_ChiNhanh ON G6NguoiDung (g6_ma_chi_nhanh);
CREATE INDEX IX_G6ThietBi_ChiNhanh ON G6ThietBi (g6_ma_chi_nhanh);
CREATE INDEX IX_G6NhanVien_ChiNhanh ON G6NhanVien (g6_ma_chi_nhanh);
CREATE INDEX IX_G6HoiVien_ChiNhanh ON G6HoiVien (g6_ma_chi_nhanh);
CREATE INDEX IX_G6DangKyGoiTap_HoiVien ON G6DangKyGoiTap (g6_ma_hoi_vien);
CREATE INDEX IX_G6DangKyGoiTap_TrangThai ON G6DangKyGoiTap (g6_trang_thai);
CREATE INDEX IX_G6DiemDanh_HoiVien ON G6DiemDanh (g6_ma_hoi_vien);
CREATE INDEX IX_G6DiemDanh_ThoiGian ON G6DiemDanh (g6_thoi_gian_vao);

PRINT N'Part 1 - Hoàn thành!';
GO
