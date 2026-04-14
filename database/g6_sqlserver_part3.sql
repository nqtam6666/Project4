-- ============================================================
-- G6 GYM MANAGEMENT + SUPPLEMENT STORE
-- SQL Server Schema - Part 3: Group 11-16
-- GROUP 11: KHO HÀNG | GROUP 12: KHÁCH HÀNG ONLINE
-- GROUP 13: TÍCH ĐIỂM | GROUP 14: GIỎ HÀNG & ĐƠN HÀNG
-- GROUP 15: KHUYẾN MÃI | GROUP 16: THANH TOÁN
-- ============================================================

-- ============================================================
-- GROUP 11: KHO HÀNG
-- ============================================================

CREATE TABLE G6TonKho (
    g6_ma_ton_kho          INT             NOT NULL IDENTITY(1,1),
    g6_ma_bien_the         INT             NOT NULL,
    g6_ma_chi_nhanh        INT             NULL,        -- NULL = kho online tổng
    g6_so_luong            INT             NOT NULL DEFAULT 0,
    g6_so_luong_dat_truoc  INT             NOT NULL DEFAULT 0, -- Đã đặt chưa giao
    g6_nguong_canh_bao     INT             NOT NULL DEFAULT 10,
    g6_ngay_cap_nhat       DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6TonKho PRIMARY KEY (g6_ma_ton_kho),
    CONSTRAINT UK_G6TonKho UNIQUE (g6_ma_bien_the, g6_ma_chi_nhanh),
    CONSTRAINT FK_G6TonKho_BienThe FOREIGN KEY (g6_ma_bien_the) REFERENCES G6BienTheSanPham (g6_ma_bien_the),
    CONSTRAINT FK_G6TonKho_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh) ON DELETE SET NULL
);

CREATE TABLE G6LichSuTonKho (
    g6_ma_lich_su          INT             NOT NULL IDENTITY(1,1),
    g6_ma_bien_the         INT             NOT NULL,
    g6_ma_chi_nhanh        INT             NULL,
    g6_loai_giao_dich      NVARCHAR(20)    NOT NULL,    -- 'nhap','xuat','dieu_chuyen','tra_hang','kiem_ke'
    g6_so_luong_thay_doi   INT             NOT NULL,    -- Âm = xuất, dương = nhập
    g6_so_luong_truoc      INT             NOT NULL,
    g6_so_luong_sau        INT             NOT NULL,
    g6_ma_don_hang         INT             NULL,
    g6_ghi_chu             NVARCHAR(255)   NULL,
    g6_nguoi_thuc_hien     INT             NULL,
    g6_thoi_gian           DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6LichSuTonKho PRIMARY KEY (g6_ma_lich_su),
    CONSTRAINT FK_G6LSTK_BienThe FOREIGN KEY (g6_ma_bien_the) REFERENCES G6BienTheSanPham (g6_ma_bien_the),
    CONSTRAINT FK_G6LSTK_NguoiTH FOREIGN KEY (g6_nguoi_thuc_hien) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
);

-- ============================================================
-- GROUP 12: KHÁCH HÀNG ONLINE
-- ============================================================

CREATE TABLE G6KhachHang (
    g6_ma_khach_hang   INT             NOT NULL IDENTITY(1,1),
    g6_so_dien_thoai   NVARCHAR(15)    NOT NULL,
    g6_email           NVARCHAR(100)   NULL,
    g6_ho_ten          NVARCHAR(100)   NULL,
    g6_ngay_sinh       DATE            NULL,
    g6_gioi_tinh       NVARCHAR(10)    NULL,
    g6_google_id       NVARCHAR(100)   NULL,            -- Social login
    g6_da_xac_thuc_otp BIT             NOT NULL DEFAULT 0,
    g6_ma_hoi_vien     INT             NULL,             -- Link nếu cũng là hội viên gym
    g6_ngay_dang_ky    DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_la_hoat_dong    BIT             NOT NULL DEFAULT 1,
    CONSTRAINT PK_G6KhachHang PRIMARY KEY (g6_ma_khach_hang),
    CONSTRAINT UK_G6KhachHang_SDT UNIQUE (g6_so_dien_thoai),
    CONSTRAINT FK_G6KH_HoiVien FOREIGN KEY (g6_ma_hoi_vien) REFERENCES G6HoiVien (g6_ma_hoi_vien) ON DELETE SET NULL
);

