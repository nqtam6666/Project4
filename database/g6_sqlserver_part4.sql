-- ============================================================
-- G6 GYM MANAGEMENT + SUPPLEMENT STORE
-- SQL Server Schema - Part 4: Group 17-20
-- GROUP 17: VẬN CHUYỂN | GROUP 18: NỘI DUNG / BLOG
-- GROUP 19: THÔNG BÁO  | GROUP 20: XÁC THỰC OTP
-- ============================================================

-- ============================================================
-- GROUP 17: VẬN CHUYỂN
-- ============================================================

CREATE TABLE G6DonViVanChuyen (
    g6_ma_don_vi           INT             NOT NULL IDENTITY(1,1),
    g6_ten_don_vi          NVARCHAR(100)   NOT NULL,
    g6_ma_api              NVARCHAR(50)    NULL,         -- Mã đơn vị: ghn, ghtk, ...
    g6_mo_ta               NVARCHAR(255)   NULL,
    g6_logo_url            NVARCHAR(500)   NULL,
    g6_trang_thai          BIT             NOT NULL DEFAULT 1, -- 1=hoạt động, 0=tắt
    g6_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6DonViVC PRIMARY KEY (g6_ma_don_vi)
);

CREATE TABLE G6VungVanChuyen (
    g6_ma_vung             INT             NOT NULL IDENTITY(1,1),
    g6_ma_don_vi           INT             NOT NULL,
    g6_ten_vung            NVARCHAR(150)   NOT NULL,     -- VD: Hà Nội, TP.HCM
    g6_ma_tinh             NVARCHAR(20)    NULL,         -- Mã tỉnh/thành theo GHN/GHTK
    g6_phi_co_ban          DECIMAL(12,2)   NOT NULL DEFAULT 0, -- Phí giao hàng cơ bản (VND)
    g6_phi_them_theo_kg    DECIMAL(12,2)   NOT NULL DEFAULT 0, -- Phí tăng thêm / kg vượt mức
    g6_trong_luong_mien_phi DECIMAL(8,3)   NOT NULL DEFAULT 0, -- Kg được miễn phí phụ phí
    g6_thoi_gian_du_kien   NVARCHAR(50)    NULL,         -- VD: 2-3 ngày làm việc
    g6_don_hang_toi_thieu_mien_phi DECIMAL(12,2) NULL,   -- Đơn tối thiểu để freeship
    g6_trang_thai          BIT             NOT NULL DEFAULT 1,
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_cap_nhat       DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6VungVC PRIMARY KEY (g6_ma_vung),
    CONSTRAINT FK_G6VungVC_DonVi FOREIGN KEY (g6_ma_don_vi) REFERENCES G6DonViVanChuyen (g6_ma_don_vi)
);

-- Seed dữ liệu đơn vị vận chuyển
INSERT INTO G6DonViVanChuyen (g6_ten_don_vi, g6_ma_api, g6_mo_ta, g6_trang_thai, g6_thu_tu_hien_thi) VALUES
(N'Giao Hàng Nhanh',     'ghn',     N'Đối tác vận chuyển GHN',     1, 1),
(N'Giao Hàng Tiết Kiệm', 'ghtk',    N'Đối tác vận chuyển GHTK',    1, 2),
(N'Viettel Post',        'viettel',  N'Đối tác vận chuyển Viettel',  1, 3),
(N'Nội thành (tự giao)', 'internal', N'Giao hàng nội bộ trong ngày', 1, 4);

-- Seed vùng vận chuyển mẫu cho GHN
INSERT INTO G6VungVanChuyen
    (g6_ma_don_vi, g6_ten_vung, g6_ma_tinh, g6_phi_co_ban, g6_phi_them_theo_kg,
     g6_trong_luong_mien_phi, g6_thoi_gian_du_kien, g6_don_hang_toi_thieu_mien_phi, g6_trang_thai) VALUES
