-- ============================================================
-- NQT SCHEMA PART 6 - Xác thực Hội viên (NqtHoiVienAuth)
-- Bảng xác thực hội viên — tách riêng khỏi G6HoiVien (thông tin cá nhân)
-- ============================================================

CREATE TABLE NqtHoiVienAuth (
    nqt_ma                   INT IDENTITY(1,1) PRIMARY KEY,
    nqt_ma_hoi_vien          INT NOT NULL,
    nqt_mat_khau_hash        NVARCHAR(255) NOT NULL,
    nqt_la_hoat_dong         BIT NOT NULL DEFAULT 1,
    nqt_lan_dang_nhap_sai    INT NOT NULL DEFAULT 0,
    nqt_khoa_den             DATETIME2 NULL,
    nqt_reset_token           NVARCHAR(8) NULL,
    nqt_reset_token_het_han   DATETIME2 NULL,
    nqt_ngay_tao             DATETIME2 NOT NULL DEFAULT GETDATE(),
    nqt_ngay_cap_nhat        DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT fk_nqthvauth_hoi_vien
        FOREIGN KEY (nqt_ma_hoi_vien)
        REFERENCES G6HoiVien(g6_ma_hoi_vien)
        ON DELETE CASCADE,
    CONSTRAINT uq_nqthvauth_hoi_vien UNIQUE (nqt_ma_hoi_vien)
);

CREATE INDEX IX_NqtHV_ma_hoi_vien ON NqtHoiVienAuth (nqt_ma_hoi_vien);
CREATE INDEX IX_NqtHV_reset_token ON NqtHoiVienAuth (nqt_reset_token);
CREATE INDEX IX_NqtHV_khoa_den    ON NqtHoiVienAuth (nqt_khoa_den);

PRINT N'Part 6 - NqtHoiVienAuth: Hoàn thành!';
GO