CREATE TABLE G6DiaChiGiaoHang (
    g6_ma_dia_chi          INT             NOT NULL IDENTITY(1,1),
    g6_ma_khach_hang       INT             NOT NULL,
    g6_ho_ten_nguoi_nhan   NVARCHAR(100)   NOT NULL,
    g6_so_dien_thoai       NVARCHAR(15)    NOT NULL,
    g6_dia_chi             NVARCHAR(255)   NOT NULL,
    g6_phuong_xa           NVARCHAR(100)   NULL,
    g6_quan_huyen          NVARCHAR(100)   NULL,
    g6_tinh_thanh          NVARCHAR(100)   NOT NULL,
    g6_la_mac_dinh         BIT             NOT NULL DEFAULT 0,
    CONSTRAINT PK_G6DiaChiGH PRIMARY KEY (g6_ma_dia_chi),
    CONSTRAINT FK_G6DiaChi_KH FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE CASCADE
);

-- ============================================================
-- GROUP 13: TÍCH ĐIỂM & HẠNG THÀNH VIÊN
-- ============================================================

CREATE TABLE G6HangThanhVien (
    g6_ma_hang             INT             NOT NULL IDENTITY(1,1),
    g6_ten_hang            NVARCHAR(50)    NOT NULL,    -- 'Đồng','Bạc','Vàng','Kim Cương'
    g6_diem_toi_thieu      INT             NOT NULL DEFAULT 0,
    g6_ti_le_tich_diem     DECIMAL(5,2)    NOT NULL DEFAULT 1.00, -- 1 điểm / X đồng
    g6_ti_le_dung_diem     DECIMAL(5,2)    NOT NULL DEFAULT 100.00, -- 1 điểm = X đồng
    g6_giam_gia_phan_tram  DECIMAL(5,2)    NOT NULL DEFAULT 0, -- % giảm giá cố định
    g6_quyen_loi           NVARCHAR(MAX)   NULL,        -- JSON: ["free_shipping","priority_booking"]
    g6_mau_hien_thi        NVARCHAR(20)    NULL,
    CONSTRAINT PK_G6HangTV PRIMARY KEY (g6_ma_hang)
);

INSERT INTO G6HangThanhVien (g6_ten_hang, g6_diem_toi_thieu, g6_ti_le_tich_diem, g6_giam_gia_phan_tram, g6_mau_hien_thi) VALUES
(N'Đồng',        0,      1.00,   0,    '#cd7f32'),
(N'Bạc',         1000,   1.20,   2,    '#c0c0c0'),
(N'Vàng',        5000,   1.50,   5,    '#ffd700'),
(N'Kim Cương',   20000,  2.00,   10,   '#b9f2ff');

CREATE TABLE G6DiemKhachHang (
    g6_ma_diem             INT             NOT NULL IDENTITY(1,1),
    g6_ma_khach_hang       INT             NOT NULL,
    g6_so_diem_hien_tai    INT             NOT NULL DEFAULT 0,
    g6_tong_diem_lich_su   INT             NOT NULL DEFAULT 0,
    g6_ma_hang             INT             NOT NULL DEFAULT 1,
    g6_ngay_cap_nhat_hang  DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6DiemKH PRIMARY KEY (g6_ma_diem),
    CONSTRAINT UK_G6DiemKH_KH UNIQUE (g6_ma_khach_hang),
    CONSTRAINT FK_G6DiemKH_KH FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE CASCADE,
    CONSTRAINT FK_G6DiemKH_Hang FOREIGN KEY (g6_ma_hang) REFERENCES G6HangThanhVien (g6_ma_hang)
);

CREATE TABLE G6GiaoDichDiem (
    g6_ma_giao_dich        INT             NOT NULL IDENTITY(1,1),
    g6_ma_khach_hang       INT             NOT NULL,
    g6_ma_don_hang         INT             NULL,
    g6_loai                NVARCHAR(20)    NOT NULL,    -- 'kich_hoat','su_dung','het_han','dieu_chinh'
    g6_so_diem             INT             NOT NULL,    -- Âm = dùng, dương = tích
    g6_so_diem_truoc       INT             NOT NULL,
    g6_so_diem_sau         INT             NOT NULL,
    g6_ghi_chu             NVARCHAR(255)   NULL,
    g6_thoi_gian           DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_het_han_diem   DATETIME2       NULL,
    CONSTRAINT PK_G6GiaoDichDiem PRIMARY KEY (g6_ma_giao_dich),
    CONSTRAINT FK_G6GDDiem_KH FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang)
);

