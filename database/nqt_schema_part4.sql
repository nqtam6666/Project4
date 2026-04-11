-- ============================================================
-- NQT GYM MANAGEMENT + SUPPLEMENT STORE
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
CREATE TABLE NqtDonViVanChuyen (
    nqt_ma_don_vi           INT             NOT NULL AUTO_INCREMENT,
    nqt_ten_don_vi          VARCHAR(100)    NOT NULL,
    nqt_ma_api              VARCHAR(50)     NULL     COMMENT 'Mã đơn vị theo chuẩn cấu hình (ghn, ghtk, ...)',
    nqt_mo_ta              VARCHAR(255)    NULL,
    nqt_logo_url            VARCHAR(500)    NULL,
    nqt_trang_thai          TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '1=hoạt động, 0=tắt',
    nqt_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_don_vi),
    KEY idx_nqt_donvivc_trangthai (nqt_trang_thai)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bảng phí vận chuyển theo vùng (province/district-level)
CREATE TABLE NqtVungVanChuyen (
    nqt_ma_vung             INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_don_vi           INT             NOT NULL,
    nqt_ten_vung            VARCHAR(150)    NOT NULL COMMENT 'VD: Hà Nội, TP.HCM',
    nqt_ma_tinh             VARCHAR(20)     NULL     COMMENT 'Mã tỉnh/thành theo GHN/GHTK',
    nqt_phi_co_ban          DECIMAL(12,2)   NOT NULL DEFAULT 0 COMMENT 'Phí giao hàng cơ bản (VND)',
    nqt_phi_them_theo_kg    DECIMAL(12,2)   NOT NULL DEFAULT 0 COMMENT 'Phí tăng thêm / kg vượt mức',
    nqt_trong_luong_mien_phi DECIMAL(8,3)  NOT NULL DEFAULT 0 COMMENT 'Kg được miễn phí phụ phí',
    nqt_thoi_gian_du_kien   VARCHAR(50)     NULL     COMMENT 'VD: 2-3 ngày làm việc',
    nqt_don_hang_toi_thieu_mien_phi DECIMAL(12,2) NULL COMMENT 'Đơn tối thiểu để freeship',
    nqt_trang_thai          TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_ngay_cap_nhat       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_vung),
    KEY idx_nqt_vungvc_donvi    (nqt_ma_don_vi),
    KEY idx_nqt_vungvc_matinh   (nqt_ma_tinh),
    CONSTRAINT fk_nqt_vungvc_donvi FOREIGN KEY (nqt_ma_don_vi) REFERENCES NqtDonViVanChuyen (nqt_ma_don_vi)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed dữ liệu đơn vị vận chuyển
INSERT INTO NqtDonViVanChuyen
    (nqt_ten_don_vi, nqt_ma_api, nqt_mo_ta, nqt_trang_thai, nqt_thu_tu_hien_thi)
VALUES
    ('Giao Hàng Nhanh',     'ghn',     'Đối tác vận chuyển GHN',     1, 1),
    ('Giao Hàng Tiết Kiệm', 'ghtk',    'Đối tác vận chuyển GHTK',    1, 2),
    ('Viettel Post',        'viettel',  'Đối tác vận chuyển Viettel',  1, 3),
    ('Nội thành (tự giao)', 'internal', 'Giao hàng nội bộ trong ngày', 1, 4);

-- Seed vùng vận chuyển mẫu cho GHN
INSERT INTO NqtVungVanChuyen
    (nqt_ma_don_vi, nqt_ten_vung, nqt_ma_tinh, nqt_phi_co_ban, nqt_phi_them_theo_kg,
     nqt_trong_luong_mien_phi, nqt_thoi_gian_du_kien, nqt_don_hang_toi_thieu_mien_phi, nqt_trang_thai)