(1, N'Hà Nội',            'HN',  25000,  5000, 3, N'1-2 ngày',     399000, 1),
(1, N'TP. Hồ Chí Minh',  'HCM', 25000,  5000, 3, N'1-2 ngày',     399000, 1),
(1, N'Đà Nẵng',          'DN',  35000,  6000, 3, N'2-3 ngày',     499000, 1),
(1, N'Các tỉnh khác',    NULL,  45000,  7000, 2, N'3-5 ngày',     599000, 1);

-- ============================================================
-- GROUP 18: NỘI DUNG / BLOG
-- ============================================================

CREATE TABLE G6DanhMucBaiViet (
    g6_ma_danh_muc         INT             NOT NULL IDENTITY(1,1),
    g6_ten_danh_muc        NVARCHAR(150)   NOT NULL,
    g6_slug                NVARCHAR(200)   NOT NULL,
    g6_mo_ta               NVARCHAR(500)   NULL,
    -- Rule 3: Self-referencing FK — KHÔNG có ON DELETE
    g6_ma_cha              INT             NULL,         -- Danh mục cha (NULL = root)
    g6_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    g6_trang_thai          BIT             NOT NULL DEFAULT 1,
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6DMBaiViet PRIMARY KEY (g6_ma_danh_muc),
    CONSTRAINT UK_G6DMBaiViet_Slug UNIQUE (g6_slug),
    CONSTRAINT FK_G6DMBV_Cha FOREIGN KEY (g6_ma_cha) REFERENCES G6DanhMucBaiViet (g6_ma_danh_muc)
);

CREATE TABLE G6BaiViet (
    g6_ma_bai_viet         INT             NOT NULL IDENTITY(1,1),
    g6_ma_danh_muc         INT             NULL,
    g6_tieu_de             NVARCHAR(300)   NOT NULL,
    g6_slug                NVARCHAR(350)   NOT NULL,
    g6_tom_tat             NVARCHAR(MAX)   NULL,         -- Mô tả ngắn / excerpt
    g6_noi_dung            NVARCHAR(MAX)   NULL,         -- Nội dung HTML đầy đủ
    g6_anh_dai_dien        NVARCHAR(500)   NULL,
    g6_tac_gia             INT             NULL,         -- FK → G6NguoiDung
    g6_luot_xem            INT             NOT NULL DEFAULT 0,
    g6_trang_thai          NVARCHAR(20)    NOT NULL DEFAULT 'nhap', -- 'nhap','xuat_ban','an'
    g6_ngay_xuat_ban       DATETIME2       NULL,
    g6_tu_khoa             NVARCHAR(500)   NULL,         -- SEO keywords, comma-separated
    g6_mo_ta_seo           NVARCHAR(300)   NULL,         -- Meta description
    g6_san_pham_lien_quan  NVARCHAR(MAX)   NULL,         -- JSON: mảng g6_ma_san_pham liên quan
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_cap_nhat       DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6BaiViet PRIMARY KEY (g6_ma_bai_viet),
    CONSTRAINT UK_G6BaiViet_Slug UNIQUE (g6_slug),
    CONSTRAINT FK_G6BV_DanhMuc FOREIGN KEY (g6_ma_danh_muc) REFERENCES G6DanhMucBaiViet (g6_ma_danh_muc) ON DELETE SET NULL,
    CONSTRAINT FK_G6BV_TacGia FOREIGN KEY (g6_tac_gia) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
);

