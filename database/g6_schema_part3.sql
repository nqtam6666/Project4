-- ============================================================
-- G6 GYM MANAGEMENT + SUPPLEMENT STORE
-- MySQL Schema - Part 3: Group 11-16
-- GROUP 11: KHO HÀNG | GROUP 12: KHÁCH HÀNG ONLINE
-- GROUP 13: TÍCH ĐIỂM | GROUP 14: GIỎ HÀNG & ĐƠN HÀNG
-- GROUP 15: KHUYẾN MÃI | GROUP 16: THANH TOÁN
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- GROUP 11: KHO HÀNG
-- ============================================================

CREATE TABLE G6TonKho (
    g6_ma_ton_kho          INT             NOT NULL AUTO_INCREMENT,
    g6_ma_bien_the         INT             NOT NULL,
    g6_ma_chi_nhanh        INT             NULL COMMENT 'NULL = kho online tổng',
    g6_so_luong            INT             NOT NULL DEFAULT 0,
    g6_so_luong_dat_truoc  INT             NOT NULL DEFAULT 0 COMMENT 'Đã đặt chưa giao',
    g6_nguong_canh_bao     INT             NOT NULL DEFAULT 10,
    g6_ngay_cap_nhat       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_ton_kho),
    UNIQUE KEY uk_g6_tonkho (g6_ma_bien_the, g6_ma_chi_nhanh),
    KEY idx_g6_tonkho_chinhanh (g6_ma_chi_nhanh),
    CONSTRAINT fk_g6_tonkho_bienthe  FOREIGN KEY (g6_ma_bien_the)  REFERENCES G6BienTheSanPham (g6_ma_bien_the),
    CONSTRAINT fk_g6_tonkho_chinhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6LichSuTonKho (
    g6_ma_lich_su          INT             NOT NULL AUTO_INCREMENT,
    g6_ma_bien_the         INT             NOT NULL,
    g6_ma_chi_nhanh        INT             NULL,
    g6_loai_giao_dich      VARCHAR(20)     NOT NULL COMMENT '''nhap'',''xuat'',''dieu_chuyen'',''tra_hang'',''kiem_ke''',
    g6_so_luong_thay_doi   INT             NOT NULL COMMENT 'Âm = xuất, dương = nhập',
    g6_so_luong_truoc      INT             NOT NULL,
    g6_so_luong_sau        INT             NOT NULL,
    g6_ma_don_hang         INT             NULL,
    g6_ghi_chu             VARCHAR(255)    NULL,
    g6_nguoi_thuc_hien     INT             NULL,
    g6_thoi_gian           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_lich_su),
    KEY idx_g6_lstonkho_bienthe  (g6_ma_bien_the),
    KEY idx_g6_lstonkho_thoigian (g6_thoi_gian),
    CONSTRAINT fk_g6_lstonkho_bienthe    FOREIGN KEY (g6_ma_bien_the)    REFERENCES G6BienTheSanPham (g6_ma_bien_the),
    CONSTRAINT fk_g6_lstonkho_nguoithh   FOREIGN KEY (g6_nguoi_thuc_hien) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 12: KHÁCH HÀNG ONLINE
-- ============================================================