-- ============================================================
-- GROUP 14: GIỎ HÀNG & ĐƠN HÀNG
-- ============================================================

CREATE TABLE G6GioHang (
    g6_ma_gio_hang     INT             NOT NULL IDENTITY(1,1),
    g6_ma_khach_hang   INT             NULL,             -- NULL = guest
    g6_session_id      NVARCHAR(100)   NULL,             -- Guest cart session
    g6_ngay_tao        DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_cap_nhat   DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6GioHang PRIMARY KEY (g6_ma_gio_hang),
    CONSTRAINT FK_G6GioHang_KH FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE CASCADE
);

CREATE TABLE G6ChiTietGioHang (
    g6_ma_chi_tiet_gio     INT             NOT NULL IDENTITY(1,1),
    g6_ma_gio_hang         INT             NOT NULL,
    g6_ma_bien_the         INT             NOT NULL,
    g6_so_luong            INT             NOT NULL DEFAULT 1,
    g6_gia_tai_thoi_diem   DECIMAL(15,0)   NOT NULL,
    g6_ngay_them           DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6CTGioHang PRIMARY KEY (g6_ma_chi_tiet_gio),
    CONSTRAINT UK_G6CTGio UNIQUE (g6_ma_gio_hang, g6_ma_bien_the),
    CONSTRAINT FK_G6CTGio_GioHang FOREIGN KEY (g6_ma_gio_hang) REFERENCES G6GioHang (g6_ma_gio_hang) ON DELETE CASCADE,
    CONSTRAINT FK_G6CTGio_BienThe FOREIGN KEY (g6_ma_bien_the) REFERENCES G6BienTheSanPham (g6_ma_bien_the)
);

CREATE TABLE G6DonHang (
    g6_ma_don_hang             INT             NOT NULL IDENTITY(1,1),
    g6_ma_don_hang_hien        NVARCHAR(20)    NOT NULL, -- G62025001234
    g6_ma_khach_hang           INT             NULL,
    g6_ten_nguoi_dat           NVARCHAR(100)   NOT NULL,
    g6_so_dien_thoai_dat       NVARCHAR(15)    NOT NULL,
    g6_email_dat               NVARCHAR(100)   NULL,
    g6_dia_chi_giao_hang       NVARCHAR(MAX)   NULL,     -- JSON snapshot địa chỉ lúc đặt
    g6_tinh_thanh_giao         NVARCHAR(100)   NULL,
    g6_phuong_thuc_giao        NVARCHAR(20)    NOT NULL DEFAULT 'giao_hang', -- 'giao_hang','nhan_tai_cua_hang'
    g6_ma_chi_nhanh_nhan       INT             NULL,     -- Nếu nhận tại cửa hàng
    g6_tong_tien_hang          DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_phi_van_chuyen          DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_giam_gia_coupon         DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_giam_gia_diem           DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_giam_gia_hang           DECIMAL(15,0)   NOT NULL DEFAULT 0, -- Giảm theo hạng thành viên
    g6_tong_thanh_toan         DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_ma_coupon_da_dung       NVARCHAR(50)    NULL,
    g6_diem_da_dung            INT             NOT NULL DEFAULT 0,
    g6_diem_tich_duoc          INT             NOT NULL DEFAULT 0,
    g6_trang_thai              NVARCHAR(30)    NOT NULL DEFAULT 'cho_xac_nhan',
    g6_trang_thai_thanh_toan   NVARCHAR(20)    NOT NULL DEFAULT 'cho_thanh_toan',
    g6_phuong_thuc_thanh_toan  NVARCHAR(30)    NULL,     -- 'cod','chuyen_khoan','vnpay','momo','the'
    g6_ghi_chu_khach           NVARCHAR(500)   NULL,
    g6_ghi_chu_noi_bo          NVARCHAR(500)   NULL,
    g6_nguon_don_hang          NVARCHAR(20)    NOT NULL DEFAULT 'website', -- 'website','dien_thoai','tai_quay','app'
    g6_nguoi_tao               INT             NULL,     -- Nhân viên tạo hộ
    g6_ngay_tao                DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_cap_nhat           DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_giao_du_kien       DATE            NULL,
    g6_ngay_giao_thuc_te       DATETIME2       NULL,
    CONSTRAINT PK_G6DonHang PRIMARY KEY (g6_ma_don_hang),
    CONSTRAINT UK_G6DonHang_MaHien UNIQUE (g6_ma_don_hang_hien),
    CONSTRAINT FK_G6DH_KhachHang FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE SET NULL,
    CONSTRAINT FK_G6DH_ChiNhanh FOREIGN KEY (g6_ma_chi_nhanh_nhan) REFERENCES G6ChiNhanh (g6_ma_chi_nhanh) ON DELETE SET NULL,
    CONSTRAINT FK_G6DH_NguoiTao FOREIGN KEY (g6_nguoi_tao) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
);

