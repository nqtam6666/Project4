-- ============================================================
-- NQT GYM MANAGEMENT + SUPPLEMENT STORE
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

CREATE TABLE NqtTonKho (
    nqt_ma_ton_kho          INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_bien_the         INT             NOT NULL,
    nqt_ma_chi_nhanh        INT             NULL COMMENT 'NULL = kho online tổng',
    nqt_so_luong            INT             NOT NULL DEFAULT 0,
    nqt_so_luong_dat_truoc  INT             NOT NULL DEFAULT 0 COMMENT 'Đã đặt chưa giao',
    nqt_nguong_canh_bao     INT             NOT NULL DEFAULT 10,
    nqt_ngay_cap_nhat       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_ton_kho),
    UNIQUE KEY uk_nqt_tonkho (nqt_ma_bien_the, nqt_ma_chi_nhanh),
    KEY idx_nqt_tonkho_chinhanh (nqt_ma_chi_nhanh),
    CONSTRAINT fk_nqt_tonkho_bienthe  FOREIGN KEY (nqt_ma_bien_the)  REFERENCES NqtBienTheSanPham (nqt_ma_bien_the),
    CONSTRAINT fk_nqt_tonkho_chinhanh FOREIGN KEY (nqt_ma_chi_nhanh) REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtLichSuTonKho (
    nqt_ma_lich_su          INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_bien_the         INT             NOT NULL,
    nqt_ma_chi_nhanh        INT             NULL,
    nqt_loai_giao_dich      VARCHAR(20)     NOT NULL COMMENT '''nhap'',''xuat'',''dieu_chuyen'',''tra_hang'',''kiem_ke''',
    nqt_so_luong_thay_doi   INT             NOT NULL COMMENT 'Âm = xuất, dương = nhập',
    nqt_so_luong_truoc      INT             NOT NULL,
    nqt_so_luong_sau        INT             NOT NULL,
    nqt_ma_don_hang         INT             NULL,
    nqt_ghi_chu             VARCHAR(255)    NULL,
    nqt_nguoi_thuc_hien     INT             NULL,
    nqt_thoi_gian           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_lich_su),
    KEY idx_nqt_lstonkho_bienthe  (nqt_ma_bien_the),
    KEY idx_nqt_lstonkho_thoigian (nqt_thoi_gian),
    CONSTRAINT fk_nqt_lstonkho_bienthe    FOREIGN KEY (nqt_ma_bien_the)    REFERENCES NqtBienTheSanPham (nqt_ma_bien_the),
    CONSTRAINT fk_nqt_lstonkho_nguoithh   FOREIGN KEY (nqt_nguoi_thuc_hien) REFERENCES NqtNguoiDung (nqt_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 12: KHÁCH HÀNG ONLINE
-- ============================================================

CREATE TABLE NqtKhachHang (
    nqt_ma_khach_hang   INT             NOT NULL AUTO_INCREMENT,
    nqt_so_dien_thoai   VARCHAR(15)     NOT NULL,
    nqt_email           VARCHAR(100)    NULL,
    nqt_ho_ten          VARCHAR(100)    NULL,
    nqt_ngay_sinh       DATE            NULL,
    nqt_gioi_tinh       VARCHAR(10)     NULL,
    nqt_google_id       VARCHAR(100)    NULL COMMENT 'Social login',
    nqt_da_xac_thuc_otp TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_ma_hoi_vien     INT             NULL COMMENT 'Link nếu cũng là hội viên gym',
    nqt_ngay_dang_ky    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_la_hoat_dong    TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nqt_ma_khach_hang),
    UNIQUE KEY uk_nqt_khachhang_sdt (nqt_so_dien_thoai),
    KEY idx_nqt_khachhang_hoivien (nqt_ma_hoi_vien),
    CONSTRAINT fk_nqt_khachhang_hoivien FOREIGN KEY (nqt_ma_hoi_vien) REFERENCES NqtHoiVien (nqt_ma_hoi_vien) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtDiaChiGiaoHang (
    nqt_ma_dia_chi          INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_khach_hang       INT             NOT NULL,
    nqt_ho_ten_nguoi_nhan   VARCHAR(100)    NOT NULL,
    nqt_so_dien_thoai       VARCHAR(15)     NOT NULL,
    nqt_dia_chi             VARCHAR(255)    NOT NULL,
    nqt_phuong_xa           VARCHAR(100)    NULL,
    nqt_quan_huyen          VARCHAR(100)    NULL,
    nqt_tinh_thanh          VARCHAR(100)    NOT NULL,
    nqt_la_mac_dinh         TINYINT(1)      NOT NULL DEFAULT 0,
    PRIMARY KEY (nqt_ma_dia_chi),
    KEY idx_nqt_diachi_khachhang (nqt_ma_khach_hang),
    CONSTRAINT fk_nqt_diachi_khachhang FOREIGN KEY (nqt_ma_khach_hang) REFERENCES NqtKhachHang (nqt_ma_khach_hang) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 13: TÍCH ĐIỂM & HẠNG THÀNH VIÊN
-- ============================================================

CREATE TABLE NqtHangThanhVien (
    nqt_ma_hang             INT             NOT NULL AUTO_INCREMENT,
    nqt_ten_hang            VARCHAR(50)     NOT NULL COMMENT '''Đồng'',''Bạc'',''Vàng'',''Kim Cương''',
    nqt_diem_toi_thieu      INT             NOT NULL DEFAULT 0,
    nqt_ti_le_tich_diem     DECIMAL(5,2)    NOT NULL DEFAULT 1.00 COMMENT '1 điểm / X đồng',
    nqt_ti_le_dung_diem     DECIMAL(5,2)    NOT NULL DEFAULT 100.00 COMMENT '1 điểm = X đồng',
    nqt_giam_gia_phan_tram  DECIMAL(5,2)    NOT NULL DEFAULT 0 COMMENT '% giảm giá cố định',
    nqt_quyen_loi           JSON            NULL COMMENT '["free_shipping","priority_booking"]',
    nqt_mau_hien_thi        VARCHAR(20)     NULL,
    PRIMARY KEY (nqt_ma_hang)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO NqtHangThanhVien (nqt_ten_hang, nqt_diem_toi_thieu, nqt_ti_le_tich_diem, nqt_giam_gia_phan_tram, nqt_mau_hien_thi) VALUES
('Đồng',        0,      1.00,   0,    '#cd7f32'),
('Bạc',         1000,   1.20,   2,    '#c0c0c0'),
('Vàng',        5000,   1.50,   5,    '#ffd700'),
('Kim Cương',   20000,  2.00,   10,   '#b9f2ff');

CREATE TABLE NqtDiemKhachHang (
    nqt_ma_diem             INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_khach_hang       INT             NOT NULL,
    nqt_so_diem_hien_tai    INT             NOT NULL DEFAULT 0,
    nqt_tong_diem_lich_su   INT             NOT NULL DEFAULT 0,
    nqt_ma_hang             INT             NOT NULL DEFAULT 1,
    nqt_ngay_cap_nhat_hang  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_diem),
    UNIQUE KEY uk_nqt_diemkh_khachhang (nqt_ma_khach_hang),
    CONSTRAINT fk_nqt_diemkh_khachhang FOREIGN KEY (nqt_ma_khach_hang) REFERENCES NqtKhachHang (nqt_ma_khach_hang) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_diemkh_hang      FOREIGN KEY (nqt_ma_hang)       REFERENCES NqtHangThanhVien (nqt_ma_hang)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtGiaoDichDiem (
    nqt_ma_giao_dich        INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_khach_hang       INT             NOT NULL,
    nqt_ma_don_hang         INT             NULL,
    nqt_loai                VARCHAR(20)     NOT NULL COMMENT '''kich_hoat'',''su_dung'',''het_han'',''dieu_chinh''',
    nqt_so_diem             INT             NOT NULL COMMENT 'Âm = dùng, dương = tích',
    nqt_so_diem_truoc       INT             NOT NULL,
    nqt_so_diem_sau         INT             NOT NULL,
    nqt_ghi_chu             VARCHAR(255)    NULL,
    nqt_thoi_gian           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_ngay_het_han_diem   DATETIME        NULL,
    PRIMARY KEY (nqt_ma_giao_dich),
    KEY idx_nqt_gddiem_khachhang (nqt_ma_khach_hang),
    KEY idx_nqt_gddiem_donhang   (nqt_ma_don_hang),
    CONSTRAINT fk_nqt_gddiem_khachhang FOREIGN KEY (nqt_ma_khach_hang) REFERENCES NqtKhachHang (nqt_ma_khach_hang)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 14: GIỎ HÀNG & ĐƠN HÀNG
-- ============================================================

CREATE TABLE NqtGioHang (
    nqt_ma_gio_hang     INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_khach_hang   INT             NULL COMMENT 'NULL = guest',
    nqt_session_id      VARCHAR(100)    NULL COMMENT 'Guest cart session',
    nqt_ngay_tao        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_ngay_cap_nhat   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_gio_hang),
    KEY idx_nqt_giohang_khachhang (nqt_ma_khach_hang),
    KEY idx_nqt_giohang_session   (nqt_session_id),
    CONSTRAINT fk_nqt_giohang_khachhang FOREIGN KEY (nqt_ma_khach_hang) REFERENCES NqtKhachHang (nqt_ma_khach_hang) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtChiTietGioHang (
    nqt_ma_chi_tiet_gio     INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_gio_hang         INT             NOT NULL,
    nqt_ma_bien_the         INT             NOT NULL,
    nqt_so_luong            INT             NOT NULL DEFAULT 1,
    nqt_gia_tai_thoi_diem   DECIMAL(15,0)   NOT NULL,
    nqt_ngay_them           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_chi_tiet_gio),
    UNIQUE KEY uk_nqt_ctgio (nqt_ma_gio_hang, nqt_ma_bien_the),
    CONSTRAINT fk_nqt_ctgio_giohang FOREIGN KEY (nqt_ma_gio_hang) REFERENCES NqtGioHang (nqt_ma_gio_hang) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_ctgio_bienthe FOREIGN KEY (nqt_ma_bien_the) REFERENCES NqtBienTheSanPham (nqt_ma_bien_the)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtDonHang (
    nqt_ma_don_hang             INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_don_hang_hien        VARCHAR(20)     NOT NULL COMMENT 'NQT2025001234',
    nqt_ma_khach_hang           INT             NULL,
    nqt_ten_nguoi_dat           VARCHAR(100)    NOT NULL,
    nqt_so_dien_thoai_dat       VARCHAR(15)     NOT NULL,
    nqt_email_dat               VARCHAR(100)    NULL,
    nqt_dia_chi_giao_hang       JSON            NULL COMMENT 'Snapshot địa chỉ lúc đặt',
    nqt_tinh_thanh_giao         VARCHAR(100)    NULL,
    nqt_phuong_thuc_giao        VARCHAR(20)     NOT NULL DEFAULT 'giao_hang' COMMENT '''giao_hang'',''nhan_tai_cua_hang''',
    nqt_ma_chi_nhanh_nhan       INT             NULL COMMENT 'Nếu nhận tại cửa hàng',
    nqt_tong_tien_hang          DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_phi_van_chuyen          DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_giam_gia_coupon         DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_giam_gia_diem           DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_giam_gia_hang           DECIMAL(15,0)   NOT NULL DEFAULT 0 COMMENT 'Giảm theo hạng thành viên',
    nqt_tong_thanh_toan         DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_ma_coupon_da_dung       VARCHAR(50)     NULL,
    nqt_diem_da_dung            INT             NOT NULL DEFAULT 0,
    nqt_diem_tich_duoc          INT             NOT NULL DEFAULT 0,
    nqt_trang_thai              VARCHAR(30)     NOT NULL DEFAULT 'cho_xac_nhan' COMMENT '''cho_xac_nhan'',''da_xac_nhan'',''dang_chuan_bi'',''dang_giao'',''da_giao'',''da_huy'',''tra_hang''',
    nqt_trang_thai_thanh_toan   VARCHAR(20)     NOT NULL DEFAULT 'cho_thanh_toan' COMMENT '''cho_thanh_toan'',''da_thanh_toan'',''hoan_tien''',
    nqt_phuong_thuc_thanh_toan  VARCHAR(30)     NULL COMMENT '''cod'',''chuyen_khoan'',''vnpay'',''momo'',''the''',
    nqt_ghi_chu_khach           VARCHAR(500)    NULL,
    nqt_ghi_chu_noi_bo          VARCHAR(500)    NULL,
    nqt_nguon_don_hang          VARCHAR(20)     NOT NULL DEFAULT 'website' COMMENT '''website'',''dien_thoai'',''tai_quay'',''app''',
    nqt_nguoi_tao               INT             NULL COMMENT 'Nhân viên tạo hộ',
    nqt_ngay_tao                DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_ngay_cap_nhat           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    nqt_ngay_giao_du_kien       DATE            NULL,
    nqt_ngay_giao_thuc_te       DATETIME        NULL,
    PRIMARY KEY (nqt_ma_don_hang),
    UNIQUE KEY uk_nqt_donhang_mahien (nqt_ma_don_hang_hien),
    KEY idx_nqt_donhang_khachhang  (nqt_ma_khach_hang),
    KEY idx_nqt_donhang_trangthai  (nqt_trang_thai),
    KEY idx_nqt_donhang_ngaytao    (nqt_ngay_tao),
    CONSTRAINT fk_nqt_donhang_khachhang FOREIGN KEY (nqt_ma_khach_hang)     REFERENCES NqtKhachHang (nqt_ma_khach_hang) ON DELETE SET NULL,
    CONSTRAINT fk_nqt_donhang_chinhanh  FOREIGN KEY (nqt_ma_chi_nhanh_nhan) REFERENCES NqtChiNhanh (nqt_ma_chi_nhanh) ON DELETE SET NULL,
    CONSTRAINT fk_nqt_donhang_nguoitao  FOREIGN KEY (nqt_nguoi_tao)         REFERENCES NqtNguoiDung (nqt_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtChiTietDonHang (
    nqt_ma_chi_tiet             INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_don_hang             INT             NOT NULL,
    nqt_ma_bien_the             INT             NOT NULL,
    nqt_ten_san_pham_snap       VARCHAR(255)    NOT NULL COMMENT 'Snapshot tên lúc đặt',
    nqt_sku_snap                VARCHAR(100)    NOT NULL,
    nqt_so_luong                INT             NOT NULL,
    nqt_don_gia                 DECIMAL(15,0)   NOT NULL,
    nqt_giam_gia_tung_san_pham  DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_thanh_tien              DECIMAL(15,0)   NOT NULL,
    PRIMARY KEY (nqt_ma_chi_tiet),
    KEY idx_nqt_ctdonhang_donhang (nqt_ma_don_hang),
    CONSTRAINT fk_nqt_ctdonhang_donhang FOREIGN KEY (nqt_ma_don_hang) REFERENCES NqtDonHang (nqt_ma_don_hang) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_ctdonhang_bienthe FOREIGN KEY (nqt_ma_bien_the) REFERENCES NqtBienTheSanPham (nqt_ma_bien_the)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtLichSuDonHang (
    nqt_ma_lich_su_don  INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_don_hang     INT             NOT NULL,
    nqt_trang_thai_cu   VARCHAR(30)     NULL,
    nqt_trang_thai_moi  VARCHAR(30)     NOT NULL,
    nqt_ghi_chu         VARCHAR(500)    NULL,
    nqt_nguoi_thay_doi  INT             NULL,
    nqt_thoi_gian       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_lich_su_don),
    KEY idx_nqt_lsdonhang_donhang (nqt_ma_don_hang),
    CONSTRAINT fk_nqt_lsdonhang_donhang   FOREIGN KEY (nqt_ma_don_hang)    REFERENCES NqtDonHang (nqt_ma_don_hang) ON DELETE CASCADE,
    CONSTRAINT fk_nqt_lsdonhang_nguoithd  FOREIGN KEY (nqt_nguoi_thay_doi) REFERENCES NqtNguoiDung (nqt_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 15: MÃ GIẢM GIÁ & KHUYẾN MÃI
-- ============================================================

CREATE TABLE NqtMaGiamGia (
    nqt_ma_coupon               INT             NOT NULL AUTO_INCREMENT,
    nqt_ma                      VARCHAR(50)     NOT NULL COMMENT '''GS30'',''SUMMER20''',
    nqt_ten_mo_ta               VARCHAR(255)    NULL,
    nqt_loai_giam               VARCHAR(20)     NOT NULL COMMENT '''so_tien_co_dinh'',''phan_tram''',
    nqt_gia_tri_giam            DECIMAL(15,0)   NOT NULL,
    nqt_don_hang_toi_thieu      DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_giam_toi_da             DECIMAL(15,0)   NULL COMMENT 'Cap cho % discount',
    nqt_so_luot_tong_cong       INT             NULL COMMENT 'NULL = không giới hạn',
    nqt_so_luot_da_dung         INT             NOT NULL DEFAULT 0,
    nqt_so_luot_moi_kh          INT             NOT NULL DEFAULT 1,
    nqt_ma_danh_muc_loai_tru    JSON            NULL COMMENT 'Category IDs bị loại trừ',
    nqt_ma_thuong_hieu_loai_tru JSON            NULL COMMENT 'Brand IDs bị loại trừ',
    nqt_chi_ap_dung_hang        INT             NULL COMMENT 'Chỉ cho tier cụ thể',
    nqt_ngay_bat_dau            DATETIME        NOT NULL,
    nqt_ngay_ket_thuc           DATETIME        NOT NULL,
    nqt_la_hoat_dong            TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_ghi_chu_noi_bo          VARCHAR(255)    NULL,
    nqt_ngay_tao                DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_coupon),
    UNIQUE KEY uk_nqt_magiam_ma (nqt_ma),
    KEY idx_nqt_magiam_ngay  (nqt_ngay_bat_dau, nqt_ngay_ket_thuc),
    CONSTRAINT fk_nqt_magiam_hang FOREIGN KEY (nqt_chi_ap_dung_hang) REFERENCES NqtHangThanhVien (nqt_ma_hang) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtKhuyenMaiMuaKem (
    nqt_ma_uu_dai           INT             NOT NULL AUTO_INCREMENT,
    nqt_ten                 VARCHAR(100)    NOT NULL,
    nqt_ma_san_pham_kich    INT             NULL COMMENT 'Sản phẩm trigger',
    nqt_ma_danh_muc_kich    INT             NULL COMMENT 'Danh mục trigger',
    nqt_ma_san_pham_tang    INT             NOT NULL COMMENT 'Sản phẩm đề xuất mua kèm',
    nqt_gia_khuyen_mai      DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_la_tang_kem         TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '1=free gift, 0=giảm giá',
    nqt_ngay_bat_dau        DATETIME        NOT NULL,
    nqt_ngay_ket_thuc       DATETIME        NOT NULL,
    nqt_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nqt_ma_uu_dai),
    CONSTRAINT fk_nqt_kmmuakem_spkich  FOREIGN KEY (nqt_ma_san_pham_kich) REFERENCES NqtSanPham (nqt_ma_san_pham) ON DELETE SET NULL,
    CONSTRAINT fk_nqt_kmmuakem_dmkich  FOREIGN KEY (nqt_ma_danh_muc_kich) REFERENCES NqtDanhMucSanPham (nqt_ma_danh_muc) ON DELETE SET NULL,
    CONSTRAINT fk_nqt_kmmuakem_sptang  FOREIGN KEY (nqt_ma_san_pham_tang) REFERENCES NqtSanPham (nqt_ma_san_pham)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtBanner (
    nqt_ma_banner           INT             NOT NULL AUTO_INCREMENT,
    nqt_vi_tri              VARCHAR(50)     NOT NULL COMMENT '''trang_chu_slider'',''popup'',''sidebar'',''header''',
    nqt_tieu_de             VARCHAR(255)    NULL,
    nqt_hinh_anh            VARCHAR(500)    NOT NULL,
    nqt_hinh_anh_mobile     VARCHAR(500)    NULL,
    nqt_url_lien_ket        VARCHAR(500)    NULL,
    nqt_mo_ta               VARCHAR(500)    NULL,
    nqt_ngay_bat_dau        DATETIME        NOT NULL,
    nqt_ngay_ket_thuc       DATETIME        NOT NULL,
    nqt_thu_tu              INT             NOT NULL DEFAULT 0,
    nqt_la_hoat_dong        TINYINT(1)      NOT NULL DEFAULT 1,
    PRIMARY KEY (nqt_ma_banner),
    KEY idx_nqt_banner_vitri (nqt_vi_tri),
    KEY idx_nqt_banner_ngay  (nqt_ngay_bat_dau, nqt_ngay_ket_thuc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- GROUP 16: THANH TOÁN
-- ============================================================

CREATE TABLE NqtThanhToan (
    nqt_ma_thanh_toan           INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_don_hang             INT             NULL,
    nqt_ma_dang_ky_goi          INT             NULL COMMENT 'Cho gym subscription',
    nqt_so_tien                 DECIMAL(15,0)   NOT NULL,
    nqt_phuong_thuc             VARCHAR(30)     NOT NULL COMMENT '''cod'',''chuyen_khoan'',''vnpay'',''momo'',''the_tin_dung''',
    nqt_trang_thai              VARCHAR(20)     NOT NULL DEFAULT 'cho_xu_ly' COMMENT '''cho_xu_ly'',''thanh_cong'',''that_bai'',''hoan_tien''',
    nqt_ma_giao_dich_ngoai      VARCHAR(255)    NULL COMMENT 'Transaction ID từ cổng thanh toán',
    nqt_ngan_hang               VARCHAR(50)     NULL,
    nqt_so_tai_khoan_gui        VARCHAR(50)     NULL,
    nqt_thoi_gian_thanh_toan    DATETIME        NULL,
    nqt_ghi_chu                 VARCHAR(500)    NULL,
    nqt_ngay_tao                DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_thanh_toan),
    KEY idx_nqt_thanhtoan_donhang (nqt_ma_don_hang),
    KEY idx_nqt_thanhtoan_trangthai(nqt_trang_thai),
    CONSTRAINT fk_nqt_thanhtoan_donhang FOREIGN KEY (nqt_ma_don_hang) REFERENCES NqtDonHang (nqt_ma_don_hang) ON DELETE SET NULL,
    CONSTRAINT fk_nqt_thanhtoan_dkgoi   FOREIGN KEY (nqt_ma_dang_ky_goi) REFERENCES NqtDangKyGoiTap (nqt_ma_dang_ky) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtHoaDon (
    nqt_ma_hoa_don          INT             NOT NULL AUTO_INCREMENT,
    nqt_so_hoa_don          VARCHAR(20)     NOT NULL COMMENT 'HD2025001234',
    nqt_ma_don_hang         INT             NULL,
    nqt_ma_thanh_toan       INT             NOT NULL,
    nqt_thong_tin_nguoi_mua JSON            NULL COMMENT 'Snapshot thông tin người mua',
    nqt_tong_tien           DECIMAL(15,0)   NOT NULL,
    nqt_thue_vat            DECIMAL(15,0)   NOT NULL DEFAULT 0,
    nqt_ngay_xuat           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_duong_dan_pdf       VARCHAR(500)    NULL,
    PRIMARY KEY (nqt_ma_hoa_don),
    UNIQUE KEY uk_nqt_hoadon_so (nqt_so_hoa_don),
    KEY idx_nqt_hoadon_donhang   (nqt_ma_don_hang),
    CONSTRAINT fk_nqt_hoadon_donhang   FOREIGN KEY (nqt_ma_don_hang)   REFERENCES NqtDonHang (nqt_ma_don_hang) ON DELETE SET NULL,
    CONSTRAINT fk_nqt_hoadon_thanhtoan FOREIGN KEY (nqt_ma_thanh_toan) REFERENCES NqtThanhToan (nqt_ma_thanh_toan)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- FK bị hoãn ở part 1 - thêm vào sau khi NqtThanhToan đã tồn tại
ALTER TABLE NqtDangKyGoiTap
    ADD CONSTRAINT fk_nqt_dkgoitap_thanhtoan FOREIGN KEY (nqt_ma_thanh_toan) REFERENCES NqtThanhToan (nqt_ma_thanh_toan) ON DELETE SET NULL;

ALTER TABLE NqtDangKyGoiPT
    ADD CONSTRAINT fk_nqt_dkgoipt_thanhtoan FOREIGN KEY (nqt_ma_thanh_toan) REFERENCES NqtThanhToan (nqt_ma_thanh_toan) ON DELETE SET NULL;

ALTER TABLE NqtDatDichVu
    ADD CONSTRAINT fk_nqt_datdichvu_thanhtoan FOREIGN KEY (nqt_ma_thanh_toan) REFERENCES NqtThanhToan (nqt_ma_thanh_toan) ON DELETE SET NULL;

-- FK điểm → đơn hàng
ALTER TABLE NqtGiaoDichDiem
    ADD CONSTRAINT fk_nqt_gddiem_donhang FOREIGN KEY (nqt_ma_don_hang) REFERENCES NqtDonHang (nqt_ma_don_hang) ON DELETE SET NULL;

-- FK lịch sử tồn kho → đơn hàng
ALTER TABLE NqtLichSuTonKho
    ADD CONSTRAINT fk_nqt_lstonkho_donhang FOREIGN KEY (nqt_ma_don_hang) REFERENCES NqtDonHang (nqt_ma_don_hang) ON DELETE SET NULL;

SET FOREIGN_KEY_CHECKS = 1;
