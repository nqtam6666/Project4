-- ============================================================
-- G6 GYM MANAGEMENT + SUPPLEMENT STORE
-- MySQL Schema - Part 4: Group 17-20
-- GROUP 17: VẬN CHUYỂN | GROUP 18: NỘI DUNG / BLOG
-- GROUP 19: THÔNG BÁO  | GROUP 20: XÁC THỰC OTP
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- GROUP 17: VẬN CHUYỂN
-- ============================================================

-- Đơn vị vận chuyển (GHN, GHTK, Viettel Post, ...)
CREATE TABLE G6DonViVanChuyen (
    g6_ma_don_vi           INT             NOT NULL AUTO_INCREMENT,
    g6_ten_don_vi          VARCHAR(100)    NOT NULL,
    g6_ma_api              VARCHAR(50)     NULL     COMMENT 'Mã đơn vị theo chuẩn cấu hình (ghn, ghtk, ...)',
    g6_mo_ta              VARCHAR(255)    NULL,
    g6_logo_url            VARCHAR(500)    NULL,
    g6_trang_thai          TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '1=hoạt động, 0=tắt',
    g6_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_don_vi),
    KEY idx_g6_donvivc_trangthai (g6_trang_thai)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bảng phí vận chuyển theo vùng (province/district-level)
CREATE TABLE G6VungVanChuyen (
    g6_ma_vung             INT             NOT NULL AUTO_INCREMENT,
    g6_ma_don_vi           INT             NOT NULL,
    g6_ten_vung            VARCHAR(150)    NOT NULL COMMENT 'VD: Hà Nội, TP.HCM',
    g6_ma_tinh             VARCHAR(20)     NULL     COMMENT 'Mã tỉnh/thành theo GHN/GHTK',
    g6_phi_co_ban          DECIMAL(12,2)   NOT NULL DEFAULT 0 COMMENT 'Phí giao hàng cơ bản (VND)',
    g6_phi_them_theo_kg    DECIMAL(12,2)   NOT NULL DEFAULT 0 COMMENT 'Phí tăng thêm / kg vượt mức',
    g6_trong_luong_mien_phi DECIMAL(8,3)  NOT NULL DEFAULT 0 COMMENT 'Kg được miễn phí phụ phí',
    g6_thoi_gian_du_kien   VARCHAR(50)     NULL     COMMENT 'VD: 2-3 ngày làm việc',
    g6_don_hang_toi_thieu_mien_phi DECIMAL(12,2) NULL COMMENT 'Đơn tối thiểu để freeship',
    g6_trang_thai          TINYINT(1)      NOT NULL DEFAULT 1,
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_ngay_cap_nhat       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_vung),
    KEY idx_g6_vungvc_donvi    (g6_ma_don_vi),
    KEY idx_g6_vungvc_matinh   (g6_ma_tinh),
    CONSTRAINT fk_g6_vungvc_donvi FOREIGN KEY (g6_ma_don_vi) REFERENCES G6DonViVanChuyen (g6_ma_don_vi)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed dữ liệu đơn vị vận chuyển
INSERT INTO G6DonViVanChuyen
    (g6_ten_don_vi, g6_ma_api, g6_mo_ta, g6_trang_thai, g6_thu_tu_hien_thi)
VALUES
    ('Giao Hàng Nhanh',     'ghn',     'Đối tác vận chuyển GHN',     1, 1),
    ('Giao Hàng Tiết Kiệm', 'ghtk',    'Đối tác vận chuyển GHTK',    1, 2),
    ('Viettel Post',        'viettel',  'Đối tác vận chuyển Viettel',  1, 3),
    ('Nội thành (tự giao)', 'internal', 'Giao hàng nội bộ trong ngày', 1, 4);

-- Seed vùng vận chuyển mẫu cho GHN
INSERT INTO G6VungVanChuyen
    (g6_ma_don_vi, g6_ten_vung, g6_ma_tinh, g6_phi_co_ban, g6_phi_them_theo_kg,
     g6_trong_luong_mien_phi, g6_thoi_gian_du_kien, g6_don_hang_toi_thieu_mien_phi, g6_trang_thai)
VALUES
    (1, 'Hà Nội',            'HN',  25000,  5000, 3, '1-2 ngày',     399000, 1),
    (1, 'TP. Hồ Chí Minh',  'HCM', 25000,  5000, 3, '1-2 ngày',     399000, 1),
    (1, 'Đà Nẵng',          'DN',  35000,  6000, 3, '2-3 ngày',     499000, 1),
    (1, 'Các tỉnh khác',    NULL,  45000,  7000, 2, '3-5 ngày',     599000, 1);

