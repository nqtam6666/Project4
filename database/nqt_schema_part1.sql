-- ============================================================
-- NQT GYM MANAGEMENT + SUPPLEMENT STORE
-- MySQL Schema - Part 1: Group 1-5
-- GROUP 1: CẤU HÌNH | GROUP 2: NGƯỜI DÙNG & PHÂN QUYỀN
-- GROUP 3: CHI NHÁNH | GROUP 4: NHÂN VIÊN | GROUP 5: HỘI VIÊN
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- GROUP 1: CẤU HÌNH HỆ THỐNG
-- ============================================================

CREATE TABLE NqtCauHinh (
    nqt_ma_cau_hinh     INT             NOT NULL AUTO_INCREMENT,
    nqt_khoa            VARCHAR(100)    NOT NULL COMMENT '''nqt_ten_website'', ''nqt_gio_mo_cua''',
    nqt_gia_tri         TEXT            NULL,
    nqt_kieu_du_lieu    VARCHAR(20)     NOT NULL DEFAULT 'string' COMMENT '''string'',''int'',''bool'',''json''',
    nqt_nhom            VARCHAR(50)     NOT NULL COMMENT '''website'',''security'',''email'',''payment'',''theme''',
    nqt_mo_ta           VARCHAR(255)    NULL,
    nqt_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_cau_hinh),
    UNIQUE KEY uk_nqt_cau_hinh_khoa (nqt_khoa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Dynamic config - không hardcode';

-- Seed data cấu hình mặc định
INSERT INTO NqtCauHinh (nqt_khoa, nqt_gia_tri, nqt_kieu_du_lieu, nqt_nhom, nqt_mo_ta) VALUES
('nqt_ten_website',            'NQT Gym',     'string',  'website',  'Tên website'),
('nqt_mo_ta_website',          '',            'string',  'website',  'Mô tả website'),
('nqt_logo_url',               '',            'string',  'website',  'URL logo'),
('nqt_favicon_url',            '',            'string',  'website',  'URL favicon'),
('nqt_so_dien_thoai_hotline',  '',            'string',  'website',  'Hotline hiển thị'),
('nqt_email_lien_he',          '',            'string',  'website',  'Email liên hệ'),
('nqt_dia_chi_tru_so',         '',            'string',  'website',  'Địa chỉ trụ sở'),
('nqt_facebook_url',           '',            'string',  'website',  'Facebook fanpage'),
('nqt_zalo_url',               '',            'string',  'website',  'Zalo OA'),
('nqt_instagram_url',          '',            'string',  'website',  'Instagram'),
('nqt_youtube_url',            '',            'string',  'website',  'YouTube channel'),
('nqt_footer_noi_dung',        '',            'string',  'website',  'Nội dung footer'),
-- Security
('nqt_loai_ma_hoa_mat_khau',   'bcrypt',      'string',  'security', 'Thuật toán mã hóa: bcrypt|argon2|pbkdf2'),
('nqt_jwt_het_han_phut',       '60',          'int',     'security', 'JWT access token hết hạn (phút)'),
('nqt_jwt_refresh_ngay',       '7',           'int',     'security', 'JWT refresh token hết hạn (ngày)'),
('nqt_so_lan_dang_nhap_sai',   '5',           'int',     'security', 'Số lần đăng nhập sai tối đa'),
('nqt_khoa_tai_khoan_phut',    '30',          'int',     'security', 'Khóa tài khoản sau N phút'),
('nqt_do_dai_mat_khau_toi_thieu','8',         'int',     'security', 'Độ dài mật khẩu tối thiểu'),
-- Email SMTP
('nqt_smtp_host',              '',            'string',  'email',    'SMTP host'),
('nqt_smtp_port',              '587',         'int',     'email',    'SMTP port'),
('nqt_smtp_username',          '',            'string',  'email',    'SMTP username'),
('nqt_smtp_mat_khau',          '',            'string',  'email',    'SMTP password'),
('nqt_smtp_ma_hoa',            'TLS',         'string',  'email',    'SMTP encryption: TLS|SSL|None'),
('nqt_email_gui_di',           '',            'string',  'email',    'From email address'),
('nqt_ten_email_gui_di',       '',            'string',  'email',    'From email name'),
-- Payment
('nqt_don_vi_tien_te',         'VND',         'string',  'payment',  'Đơn vị tiền tệ'),
('nqt_vnpay_terminal_id',      '',            'string',  'payment',  'VNPay Terminal ID'),
('nqt_vnpay_secret_key',       '',            'string',  'payment',  'VNPay Secret Key'),
('nqt_momo_partner_code',      '',            'string',  'payment',  'MoMo Partner Code'),
('nqt_momo_access_key',        '',            'string',  'payment',  'MoMo Access Key'),
('nqt_momo_secret_key',        '',            'string',  'payment',  'MoMo Secret Key'),
('nqt_thue_vat_phan_tram',     '0',           'int',     'payment',  'Thuế VAT %'),
-- Notification
('nqt_so_ngay_nhac_het_han',   '7',           'int',     'website',  'Nhắc hội viên trước N ngày hết hạn'),
('nqt_so_ngay_nhac_lan_2',     '3',           'int',     'website',  'Nhắc lần 2 trước N ngày hết hạn'),
-- Loyalty
('nqt_diem_tren_moi_1000_dong','1',           'int',     'website',  '1 điểm / N đồng chi tiêu'),
('nqt_1_diem_bang_dong',       '100',         'int',     'website',  '1 điểm = N đồng khi dùng'),
-- OTP
('nqt_otp_het_han_phut',       '5',           'int',     'security', 'OTP hết hạn sau N phút'),
('nqt_otp_so_lan_nhap_sai',    '3',           'int',     'security', 'OTP sai tối đa N lần'),
-- Theme
('nqt_mau_chinh',              '#0d6efd',     'string',  'theme',    'Màu chủ đạo (hex)'),
('nqt_mau_phu',                '#6c757d',     'string',  'theme',    'Màu phụ (hex)'),
('nqt_che_do_toi',             '0',           'bool',    'theme',    'Bật chế độ tối mặc định');

-- ============================================================
-- GROUP 2: NGƯỜI DÙNG & PHÂN QUYỀN
-- ============================================================

CREATE TABLE NqtVaiTro (
    nqt_ma_vai_tro      INT             NOT NULL AUTO_INCREMENT,
    nqt_ten_vai_tro     VARCHAR(50)     NOT NULL COMMENT '''NqtQuanTri'',''NqtQuanLy'',''NqtHuanLuyenVien'',''NqtLeTan''',
    nqt_mo_ta           VARCHAR(255)    NULL,
    PRIMARY KEY (nqt_ma_vai_tro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO NqtVaiTro (nqt_ten_vai_tro, nqt_mo_ta) VALUES
('NqtQuanTri',       'Quản trị hệ thống - toàn quyền'),
('NqtQuanLy',        'Quản lý chi nhánh'),
('NqtHuanLuyenVien', 'Huấn luyện viên PT'),
('NqtLeTan',         'Lễ tân - check-in, đăng ký hội viên');

CREATE TABLE NqtQuyenHan (
    nqt_ma_quyen        INT             NOT NULL AUTO_INCREMENT,
    nqt_ten_quyen       VARCHAR(100)    NOT NULL COMMENT '''nqt_xem_doanh_thu'',''nqt_sua_hoi_vien''',
    nqt_nhom_quyen      VARCHAR(50)     NOT NULL COMMENT '''hoi_vien'',''san_pham'',''bao_cao'',''cau_hinh''',
    PRIMARY KEY (nqt_ma_quyen)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed quyền hạn
INSERT INTO NqtQuyenHan (nqt_ten_quyen, nqt_nhom_quyen) VALUES
('nqt_xem_hoi_vien',        'hoi_vien'),
('nqt_tao_hoi_vien',        'hoi_vien'),
('nqt_sua_hoi_vien',        'hoi_vien'),
('nqt_xoa_hoi_vien',        'hoi_vien'),
('nqt_xem_san_pham',        'san_pham'),
('nqt_tao_san_pham',        'san_pham'),
('nqt_sua_san_pham',        'san_pham'),
('nqt_xoa_san_pham',        'san_pham'),
('nqt_xem_don_hang',        'don_hang'),
('nqt_cap_nhat_don_hang',   'don_hang'),
('nqt_huy_don_hang',        'don_hang'),
('nqt_xem_doanh_thu',       'bao_cao'),
('nqt_xuat_bao_cao',        'bao_cao'),
('nqt_xem_cau_hinh',        'cau_hinh'),
('nqt_sua_cau_hinh',        'cau_hinh'),
('nqt_quan_ly_nhan_vien',   'nhan_vien'),
('nqt_xem_kho_hang',        'kho_hang'),
('nqt_dieu_chinh_kho',      'kho_hang'),
('nqt_checkin_hoi_vien',    'hoi_vien'),
('nqt_xem_lich_lop_hoc',    'lop_hoc'),
('nqt_quan_ly_lop_hoc',     'lop_hoc');

-- NqtChiNhanh phải tạo trước NqtNguoiDung (FK)
CREATE TABLE NqtChiNhanh (
    nqt_ma_chi_nhanh    INT             NOT NULL AUTO_INCREMENT,
    nqt_ten_chi_nhanh   VARCHAR(100)    NOT NULL,
    nqt_dia_chi         VARCHAR(255)    NULL,
    nqt_thanh_pho       VARCHAR(50)     NULL,
    nqt_tinh            VARCHAR(50)     NULL,
    nqt_hotline         VARCHAR(15)     NULL,
    nqt_email           VARCHAR(100)    NULL,
    nqt_gio_mo_cua      TIME            NULL,
    nqt_gio_dong_cua    TIME            NULL,
    nqt_gio_mo_lich     JSON            NULL COMMENT '{"mon":"8:00","tue":"8:00",...}',
    nqt_vi_do           DECIMAL(9,6)    NULL,
    nqt_kinh_do         DECIMAL(9,6)    NULL,
    nqt_google_maps_url VARCHAR(500)    NULL,
    nqt_hinh_anh        JSON            NULL COMMENT '["url1","url2"]',
    nqt_suc_chua_toi_da INT             NULL COMMENT 'Max members cùng lúc',
    nqt_co_sauna        TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_co_ho_boi       TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtNguoiDung (
    nqt_ma_nguoi_dung   INT             NOT NULL AUTO_INCREMENT,
    nqt_ten_dang_nhap   VARCHAR(50)     NOT NULL,
    nqt_mat_khau        VARCHAR(255)    NOT NULL,
    nqt_ho_ten          VARCHAR(100)    NOT NULL,
    nqt_email           VARCHAR(100)    NULL,
    nqt_so_dien_thoai   VARCHAR(15)     NULL,
    nqt_ma_chi_nhanh    INT             NULL COMMENT 'NULL = admin toàn hệ thống',
    nqt_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_lan_dang_nhap_sai INT           NOT NULL DEFAULT 0,
    nqt_khoa_den        DATETIME        NULL COMMENT 'Rate limiting - khóa đến thời điểm này',
    nqt_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_nguoi_dung),
    UNIQUE KEY uk_nqt_nguoi_dung_tendangnhap (nqt_ten_dang_nhap),
    UNIQUE KEY uk_nqt_nguoi_dung_email (nqt_email),
    KEY idx_nqt_nguoi_dung_chinhanh (nqt_ma_chi_nhanh),
    CONSTRAINT fk_nqt_nguoidung_chinhanh FOREIGN KEY (nqt_ma_chi_nhanh) REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtNguoiDungVaiTro (
    nqt_ma_nguoi_dung   INT             NOT NULL,
    nqt_ma_vai_tro      INT             NOT NULL,
    PRIMARY KEY (nqt_ma_nguoi_dung, nqt_ma_vai_tro),
    CONSTRAINT fk_nqt_ndvt_nguoidung FOREIGN KEY (nqt_ma_nguoi_dung) REFERENCES NqtNguoiDung (nqt_ma_nguoi_dung) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_ndvt_vaitro   FOREIGN KEY (nqt_ma_vai_tro)    REFERENCES NqtVaiTro (nqt_ma_vai_tro) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtVaiTroQuyen (
    nqt_ma_vai_tro      INT             NOT NULL,
    nqt_ma_quyen        INT             NOT NULL,
    PRIMARY KEY (nqt_ma_vai_tro, nqt_ma_quyen),
    CONSTRAINT fk_nqt_vtq_vaitro  FOREIGN KEY (nqt_ma_vai_tro) REFERENCES NqtVaiTro (nqt_ma_vai_tro) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_vtq_quyen   FOREIGN KEY (nqt_ma_quyen)   REFERENCES NqtQuyenHan (nqt_ma_quyen) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 3: CHI NHÁNH & THIẾT BỊ (NqtChiNhanh đã tạo ở trên)
-- ============================================================

CREATE TABLE NqtThietBi (
    nqt_ma_thiet_bi         INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_chi_nhanh        INT             NOT NULL,
    nqt_ten_thiet_bi        VARCHAR(100)    NOT NULL,
    nqt_thuong_hieu         VARCHAR(100)    NULL,
    nqt_model               VARCHAR(100)    NULL,
    nqt_so_serie            VARCHAR(100)    NULL,
    nqt_ngay_mua            DATE            NULL,
    nqt_ngay_bao_hanh_het   DATE            NULL,
    nqt_ngay_bao_tri_cuoi   DATE            NULL,
    nqt_ngay_bao_tri_tiep   DATE            NULL,
    nqt_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'hoat_dong' COMMENT '''hoat_dong'',''bao_tri'',''hong'',''thanh_ly''',
    nqt_hinh_anh            VARCHAR(500)    NULL,
    nqt_ghi_chu             TEXT            NULL,
    PRIMARY KEY (nqt_ma_thiet_bi),
    KEY idx_nqt_thietbi_chinhanh (nqt_ma_chi_nhanh),
    KEY idx_nqt_thietbi_trangthai (nqt_trang_thai),
    CONSTRAINT fk_nqt_thietbi_chinhanh FOREIGN KEY (nqt_ma_chi_nhanh) REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 4: NHÂN VIÊN
-- ============================================================

CREATE TABLE NqtNhanVien (
    nqt_ma_nhan_vien    INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_nguoi_dung   INT             NULL,
    nqt_ma_chi_nhanh    INT             NOT NULL,
    nqt_ho_ten          VARCHAR(100)    NOT NULL,
    nqt_ngay_sinh       DATE            NULL,
    nqt_gioi_tinh       VARCHAR(10)     NULL COMMENT '''nam'',''nu'',''khac''',
    nqt_so_dien_thoai   VARCHAR(15)     NULL,
    nqt_email           VARCHAR(100)    NULL,
    nqt_dia_chi         VARCHAR(255)    NULL,
    nqt_so_cccd         VARCHAR(20)     NULL,
    nqt_ngay_vao_lam    DATE            NOT NULL,
    nqt_ngay_nghi_viec  DATE            NULL,
    nqt_luong_co_ban    DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_trang_thai      VARCHAR(20)     NOT NULL DEFAULT 'dang_lam' COMMENT '''dang_lam'',''nghi_viec'',''thu_viec''',
    nqt_hinh_anh        VARCHAR(500)    NULL,
    nqt_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_nhan_vien),
    KEY idx_nqt_nhanvien_nguoidung (nqt_ma_nguoi_dung),
    KEY idx_nqt_nhanvien_chinhanh (nqt_ma_chi_nhanh),
    CONSTRAINT fk_nqt_nhanvien_nguoidung FOREIGN KEY (nqt_ma_nguoi_dung) REFERENCES NqtNguoiDung (nqt_ma_nguoi_dung) ON DELETE SET NULL,
    CONSTRAINT fk_nqt_nhanvien_chinhanh  FOREIGN KEY (nqt_ma_chi_nhanh)  REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtLichLamViec (
    nqt_ma_lich         INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_nhan_vien    INT             NOT NULL,
    nqt_ma_chi_nhanh    INT             NOT NULL,
    nqt_thu_trong_tuan  TINYINT         NOT NULL COMMENT '1=Thứ 2 ... 7=Chủ nhật',
    nqt_gio_bat_dau     TIME            NOT NULL,
    nqt_gio_ket_thuc    TIME            NOT NULL,
    nqt_tuan_hieu_luc   DATE            NULL COMMENT 'NULL = lặp mỗi tuần',
    PRIMARY KEY (nqt_ma_lich),
    KEY idx_nqt_lichlam_nhanvien (nqt_ma_nhan_vien),
    CONSTRAINT fk_nqt_lichlam_nhanvien FOREIGN KEY (nqt_ma_nhan_vien) REFERENCES NqtNhanVien (nqt_ma_nhan_vien) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_lichlam_chinhanh FOREIGN KEY (nqt_ma_chi_nhanh) REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 5: HỘI VIÊN
-- ============================================================

CREATE TABLE NqtHoiVien (
    nqt_ma_hoi_vien     INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_chi_nhanh    INT             NOT NULL COMMENT 'Chi nhánh đăng ký chính',
    nqt_ho_ten          VARCHAR(100)    NOT NULL,
    nqt_ngay_sinh       DATE            NULL,
    nqt_gioi_tinh       VARCHAR(10)     NULL,
    nqt_so_dien_thoai   VARCHAR(15)     NOT NULL,
    nqt_email           VARCHAR(100)    NULL,
    nqt_dia_chi         VARCHAR(255)    NULL,
    nqt_so_cccd         VARCHAR(20)     NULL,
    nqt_ngay_dang_ky    DATE            NOT NULL DEFAULT (CURRENT_DATE),
    nqt_anh_the         VARCHAR(500)    NULL,
    nqt_ma_qr           VARCHAR(100)    NOT NULL COMMENT 'QR check-in',
    nqt_nguon_gioi_thieu VARCHAR(100)   NULL COMMENT '''facebook'',''ban_be'',''truc_tiep''',
    nqt_ma_gioi_thieu   INT             NULL COMMENT 'FK tự tham chiếu - ai giới thiệu',
    nqt_ghi_chu         TEXT            NULL,
    nqt_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_hoi_vien),
    UNIQUE KEY uk_nqt_hoivien_sdt (nqt_so_dien_thoai),
    UNIQUE KEY uk_nqt_hoivien_qr (nqt_ma_qr),
    KEY idx_nqt_hoivien_chinhanh (nqt_ma_chi_nhanh),
    KEY idx_nqt_hoivien_gioi_thieu (nqt_ma_gioi_thieu),
    CONSTRAINT fk_nqt_hoivien_chinhanh    FOREIGN KEY (nqt_ma_chi_nhanh)  REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh),
    CONSTRAINT fk_nqt_hoivien_gioithieu   FOREIGN KEY (nqt_ma_gioi_thieu) REFERENCES NqtHoiVien (nqt_ma_hoi_vien) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtGoiTap (
    nqt_ma_goi_tap          INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_chi_nhanh        INT             NULL COMMENT 'NULL = áp dụng tất cả chi nhánh',
    nqt_ten_goi             VARCHAR(100)    NOT NULL,
    nqt_mo_ta               TEXT            NULL,
    nqt_so_ngay             INT             NOT NULL COMMENT '30, 90, 180, 365',
    nqt_gia                 DECIMAL(15,0)   NOT NULL,
    nqt_gia_khuyen_mai      DECIMAL(15,0)   NULL,
    nqt_so_luot_checkin_ngay INT            NOT NULL DEFAULT 1,
    nqt_duoc_dua_khach      TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_so_khach_duoc_dua   INT             NOT NULL DEFAULT 0,
    nqt_co_pt               TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_so_buoi_pt          INT             NOT NULL DEFAULT 0,
    nqt_co_sauna            TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_mau_hien_thi        VARCHAR(20)     NULL COMMENT 'Hex color cho card',
    nqt_la_noi_bat          TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    nqt_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_goi_tap),
    KEY idx_nqt_goitap_chinhanh (nqt_ma_chi_nhanh),
    CONSTRAINT fk_nqt_goitap_chinhanh FOREIGN KEY (nqt_ma_chi_nhanh) REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- NqtThanhToan tạo trước vì NqtDangKyGoiTap FK đến nó
-- (Tạo ở part 3, dùng ALTER TABLE để thêm FK sau)

CREATE TABLE NqtDangKyGoiTap (
    nqt_ma_dang_ky      INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_hoi_vien     INT             NOT NULL,
    nqt_ma_goi_tap      INT             NOT NULL,
    nqt_ma_chi_nhanh    INT             NOT NULL,
    nqt_ngay_bat_dau    DATE            NOT NULL,
    nqt_ngay_het_han    DATE            NOT NULL,
    nqt_gia_thuc_te     DECIMAL(15,0)   NOT NULL,
    nqt_ma_thanh_toan   INT             NULL COMMENT 'FK thêm sau khi tạo NqtThanhToan',
    nqt_trang_thai      VARCHAR(20)     NOT NULL DEFAULT 'dang_hoat_dong' COMMENT '''dang_hoat_dong'',''het_han'',''tam_dung'',''huy''',
    nqt_ly_do_tam_dung  VARCHAR(255)    NULL,
    nqt_ngay_tam_dung   DATE            NULL,
    nqt_ngay_tiep_tuc   DATE            NULL,
    nqt_tu_dong_gia_han TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_ghi_chu         TEXT            NULL,
    nqt_nguoi_tao       INT             NULL,
    nqt_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_dang_ky),
    KEY idx_nqt_dkgoitap_hoivien  (nqt_ma_hoi_vien),
    KEY idx_nqt_dkgoitap_goitap   (nqt_ma_goi_tap),
    KEY idx_nqt_dkgoitap_trangthai(nqt_trang_thai),
    KEY idx_nqt_dkgoitap_hethan   (nqt_ngay_het_han),
    CONSTRAINT fk_nqt_dkgoitap_hoivien  FOREIGN KEY (nqt_ma_hoi_vien)  REFERENCES NqtHoiVien (nqt_ma_hoi_vien),
    CONSTRAINT fk_nqt_dkgoitap_goitap   FOREIGN KEY (nqt_ma_goi_tap)   REFERENCES NqtGoiTap (nqt_ma_goi_tap),
    CONSTRAINT fk_nqt_dkgoitap_chinhanh FOREIGN KEY (nqt_ma_chi_nhanh) REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh),
    CONSTRAINT fk_nqt_dkgoitap_nguoitao FOREIGN KEY (nqt_nguoi_tao)    REFERENCES NqtNguoiDung (nqt_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtDiemDanh (
    nqt_ma_diem_danh    INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_dang_ky      INT             NOT NULL,
    nqt_ma_hoi_vien     INT             NOT NULL,
    nqt_ma_chi_nhanh    INT             NOT NULL,
    nqt_thoi_gian_vao   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_thoi_gian_ra    DATETIME        NULL,
    nqt_phuong_thuc     VARCHAR(20)     NOT NULL DEFAULT 'qr' COMMENT '''qr'',''the'',''nhan_vien'',''app''',
    nqt_nguoi_xac_nhan  INT             NULL,
    nqt_ghi_chu         VARCHAR(255)    NULL,
    PRIMARY KEY (nqt_ma_diem_danh),
    KEY idx_nqt_diemdanh_hoivien  (nqt_ma_hoi_vien),
    KEY idx_nqt_diemdanh_dangky   (nqt_ma_dang_ky),
    KEY idx_nqt_diemdanh_thoigian (nqt_thoi_gian_vao),
    CONSTRAINT fk_nqt_diemdanh_dangky    FOREIGN KEY (nqt_ma_dang_ky)    REFERENCES NqtDangKyGoiTap (nqt_ma_dang_ky),
    CONSTRAINT fk_nqt_diemdanh_hoivien   FOREIGN KEY (nqt_ma_hoi_vien)   REFERENCES NqtHoiVien (nqt_ma_hoi_vien),
    CONSTRAINT fk_nqt_diemdanh_chinhanh  FOREIGN KEY (nqt_ma_chi_nhanh)  REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh),
    CONSTRAINT fk_nqt_diemdanh_nguoixn   FOREIGN KEY (nqt_nguoi_xac_nhan) REFERENCES NqtNguoiDung (nqt_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtChiSoCoThe (
    nqt_ma_chi_so       INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_hoi_vien     INT             NOT NULL,
    nqt_ngay_do         DATE            NOT NULL,
    nqt_can_nang        DECIMAL(5,2)    NULL COMMENT 'kg',
    nqt_chieu_cao       DECIMAL(5,2)    NULL COMMENT 'cm',
    nqt_chi_so_bmi      DECIMAL(5,2)    NULL COMMENT 'Tính tự động',
    nqt_ti_le_mo        DECIMAL(5,2)    NULL COMMENT '%',
    nqt_ti_le_co        DECIMAL(5,2)    NULL COMMENT '%',
    nqt_ti_le_nuoc      DECIMAL(5,2)    NULL COMMENT '%',
    nqt_khoi_luong_co   DECIMAL(5,2)    NULL COMMENT 'kg',
    nqt_vong_nguc       DECIMAL(5,2)    NULL COMMENT 'cm',
    nqt_vong_eo         DECIMAL(5,2)    NULL COMMENT 'cm',
    nqt_vong_hong       DECIMAL(5,2)    NULL COMMENT 'cm',
    nqt_vong_tay_trai   DECIMAL(5,2)    NULL COMMENT 'cm',
    nqt_vong_dui_trai   DECIMAL(5,2)    NULL COMMENT 'cm',
    nqt_nguoi_do        INT             NULL COMMENT 'PT hoặc tự nhập',
    nqt_ghi_chu         TEXT            NULL,
    nqt_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_chi_so),
    KEY idx_nqt_chisocothe_hoivien (nqt_ma_hoi_vien),
    KEY idx_nqt_chisocothe_ngaydo  (nqt_ngay_do),
    CONSTRAINT fk_nqt_chisocothe_hoivien FOREIGN KEY (nqt_ma_hoi_vien) REFERENCES NqtHoiVien (nqt_ma_hoi_vien) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_chisocothe_nguoido FOREIGN KEY (nqt_nguoi_do)    REFERENCES NqtNguoiDung (nqt_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