CREATE TABLE G6DanhGiaSanPham (
    g6_ma_danh_gia         INT             NOT NULL IDENTITY(1,1),
    g6_ma_san_pham         INT             NOT NULL,
    g6_ma_khach_hang       INT             NULL,         -- NULL = khách vãng lai
    g6_ma_don_hang         INT             NULL,         -- Đánh giá sau mua hàng
    g6_ten_nguoi_dung      NVARCHAR(100)   NULL,         -- Tên hiển thị khi review
    g6_so_sao              TINYINT         NOT NULL,     -- 1-5
    g6_tieu_de             NVARCHAR(200)   NULL,
    g6_noi_dung            NVARCHAR(MAX)   NULL,
    g6_hinh_anh            NVARCHAR(MAX)   NULL,         -- JSON: mảng URL ảnh đính kèm review
    g6_da_mua              BIT             NOT NULL DEFAULT 0, -- 1 = đã xác nhận mua hàng
    g6_trang_thai          NVARCHAR(20)    NOT NULL DEFAULT 'cho_duyet', -- 'cho_duyet','duoc_duyet','bi_an'
    g6_phan_hoi_shop       NVARCHAR(MAX)   NULL,         -- Shop phản hồi review
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_duyet          DATETIME2       NULL,
    CONSTRAINT PK_G6DanhGiaSP PRIMARY KEY (g6_ma_danh_gia),
    CONSTRAINT FK_G6DG_SanPham FOREIGN KEY (g6_ma_san_pham) REFERENCES G6SanPham (g6_ma_san_pham),
    CONSTRAINT FK_G6DG_KhachHang FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE SET NULL,
    CONSTRAINT FK_G6DG_DonHang FOREIGN KEY (g6_ma_don_hang) REFERENCES G6DonHang (g6_ma_don_hang) ON DELETE SET NULL
);

-- Seed danh mục bài viết
INSERT INTO G6DanhMucBaiViet
    (g6_ten_danh_muc, g6_slug, g6_mo_ta, g6_ma_cha, g6_thu_tu_hien_thi, g6_trang_thai) VALUES
(N'Kiến thức Gym',          'kien-thuc-gym',           N'Hướng dẫn tập luyện, kỹ thuật, chương trình',  NULL, 1, 1),
(N'Dinh dưỡng thể thao',    'dinh-duong-the-thao',     N'Chế độ ăn, bổ sung, thực phẩm chức năng',      NULL, 2, 1),
(N'Đánh giá sản phẩm',      'danh-gia-san-pham',       N'Review whey protein, BCAA, pre-workout,...',   NULL, 3, 1),
(N'Tin tức & Sự kiện',      'tin-tuc-su-kien',         N'Tin tức ngành gym và sự kiện phòng tập',        NULL, 4, 1),
(N'Câu hỏi thường gặp',     'cau-hoi-thuong-gap',      N'FAQ về tập luyện và thực phẩm bổ sung',        NULL, 5, 1),
-- Sub-categories
(N'Kỹ thuật tập luyện',     'ky-thuat-tap-luyen',      NULL, 1, 1, 1),
(N'Chương trình tập',       'chuong-trinh-tap',        NULL, 1, 2, 1),
(N'Phục hồi & Nghỉ ngơi',  'phuc-hoi-nghi-ngoi',      NULL, 1, 3, 1),
(N'Protein & Amino Acid',   'protein-amino-acid',      NULL, 2, 1, 1),
(N'Creatine & Pre-workout', 'creatine-pre-workout',    NULL, 2, 2, 1),
(N'Giảm cân & Đốt mỡ',     'giam-can-dot-mo',         NULL, 2, 3, 1);

-- ============================================================
-- GROUP 19: THÔNG BÁO
-- ============================================================

