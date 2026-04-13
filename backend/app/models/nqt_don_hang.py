from backend.app import db
from datetime import datetime


class NqtGioHang(db.Model):
    __tablename__ = 'NqtGioHang'

    nqt_ma_gio_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('NqtKhachHang.nqt_ma_khach_hang', ondelete='CASCADE'))
    nqt_phien_khach = db.Column(db.String(100))
    nqt_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    nqt_chi_tiet = db.relationship('NqtChiTietGioHang', back_populates='nqt_gio_hang', cascade='all, delete-orphan')

    def nqt_to_dict(self):
        return {
            'nqt_ma_gio_hang': self.nqt_ma_gio_hang,
            'nqt_ma_khach_hang': self.nqt_ma_khach_hang,
            'nqt_chi_tiet': [ct.nqt_to_dict() for ct in self.nqt_chi_tiet],
        }


class NqtChiTietGioHang(db.Model):
    __tablename__ = 'NqtChiTietGioHang'

    nqt_ma_chi_tiet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_gio_hang = db.Column(db.Integer, db.ForeignKey('NqtGioHang.nqt_ma_gio_hang', ondelete='CASCADE'),
                                 nullable=False)
    nqt_ma_bien_the = db.Column(db.Integer, nullable=False)
    nqt_so_luong = db.Column(db.Integer, nullable=False, default=1)
    nqt_don_gia = db.Column(db.Numeric(15, 0), nullable=False)

    nqt_gio_hang = db.relationship('NqtGioHang', back_populates='nqt_chi_tiet')

    def nqt_to_dict(self):
        return {
            'nqt_ma_chi_tiet': self.nqt_ma_chi_tiet,
            'nqt_ma_bien_the': self.nqt_ma_bien_the,
            'nqt_so_luong': self.nqt_so_luong,
            'nqt_don_gia': float(self.nqt_don_gia),
        }


class NqtDonHang(db.Model):
    __tablename__ = 'NqtDonHang'

    nqt_ma_don_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('NqtKhachHang.nqt_ma_khach_hang', ondelete='SET NULL'))
    nqt_ma_nguoi_xu_ly = db.Column(db.Integer, db.ForeignKey('NqtNguoiDung.nqt_ma_nguoi_dung', ondelete='SET NULL'))
    nqt_ma_van_chuyen = db.Column(db.Integer, db.ForeignKey('NqtDonViVanChuyen.nqt_ma_don_vi'))
    nqt_ma_giam_gia = db.Column(db.Integer, db.ForeignKey('NqtMaGiamGia.nqt_ma_ma_giam_gia', ondelete='SET NULL'))
    nqt_ho_ten_nguoi_nhan = db.Column(db.String(100), nullable=False)
    nqt_so_dien_thoai = db.Column(db.String(15), nullable=False)
    nqt_dia_chi_giao_hang = db.Column(db.String(500), nullable=False)
    nqt_tong_tien_hang = db.Column(db.Numeric(15, 0), nullable=False)
    nqt_phi_van_chuyen = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    nqt_so_tien_giam = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    nqt_diem_su_dung = db.Column(db.Integer, nullable=False, default=0)
    nqt_tien_diem_tru = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    nqt_tong_thanh_toan = db.Column(db.Numeric(15, 0), nullable=False)
    nqt_trang_thai = db.Column(db.String(30), nullable=False, default='cho_xac_nhan')
    nqt_phuong_thuc_thanh_toan = db.Column(db.String(30), nullable=False, default='cod')
    nqt_ghi_chu_khach = db.Column(db.Text)
    nqt_ghi_chu_noi_bo = db.Column(db.Text)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nqt_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    nqt_chi_tiet = db.relationship('NqtChiTietDonHang', back_populates='nqt_don_hang', cascade='all, delete-orphan')
    nqt_lich_su = db.relationship('NqtLichSuDonHang', back_populates='nqt_don_hang', cascade='all, delete-orphan')

    def nqt_to_dict(self):
        return {
            'nqt_ma_don_hang': self.nqt_ma_don_hang,
            'nqt_ma_khach_hang': self.nqt_ma_khach_hang,
            'nqt_ho_ten_nguoi_nhan': self.nqt_ho_ten_nguoi_nhan,
            'nqt_so_dien_thoai': self.nqt_so_dien_thoai,
            'nqt_dia_chi_giao_hang': self.nqt_dia_chi_giao_hang,
            'nqt_tong_tien_hang': float(self.nqt_tong_tien_hang),
            'nqt_phi_van_chuyen': float(self.nqt_phi_van_chuyen),
            'nqt_so_tien_giam': float(self.nqt_so_tien_giam),
            'nqt_tong_thanh_toan': float(self.nqt_tong_thanh_toan),
            'nqt_trang_thai': self.nqt_trang_thai,
            'nqt_phuong_thuc_thanh_toan': self.nqt_phuong_thuc_thanh_toan,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat() if self.nqt_ngay_tao else None,
        }


class NqtChiTietDonHang(db.Model):
    __tablename__ = 'NqtChiTietDonHang'

    nqt_ma_chi_tiet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_don_hang = db.Column(db.Integer, db.ForeignKey('NqtDonHang.nqt_ma_don_hang', ondelete='CASCADE'),
                                 nullable=False)
    nqt_ma_bien_the = db.Column(db.Integer, nullable=False)
    nqt_ten_san_pham = db.Column(db.String(200), nullable=False)
    nqt_sku = db.Column(db.String(100))
    nqt_so_luong = db.Column(db.Integer, nullable=False)
    nqt_don_gia = db.Column(db.Numeric(15, 0), nullable=False)
    nqt_thanh_tien = db.Column(db.Numeric(15, 0), nullable=False)

    nqt_don_hang = db.relationship('NqtDonHang', back_populates='nqt_chi_tiet')

    def nqt_to_dict(self):
        return {
            'nqt_ma_chi_tiet': self.nqt_ma_chi_tiet,
            'nqt_ma_bien_the': self.nqt_ma_bien_the,
            'nqt_ten_san_pham': self.nqt_ten_san_pham,
            'nqt_sku': self.nqt_sku,
            'nqt_so_luong': self.nqt_so_luong,
            'nqt_don_gia': float(self.nqt_don_gia),
            'nqt_thanh_tien': float(self.nqt_thanh_tien),
        }


class NqtLichSuDonHang(db.Model):
    __tablename__ = 'NqtLichSuDonHang'

    nqt_ma_lich_su = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_don_hang = db.Column(db.Integer, db.ForeignKey('NqtDonHang.nqt_ma_don_hang', ondelete='CASCADE'),
                                 nullable=False)
    nqt_trang_thai_cu = db.Column(db.String(30))
    nqt_trang_thai_moi = db.Column(db.String(30), nullable=False)
    nqt_ghi_chu = db.Column(db.String(255))
    nqt_nguoi_thay_doi = db.Column(db.Integer, db.ForeignKey('NqtNguoiDung.nqt_ma_nguoi_dung', ondelete='SET NULL'))
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    nqt_don_hang = db.relationship('NqtDonHang', back_populates='nqt_lich_su')

    def nqt_to_dict(self):
        return {
            'nqt_ma_lich_su': self.nqt_ma_lich_su,
            'nqt_trang_thai_cu': self.nqt_trang_thai_cu,
            'nqt_trang_thai_moi': self.nqt_trang_thai_moi,
            'nqt_ghi_chu': self.nqt_ghi_chu,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat(),
        }