-- ============================================================
-- GROUP 18: NỘI DUNG / BLOG
-- ============================================================

CREATE TABLE G6DanhMucBaiViet (
    g6_ma_danh_muc         INT             NOT NULL AUTO_INCREMENT,
    g6_ten_danh_muc        VARCHAR(150)    NOT NULL,
    g6_slug                VARCHAR(200)    NOT NULL,
    g6_mo_ta              VARCHAR(500)    NULL,
    g6_ma_cha              INT             NULL     COMMENT 'Danh mục cha (NULL = root)',
    g6_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    g6_trang_thai          TINYINT(1)      NOT NULL DEFAULT 1,
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_danh_muc),
    UNIQUE KEY uk_g6_dmbaiviet_slug (g6_slug),
    KEY idx_g6_dmbaiviet_cha       (g6_ma_cha),
    CONSTRAINT fk_g6_dmbaiviet_cha FOREIGN KEY (g6_ma_cha) REFERENCES G6DanhMucBaiViet (g6_ma_danh_muc) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6BaiViet (
    g6_ma_bai_viet         INT             NOT NULL AUTO_INCREMENT,
    g6_ma_danh_muc         INT             NULL,
    g6_tieu_de             VARCHAR(300)    NOT NULL,
    g6_slug                VARCHAR(350)    NOT NULL,
    g6_tom_tat             TEXT            NULL     COMMENT 'Mô tả ngắn / excerpt',
    g6_noi_dung            LONGTEXT        NULL     COMMENT 'Nội dung HTML đầy đủ',
    g6_anh_dai_dien        VARCHAR(500)    NULL,
    g6_tac_gia             INT             NULL     COMMENT 'FK → G6NguoiDung',
    g6_luot_xem            INT             NOT NULL DEFAULT 0,
    g6_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'nhap'  COMMENT '''nhap'',''xuat_ban'',''an''',
    g6_ngay_xuat_ban       DATETIME        NULL,
    g6_tu_khoa             VARCHAR(500)    NULL     COMMENT 'SEO keywords, comma-separated',
    g6_mo_ta_seo           VARCHAR(300)    NULL     COMMENT 'Meta description',
    g6_san_pham_lien_quan  JSON            NULL     COMMENT 'Mảng g6_ma_san_pham liên quan',
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_ngay_cap_nhat       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_bai_viet),
    UNIQUE KEY uk_g6_baiviet_slug  (g6_slug),
    KEY idx_g6_baiviet_danhmuc     (g6_ma_danh_muc),
    KEY idx_g6_baiviet_trangthai   (g6_trang_thai),
    KEY idx_g6_baiviet_ngayxuatban (g6_ngay_xuat_ban),
    CONSTRAINT fk_g6_baiviet_danhmuc FOREIGN KEY (g6_ma_danh_muc) REFERENCES G6DanhMucBaiViet (g6_ma_danh_muc) ON DELETE SET NULL,
    CONSTRAINT fk_g6_baiviet_tacgia  FOREIGN KEY (g6_tac_gia)      REFERENCES G6NguoiDung     (g6_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE G6DanhGiaSanPham (
    g6_ma_danh_gia         INT             NOT NULL AUTO_INCREMENT,
    g6_ma_san_pham         INT             NOT NULL,
    g6_ma_khach_hang       INT             NULL     COMMENT 'NULL = khách vãng lai',
    g6_ma_don_hang         INT             NULL     COMMENT 'Đánh giá sau mua hàng',
    g6_ten_nguoi_dung      VARCHAR(100)    NULL     COMMENT 'Tên hiển thị khi review',
    g6_so_sao              TINYINT         NOT NULL COMMENT '1-5',
    g6_tieu_de             VARCHAR(200)    NULL,
    g6_noi_dung            TEXT            NULL,
    g6_hinh_anh            JSON            NULL     COMMENT 'Mảng URL ảnh đính kèm review',
    g6_da_mua              TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '1 = đã xác nhận mua hàng',
    g6_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'cho_duyet' COMMENT '''cho_duyet'',''duoc_duyet'',''bi_an''',
    g6_phan_hoi_shop       TEXT            NULL     COMMENT 'Shop phản hồi review',
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_ngay_duyet          DATETIME        NULL,
    PRIMARY KEY (g6_ma_danh_gia),
    KEY idx_g6_danhgia_sanpham   (g6_ma_san_pham),
    KEY idx_g6_danhgia_trangthai (g6_trang_thai),
    KEY idx_g6_danhgia_sosao     (g6_so_sao),
    CONSTRAINT fk_g6_danhgia_sanpham   FOREIGN KEY (g6_ma_san_pham)   REFERENCES G6SanPham   (g6_ma_san_pham),
    CONSTRAINT fk_g6_danhgia_khachhang FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang (g6_ma_khach_hang) ON DELETE SET NULL,
    CONSTRAINT fk_g6_danhgia_donhang   FOREIGN KEY (g6_ma_don_hang)   REFERENCES G6DonHang   (g6_ma_don_hang)   ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed danh mục bài viết
INSERT INTO G6DanhMucBaiViet
    (g6_ten_danh_muc, g6_slug, g6_mo_ta, g6_ma_cha, g6_thu_tu_hien_thi, g6_trang_thai)
VALUES
    ('Kiến thức Gym',          'kien-thuc-gym',           'Hướng dẫn tập luyện, kỹ thuật, chương trình',  NULL, 1, 1),
    ('Dinh dưỡng thể thao',    'dinh-duong-the-thao',     'Chế độ ăn, bổ sung, thực phẩm chức năng',      NULL, 2, 1),
    ('Đánh giá sản phẩm',      'danh-gia-san-pham',       'Review whey protein, BCAA, pre-workout,...',   NULL, 3, 1),
    ('Tin tức & Sự kiện',      'tin-tuc-su-kien',         'Tin tức ngành gym và sự kiện phòng tập',        NULL, 4, 1),
    ('Câu hỏi thường gặp',     'cau-hoi-thuong-gap',      'FAQ về tập luyện và thực phẩm bổ sung',        NULL, 5, 1),
    -- Sub-categories
    ('Kỹ thuật tập luyện',     'ky-thuat-tap-luyen',      NULL, 1, 1, 1),
    ('Chương trình tập',       'chuong-trinh-tap',        NULL, 1, 2, 1),
    ('Phục hồi & Nghỉ ngơi',  'phuc-hoi-nghi-ngoi',      NULL, 1, 3, 1),
    ('Protein & Amino Acid',   'protein-amino-acid',      NULL, 2, 1, 1),
    ('Creatine & Pre-workout', 'creatine-pre-workout',    NULL, 2, 2, 1),
    ('Giảm cân & Đốt mỡ',     'giam-can-dot-mo',         NULL, 2, 3, 1);

-- ============================================================
-- GROUP 19: THÔNG BÁO
-- ============================================================

CREATE TABLE G6ThongBao (
    g6_ma_thong_bao        INT             NOT NULL AUTO_INCREMENT,
    g6_ma_nguoi_nhan       INT             NULL     COMMENT 'NULL = broadcast toàn hệ thống',
    g6_loai_nguoi_nhan     VARCHAR(20)     NOT NULL DEFAULT 'nguoi_dung' COMMENT '''nguoi_dung'',''khach_hang'',''broadcast''',
    g6_tieu_de             VARCHAR(300)    NOT NULL,
    g6_noi_dung            TEXT            NOT NULL,
    g6_loai_thong_bao      VARCHAR(50)     NOT NULL COMMENT '''he_thong'',''goi_tap'',''lich_dat'',''don_hang'',''khuyen_mai'',''nhac_hen''',
    g6_doi_tuong_id        INT             NULL     COMMENT 'ID liên quan (mã đơn hàng, mã lịch, ...)',
    g6_duong_dan           VARCHAR(500)    NULL     COMMENT 'Deep-link hoặc URL chi tiết',
    g6_da_doc              TINYINT(1)      NOT NULL DEFAULT 0,
    g6_kenh_gui            VARCHAR(20)     NOT NULL DEFAULT 'app'  COMMENT '''app'',''email'',''sms'',''push''',
    g6_thoi_gian_gui       DATETIME        NULL     COMMENT 'NULL = gửi ngay khi tạo',
    g6_da_gui              TINYINT(1)      NOT NULL DEFAULT 0,
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_thong_bao),
    KEY idx_g6_thongbao_nguoinhan (g6_ma_nguoi_nhan),
    KEY idx_g6_thongbao_dadoc     (g6_da_doc),
    KEY idx_g6_thongbao_loai      (g6_loai_thong_bao),
    KEY idx_g6_thongbao_thoigiangui (g6_thoi_gian_gui),
    CONSTRAINT fk_g6_thongbao_nguoinhan FOREIGN KEY (g6_ma_nguoi_nhan) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Lịch gửi thông báo (scheduled / recurring notifications)
CREATE TABLE G6LichGuiThongBao (
    g6_ma_lich             INT             NOT NULL AUTO_INCREMENT,
    g6_ten_lich            VARCHAR(200)    NOT NULL,
    g6_loai_thong_bao      VARCHAR(50)     NOT NULL,
    g6_tieu_de_mau         VARCHAR(300)    NOT NULL COMMENT 'Template với biến {ten}, {ngay}, ...',
    g6_noi_dung_mau        TEXT            NOT NULL,
    g6_kenh_gui            VARCHAR(20)     NOT NULL DEFAULT 'email' COMMENT '''email'',''sms'',''push'',''app''',
    g6_dieu_kien_gui       JSON            NULL     COMMENT 'Điều kiện lọc người nhận (VD: gói hết hạn trong N ngày)',
    g6_loai_lap_lich       VARCHAR(20)     NOT NULL DEFAULT 'mot_lan' COMMENT '''mot_lan'',''hang_ngay'',''hang_tuan'',''hang_thang''',
    g6_cron_bieu_thuc      VARCHAR(100)    NULL     COMMENT 'Cron expression nếu recurring',
    g6_thoi_gian_gui_tiep  DATETIME        NULL,
    g6_trang_thai          TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '1=bật, 0=tắt',
    g6_lan_gui_cuoi        DATETIME        NULL,
    g6_so_lan_da_gui       INT             NOT NULL DEFAULT 0,
    g6_nguoi_tao           INT             NULL,
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    g6_ngay_cap_nhat       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_lich),
    KEY idx_g6_lichguitb_trangthai    (g6_trang_thai),
    KEY idx_g6_lichguitb_thoigiangui  (g6_thoi_gian_gui_tiep),
    CONSTRAINT fk_g6_lichguitb_nguoitao FOREIGN KEY (g6_nguoi_tao) REFERENCES G6NguoiDung (g6_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed lịch nhắc nhở mặc định (Business logic driven by G6CauHinh)
INSERT INTO G6LichGuiThongBao
    (g6_ten_lich, g6_loai_thong_bao, g6_tieu_de_mau, g6_noi_dung_mau,
     g6_kenh_gui, g6_loai_lap_lich, g6_cron_bieu_thuc, g6_trang_thai)
VALUES
    (
        'Nhắc gia hạn gói tập',
        'goi_tap',
        'Gói tập của bạn sắp hết hạn - {ten}',
        'Xin chào {ten}, gói tập của bạn sẽ hết hạn vào ngày {ngay_het_han}. Hãy gia hạn sớm để không bị gián đoạn lịch tập!',
        'email',
        'hang_ngay',
        '0 8 * * *',
        1
    ),
    (
        'Chúc mừng sinh nhật hội viên',
        'he_thong',
        'Chúc mừng sinh nhật {ten}! 🎂',
        'G6 Gym chúc mừng sinh nhật {ten}! Như một món quà đặc biệt, bạn được tặng {qua_sinh_nhat}. Chúc bạn một ngày tuyệt vời!',
        'email',
        'hang_ngay',
        '0 7 * * *',
        1
    ),
    (
        'Nhắc lịch hẹn PT ngày mai',
        'lich_dat',
        'Nhắc lịch: Buổi tập PT ngày mai - {ten}',
        'Xin chào {ten}, bạn có lịch tập với PT {ten_hlv} vào lúc {gio_bat_dau} ngày {ngay_tap} tại {dia_diem}. Hẹn gặp bạn!',
        'sms',
        'hang_ngay',
        '0 20 * * *',
        1
    ),
    (
        'Xác nhận đơn hàng',
        'don_hang',
        'Xác nhận đơn hàng #{ma_don_hang}',
        'Xin chào {ten}, đơn hàng #{ma_don_hang} của bạn đã được xác nhận. Tổng tiền: {tong_tien}. Dự kiến giao: {ngay_giao}.',
        'email',
        'mot_lan',
        NULL,
        1
    ),
    (
        'Thông báo khuyến mãi',
        'khuyen_mai',
        'Ưu đãi đặc biệt dành cho bạn - {ten}',
        'Xin chào {ten}! Chúng tôi có chương trình khuyến mãi hấp dẫn: {noi_dung_km}. Thời hạn: {han_su_dung}. Đừng bỏ lỡ!',
        'push',
        'mot_lan',
        NULL,
        0
    );

-- ============================================================
-- GROUP 20: XÁC THỰC OTP
-- ============================================================

CREATE TABLE G6OtpXacThuc (
    g6_ma_otp              INT             NOT NULL AUTO_INCREMENT,
    g6_so_dien_thoai       VARCHAR(15)     NULL     COMMENT 'Xác thực qua SMS',
    g6_email               VARCHAR(100)    NULL     COMMENT 'Xác thực qua email',
    g6_ma_otp_value        VARCHAR(10)     NOT NULL COMMENT 'Mã OTP (6-10 ký tự, lưu hash)',
    g6_muc_dich            VARCHAR(50)     NOT NULL COMMENT '''dang_ky'',''quen_mat_khau'',''xac_thuc_email'',''doi_so_dt'',''xac_nhan_don_hang''',
    g6_so_lan_thu          TINYINT         NOT NULL DEFAULT 0,
    g6_da_su_dung          TINYINT(1)      NOT NULL DEFAULT 0,
    g6_thoi_gian_het_han   DATETIME        NOT NULL,
    g6_ip_yeu_cau          VARCHAR(45)     NULL     COMMENT 'IPv4 hoặc IPv6',
    g6_thiet_bi_yeu_cau    VARCHAR(500)    NULL     COMMENT 'User-Agent',
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_otp),
    KEY idx_g6_otp_sdt        (g6_so_dien_thoai),
    KEY idx_g6_otp_email      (g6_email),
    KEY idx_g6_otp_hethan     (g6_thoi_gian_het_han),
    KEY idx_g6_otp_mucdich    (g6_muc_dich)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Token phiên đăng nhập (refresh token / remember-me)
CREATE TABLE G6PhienDangNhap (
    g6_ma_phien            INT             NOT NULL AUTO_INCREMENT,
    g6_ma_nguoi_dung       INT             NULL     COMMENT 'NULL = khách hàng online',
    g6_ma_khach_hang       INT             NULL,
    g6_token_hash          VARCHAR(255)    NOT NULL COMMENT 'Hash của refresh token',
    g6_thiet_bi            VARCHAR(500)    NULL     COMMENT 'User-Agent / Device fingerprint',
    g6_ip_dang_nhap        VARCHAR(45)     NULL,
    g6_thoi_gian_het_han   DATETIME        NOT NULL,
    g6_da_thu_hoi          TINYINT(1)      NOT NULL DEFAULT 0,
    g6_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_phien),
    KEY idx_g6_phien_token    (g6_token_hash),
    KEY idx_g6_phien_nguoidung (g6_ma_nguoi_dung),
    KEY idx_g6_phien_hethan   (g6_thoi_gian_het_han),
    CONSTRAINT fk_g6_phien_nguoidung  FOREIGN KEY (g6_ma_nguoi_dung)  REFERENCES G6NguoiDung  (g6_ma_nguoi_dung)  ON DELETE CASCADE,
    CONSTRAINT fk_g6_phien_khachhang  FOREIGN KEY (g6_ma_khach_hang)  REFERENCES G6KhachHang  (g6_ma_khach_hang)  ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Nhật ký hoạt động người dùng (audit log)
CREATE TABLE G6NhatKyHoatDong (
    g6_ma_nhat_ky          BIGINT          NOT NULL AUTO_INCREMENT,
    g6_ma_nguoi_dung       INT             NULL,
    g6_ma_khach_hang       INT             NULL,
    g6_hanh_dong           VARCHAR(100)    NOT NULL COMMENT 'VD: dang_nhap, cap_nhat_thong_tin, tao_don_hang',
    g6_loai_doi_tuong      VARCHAR(50)     NULL     COMMENT 'VD: G6HoiVien, G6DonHang',
    g6_ma_doi_tuong        INT             NULL,
    g6_du_lieu_truoc       JSON            NULL     COMMENT 'Trạng thái trước khi thay đổi',
    g6_du_lieu_sau         JSON            NULL     COMMENT 'Trạng thái sau khi thay đổi',
    g6_ip_nguoi_dung       VARCHAR(45)     NULL,
    g6_thiet_bi            VARCHAR(500)    NULL,
    g6_ket_qua             VARCHAR(20)     NOT NULL DEFAULT 'thanh_cong' COMMENT '''thanh_cong'',''that_bai''',
    g6_ghi_chu             VARCHAR(500)    NULL,
    g6_thoi_gian           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (g6_ma_nhat_ky),
    KEY idx_g6_nkhoatdong_nguoidung (g6_ma_nguoi_dung),
    KEY idx_g6_nkhoatdong_hanhdong  (g6_hanh_dong),
    KEY idx_g6_nkhoatdong_thoigian  (g6_thoi_gian),
    CONSTRAINT fk_g6_nkhoatdong_nguoidung FOREIGN KEY (g6_ma_nguoi_dung) REFERENCES G6NguoiDung  (g6_ma_nguoi_dung) ON DELETE SET NULL,
    CONSTRAINT fk_g6_nkhoatdong_khachhang FOREIGN KEY (g6_ma_khach_hang) REFERENCES G6KhachHang  (g6_ma_khach_hang) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
