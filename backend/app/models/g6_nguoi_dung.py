import bcrypt
from backend.app import db
from datetime import datetime, timedelta


class G6VaiTro(db.Model):
    __tablename__ = 'G6VaiTro'

    g6_ma_vai_tro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten_vai_tro = db.Column(db.String(50), nullable=False)
    g6_mo_ta = db.Column(db.String(255))

    g6_nguoi_dung = db.relationship('G6NguoiDungVaiTro', back_populates='g6_vai_tro', cascade='all, delete-orphan')
    g6_quyen = db.relationship('G6VaiTroQuyen', back_populates='g6_vai_tro', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_vai_tro': self.g6_ma_vai_tro,
            'g6_ten_vai_tro': self.g6_ten_vai_tro,
            'g6_mo_ta': self.g6_mo_ta,
        }


class G6QuyenHan(db.Model):
    __tablename__ = 'G6QuyenHan'

    g6_ma_quyen = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten_quyen = db.Column(db.String(100), nullable=False)
    g6_nhom_quyen = db.Column(db.String(50), nullable=False)

    g6_vai_tro = db.relationship('G6VaiTroQuyen', back_populates='g6_quyen', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_quyen': self.g6_ma_quyen,
            'g6_ten_quyen': self.g6_ten_quyen,
            'g6_nhom_quyen': self.g6_nhom_quyen,
        }


class G6NguoiDungVaiTro(db.Model):
    __tablename__ = 'G6NguoiDungVaiTro'

    g6_ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='CASCADE'),
                                   primary_key=True)
    g6_ma_vai_tro = db.Column(db.Integer, db.ForeignKey('G6VaiTro.g6_ma_vai_tro', ondelete='CASCADE'),
                                primary_key=True)

    g6_nguoi_dung = db.relationship('G6NguoiDung', back_populates='g6_vai_tro')
    g6_vai_tro = db.relationship('G6VaiTro', back_populates='g6_nguoi_dung')


class G6VaiTroQuyen(db.Model):
    __tablename__ = 'G6VaiTroQuyen'

    g6_ma_vai_tro = db.Column(db.Integer, db.ForeignKey('G6VaiTro.g6_ma_vai_tro', ondelete='CASCADE'),
                                primary_key=True)
    g6_ma_quyen = db.Column(db.Integer, db.ForeignKey('G6QuyenHan.g6_ma_quyen', ondelete='CASCADE'),
                              primary_key=True)

    g6_vai_tro = db.relationship('G6VaiTro', back_populates='g6_quyen')
    g6_quyen = db.relationship('G6QuyenHan', back_populates='g6_vai_tro')