CREATE TABLE G6ChiTietDonHang (
    g6_ma_chi_tiet             INT             NOT NULL IDENTITY(1,1),
    g6_ma_don_hang             INT             NOT NULL,
    g6_ma_bien_the             INT             NOT NULL,
    g6_ten_san_pham_snap       NVARCHAR(255)   NOT NULL, -- Snapshot tên lúc đặt
    g6_sku_snap                NVARCHAR(100)   NOT NULL,
    g6_so_luong                INT             NOT NULL,
    g6_don_gia                 DECIMAL(15,0)   NOT NULL,
    g6_giam_gia_tung_san_pham  DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_thanh_tien              DECIMAL(15,0)   NOT NULL,
    CONSTRAINT PK_G6CTDonHang PRIMARY KEY (g6_ma_chi_tiet),
    CONSTRAINT FK_G6CTDH_DonHang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE CASCADE,
    CONSTRAINT FK_G6CTDH_BienThe FOREIGN KEY (g6_ma_bien_the) REFERENCES G6BienTheSanPham (g6_ma_bien_the)
);

CREATE TABLE G6LichSuDonHang (
    g6_ma_lich_su_don  INT             NOT NULL IDENTITY(1,1),
    g6_ma_don_hang     INT             NOT NULL,
    g6_trang_thai_cu   NVARCHAR(30)    NULL,
    g6_trang_thai_moi  NVARCHAR(30)    NOT NULL,
    g6_ghi_chu         NVARCHAR(500)   NULL,
    g6_nguoi_thay_doi  INT             NULL,
    g6_thoi_gian       DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6LichSuDH PRIMARY KEY (g6_ma_lich_su_don),
    CONSTRAINT FK_G6LSDH_DonHang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE CASCADE,
    CONSTRAINT FK_G6LSDH_NguoiTD FOREIGN KEY (g6_nguoi_thay_doi) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
);

-- ============================================================
-- GROUP 15: MÃ GIẢM GIÁ & KHUYẾN MÃI
-- ============================================================

CREATE TABLE G6MaGiamGia (
    g6_ma_coupon               INT             NOT NULL IDENTITY(1,1),
    g6_ma                      NVARCHAR(50)    NOT NULL, -- 'GS30','SUMMER20'
    g6_ten_mo_ta               NVARCHAR(255)   NULL,
    g6_loai_giam               NVARCHAR(20)    NOT NULL, -- 'so_tien_co_dinh','phan_tram'
    g6_gia_tri_giam            DECIMAL(15,0)   NOT NULL,
    g6_don_hang_toi_thieu      DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_giam_toi_da             DECIMAL(15,0)   NULL,     -- Cap cho % discount
    g6_so_luot_tong_cong       INT             NULL,     -- NULL = không giới hạn
    g6_so_luot_da_dung         INT             NOT NULL DEFAULT 0,
    g6_so_luot_moi_kh          INT             NOT NULL DEFAULT 1,
    g6_ma_danh_muc_loai_tru    NVARCHAR(MAX)   NULL,     -- JSON: Category IDs bị loại trừ
    g6_ma_thuong_hieu_loai_tru NVARCHAR(MAX)   NULL,     -- JSON: Brand IDs bị loại trừ
    g6_chi_ap_dung_hang        INT             NULL,     -- Chỉ cho tier cụ thể
    g6_ngay_bat_dau            DATETIME2       NOT NULL,
    g6_ngay_ket_thuc           DATETIME2       NOT NULL,
    g6_la_hoat_dong            BIT             NOT NULL DEFAULT 1,
    g6_ghi_chu_noi_bo          NVARCHAR(255)   NULL,
    g6_ngay_tao                DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6MaGiamGia PRIMARY KEY (g6_ma_coupon),
    CONSTRAINT UK_G6MaGiam_Ma UNIQUE (g6_ma),
    CONSTRAINT FK_G6MaGiam_Hang FOREIGN KEY (g6_chi_ap_dung_hang) REFERENCES G6HangThanhVien (g6_ma_hang) ON DELETE SET NULL
);