CREATE TABLE G6ThongBao (
    g6_ma_thong_bao        INT             NOT NULL IDENTITY(1,1),
    g6_ma_nguoi_nhan       INT             NULL,         -- NULL = broadcast toàn hệ thống
    g6_loai_nguoi_nhan     NVARCHAR(20)    NOT NULL DEFAULT 'nguoi_dung', -- 'nguoi_dung','khach_hang','broadcast'
    g6_tieu_de             NVARCHAR(300)   NOT NULL,
    g6_noi_dung            NVARCHAR(MAX)   NOT NULL,
    g6_loai_thong_bao      NVARCHAR(50)    NOT NULL,     -- 'he_thong','goi_tap','lich_dat','don_hang','khuyen_mai','nhac_hen'
    g6_doi_tuong_id        INT             NULL,         -- ID liên quan
    g6_duong_dan           NVARCHAR(500)   NULL,         -- Deep-link hoặc URL chi tiết
    g6_da_doc              BIT             NOT NULL DEFAULT 0,
    g6_kenh_gui            NVARCHAR(20)    NOT NULL DEFAULT 'app', -- 'app','email','sms','push'
    g6_thoi_gian_gui       DATETIME2       NULL,         -- NULL = gửi ngay khi tạo
    g6_da_gui              BIT             NOT NULL DEFAULT 0,
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6ThongBao PRIMARY KEY (g6_ma_thong_bao),
    CONSTRAINT FK_G6TB_NguoiNhan FOREIGN KEY (g6_ma_nguoi_nhan) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE CASCADE
);

CREATE TABLE G6LichGuiThongBao (
    g6_ma_lich             INT             NOT NULL IDENTITY(1,1),
    g6_ten_lich            NVARCHAR(200)   NOT NULL,
    g6_loai_thong_bao      NVARCHAR(50)    NOT NULL,
    g6_tieu_de_mau         NVARCHAR(300)   NOT NULL,     -- Template với biến {ten}, {ngay}, ...
    g6_noi_dung_mau        NVARCHAR(MAX)   NOT NULL,
    g6_kenh_gui            NVARCHAR(20)    NOT NULL DEFAULT 'email', -- 'email','sms','push','app'
    g6_dieu_kien_gui       NVARCHAR(MAX)   NULL,         -- JSON: điều kiện lọc người nhận
    g6_loai_lap_lich       NVARCHAR(20)    NOT NULL DEFAULT 'mot_lan', -- 'mot_lan','hang_ngay','hang_tuan','hang_thang'
    g6_cron_bieu_thuc      NVARCHAR(100)   NULL,         -- Cron expression nếu recurring
    g6_thoi_gian_gui_tiep  DATETIME2       NULL,
    g6_trang_thai          BIT             NOT NULL DEFAULT 1, -- 1=bật, 0=tắt
    g6_lan_gui_cuoi        DATETIME2       NULL,
    g6_so_lan_da_gui       INT             NOT NULL DEFAULT 0,
    g6_nguoi_tao           INT             NULL,
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    g6_ngay_cap_nhat       DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6LichGuiTB PRIMARY KEY (g6_ma_lich),
    CONSTRAINT FK_G6LGTB_NguoiTao FOREIGN KEY (g6_nguoi_tao) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
);

-- Seed lịch nhắc nhở mặc định
INSERT INTO G6LichGuiThongBao
    (g6_ten_lich, g6_loai_thong_bao, g6_tieu_de_mau, g6_noi_dung_mau,
     g6_kenh_gui, g6_loai_lap_lich, g6_cron_bieu_thuc, g6_trang_thai) VALUES