class G6NguoiDung(db.Model):
    """Bảng người dùng thống nhất — gộp HoiVien + KhachHang + NguoiDung cũ."""
    __tablename__ = 'G6NguoiDung'

    g6_ma_nguoi_dung = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # ── Thông tin đăng nhập ───────────────────────────────────────────────
    # ── Thông tin đăng nhập ───────────────────────────────────────────────
    g6_ten_dang_nhap = db.Column(db.String(50))                       # Bỏ unique=True để dùng Index lọc bên dưới
    g6_mat_khau = db.Column(db.String(255))                           # nullable cho khách vãng lai
    g6_ho_ten = db.Column(db.String(100), nullable=False)
    g6_email = db.Column(db.String(100))
    g6_so_dien_thoai = db.Column(db.String(15))

    # ── Thông tin cá nhân (từ G6HoiVien) ──────────────────────────────────
    g6_ngay_sinh = db.Column(db.Date)
    g6_gioi_tinh = db.Column(db.String(10))
    g6_dia_chi = db.Column(db.String(255))
    g6_so_cccd = db.Column(db.String(20))
    g6_anh_the = db.Column(db.String(500))
    g6_anh_dai_dien = db.Column(db.String(500))

    # ── Phân loại ─────────────────────────────────────────────────────────
    g6_la_nhan_vien = db.Column(db.Boolean, nullable=False, default=False)
    g6_la_hoi_vien = db.Column(db.Boolean, nullable=False, default=False)
    g6_la_khach_hang = db.Column(db.Boolean, nullable=False, default=False)

    # ── Hội viên chuyên dụng ──────────────────────────────────────────────
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh', ondelete='SET NULL'))
    g6_ngay_dang_ky = db.Column(db.Date)                              # ngày đăng ký hội viên
    g6_ma_qr = db.Column(db.String(100))
    g6_nguon_gioi_thieu = db.Column(db.String(100))
    g6_ma_gioi_thieu = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung'))
    g6_ghi_chu = db.Column(db.Text)

    # ── Khách hàng chuyên dụng (từ G6KhachHang) ──────────────────────────
    g6_google_id = db.Column(db.String(100))
    g6_la_xac_thuc_otp = db.Column(db.Boolean, nullable=False, default=False)

    # ── Bảo mật / Lockout ─────────────────────────────────────────────────
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_lan_dang_nhap_sai = db.Column(db.Integer, nullable=False, default=0)
    g6_khoa_den = db.Column(db.DateTime)
    g6_reset_token = db.Column(db.String(8))
    g6_reset_token_het_han = db.Column(db.DateTime)

    # ── Timestamps ────────────────────────────────────────────────────────
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.Index('ix_g6_nguoi_dung_ten_dang_nhap', 'g6_ten_dang_nhap', unique=True, 
                 mssql_where=db.text('g6_ten_dang_nhap IS NOT NULL')),
    )

    # ── Relationships ─────────────────────────────────────────────────────
    g6_chi_nhanh = db.relationship('G6ChiNhanh', foreign_keys=[g6_ma_chi_nhanh])
    g6_nguoi_gioi_thieu_rel = db.relationship('G6NguoiDung', remote_side='G6NguoiDung.g6_ma_nguoi_dung',
                                               foreign_keys=[g6_ma_gioi_thieu])
    g6_vai_tro = db.relationship('G6NguoiDungVaiTro', back_populates='g6_nguoi_dung', cascade='all, delete-orphan')

    # Hội viên relationships
    g6_dang_ky = db.relationship('G6DangKyGoiTap', 
                                  primaryjoin="G6NguoiDung.g6_ma_nguoi_dung == G6DangKyGoiTap.g6_ma_nguoi_dung",
                                  foreign_keys="G6DangKyGoiTap.g6_ma_nguoi_dung",
                                  back_populates='g6_nguoi_dung', cascade='all, delete-orphan')
    g6_diem_danh = db.relationship('G6DiemDanh', 
                                    primaryjoin="G6NguoiDung.g6_ma_nguoi_dung == G6DiemDanh.g6_ma_nguoi_dung",
                                    foreign_keys="G6DiemDanh.g6_ma_nguoi_dung",
                                    back_populates='g6_nguoi_dung', cascade='all, delete-orphan')
    g6_chi_so = db.relationship('G6ChiSoCoThe', 
                                 primaryjoin="G6NguoiDung.g6_ma_nguoi_dung == G6ChiSoCoThe.g6_ma_nguoi_dung",
                                 foreign_keys="G6ChiSoCoThe.g6_ma_nguoi_dung",
                                 back_populates='g6_nguoi_dung', cascade='all, delete-orphan')

    # Khách hàng relationships
    g6_dia_chi_giao = db.relationship('G6DiaChiGiaoHang', back_populates='g6_nguoi_dung', cascade='all, delete-orphan')
    g6_diem = db.relationship('G6DiemKhachHang', back_populates='g6_nguoi_dung', uselist=False)
    g6_don_hang = db.relationship('G6DonHang', 
                                   primaryjoin="G6NguoiDung.g6_ma_nguoi_dung == G6DonHang.g6_ma_nguoi_dung",
                                   foreign_keys="G6DonHang.g6_ma_nguoi_dung",
                                   back_populates='g6_nguoi_dung')
    g6_gio_hang = db.relationship('G6GioHang', 
                                   primaryjoin="G6NguoiDung.g6_ma_nguoi_dung == G6GioHang.g6_ma_nguoi_dung",
                                   foreign_keys="G6GioHang.g6_ma_nguoi_dung",
                                   back_populates='g6_nguoi_dung', uselist=False)

    # ── Password helpers ──────────────────────────────────────────────────
    def nqt_dat_mat_khau(self, nqt_mat_khau_plain: str):
        self.g6_mat_khau = bcrypt.hashpw(
            nqt_mat_khau_plain.encode(), bcrypt.gensalt()
        ).decode()

    def nqt_kiem_tra_mat_khau(self, nqt_mat_khau_plain: str) -> bool:
        if not self.g6_mat_khau:
            return False
        return bcrypt.checkpw(
            nqt_mat_khau_plain.encode(),
            self.g6_mat_khau.encode()
        )

    # ── Lockout helpers ───────────────────────────────────────────────────
    def nqt_khoa_tai_khoan(self, nqt_phut=30):
        self.g6_khoa_den = datetime.utcnow() + timedelta(minutes=nqt_phut)
        self.g6_lan_dang_nhap_sai = 0

    def nqt_mo_khoa(self):
        self.g6_khoa_den = None
        self.g6_lan_dang_nhap_sai = 0

    # ── Serialize ─────────────────────────────────────────────────────────
    def g6_to_dict(self):
        res = {
            'g6_ma_nguoi_dung': self.g6_ma_nguoi_dung,
            'g6_ten_dang_nhap': self.g6_ten_dang_nhap,
            'g6_ho_ten': self.g6_ho_ten,
            'g6_email': self.g6_email,
            'g6_so_dien_thoai': self.g6_so_dien_thoai,
            'g6_ngay_sinh': str(self.g6_ngay_sinh) if self.g6_ngay_sinh else None,
            'g6_gioi_tinh': self.g6_gioi_tinh,
            'g6_dia_chi': self.g6_dia_chi,
            'g6_so_cccd': self.g6_so_cccd,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
            'g6_la_hoi_vien': self.g6_la_hoi_vien,
            'g6_la_khach_hang': self.g6_la_khach_hang,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat() if self.g6_ngay_tao else None,
            'g6_vai_tro': [ndvt.g6_vai_tro.g6_ten_vai_tro for ndvt in self.g6_vai_tro],
        }
        # Thông tin hội viên
        if self.g6_la_hoi_vien:
            res['g6_ngay_dang_ky'] = str(self.g6_ngay_dang_ky) if self.g6_ngay_dang_ky else None
            res['g6_ma_qr'] = self.g6_ma_qr
            res['g6_anh_the'] = self.g6_anh_the
            res['g6_ghi_chu'] = self.g6_ghi_chu
        return res