CREATE TABLE G6KhuyenMaiMuaKem (
    g6_ma_uu_dai           INT             NOT NULL IDENTITY(1,1),
    g6_ten                 NVARCHAR(100)   NOT NULL,
    g6_ma_san_pham_kich    INT             NULL,         -- Sản phẩm trigger
    g6_ma_danh_muc_kich    INT             NULL,         -- Danh mục trigger
    g6_ma_san_pham_tang    INT             NOT NULL,     -- Sản phẩm đề xuất mua kèm
    g6_gia_khuyen_mai      DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_la_tang_kem         BIT             NOT NULL DEFAULT 0, -- 1=free gift, 0=giảm giá
    g6_ngay_bat_dau        DATETIME2       NOT NULL,
    g6_ngay_ket_thuc       DATETIME2       NOT NULL,
    g6_la_hoat_dong        BIT             NOT NULL DEFAULT 1,
    CONSTRAINT PK_G6KMuaKem PRIMARY KEY (g6_ma_uu_dai),
    CONSTRAINT FK_G6KM_SPKich FOREIGN KEY (g6_ma_san_pham_kich) REFERENCES G6SanPham (g6_ma_san_pham) ON DELETE SET NULL,
    CONSTRAINT FK_G6KM_DMKich FOREIGN KEY (g6_ma_danh_muc_kich) REFERENCES G6DanhMucSanPham (g6_ma_danh_muc) ON DELETE SET NULL,
    CONSTRAINT FK_G6KM_SPTang FOREIGN KEY (g6_ma_san_pham_tang) REFERENCES G6SanPham (g6_ma_san_pham)
);

CREATE TABLE G6Banner (
    g6_ma_banner           INT             NOT NULL IDENTITY(1,1),
    g6_vi_tri              NVARCHAR(50)    NOT NULL,     -- 'trang_chu_slider','popup','sidebar','header'
    g6_tieu_de             NVARCHAR(255)   NULL,
    g6_hinh_anh            NVARCHAR(500)   NOT NULL,
    g6_hinh_anh_mobile     NVARCHAR(500)   NULL,
    g6_url_lien_ket        NVARCHAR(500)   NULL,
    g6_mo_ta               NVARCHAR(500)   NULL,
    g6_ngay_bat_dau        DATETIME2       NOT NULL,
    g6_ngay_ket_thuc       DATETIME2       NOT NULL,
    g6_thu_tu              INT             NOT NULL DEFAULT 0,
    g6_la_hoat_dong        BIT             NOT NULL DEFAULT 1,
    CONSTRAINT PK_G6Banner PRIMARY KEY (g6_ma_banner)
);

-- ============================================================
-- GROUP 16: THANH TOÁN
-- ============================================================

CREATE TABLE G6ThanhToan (
    g6_ma_thanh_toan           INT             NOT NULL IDENTITY(1,1),
    g6_ma_don_hang             INT             NULL,
    g6_ma_dang_ky_goi          INT             NULL,     -- Cho gym subscription
    g6_so_tien                 DECIMAL(15,0)   NOT NULL,
    g6_phuong_thuc             NVARCHAR(30)    NOT NULL, -- 'cod','chuyen_khoan','vnpay','momo','the_tin_dung'
    g6_trang_thai              NVARCHAR(20)    NOT NULL DEFAULT 'cho_xu_ly', -- 'cho_xu_ly','thanh_cong','that_bai','hoan_tien'
    g6_ma_giao_dich_ngoai      NVARCHAR(255)   NULL,     -- Transaction ID từ cổng thanh toán
    g6_ngan_hang               NVARCHAR(50)    NULL,
    g6_so_tai_khoan_gui        NVARCHAR(50)    NULL,
    g6_thoi_gian_thanh_toan    DATETIME2       NULL,
    g6_ghi_chu                 NVARCHAR(500)   NULL,
    g6_ngay_tao                DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6ThanhToan PRIMARY KEY (g6_ma_thanh_toan),
    CONSTRAINT FK_G6TT_DonHang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE SET NULL,
    CONSTRAINT FK_G6TT_DKGoi FOREIGN KEY (g6_ma_dang_ky_goi) REFERENCES G6DangKyGoiTap (g6_ma_dang_ky) ON DELETE SET NULL
);

