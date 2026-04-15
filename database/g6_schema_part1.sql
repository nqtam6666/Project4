-- ============================================================
-- G6 GYM MANAGEMENT + SUPPLEMENT STORE
-- MySQL Schema - Part 1: Group 1-5
-- GROUP 1: CẤU HÌNH | GROUP 2: NGƯỜI DÙNG & PHÂN QUYỀN
-- GROUP 3: CHI NHÁNH | GROUP 4: NHÂN VIÊN | GROUP 5: HỘI VIÊN
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- GROUP 1: CẤU HÌNH HỆ THỐNG
-- ============================================================

CREATE TABLE G6CauHinh (
    g6_ma_cau_hinh     INT             NOT NULL AUTO_INCREMENT,
    g6_khoa            VARCHAR(100)    NOT NULL COMMENT '''g6_ten_website'', ''g6_gio_mo_cua''',
    g6_gia_tri         TEXT            NULL,
    g6_kieu_du_lieu    VARCHAR(20)     NOT NULL DEFAULT 'string' COMMENT '''string'',''int'',''bool'',''json''',
    g6_nhom            VARCHAR(50)     NOT NULL COMMENT '''website'',''security'',''email'',''payment'',''theme''',
    g6_mo_ta           VARCHAR(255)    NULL,
    g6_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_cau_hinh),
    UNIQUE KEY uk_g6_cau_hinh_khoa (g6_khoa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Dynamic config - không hardcode';

-- Seed data cấu hình mặc định
INSERT INTO G6CauHinh (g6_khoa, g6_gia_tri, g6_kieu_du_lieu, g6_nhom, g6_mo_ta) VALUES
('g6_ten_website',            'G6 Gym',     'string',  'website',  'Tên website'),
('g6_mo_ta_website',          '',            'string',  'website',  'Mô tả website'),
('g6_logo_url',               '',            'string',  'website',  'URL logo'),
('g6_favicon_url',            '',            'string',  'website',  'URL favicon'),
('g6_so_dien_thoai_hotline',  '',            'string',  'website',  'Hotline hiển thị'),
('g6_email_lien_he',          '',            'string',  'website',  'Email liên hệ'),
('g6_dia_chi_tru_so',         '',            'string',  'website',  'Địa chỉ trụ sở'),
('g6_facebook_url',           '',            'string',  'website',  'Facebook fanpage'),
('g6_zalo_url',               '',            'string',  'website',  'Zalo OA'),
('g6_instagram_url',          '',            'string',  'website',  'Instagram'),
('g6_youtube_url',            '',            'string',  'website',  'YouTube channel'),
('g6_footer_noi_dung',        '',            'string',  'website',  'Nội dung footer'),
-- Security
('g6_loai_ma_hoa_mat_khau',   'bcrypt',      'string',  'security', 'Thuật toán mã hóa: bcrypt|argon2|pbkdf2'),
('g6_jwt_het_han_phut',       '60',          'int',     'security', 'JWT access token hết hạn (phút)'),
('g6_jwt_refresh_ngay',       '7',           'int',     'security', 'JWT refresh token hết hạn (ngày)'),
('g6_so_lan_dang_nhap_sai',   '5',           'int',     'security', 'Số lần đăng nhập sai tối đa'),
('g6_khoa_tai_khoan_phut',    '30',          'int',     'security', 'Khóa tài khoản sau N phút'),
('g6_do_dai_mat_khau_toi_thieu','8',         'int',     'security', 'Độ dài mật khẩu tối thiểu'),
-- Email SMTP
('g6_smtp_host',              '',            'string',  'email',    'SMTP host'),
('g6_smtp_port',              '587',         'int',     'email',    'SMTP port'),
('g6_smtp_username',          '',            'string',  'email',    'SMTP username'),
('g6_smtp_mat_khau',          '',            'string',  'email',    'SMTP password'),
('g6_smtp_ma_hoa',            'TLS',         'string',  'email',    'SMTP encryption: TLS|SSL|None'),
('g6_email_gui_di',           '',            'string',  'email',    'From email address'),
('g6_ten_email_gui_di',       '',            'string',  'email',    'From email name'),
-- Payment
('g6_don_vi_tien_te',         'VND',         'string',  'payment',  'Đơn vị tiền tệ'),
('g6_vnpay_terminal_id',      '',            'string',  'payment',  'VNPay Terminal ID'),
('g6_vnpay_secret_key',       '',            'string',  'payment',  'VNPay Secret Key'),
('g6_momo_partner_code',      '',            'string',  'payment',  'MoMo Partner Code'),
('g6_momo_access_key',        '',            'string',  'payment',  'MoMo Access Key'),
('g6_momo_secret_key',        '',            'string',  'payment',  'MoMo Secret Key'),
('g6_thue_vat_phan_tram',     '0',           'int',     'payment',  'Thuế VAT %'),
-- Notification
('g6_so_ngay_nhac_het_han',   '7',           'int',     'business', 'Nhắc hội viên trước N ngày hết hạn'),
('g6_so_ngay_nhac_lan_2',     '3',           'int',     'business', 'Nhắc lần 2 trước N ngày hết hạn'),
-- Loyalty
('g6_diem_tren_moi_1000_dong','1',           'int',     'loyalty',  '1 điểm / N đồng chi tiêu'),
('g6_1_diem_bang_dong',       '100',         'int',     'loyalty',  '1 điểm = N đồng khi dùng'),
-- OTP
('g6_otp_het_han_phut',       '5',           'int',     'security', 'OTP hết hạn sau N phút'),
('g6_otp_so_lan_nhap_sai',    '3',           'int',     'security', 'OTP sai tối đa N lần'),
-- Theme
('g6_mau_chinh',              '#0d6efd',     'string',  'theme',    'Màu chủ đạo (hex)'),
('g6_mau_phu',                '#6c757d',     'string',  'theme',    'Màu phụ (hex)'),
('g6_che_do_toi',             '0',           'bool',    'theme',    'Bật chế độ tối mặc định');

-- ============================================================
-- GROUP 2: NGƯỜI DÙNG & PHÂN QUYỀN
-- ============================================================

CREATE TABLE G6VaiTro (
    g6_ma_vai_tro      INT             NOT NULL AUTO_INCREMENT,
    g6_ten_vai_tro     VARCHAR(50)     NOT NULL COMMENT '''G6QuanTri'',''G6QuanLy'',''G6HuanLuyenVien'',''G6LeTan''',
    g6_mo_ta           VARCHAR(255)    NULL,
    PRIMARY KEY (g6_ma_vai_tro)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO G6VaiTro (g6_ten_vai_tro, g6_mo_ta) VALUES
('G6QuanTri',       'Quản trị hệ thống - toàn quyền'),
('G6QuanLy',        'Quản lý chi nhánh'),
('G6HuanLuyenVien', 'Huấn luyện viên PT'),
('G6LeTan',         'Lễ tân - check-in, đăng ký hội viên');

CREATE TABLE G6QuyenHan (
    g6_ma_quyen        INT             NOT NULL AUTO_INCREMENT,
    g6_ten_quyen       VARCHAR(100)    NOT NULL COMMENT '''g6_xem_doanh_thu'',''g6_sua_hoi_vien''',
    g6_nhom_quyen      VARCHAR(50)     NOT NULL COMMENT '''hoi_vien'',''san_pham'',''bao_cao'',''cau_hinh''',
    PRIMARY KEY (g6_ma_quyen)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed quyền hạn
INSERT INTO G6QuyenHan (g6_ten_quyen, g6_nhom_quyen) VALUES
('g6_xem_hoi_vien',        'hoi_vien'),
('g6_tao_hoi_vien',        'hoi_vien'),
('g6_sua_hoi_vien',        'hoi_vien'),
('g6_xoa_hoi_vien',        'hoi_vien'),
('g6_xem_san_pham',        'san_pham'),
('g6_tao_san_pham',        'san_pham'),
('g6_sua_san_pham',        'san_pham'),
('g6_xoa_san_pham',        'san_pham'),
('g6_xem_don_hang',        'don_hang'),
('g6_cap_nhat_don_hang',   'don_hang'),
('g6_huy_don_hang',        'don_hang'),
('g6_xem_doanh_thu',       'bao_cao'),
('g6_xuat_bao_cao',        'bao_cao'),
('g6_xem_cau_hinh',        'cau_hinh'),
('g6_sua_cau_hinh',        'cau_hinh'),
('g6_quan_ly_nhan_vien',   'nhan_vien'),
('g6_xem_kho_hang',        'kho_hang'),
('g6_dieu_chinh_kho',      'kho_hang'),
('g6_checkin_hoi_vien',    'hoi_vien'),
('g6_xem_lich_lop_hoc',    'lop_hoc'),
('g6_quan_ly_lop_hoc',     'lop_hoc');

-- G6ChiNhanh phải tạo trước G6NguoiDung (FK)
CREATE TABLE G6ChiNhanh (
    g6_ma_chi_nhanh    INT             NOT NULL AUTO_INCREMENT,
    g6_ten_chi_nhanh   VARCHAR(100)    NOT NULL,
    g6_dia_chi         VARCHAR(255)    NULL,
    g6_thanh_pho       VARCHAR(50)     NULL,
    g6_tinh            VARCHAR(50)     NULL,
    g6_hotline         VARCHAR(15)     NULL,
    g6_email           VARCHAR(100)    NULL,
    g6_gio_mo_cua      TIME            NULL,
    g6_gio_dong_cua    TIME            NULL,
    g6_gio_mo_lich     JSON            NULL COMMENT '{"mon":"8:00","tue":"8:00",...}',
    g6_vi_do           DECIMAL(9,6)    NULL,
    g6_kinh_do         DECIMAL(9,6)    NULL,
    g6_google_maps_url VARCHAR(500)    NULL,
    g6_hinh_anh        JSON            NULL COMMENT '["url1","url2"]',
    g6_suc_chua_toi_da INT             NULL COMMENT 'Max members cùng lúc',
    g6_co_sauna        TINYINT(1)      NOT NULL DEFAULT 0,
    g6_co_ho_boi       TINYINT(1)      NOT NULL DEFAULT 0,
    g6_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    g6_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6NguoiDung (
    g6_ma_nguoi_dung   INT             NOT NULL AUTO_INCREMENT,
    g6_ten_dang_nhap   VARCHAR(50)     NOT NULL,
    g6_mat_khau        VARCHAR(255)    NOT NULL,
    g6_ho_ten          VARCHAR(100)    NOT NULL,
    g6_email           VARCHAR(100)    NULL,
    g6_so_dien_thoai   VARCHAR(15)     NULL,
    g6_ma_chi_nhanh    INT             NULL COMMENT 'NULL = admin toàn hệ thống',
    g6_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    g6_lan_dang_nhap_sai INT           NOT NULL DEFAULT 0,
    g6_khoa_den        DATETIME        NULL COMMENT 'Rate limiting - khóa đến thời điểm này',
    g6_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_nguoi_dung),
    UNIQUE KEY uk_g6_nguoi_dung_tendangnhap (g6_ten_dang_nhap),
    UNIQUE KEY uk_g6_nguoi_dung_email (g6_email),
    KEY idx_g6_nguoi_dung_chinhanh (g6_ma_chi_nhanh),
    CONSTRAINT fk_g6_nguoidung_chinhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6NguoiDungVaiTro (
    g6_ma_nguoi_dung   INT             NOT NULL,
    g6_ma_vai_tro      INT             NOT NULL,
    PRIMARY KEY (g6_ma_nguoi_dung, g6_ma_vai_tro),
    CONSTRAINT fk_g6_ndvt_nguoidung FOREIGN KEY (g6_ma_nguoi_dung) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE CASCADE,
    CONSTRAINT fk_g6_ndvt_vaitro   FOREIGN KEY (g6_ma_vai_tro)    REFERENCES G6VaiTro (g6_ma_vai_tro) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6VaiTroQuyen (
    g6_ma_vai_tro      INT             NOT NULL,
    g6_ma_quyen        INT             NOT NULL,
    PRIMARY KEY (g6_ma_vai_tro, g6_ma_quyen),
    CONSTRAINT fk_g6_vtq_vaitro  FOREIGN KEY (g6_ma_vai_tro) REFERENCES G6VaiTro (g6_ma_vai_tro) ON DELETE CASCADE,
    CONSTRAINT fk_g6_vtq_quyen   FOREIGN KEY (g6_ma_quyen)   REFERENCES G6QuyenHan (g6_ma_quyen) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 3: CHI NHÁNH & THIẾT BỊ (G6ChiNhanh đã tạo ở trên)
-- ============================================================

CREATE TABLE G6ThietBi (
    g6_ma_thiet_bi         INT             NOT NULL AUTO_INCREMENT,
    g6_ma_chi_nhanh        INT             NOT NULL,
    g6_ten_thiet_bi        VARCHAR(100)    NOT NULL,
    g6_thuong_hieu         VARCHAR(100)    NULL,
    g6_model               VARCHAR(100)    NULL,
    g6_so_serie            VARCHAR(100)    NULL,
    g6_ngay_mua            DATE            NULL,
    g6_ngay_bao_hanh_het   DATE            NULL,
    g6_ngay_bao_tri_cuoi   DATE            NULL,
    g6_ngay_bao_tri_tiep   DATE            NULL,
    g6_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'hoat_dong' COMMENT '''hoat_dong'',''bao_tri'',''hong'',''thanh_ly''',
    g6_hinh_anh            VARCHAR(500)    NULL,
    g6_ghi_chu             TEXT            NULL,
    PRIMARY KEY (g6_ma_thiet_bi),
    KEY idx_g6_thietbi_chinhanh (g6_ma_chi_nhanh),
    KEY idx_g6_thietbi_trangthai (g6_trang_thai),
    CONSTRAINT fk_g6_thietbi_chinhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 4: NHÂN VIÊN
-- ============================================================

CREATE TABLE G6NhanVien (
    g6_ma_nhan_vien    INT             NOT NULL AUTO_INCREMENT,
    g6_ma_nguoi_dung   INT             NULL,
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_ho_ten          VARCHAR(100)    NOT NULL,
    g6_ngay_sinh       DATE            NULL,
    g6_gioi_tinh       VARCHAR(10)     NULL COMMENT '''nam'',''nu'',''khac''',
    g6_so_dien_thoai   VARCHAR(15)     NULL,
    g6_email           VARCHAR(100)    NULL,
    g6_dia_chi         VARCHAR(255)    NULL,
    g6_so_cccd         VARCHAR(20)     NULL,
    g6_ngay_vao_lam    DATE            NOT NULL,
    g6_ngay_nghi_viec  DATE            NULL,
    g6_luong_co_ban    DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_trang_thai      VARCHAR(20)     NOT NULL DEFAULT 'dang_lam' COMMENT '''dang_lam'',''nghi_viec'',''thu_viec''',
    g6_hinh_anh        VARCHAR(500)    NULL,
    g6_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_nhan_vien),
    KEY idx_g6_nhanvien_nguoidung (g6_ma_nguoi_dung),
    KEY idx_g6_nhanvien_chinhanh (g6_ma_chi_nhanh),
    CONSTRAINT fk_g6_nhanvien_nguoidung FOREIGN KEY (g6_ma_nguoi_dung) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL,
    CONSTRAINT fk_g6_nhanvien_chinhanh  FOREIGN KEY (g6_ma_chi_nhanh)  REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6LichLamViec (
    g6_ma_lich         INT             NOT NULL AUTO_INCREMENT,
    g6_ma_nhan_vien    INT             NOT NULL,
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_thu_trong_tuan  TINYINT         NOT NULL COMMENT '1=Thứ 2 ... 7=Chủ nhật',
    g6_gio_bat_dau     TIME            NOT NULL,
    g6_gio_ket_thuc    TIME            NOT NULL,
    g6_tuan_hieu_luc   DATE            NULL COMMENT 'NULL = lặp mỗi tuần',
    PRIMARY KEY (g6_ma_lich),
    KEY idx_g6_lichlam_nhanvien (g6_ma_nhan_vien),
    CONSTRAINT fk_g6_lichlam_nhanvien FOREIGN KEY (g6_ma_nhan_vien) REFERENCES G6NhanVien (g6_ma_nhan_vien) ON DELETE CASCADE,
    CONSTRAINT fk_g6_lichlam_chinhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 5: HỘI VIÊN
-- ============================================================

CREATE TABLE G6HoiVien (
    g6_ma_hoi_vien     INT             NOT NULL AUTO_INCREMENT,
    g6_ma_chi_nhanh    INT             NOT NULL COMMENT 'Chi nhánh đăng ký chính',
    g6_ho_ten          VARCHAR(100)    NOT NULL,
    g6_ngay_sinh       DATE            NULL,
    g6_gioi_tinh       VARCHAR(10)     NULL,
    g6_so_dien_thoai   VARCHAR(15)     NOT NULL,
    g6_email           VARCHAR(100)    NULL,
    g6_dia_chi         VARCHAR(255)    NULL,
    g6_so_cccd         VARCHAR(20)     NULL,
    g6_ngay_dang_ky    DATE            NOT NULL DEFAULT (CURRENT_DATE),
    g6_anh_the         VARCHAR(500)    NULL,
    g6_ma_qr           VARCHAR(100)    NOT NULL COMMENT 'QR check-in',
    g6_nguon_gioi_thieu VARCHAR(100)   NULL COMMENT '''facebook'',''ban_be'',''truc_tiep''',
    g6_ma_gioi_thieu   INT             NULL COMMENT 'FK tự tham chiếu - ai giới thiệu',
    g6_ghi_chu         TEXT            NULL,
    g6_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    g6_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_hoi_vien),
    UNIQUE KEY uk_g6_hoivien_sdt (g6_so_dien_thoai),
    UNIQUE KEY uk_g6_hoivien_qr (g6_ma_qr),
    KEY idx_g6_hoivien_chinhanh (g6_ma_chi_nhanh),
    KEY idx_g6_hoivien_gioi_thieu (g6_ma_gioi_thieu),
    CONSTRAINT fk_g6_hoivien_chinhanh    FOREIGN KEY (g6_ma_chi_nhanh)  REFERENCES G6ChiNhanh (g6_ma_chi_nhanh),
    CONSTRAINT fk_g6_hoivien_gioithieu   FOREIGN KEY (g6_ma_gioi_thieu) REFERENCES G6HoiVien (g6_ma_hoi_vien) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6GoiTap (
    g6_ma_goi_tap          INT             NOT NULL AUTO_INCREMENT,
    g6_ma_chi_nhanh        INT             NULL COMMENT 'NULL = áp dụng tất cả chi nhánh',
    g6_ten_goi             VARCHAR(100)    NOT NULL,
    g6_mo_ta               TEXT            NULL,
    g6_so_ngay             INT             NOT NULL COMMENT '30, 90, 180, 365',
    g6_gia                 DECIMAL(15,0)   NOT NULL,
    g6_gia_khuyen_mai      DECIMAL(15,0)   NULL,
    g6_so_luot_checkin_ngay INT            NOT NULL DEFAULT 1,
    g6_duoc_dua_khach      TINYINT(1)      NOT NULL DEFAULT 0,
    g6_so_khach_duoc_dua   INT             NOT NULL DEFAULT 0,
    g6_co_pt               TINYINT(1)      NOT NULL DEFAULT 0,
    g6_so_buoi_pt          INT             NOT NULL DEFAULT 0,
    g6_co_sauna            TINYINT(1)      NOT NULL DEFAULT 0,
    g6_mau_hien_thi        VARCHAR(20)     NULL COMMENT 'Hex color cho card',
    g6_la_noi_bat          TINYINT(1)      NOT NULL DEFAULT 0,
    g6_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    g6_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_goi_tap),
    KEY idx_g6_goitap_chinhanh (g6_ma_chi_nhanh),
    CONSTRAINT fk_g6_goitap_chinhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- G6ThanhToan tạo trước vì G6DangKyGoiTap FK đến nó
-- (Tạo ở part 3, dùng ALTER TABLE để thêm FK sau)

CREATE TABLE G6DangKyGoiTap (
    g6_ma_dang_ky      INT             NOT NULL AUTO_INCREMENT,
    g6_ma_hoi_vien     INT             NOT NULL,
    g6_ma_goi_tap      INT             NOT NULL,
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_ngay_bat_dau    DATE            NOT NULL,
    g6_ngay_het_han    DATE            NOT NULL,
    g6_gia_thuc_te     DECIMAL(15,0)   NOT NULL,
    g6_ma_thanh_toan   INT             NULL COMMENT 'FK thêm sau khi tạo G6ThanhToan',
    g6_trang_thai      VARCHAR(20)     NOT NULL DEFAULT 'dang_hoat_dong' COMMENT '''dang_hoat_dong'',''het_han'',''tam_dung'',''huy''',
    g6_ly_do_tam_dung  VARCHAR(255)    NULL,
    g6_ngay_tam_dung   DATE            NULL,
    g6_ngay_tiep_tuc   DATE            NULL,
    g6_tu_dong_gia_han TINYINT(1)      NOT NULL DEFAULT 0,
    g6_ghi_chu         TEXT            NULL,
    g6_nguoi_tao       INT             NULL,
    g6_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_dang_ky),
    KEY idx_g6_dkgoitap_hoivien  (g6_ma_hoi_vien),
    KEY idx_g6_dkgoitap_goitap   (g6_ma_goi_tap),
    KEY idx_g6_dkgoitap_trangthai(g6_trang_thai),
    KEY idx_g6_dkgoitap_hethan   (g6_ngay_het_han),
    CONSTRAINT fk_g6_dkgoitap_hoivien  FOREIGN KEY (g6_ma_hoi_vien)  REFERENCES G6HoiVien (g6_ma_hoi_vien),
    CONSTRAINT fk_g6_dkgoitap_goitap   FOREIGN KEY (g6_ma_goi_tap)   REFERENCES G6GoiTap (g6_ma_goi_tap),
    CONSTRAINT fk_g6_dkgoitap_chinhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh),
    CONSTRAINT fk_g6_dkgoitap_nguoitao FOREIGN KEY (g6_nguoi_tao)    REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6DiemDanh (
    g6_ma_diem_danh    INT             NOT NULL AUTO_INCREMENT,
    g6_ma_dang_ky      INT             NOT NULL,
    g6_ma_hoi_vien     INT             NOT NULL,
    g6_ma_chi_nhanh    INT             NOT NULL,
    g6_thoi_gian_vao   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_thoi_gian_ra    DATETIME        NULL,
    g6_phuong_thuc     VARCHAR(20)     NOT NULL DEFAULT 'qr' COMMENT '''qr'',''the'',''nhan_vien'',''app''',
    g6_nguoi_xac_nhan  INT             NULL,
    g6_ghi_chu         VARCHAR(255)    NULL,
    PRIMARY KEY (g6_ma_diem_danh),
    KEY idx_g6_diemdanh_hoivien  (g6_ma_hoi_vien),
    KEY idx_g6_diemdanh_dangky   (g6_ma_dang_ky),
    KEY idx_g6_diemdanh_thoigian (g6_thoi_gian_vao),
    CONSTRAINT fk_g6_diemdanh_dangky    FOREIGN KEY (g6_ma_dang_ky)    REFERENCES G6DangKyGoiTap (g6_ma_dang_ky),
    CONSTRAINT fk_g6_diemdanh_hoivien   FOREIGN KEY (g6_ma_hoi_vien)   REFERENCES G6HoiVien (g6_ma_hoi_vien),
    CONSTRAINT fk_g6_diemdanh_chinhanh  FOREIGN KEY (g6_ma_chi_nhanh)  REFERENCES G6ChiNhanh (g6_ma_chi_nhanh),
    CONSTRAINT fk_g6_diemdanh_nguoixn   FOREIGN KEY (g6_nguoi_xac_nhan) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6ChiSoCoThe (
    g6_ma_chi_so       INT             NOT NULL AUTO_INCREMENT,
    g6_ma_hoi_vien     INT             NOT NULL,
    g6_ngay_do         DATE            NOT NULL,
    g6_can_nang        DECIMAL(5,2)    NULL COMMENT 'kg',
    g6_chieu_cao       DECIMAL(5,2)    NULL COMMENT 'cm',
    g6_chi_so_bmi      DECIMAL(5,2)    NULL COMMENT 'Tính tự động',
    g6_ti_le_mo        DECIMAL(5,2)    NULL COMMENT '%',
    g6_ti_le_co        DECIMAL(5,2)    NULL COMMENT '%',
    g6_ti_le_nuoc      DECIMAL(5,2)    NULL COMMENT '%',
    g6_khoi_luong_co   DECIMAL(5,2)    NULL COMMENT 'kg',
    g6_vong_nguc       DECIMAL(5,2)    NULL COMMENT 'cm',
    g6_vong_eo         DECIMAL(5,2)    NULL COMMENT 'cm',
    g6_vong_hong       DECIMAL(5,2)    NULL COMMENT 'cm',
    g6_vong_tay_trai   DECIMAL(5,2)    NULL COMMENT 'cm',
    g6_vong_dui_trai   DECIMAL(5,2)    NULL COMMENT 'cm',
    g6_nguoi_do        INT             NULL COMMENT 'PT hoặc tự nhập',
    g6_ghi_chu         TEXT            NULL,
    g6_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_chi_so),
    KEY idx_g6_chisocothe_hoivien (g6_ma_hoi_vien),
    KEY idx_g6_chisocothe_ngaydo  (g6_ngay_do),
    CONSTRAINT fk_g6_chisocothe_hoivien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien) ON DELETE CASCADE,
    CONSTRAINT fk_g6_chisocothe_nguoido FOREIGN KEY (g6_nguoi_do)    REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