(
    N'Nhắc gia hạn gói tập',
    'goi_tap',
    N'Gói tập của bạn sắp hết hạn - {ten}',
    N'Xin chào {ten}, gói tập của bạn sẽ hết hạn vào ngày {ngay_het_han}. Hãy gia hạn sớm để không bị gián đoạn lịch tập!',
    'email', 'hang_ngay', '0 8 * * *', 1
),
(
    N'Chúc mừng sinh nhật hội viên',
    'he_thong',
    N'Chúc mừng sinh nhật {ten}! 🎂',
    N'G6 Gym chúc mừng sinh nhật {ten}! Như một món quà đặc biệt, bạn được tặng {qua_sinh_nhat}. Chúc bạn một ngày tuyệt vời!',
    'email', 'hang_ngay', '0 7 * * *', 1
),
(
    N'Nhắc lịch hẹn PT ngày mai',
    'lich_dat',
    N'Nhắc lịch: Buổi tập PT ngày mai - {ten}',
    N'Xin chào {ten}, bạn có lịch tập với PT {ten_hlv} vào lúc {gio_bat_dau} ngày {ngay_tap} tại {dia_diem}. Hẹn gặp bạn!',
    'sms', 'hang_ngay', '0 20 * * *', 1
),
(
    N'Xác nhận đơn hàng',
    'don_hang',
    N'Xác nhận đơn hàng #{ma_don_hang}',
    N'Xin chào {ten}, đơn hàng #{ma_don_hang} của bạn đã được xác nhận. Tổng tiền: {tong_tien}. Dự kiến giao: {ngay_giao}.',
    'email', 'mot_lan', NULL, 1
),
(
    N'Thông báo khuyến mãi',
    'khuyen_mai',
    N'Ưu đãi đặc biệt dành cho bạn - {ten}',
    N'Xin chào {ten}! Chúng tôi có chương trình khuyến mãi hấp dẫn: {noi_dung_km}. Thời hạn: {han_su_dung}. Đừng bỏ lỡ!',
    'push', 'mot_lan', NULL, 0
);

-- ============================================================
-- GROUP 20: XÁC THỰC OTP
-- ============================================================

CREATE TABLE G6OtpXacThuc (
    g6_ma_otp              INT             NOT NULL IDENTITY(1,1),
    g6_so_dien_thoai       NVARCHAR(15)    NULL,         -- Xác thực qua SMS
    g6_email               NVARCHAR(100)   NULL,         -- Xác thực qua email
    g6_ma_otp_value        NVARCHAR(10)    NOT NULL,     -- Mã OTP (6-10 ký tự, lưu hash)
    g6_muc_dich            NVARCHAR(50)    NOT NULL,     -- 'dang_ky','quen_mat_khau','xac_thuc_email','doi_so_dt','xac_nhan_don_hang'
    g6_so_lan_thu          TINYINT         NOT NULL DEFAULT 0,
    g6_da_su_dung          BIT             NOT NULL DEFAULT 0,
    g6_thoi_gian_het_han   DATETIME2       NOT NULL,
    g6_ip_yeu_cau          NVARCHAR(45)    NULL,         -- IPv4 hoặc IPv6
    g6_thiet_bi_yeu_cau    NVARCHAR(500)   NULL,         -- User-Agent
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6OtpXacThuc PRIMARY KEY (g6_ma_otp)
);

CREATE TABLE G6PhienDangNhap (
    g6_ma_phien            INT             NOT NULL IDENTITY(1,1),
    g6_ma_nguoi_dung       INT             NULL,         -- NULL = khách hàng online
    g6_ma_khach_hang       INT             NULL,
    g6_token_hash          NVARCHAR(255)   NOT NULL,     -- Hash của refresh token
    g6_thiet_bi            NVARCHAR(500)   NULL,         -- User-Agent / Device fingerprint
    g6_ip_dang_nhap        NVARCHAR(45)    NULL,
    g6_thoi_gian_het_han   DATETIME2       NOT NULL,
    g6_da_thu_hoi          BIT             NOT NULL DEFAULT 0,
    g6_ngay_tao            DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6PhienDN PRIMARY KEY (g6_ma_phien),
    CONSTRAINT FK_G6Phien_NguoiDung FOREIGN KEY (g6_ma_nguoi_dung) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE CASCADE,
    CONSTRAINT FK_G6Phien_KhachHang FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE CASCADE
);