CREATE TABLE G6HoaDon (
    g6_ma_hoa_don          INT             NOT NULL IDENTITY(1,1),
    g6_so_hoa_don          NVARCHAR(20)    NOT NULL,     -- HD2025001234
    g6_ma_don_hang         INT             NULL,
    g6_ma_thanh_toan       INT             NOT NULL,
    g6_thong_tin_nguoi_mua NVARCHAR(MAX)   NULL,         -- JSON snapshot thông tin người mua
    g6_tong_tien           DECIMAL(15,0)   NOT NULL,
    g6_thue_vat            DECIMAL(15,0)   NOT NULL DEFAULT 0,
    g6_ngay_xuat           DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_duong_dan_pdf       NVARCHAR(500)   NULL,
    CONSTRAINT PK_G6HoaDon PRIMARY KEY (g6_ma_hoa_don),
    CONSTRAINT UK_G6HoaDon_So UNIQUE (g6_so_hoa_don),
    CONSTRAINT FK_G6HD_DonHang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE SET NULL,
    CONSTRAINT FK_G6HD_ThanhToan FOREIGN KEY (g6_ma_thanh_toan) REFERENCES G6ThanhToan (g6_ma_thanh_toan)
);

-- FK bị hoãn ở part 1 - thêm vào sau khi G6ThanhToan đã tồn tại
ALTER TABLE G6DangKyGoiTap
    ADD CONSTRAINT FK_G6DKGT_ThanhToan FOREIGN KEY (g6_ma_thanh_toan) REFERENCES G6ThanhToan (g6_ma_thanh_toan) ON DELETE SET NULL;

ALTER TABLE G6DangKyGoiPT
    ADD CONSTRAINT FK_G6DKPT_ThanhToan FOREIGN KEY (g6_ma_thanh_toan) REFERENCES G6ThanhToan (g6_ma_thanh_toan) ON DELETE SET NULL;

ALTER TABLE G6DatDichVu
    ADD CONSTRAINT FK_G6DatDV_ThanhToan FOREIGN KEY (g6_ma_thanh_toan) REFERENCES G6ThanhToan (g6_ma_thanh_toan) ON DELETE SET NULL;

-- FK điểm → đơn hàng
ALTER TABLE G6GiaoDichDiem
    ADD CONSTRAINT FK_G6GDDiem_DonHang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE SET NULL;

-- FK lịch sử tồn kho → đơn hàng
ALTER TABLE G6LichSuTonKho
    ADD CONSTRAINT FK_G6LSTK_DonHang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE SET NULL;

-- Index
CREATE INDEX IX_G6TonKho_ChiNhanh ON G6TonKho (g6_ma_chi_nhanh);
CREATE INDEX IX_G6LSTK_BienThe ON G6LichSuTonKho (g6_ma_bien_the);
CREATE INDEX IX_G6LSTK_ThoiGian ON G6LichSuTonKho (g6_thoi_gian);
CREATE INDEX IX_G6KhachHang_HoiVien ON G6KhachHang (g6_ma_hoi_vien);
CREATE INDEX IX_G6DiaChi_KH ON G6DiaChiGiaoHang (g6_ma_khach_hang);
CREATE INDEX IX_G6GDDiem_KH ON G6GiaoDichDiem (g6_ma_khach_hang);
CREATE INDEX IX_G6GioHang_KH ON G6GioHang (g6_ma_khach_hang);
CREATE INDEX IX_G6GioHang_Session ON G6GioHang (g6_session_id);
CREATE INDEX IX_G6DonHang_KH ON G6DonHang (g6_ma_khach_hang);
CREATE INDEX IX_G6DonHang_TrangThai ON G6DonHang (g6_trang_thai);
CREATE INDEX IX_G6DonHang_NgayTao ON G6DonHang (g6_ngay_tao);
CREATE INDEX IX_G6CTDH_DonHang ON G6ChiTietDonHang (g6_ma_don_hang);
CREATE INDEX IX_G6LSDH_DonHang ON G6LichSuDonHang (g6_ma_don_hang);
CREATE INDEX IX_G6MaGiam_Ngay ON G6MaGiamGia (g6_ngay_bat_dau, g6_ngay_ket_thuc);
CREATE INDEX IX_G6Banner_ViTri ON G6Banner (g6_vi_tri);
CREATE INDEX IX_G6TT_DonHang ON G6ThanhToan (g6_ma_don_hang);
CREATE INDEX IX_G6TT_TrangThai ON G6ThanhToan (g6_trang_thai);
CREATE INDEX IX_G6HD_DonHang ON G6HoaDon (g6_ma_don_hang);

PRINT N'Part 3 - Hoàn thành!';
GO