CREATE TABLE G6KhachHang (
    g6_ma_khach_hang   INT             NOT NULL AUTO_INCREMENT,
    g6_so_dien_thoai   VARCHAR(15)     NOT NULL,
    g6_email           VARCHAR(100)    NULL,
    g6_ho_ten          VARCHAR(100)    NULL,
    g6_ngay_sinh       DATE            NULL,
    g6_gioi_tinh       VARCHAR(10)     NULL,
    g6_google_id       VARCHAR(100)    NULL COMMENT 'Social login',
    g6_da_xac_thuc_otp TINYINT(1)      NOT NULL DEFAULT 0,
    g6_ma_hoi_vien     INT             NULL COMMENT 'Link nếu cũng là hội viên gym',
    g6_ngay_dang_ky    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (g6_ma_khach_hang),
    UNIQUE KEY uk_g6_khachhang_sdt (g6_so_dien_thoai),
    KEY idx_g6_khachhang_hoivien (g6_ma_hoi_vien),
    CONSTRAINT fk_g6_khachhang_hoivien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6DiaChiGiaoHang (
    g6_ma_dia_chi          INT             NOT NULL AUTO_INCREMENT,
    g6_ma_khach_hang       INT             NOT NULL,
    g6_ho_ten_nguoi_nhan   VARCHAR(100)    NOT NULL,
    g6_so_dien_thoai       VARCHAR(15)     NOT NULL,
    g6_dia_chi             VARCHAR(255)    NOT NULL,
    g6_phuong_xa           VARCHAR(100)    NULL,
    g6_quan_huyen          VARCHAR(100)    NULL,
    g6_tinh_thanh          VARCHAR(100)    NOT NULL,
    g6_la_mac_dinh         TINYINT(1)      NOT NULL DEFAULT 0,
    PRIMARY KEY (g6_ma_dia_chi),
    KEY idx_g6_diachi_khachhang (g6_ma_khach_hang),
    CONSTRAINT fk_g6_diachi_khachhang FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 13: TÍCH ĐIỂM & HẠNG THÀNH VIÊN
-- ============================================================

CREATE TABLE G6HangThanhVien (
    g6_ma_hang             INT             NOT NULL AUTO_INCREMENT,
    g6_ten_hang            VARCHAR(50)     NOT NULL COMMENT '''Đồng'',''Bạc'',''Vàng'',''Kim Cương''',
    g6_diem_toi_thieu      INT             NOT NULL DEFAULT 0,
    g6_ti_le_tich_diem     DECIMAL(5,2)    NOT NULL DEFAULT 1.00 COMMENT '1 điểm / X đồng',
    g6_ti_le_dung_diem     DECIMAL(5,2)    NOT NULL DEFAULT 100.00 COMMENT '1 điểm = X đồng',
    g6_giam_gia_phan_tram  DECIMAL(5,2)    NOT NULL DEFAULT 0 COMMENT '% giảm giá cố định',
    g6_quyen_loi           JSON            NULL COMMENT '["free_shipping","priority_booking"]',
    g6_mau_hien_thi        VARCHAR(20)     NULL,
    PRIMARY KEY (g6_ma_hang)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO G6HangThanhVien (g6_ten_hang, g6_diem_toi_thieu, g6_ti_le_tich_diem, g6_giam_gia_phan_tram, g6_mau_hien_thi) VALUES
('Đồng',        0,      1.00,   0,    '#cd7f32'),
('Bạc',         1000,   1.20,   2,    '#c0c0c0'),
('Vàng',        5000,   1.50,   5,    '#ffd700'),
('Kim Cương',   20000,  2.00,   10,   '#b9f2ff');

CREATE TABLE G6DiemKhachHang (
    g6_ma_diem             INT             NOT NULL AUTO_INCREMENT,
    g6_ma_khach_hang       INT             NOT NULL,
    g6_so_diem_hien_tai    INT             NOT NULL DEFAULT 0,
    g6_tong_diem_lich_su   INT             NOT NULL DEFAULT 0,
    g6_ma_hang             INT             NOT NULL DEFAULT 1,
    g6_ngay_cap_nhat_hang  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_diem),
    UNIQUE KEY uk_g6_diemkh_khachhang (g6_ma_khach_hang),
    CONSTRAINT fk_g6_diemkh_khachhang FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE CASCADE,
    CONSTRAINT fk_g6_diemkh_hang      FOREIGN KEY (g6_ma_hang)       REFERENCES G6HangThanhVien (g6_ma_hang)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6GiaoDichDiem (
    g6_ma_giao_dich        INT             NOT NULL AUTO_INCREMENT,
    g6_ma_khach_hang       INT             NOT NULL,
    g6_ma_don_hang         INT             NULL,
    g6_loai                VARCHAR(20)     NOT NULL COMMENT '''kich_hoat'',''su_dung'',''het_han'',''dieu_chinh''',
    g6_so_diem             INT             NOT NULL COMMENT 'Âm = dùng, dương = tích',
    g6_so_diem_truoc       INT             NOT NULL,
    g6_so_diem_sau         INT             NOT NULL,
    g6_ghi_chu             VARCHAR(255)    NULL,
    g6_thoi_gian           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_ngay_het_han_diem   DATETIME        NULL,
    PRIMARY KEY (g6_ma_giao_dich),
    KEY idx_g6_gddiem_khachhang (g6_ma_khach_hang),
    KEY idx_g6_gddiem_donhang   (g6_ma_don_hang),
    CONSTRAINT fk_g6_gddiem_khachhang FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 14: GIỎ HÀNG & ĐƠN HÀNG
-- ============================================================

CREATE TABLE G6GioHang (
    g6_ma_gio_hang     INT             NOT NULL AUTO_INCREMENT,
    g6_ma_khach_hang   INT             NULL COMMENT 'NULL = guest',
    g6_session_id      VARCHAR(100)    NULL COMMENT 'Guest cart session',
    g6_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_gio_hang),
    KEY idx_g6_giohang_khachhang (g6_ma_khach_hang),
    KEY idx_g6_giohang_session   (g6_session_id),
    CONSTRAINT fk_g6_giohang_khachhang FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6ChiTietGioHang (
    g6_ma_chi_tiet_gio     INT             NOT NULL AUTO_INCREMENT,
    g6_ma_gio_hang         INT             NOT NULL,
    g6_ma_bien_the         INT             NOT NULL,
    g6_so_luong            INT             NOT NULL DEFAULT 1,
    g6_gia_tai_thoi_diem   DECIMAL(15,0)   NOT NULL,
    g6_ngay_them           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_chi_tiet_gio),
    UNIQUE KEY uk_g6_ctgio (g6_ma_gio_hang, g6_ma_bien_the),
    CONSTRAINT fk_g6_ctgio_giohang FOREIGN KEY (g6_ma_gio_hang) REFERENCES G6GioHang (g6_ma_gio_hang) ON DELETE CASCADE,
    CONSTRAINT fk_g6_ctgio_bienthe FOREIGN KEY (g6_ma_bien_the) REFERENCES G6BienTheSanPham (g6_ma_bien_the)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6DonHang (
    g6_ma_don_hang             INT             NOT NULL AUTO_INCREMENT,
    g6_ma_don_hang_hien        VARCHAR(20)     NOT NULL COMMENT 'G62025001234',
    g6_ma_khach_hang           INT             NULL,
    g6_ten_nguoi_dat           VARCHAR(100)    NOT NULL,
    g6_so_dien_thoai_dat       VARCHAR(15)     NOT NULL,
    g6_email_dat               VARCHAR(100)    NULL,
    g6_dia_chi_giao_hang       JSON            NULL COMMENT 'Snapshot địa chỉ lúc đặt',
    g6_tinh_thanh_giao         VARCHAR(100)    NULL,
    g6_phuong_thuc_giao        VARCHAR(20)     NOT NULL DEFAULT 'giao_hang' COMMENT '''giao_hang'',''nhan_tai_cua_hang''',
    g6_ma_chi_nhanh_nhan       INT             NULL COMMENT 'Nếu nhận tại cửa hàng',
    g6_tong_tien_hang          DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_phi_van_chuyen          DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_giam_gia_coupon         DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_giam_gia_diem           DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_giam_gia_hang           DECIMAL(15,0)   NOT NULL DEFAULT 0 COMMENT 'Giảm theo hạng thành viên',
    g6_tong_thanh_toan         DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_ma_coupon_da_dung       VARCHAR(50)     NULL,
    g6_diem_da_dung            INT             NOT NULL DEFAULT 0,
    g6_diem_tich_duoc          INT             NOT NULL DEFAULT 0,
    g6_trang_thai              VARCHAR(30)     NOT NULL DEFAULT 'cho_xac_nhan' COMMENT '''cho_xac_nhan'',''da_xac_nhan'',''dang_chuan_bi'',''dang_giao'',''da_giao'',''da_huy'',''tra_hang''',
    g6_trang_thai_thanh_toan   VARCHAR(20)     NOT NULL DEFAULT 'cho_thanh_toan' COMMENT '''cho_thanh_toan'',''da_thanh_toan'',''hoan_tien''',
    g6_phuong_thuc_thanh_toan  VARCHAR(30)     NULL COMMENT '''cod'',''chuyen_khoan'',''vnpay'',''momo'',''the''',
    g6_ghi_chu_khach           VARCHAR(500)    NULL,
    g6_ghi_chu_noi_bo          VARCHAR(500)    NULL,
    g6_nguon_don_hang          VARCHAR(20)     NOT NULL DEFAULT 'website' COMMENT '''website'',''dien_thoai'',''tai_quay'',''app''',
    g6_nguoi_tao               INT             NULL COMMENT 'Nhân viên tạo hộ',
    g6_ngay_tao                DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_ngay_cap_nhat           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    g6_ngay_giao_du_kien       DATE            NULL,
    g6_ngay_giao_thuc_te       DATETIME        NULL,
    PRIMARY KEY (g6_ma_don_hang),
    UNIQUE KEY uk_g6_donhang_mahien (g6_ma_don_hang_hien),
    KEY idx_g6_donhang_khachhang  (g6_ma_khach_hang),
    KEY idx_g6_donhang_trangthai  (g6_trang_thai),
    KEY idx_g6_donhang_ngaytao    (g6_ngay_tao),
    CONSTRAINT fk_g6_donhang_khachhang FOREIGN KEY (g6_ma_khach_hang)     REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE SET NULL,
    CONSTRAINT fk_g6_donhang_chinhanh  FOREIGN KEY (g6_ma_chi_nhanh_nhan) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh) ON DELETE SET NULL,
    CONSTRAINT fk_g6_donhang_nguoitao  FOREIGN KEY (g6_nguoi_tao)         REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6ChiTietDonHang (
    g6_ma_chi_tiet             INT             NOT NULL AUTO_INCREMENT,
    g6_ma_don_hang             INT             NOT NULL,
    g6_ma_bien_the             INT             NOT NULL,
    g6_ten_san_pham_snap       VARCHAR(255)    NOT NULL COMMENT 'Snapshot tên lúc đặt',
    g6_sku_snap                VARCHAR(100)    NOT NULL,
    g6_so_luong                INT             NOT NULL,
    g6_don_gia                 DECIMAL(15,0)   NOT NULL,
    g6_giam_gia_tung_san_pham  DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_thanh_tien              DECIMAL(15,0)   NOT NULL,
    PRIMARY KEY (g6_ma_chi_tiet),
    KEY idx_g6_ctdonhang_donhang (g6_ma_don_hang),
    CONSTRAINT fk_g6_ctdonhang_donhang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE CASCADE,
    CONSTRAINT fk_g6_ctdonhang_bienthe FOREIGN KEY (g6_ma_bien_the) REFERENCES G6BienTheSanPham (g6_ma_bien_the)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6LichSuDonHang (
    g6_ma_lich_su_don  INT             NOT NULL AUTO_INCREMENT,
    g6_ma_don_hang     INT             NOT NULL,
    g6_trang_thai_cu   VARCHAR(30)     NULL,
    g6_trang_thai_moi  VARCHAR(30)     NOT NULL,
    g6_ghi_chu         VARCHAR(500)    NULL,
    g6_nguoi_thay_doi  INT             NULL,
    g6_thoi_gian       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_lich_su_don),
    KEY idx_g6_lsdonhang_donhang (g6_ma_don_hang),
    CONSTRAINT fk_g6_lsdonhang_donhang   FOREIGN KEY (g6_ma_don_hang)    REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE CASCADE,
    CONSTRAINT fk_g6_lsdonhang_nguoithd  FOREIGN KEY (g6_nguoi_thay_doi) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 15: MÃ GIẢM GIÁ & KHUYẾN MÃI
-- ============================================================

CREATE TABLE G6MaGiamGia (
    g6_ma_coupon               INT             NOT NULL AUTO_INCREMENT,
    g6_ma                      VARCHAR(50)     NOT NULL COMMENT '''GS30'',''SUMMER20''',
    g6_ten_mo_ta               VARCHAR(255)    NULL,
    g6_loai_giam               VARCHAR(20)     NOT NULL COMMENT '''so_tien_co_dinh'',''phan_tram''',
    g6_gia_tri_giam            DECIMAL(15,0)   NOT NULL,
    g6_don_hang_toi_thieu      DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_giam_toi_da             DECIMAL(15,0)   NULL COMMENT 'Cap cho % discount',
    g6_so_luot_tong_cong       INT             NULL COMMENT 'NULL = không giới hạn',
    g6_so_luot_da_dung         INT             NOT NULL DEFAULT 0,
    g6_so_luot_moi_kh          INT             NOT NULL DEFAULT 1,
    g6_ma_danh_muc_loai_tru    JSON            NULL COMMENT 'Category IDs bị loại trừ',
    g6_ma_thuong_hieu_loai_tru JSON            NULL COMMENT 'Brand IDs bị loại trừ',
    g6_chi_ap_dung_hang        INT             NULL COMMENT 'Chỉ cho tier cụ thể',
    g6_ngay_bat_dau            DATETIME        NOT NULL,
    g6_ngay_ket_thuc           DATETIME        NOT NULL,
    g6_la_hoat_dong            TINYINT(1)      NOT NULL DEFAULT 1,
    g6_ghi_chu_noi_bo          VARCHAR(255)    NULL,
    g6_ngay_tao                DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_coupon),
    UNIQUE KEY uk_g6_magiam_ma (g6_ma),
    KEY idx_g6_magiam_ngay  (g6_ngay_bat_dau, g6_ngay_ket_thuc),
    CONSTRAINT fk_g6_magiam_hang FOREIGN KEY (g6_chi_ap_dung_hang) REFERENCES G6HangThanhVien (g6_ma_hang) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6KhuyenMaiMuaKem (
    g6_ma_uu_dai           INT             NOT NULL AUTO_INCREMENT,
    g6_ten                 VARCHAR(100)    NOT NULL,
    g6_ma_san_pham_kich    INT             NULL COMMENT 'Sản phẩm trigger',
    g6_ma_danh_muc_kich    INT             NULL COMMENT 'Danh mục trigger',
    g6_ma_san_pham_tang    INT             NOT NULL COMMENT 'Sản phẩm đề xuất mua kèm',
    g6_gia_khuyen_mai      DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_la_tang_kem         TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '1=free gift, 0=giảm giá',
    g6_ngay_bat_dau        DATETIME        NOT NULL,
    g6_ngay_ket_thuc       DATETIME        NOT NULL,
    g6_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (g6_ma_uu_dai),
    CONSTRAINT fk_g6_kmmuakem_spkich  FOREIGN KEY (g6_ma_san_pham_kich) REFERENCES G6SanPham (g6_ma_san_pham) ON DELETE SET NULL,
    CONSTRAINT fk_g6_kmmuakem_dmkich  FOREIGN KEY (g6_ma_danh_muc_kich) REFERENCES G6DanhMucSanPham (g6_ma_danh_muc) ON DELETE SET NULL,
    CONSTRAINT fk_g6_kmmuakem_sptang  FOREIGN KEY (g6_ma_san_pham_tang) REFERENCES G6SanPham (g6_ma_san_pham)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6Banner (
    g6_ma_banner           INT             NOT NULL AUTO_INCREMENT,
    g6_vi_tri              VARCHAR(50)     NOT NULL COMMENT '''trang_chu_slider'',''popup'',''sidebar'',''header''',
    g6_tieu_de             VARCHAR(255)    NULL,
    g6_hinh_anh            VARCHAR(500)    NOT NULL,
    g6_hinh_anh_mobile     VARCHAR(500)    NULL,
    g6_url_lien_ket        VARCHAR(500)    NULL,
    g6_mo_ta               VARCHAR(500)    NULL,
    g6_ngay_bat_dau        DATETIME        NOT NULL,
    g6_ngay_ket_thuc       DATETIME        NOT NULL,
    g6_thu_tu              INT             NOT NULL DEFAULT 0,
    g6_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (g6_ma_banner),
    KEY idx_g6_banner_vitri (g6_vi_tri),
    KEY idx_g6_banner_ngay  (g6_ngay_bat_dau, g6_ngay_ket_thuc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 16: THANH TOÁN
-- ============================================================

CREATE TABLE G6ThanhToan (
    g6_ma_thanh_toan           INT             NOT NULL AUTO_INCREMENT,
    g6_ma_don_hang             INT             NULL,
    g6_ma_dang_ky_goi          INT             NULL COMMENT 'Cho gym subscription',
    g6_so_tien                 DECIMAL(15,0)   NOT NULL,
    g6_phuong_thuc             VARCHAR(30)     NOT NULL COMMENT '''cod'',''chuyen_khoan'',''vnpay'',''momo'',''the_tin_dung''',
    g6_trang_thai              VARCHAR(20)     NOT NULL DEFAULT 'cho_xu_ly' COMMENT '''cho_xu_ly'',''thanh_cong'',''that_bai'',''hoan_tien''',
    g6_ma_giao_dich_ngoai      VARCHAR(255)    NULL COMMENT 'Transaction ID từ cổng thanh toán',
    g6_ngan_hang               VARCHAR(50)     NULL,
    g6_so_tai_khoan_gui        VARCHAR(50)     NULL,
    g6_thoi_gian_thanh_toan    DATETIME        NULL,
    g6_ghi_chu                 VARCHAR(500)    NULL,
    g6_ngay_tao                DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_thanh_toan),
    KEY idx_g6_thanhtoan_donhang (g6_ma_don_hang),
    KEY idx_g6_thanhtoan_trangthai(g6_trang_thai),
    CONSTRAINT fk_g6_thanhtoan_donhang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE SET NULL,
    CONSTRAINT fk_g6_thanhtoan_dkgoi   FOREIGN KEY (g6_ma_dang_ky_goi) REFERENCES G6DangKyGoiTap (g6_ma_dang_ky) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6HoaDon (
    g6_ma_hoa_don          INT             NOT NULL AUTO_INCREMENT,
    g6_so_hoa_don          VARCHAR(20)     NOT NULL COMMENT 'HD2025001234',
    g6_ma_don_hang         INT             NULL,
    g6_ma_thanh_toan       INT             NOT NULL,
    g6_thong_tin_nguoi_mua JSON            NULL COMMENT 'Snapshot thông tin người mua',
    g6_tong_tien           DECIMAL(15,0)   NOT NULL,
    g6_thue_vat            DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_ngay_xuat           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_duong_dan_pdf       VARCHAR(500)    NULL,
    PRIMARY KEY (g6_ma_hoa_don),
    UNIQUE KEY uk_g6_hoadon_so (g6_so_hoa_don),
    KEY idx_g6_hoadon_donhang   (g6_ma_don_hang),
    CONSTRAINT fk_g6_hoadon_donhang   FOREIGN KEY (g6_ma_don_hang)   REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE SET NULL,
    CONSTRAINT fk_g6_hoadon_thanhtoan FOREIGN KEY (g6_ma_thanh_toan) REFERENCES G6ThanhToan (g6_ma_thanh_toan)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- FK bị hoãn ở part 1 - thêm vào sau khi G6ThanhToan đã tồn tại
ALTER TABLE G6DangKyGoiTap
    ADD CONSTRAINT fk_g6_dkgoitap_thanhtoan FOREIGN KEY (g6_ma_thanh_toan) REFERENCES G6ThanhToan (g6_ma_thanh_toan) ON DELETE SET NULL;

ALTER TABLE G6DangKyGoiPT
    ADD CONSTRAINT fk_g6_dkgoipt_thanhtoan FOREIGN KEY (g6_ma_thanh_toan) REFERENCES G6ThanhToan (g6_ma_thanh_toan) ON DELETE SET NULL;

ALTER TABLE G6DatDichVu
    ADD CONSTRAINT fk_g6_datdichvu_thanhtoan FOREIGN KEY (g6_ma_thanh_toan) REFERENCES G6ThanhToan (g6_ma_thanh_toan) ON DELETE SET NULL;

-- FK điểm → đơn hàng
ALTER TABLE G6GiaoDichDiem
    ADD CONSTRAINT fk_g6_gddiem_donhang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE SET NULL;

-- FK lịch sử tồn kho → đơn hàng
ALTER TABLE G6LichSuTonKho
    ADD CONSTRAINT fk_g6_lstonkho_donhang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE SET NULL;

SET FOREIGN_KEY_CHECKS = 1;