CREATE TABLE G6NhatKyHoatDong (
    g6_ma_nhat_ky          BIGINT          NOT NULL IDENTITY(1,1),
    g6_ma_nguoi_dung       INT             NULL,
    g6_ma_khach_hang       INT             NULL,
    g6_hanh_dong           NVARCHAR(100)   NOT NULL,     -- VD: dang_nhap, cap_nhat_thong_tin
    g6_loai_doi_tuong      NVARCHAR(50)    NULL,         -- VD: G6HoiVien, G6DonHang
    g6_ma_doi_tuong        INT             NULL,
    g6_du_lieu_truoc       NVARCHAR(MAX)   NULL,         -- JSON: trạng thái trước khi thay đổi
    g6_du_lieu_sau         NVARCHAR(MAX)   NULL,         -- JSON: trạng thái sau khi thay đổi
    g6_ip_nguoi_dung       NVARCHAR(45)    NULL,
    g6_thiet_bi            NVARCHAR(500)   NULL,
    g6_ket_qua             NVARCHAR(20)    NOT NULL DEFAULT 'thanh_cong', -- 'thanh_cong','that_bai'
    g6_ghi_chu             NVARCHAR(500)   NULL,
    g6_thoi_gian           DATETIME2       NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_G6NhatKyHD PRIMARY KEY (g6_ma_nhat_ky),
    CONSTRAINT FK_G6NKHD_NguoiDung FOREIGN KEY (g6_ma_nguoi_dung) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL,
    CONSTRAINT FK_G6NKHD_KhachHang FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE SET NULL
);

-- Index
CREATE INDEX IX_G6DonViVC_TrangThai ON G6DonViVanChuyen (g6_trang_thai);
CREATE INDEX IX_G6VungVC_DonVi ON G6VungVanChuyen (g6_ma_don_vi);
CREATE INDEX IX_G6VungVC_MaTinh ON G6VungVanChuyen (g6_ma_tinh);
CREATE INDEX IX_G6DMBV_Cha ON G6DanhMucBaiViet (g6_ma_cha);
CREATE INDEX IX_G6BV_DanhMuc ON G6BaiViet (g6_ma_danh_muc);
CREATE INDEX IX_G6BV_TrangThai ON G6BaiViet (g6_trang_thai);
CREATE INDEX IX_G6BV_NgayXuatBan ON G6BaiViet (g6_ngay_xuat_ban);
CREATE INDEX IX_G6DG_SanPham ON G6DanhGiaSanPham (g6_ma_san_pham);
CREATE INDEX IX_G6DG_TrangThai ON G6DanhGiaSanPham (g6_trang_thai);
CREATE INDEX IX_G6DG_SoSao ON G6DanhGiaSanPham (g6_so_sao);
CREATE INDEX IX_G6TB_NguoiNhan ON G6ThongBao (g6_ma_nguoi_nhan);
CREATE INDEX IX_G6TB_DaDoc ON G6ThongBao (g6_da_doc);
CREATE INDEX IX_G6TB_Loai ON G6ThongBao (g6_loai_thong_bao);
CREATE INDEX IX_G6TB_ThoiGianGui ON G6ThongBao (g6_thoi_gian_gui);
CREATE INDEX IX_G6LGTB_TrangThai ON G6LichGuiThongBao (g6_trang_thai);
CREATE INDEX IX_G6OTP_SDT ON G6OtpXacThuc (g6_so_dien_thoai);
CREATE INDEX IX_G6OTP_Email ON G6OtpXacThuc (g6_email);
CREATE INDEX IX_G6OTP_HetHan ON G6OtpXacThuc (g6_thoi_gian_het_han);
CREATE INDEX IX_G6Phien_Token ON G6PhienDangNhap (g6_token_hash);
CREATE INDEX IX_G6Phien_NguoiDung ON G6PhienDangNhap (g6_ma_nguoi_dung);
CREATE INDEX IX_G6NKHD_NguoiDung ON G6NhatKyHoatDong (g6_ma_nguoi_dung);
CREATE INDEX IX_G6NKHD_HanhDong ON G6NhatKyHoatDong (g6_hanh_dong);
CREATE INDEX IX_G6NKHD_ThoiGian ON G6NhatKyHoatDong (g6_thoi_gian);

PRINT N'Part 4 - Hoàn thành!';
GO