VALUES
    (1, 'Hà Nội',            'HN',  25000,  5000, 3, '1-2 ngày',     399000, 1),
    (1, 'TP. Hồ Chí Minh',  'HCM', 25000,  5000, 3, '1-2 ngày',     399000, 1),
    (1, 'Đà Nẵng',          'DN',  35000,  6000, 3, '2-3 ngày',     499000, 1),
    (1, 'Các tỉnh khác',    NULL,  45000,  7000, 2, '3-5 ngày',     599000, 1);

-- ============================================================
-- GROUP 18: NỘI DUNG / BLOG
-- ============================================================

CREATE TABLE NqtDanhMucBaiViet (
    nqt_ma_danh_muc         INT             NOT NULL AUTO_INCREMENT,
    nqt_ten_danh_muc        VARCHAR(150)    NOT NULL,
    nqt_slug                VARCHAR(200)    NOT NULL,
    nqt_mo_ta              VARCHAR(500)    NULL,
    nqt_ma_cha              INT             NULL     COMMENT 'Danh mục cha (NULL = root)',
    nqt_thu_tu_hien_thi     INT             NOT NULL DEFAULT 0,
    nqt_trang_thai          TINYINT(1)      NOT NULL DEFAULT 1,
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_danh_muc),
    UNIQUE KEY uk_nqt_dmbaiviet_slug (nqt_slug),
    KEY idx_nqt_dmbaiviet_cha       (nqt_ma_cha),
    CONSTRAINT fk_nqt_dmbaiviet_cha FOREIGN KEY (nqt_ma_cha) REFERENCES NqtDanhMucBaiViet (nqt_ma_danh_muc) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtBaiViet (
    nqt_ma_bai_viet         INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_danh_muc         INT             NULL,
    nqt_tieu_de             VARCHAR(300)    NOT NULL,
    nqt_slug                VARCHAR(350)    NOT NULL,
    nqt_tom_tat             TEXT            NULL     COMMENT 'Mô tả ngắn / excerpt',
    nqt_noi_dung            LONGTEXT        NULL     COMMENT 'Nội dung HTML đầy đủ',
    nqt_anh_dai_dien        VARCHAR(500)    NULL,
    nqt_tac_gia             INT             NULL     COMMENT 'FK → NqtNguoiDung',
    nqt_luot_xem            INT             NOT NULL DEFAULT 0,
    nqt_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'nhap'  COMMENT '''nhap'',''xuat_ban'',''an''',
    nqt_ngay_xuat_ban       DATETIME        NULL,
    nqt_tu_khoa             VARCHAR(500)    NULL     COMMENT 'SEO keywords, comma-separated',
    nqt_mo_ta_seo           VARCHAR(300)    NULL     COMMENT 'Meta description',
    nqt_san_pham_lien_quan  JSON            NULL     COMMENT 'Mảng nqt_ma_san_pham liên quan',
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_ngay_cap_nhat       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_bai_viet),
    UNIQUE KEY uk_nqt_baiviet_slug  (nqt_slug),
    KEY idx_nqt_baiviet_danhmuc     (nqt_ma_danh_muc),
    KEY idx_nqt_baiviet_trangthai   (nqt_trang_thai),
    KEY idx_nqt_baiviet_ngayxuatban (nqt_ngay_xuat_ban),
    CONSTRAINT fk_nqt_baiviet_danhmuc FOREIGN KEY (nqt_ma_danh_muc) REFERENCES NqtDanhMucBaiViet (nqt_ma_danh_muc) ON DELETE SET NULL,
    CONSTRAINT fk_nqt_baiviet_tacgia  FOREIGN KEY (nqt_tac_gia)      REFERENCES NqtNguoiDung     (nqt_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE NqtDanhGiaSanPham (
    nqt_ma_danh_gia         INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_san_pham         INT             NOT NULL,
    nqt_ma_khach_hang       INT             NULL     COMMENT 'NULL = khách vãng lai',
    nqt_ma_don_hang         INT             NULL     COMMENT 'Đánh giá sau mua hàng',
    nqt_ten_nguoi_dung      VARCHAR(100)    NULL     COMMENT 'Tên hiển thị khi review',
    nqt_so_sao              TINYINT         NOT NULL COMMENT '1-5',
    nqt_tieu_de             VARCHAR(200)    NULL,
    nqt_noi_dung            TEXT            NULL,
    nqt_hinh_anh            JSON            NULL     COMMENT 'Mảng URL ảnh đính kèm review',
    nqt_da_mua              TINYINT(1)      NOT NULL DEFAULT 0 COMMENT '1 = đã xác nhận mua hàng',
    nqt_trang_thai          VARCHAR(20)     NOT NULL DEFAULT 'cho_duyet' COMMENT '''cho_duyet'',''duoc_duyet'',''bi_an''',
    nqt_phan_hoi_shop       TEXT            NULL     COMMENT 'Shop phản hồi review',
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_ngay_duyet          DATETIME        NULL,
    PRIMARY KEY (nqt_ma_danh_gia),
    KEY idx_nqt_danhgia_sanpham   (nqt_ma_san_pham),
    KEY idx_nqt_danhgia_trangthai (nqt_trang_thai),
    KEY idx_nqt_danhgia_sosao     (nqt_so_sao),
    CONSTRAINT fk_nqt_danhgia_sanpham   FOREIGN KEY (nqt_ma_san_pham)   REFERENCES NqtSanPham   (nqt_ma_san_pham),
    CONSTRAINT fk_nqt_danhgia_khachhang FOREIGN KEY (nqt_ma_khach_hang) REFERENCES NqtKhachHang (nqt_ma_khach_hang) ON DELETE SET NULL,
    CONSTRAINT fk_nqt_danhgia_donhang   FOREIGN KEY (nqt_ma_don_hang)   REFERENCES NqtDonHang   (nqt_ma_don_hang)   ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed danh mục bài viết
INSERT INTO NqtDanhMucBaiViet
    (nqt_ten_danh_muc, nqt_slug, nqt_mo_ta, nqt_ma_cha, nqt_thu_tu_hien_thi, nqt_trang_thai)
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

CREATE TABLE NqtThongBao (
    nqt_ma_thong_bao        INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_nguoi_nhan       INT             NULL     COMMENT 'NULL = broadcast toàn hệ thống',
    nqt_loai_nguoi_nhan     VARCHAR(20)     NOT NULL DEFAULT 'nguoi_dung' COMMENT '''nguoi_dung'',''khach_hang'',''broadcast''',
    nqt_tieu_de             VARCHAR(300)    NOT NULL,
    nqt_noi_dung            TEXT            NOT NULL,
    nqt_loai_thong_bao      VARCHAR(50)     NOT NULL COMMENT '''he_thong'',''goi_tap'',''lich_dat'',''don_hang'',''khuyen_mai'',''nhac_hen''',
    nqt_doi_tuong_id        INT             NULL     COMMENT 'ID liên quan (mã đơn hàng, mã lịch, ...)',
    nqt_duong_dan           VARCHAR(500)    NULL     COMMENT 'Deep-link hoặc URL chi tiết',
    nqt_da_doc              TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_kenh_gui            VARCHAR(20)     NOT NULL DEFAULT 'app'  COMMENT '''app'',''email'',''sms'',''push''',
    nqt_thoi_gian_gui       DATETIME        NULL     COMMENT 'NULL = gửi ngay khi tạo',
    nqt_da_gui              TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_thong_bao),
    KEY idx_nqt_thongbao_nguoinhan (nqt_ma_nguoi_nhan),
    KEY idx_nqt_thongbao_dadoc     (nqt_da_doc),
    KEY idx_nqt_thongbao_loai      (nqt_loai_thong_bao),
    KEY idx_nqt_thongbao_thoigiangui (nqt_thoi_gian_gui),
    CONSTRAINT fk_nqt_thongbao_nguoinhan FOREIGN KEY (nqt_ma_nguoi_nhan) REFERENCES NqtNguoiDung (nqt_ma_nguoi_dung) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Lịch gửi thông báo (scheduled / recurring notifications)
CREATE TABLE NqtLichGuiThongBao (
    nqt_ma_lich             INT             NOT NULL AUTO_INCREMENT,
    nqt_ten_lich            VARCHAR(200)    NOT NULL,
    nqt_loai_thong_bao      VARCHAR(50)     NOT NULL,
    nqt_tieu_de_mau         VARCHAR(300)    NOT NULL COMMENT 'Template với biến {ten}, {ngay}, ...',
    nqt_noi_dung_mau        TEXT            NOT NULL,
    nqt_kenh_gui            VARCHAR(20)     NOT NULL DEFAULT 'email' COMMENT '''email'',''sms'',''push'',''app''',
    nqt_dieu_kien_gui       JSON            NULL     COMMENT 'Điều kiện lọc người nhận (VD: gói hết hạn trong N ngày)',
    nqt_loai_lap_lich       VARCHAR(20)     NOT NULL DEFAULT 'mot_lan' COMMENT '''mot_lan'',''hang_ngay'',''hang_tuan'',''hang_thang''',
    nqt_cron_bieu_thuc      VARCHAR(100)    NULL     COMMENT 'Cron expression nếu recurring',
    nqt_thoi_gian_gui_tiep  DATETIME        NULL,
    nqt_trang_thai          TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '1=bật, 0=tắt',
    nqt_lan_gui_cuoi        DATETIME        NULL,
    nqt_so_lan_da_gui       INT             NOT NULL DEFAULT 0,
    nqt_nguoi_tao           INT             NULL,
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nqt_ngay_cap_nhat       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_lich),
    KEY idx_nqt_lichguitb_trangthai    (nqt_trang_thai),
    KEY idx_nqt_lichguitb_thoigiangui  (nqt_thoi_gian_gui_tiep),
    CONSTRAINT fk_nqt_lichguitb_nguoitao FOREIGN KEY (nqt_nguoi_tao) REFERENCES NqtNguoiDung (nqt_ma_nguoi_dung) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed lịch nhắc nhở mặc định (Business logic driven by NqtCauHinh)
INSERT INTO NqtLichGuiThongBao
    (nqt_ten_lich, nqt_loai_thong_bao, nqt_tieu_de_mau, nqt_noi_dung_mau,
     nqt_kenh_gui, nqt_loai_lap_lich, nqt_cron_bieu_thuc, nqt_trang_thai)
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
        'NQT Gym chúc mừng sinh nhật {ten}! Như một món quà đặc biệt, bạn được tặng {qua_sinh_nhat}. Chúc bạn một ngày tuyệt vời!',
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

CREATE TABLE NqtOtpXacThuc (
    nqt_ma_otp              INT             NOT NULL AUTO_INCREMENT,
    nqt_so_dien_thoai       VARCHAR(15)     NULL     COMMENT 'Xác thực qua SMS',
    nqt_email               VARCHAR(100)    NULL     COMMENT 'Xác thực qua email',
    nqt_ma_otp_value        VARCHAR(10)     NOT NULL COMMENT 'Mã OTP (6-10 ký tự, lưu hash)',
    nqt_muc_dich            VARCHAR(50)     NOT NULL COMMENT '''dang_ky'',''quen_mat_khau'',''xac_thuc_email'',''doi_so_dt'',''xac_nhan_don_hang''',
    nqt_so_lan_thu          TINYINT         NOT NULL DEFAULT 0,
    nqt_da_su_dung          TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_thoi_gian_het_han   DATETIME        NOT NULL,
    nqt_ip_yeu_cau          VARCHAR(45)     NULL     COMMENT 'IPv4 hoặc IPv6',
    nqt_thiet_bi_yeu_cau    VARCHAR(500)    NULL     COMMENT 'User-Agent',
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_otp),
    KEY idx_nqt_otp_sdt        (nqt_so_dien_thoai),
    KEY idx_nqt_otp_email      (nqt_email),
    KEY idx_nqt_otp_hethan     (nqt_thoi_gian_het_han),
    KEY idx_nqt_otp_mucdich    (nqt_muc_dich)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Token phiên đăng nhập (refresh token / remember-me)
CREATE TABLE NqtPhienDangNhap (
    nqt_ma_phien            INT             NOT NULL AUTO_INCREMENT,
    nqt_ma_nguoi_dung       INT             NULL     COMMENT 'NULL = khách hàng online',
    nqt_ma_khach_hang       INT             NULL,
    nqt_token_hash          VARCHAR(255)    NOT NULL COMMENT 'Hash của refresh token',
    nqt_thiet_bi            VARCHAR(500)    NULL     COMMENT 'User-Agent / Device fingerprint',
    nqt_ip_dang_nhap        VARCHAR(45)     NULL,
    nqt_thoi_gian_het_han   DATETIME        NOT NULL,
    nqt_da_thu_hoi          TINYINT(1)      NOT NULL DEFAULT 0,
    nqt_ngay_tao            DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_phien),
    KEY idx_nqt_phien_token    (nqt_token_hash),
    KEY idx_nqt_phien_nguoidung (nqt_ma_nguoi_dung),
    KEY idx_nqt_phien_hethan   (nqt_thoi_gian_het_han),
    CONSTRAINT fk_nqt_phien_nguoidung  FOREIGN KEY (nqt_ma_nguoi_dung)  REFERENCES NqtNguoiDung  (nqt_ma_nguoi_dung)  ON DELETE CASCADE,
    CONSTRAINT fk_nqt_phien_khachhang  FOREIGN KEY (nqt_ma_khach_hang)  REFERENCES NqtKhachHang  (nqt_ma_khach_hang)  ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Nhật ký hoạt động người dùng (audit log)
CREATE TABLE NqtNhatKyHoatDong (
    nqt_ma_nhat_ky          BIGINT          NOT NULL AUTO_INCREMENT,
    nqt_ma_nguoi_dung       INT             NULL,
    nqt_ma_khach_hang       INT             NULL,
    nqt_hanh_dong           VARCHAR(100)    NOT NULL COMMENT 'VD: dang_nhap, cap_nhat_thong_tin, tao_don_hang',
    nqt_loai_doi_tuong      VARCHAR(50)     NULL     COMMENT 'VD: NqtHoiVien, NqtDonHang',
    nqt_ma_doi_tuong        INT             NULL,
    nqt_du_lieu_truoc       JSON            NULL     COMMENT 'Trạng thái trước khi thay đổi',
    nqt_du_lieu_sau         JSON            NULL     COMMENT 'Trạng thái sau khi thay đổi',
    nqt_ip_nguoi_dung       VARCHAR(45)     NULL,
    nqt_thiet_bi            VARCHAR(500)    NULL,
    nqt_ket_qua             VARCHAR(20)     NOT NULL DEFAULT 'thanh_cong' COMMENT '''thanh_cong'',''that_bai''',
    nqt_ghi_chu             VARCHAR(500)    NULL,
    nqt_thoi_gian           DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (nqt_ma_nhat_ky),
    KEY idx_nqt_nkhoatdong_nguoidung (nqt_ma_nguoi_dung),
    KEY idx_nqt_nkhoatdong_hanhdong  (nqt_hanh_dong),
    KEY idx_nqt_nkhoatdong_thoigian  (nqt_thoi_gian),
    CONSTRAINT fk_nqt_nkhoatdong_nguoidung FOREIGN KEY (nqt_ma_nguoi_dung) REFERENCES NqtNguoiDung  (nqt_ma_nguoi_dung) ON DELETE SET NULL,
    CONSTRAINT fk_nqt_nkhoatdong_khachhang FOREIGN KEY (nqt_ma_khach_hang) REFERENCES NqtKhachHang  (nqt_ma_khach_hang) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
