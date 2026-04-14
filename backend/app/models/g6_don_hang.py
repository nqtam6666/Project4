from backend.app import db
from datetime import datetime


class G6GioHang(db.Model):
    __tablename__ = 'G6GioHang'

    g6_ma_gio_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('G6KhachHang.g6_ma_khach_hang', ondelete='CASCADE'))
    g6_phien_khach = db.Column(db.String(100))
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    g6_chi_tiet = db.relationship('G6ChiTietGioHang', back_populates='g6_gio_hang', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_gio_hang': self.g6_ma_gio_hang,
            'g6_ma_khach_hang': self.g6_ma_khach_hang,
            'g6_chi_tiet': [ct.g6_to_dict() for ct in self.g6_chi_tiet],
        }


class G6ChiTietGioHang(db.Model):
    __tablename__ = 'G6ChiTietGioHang'

    g6_ma_chi_tiet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_gio_hang = db.Column(db.Integer, db.ForeignKey('G6GioHang.g6_ma_gio_hang', ondelete='CASCADE'),
                                 nullable=False)
    g6_ma_bien_the = db.Column(db.Integer, nullable=False)
    g6_so_luong = db.Column(db.Integer, nullable=False, default=1)
    g6_don_gia = db.Column(db.Numeric(15, 0), nullable=False)

    g6_gio_hang = db.relationship('G6GioHang', back_populates='g6_chi_tiet')

    def g6_to_dict(self):
        return {
            'g6_ma_chi_tiet': self.g6_ma_chi_tiet,
            'g6_ma_bien_the': self.g6_ma_bien_the,
            'g6_so_luong': self.g6_so_luong,
            'g6_don_gia': float(self.g6_don_gia),
        }


class G6DonHang(db.Model):
    __tablename__ = 'G6DonHang'

    g6_ma_don_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('G6KhachHang.g6_ma_khach_hang', ondelete='SET NULL'))
    g6_ma_nguoi_xu_ly = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    g6_ma_van_chuyen = db.Column(db.Integer, db.ForeignKey('G6DonViVanChuyen.g6_ma_don_vi'))
    g6_ma_giam_gia = db.Column(db.Integer, db.ForeignKey('G6MaGiamGia.g6_ma_ma_giam_gia', ondelete='SET NULL'))
    g6_ho_ten_nguoi_nhan = db.Column(db.String(100), nullable=False)
    g6_so_dien_thoai = db.Column(db.String(15), nullable=False)
    g6_dia_chi_giao_hang = db.Column(db.String(500), nullable=False)
    g6_tong_tien_hang = db.Column(db.Numeric(15, 0), nullable=False)
    g6_phi_van_chuyen = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    g6_so_tien_giam = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    g6_diem_su_dung = db.Column(db.Integer, nullable=False, default=0)
    g6_tien_diem_tru = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    g6_tong_thanh_toan = db.Column(db.Numeric(15, 0), nullable=False)
    g6_trang_thai = db.Column(db.String(30), nullable=False, default='cho_xac_nhan')
    g6_phuong_thuc_thanh_toan = db.Column(db.String(30), nullable=False, default='cod')
    g6_ghi_chu_khach = db.Column(db.Text)
    g6_ghi_chu_noi_bo = db.Column(db.Text)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    g6_chi_tiet = db.relationship('G6ChiTietDonHang', back_populates='g6_don_hang', cascade='all, delete-orphan')
    g6_lich_su = db.relationship('G6LichSuDonHang', back_populates='g6_don_hang', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_don_hang': self.g6_ma_don_hang,
            'g6_ma_khach_hang': self.g6_ma_khach_hang,
            'g6_ho_ten_nguoi_nhan': self.g6_ho_ten_nguoi_nhan,
            'g6_so_dien_thoai': self.g6_so_dien_thoai,
            'g6_dia_chi_giao_hang': self.g6_dia_chi_giao_hang,
            'g6_tong_tien_hang': float(self.g6_tong_tien_hang),
            'g6_phi_van_chuyen': float(self.g6_phi_van_chuyen),
            'g6_so_tien_giam': float(self.g6_so_tien_giam),
            'g6_tong_thanh_toan': float(self.g6_tong_thanh_toan),
            'g6_trang_thai': self.g6_trang_thai,
            'g6_phuong_thuc_thanh_toan': self.g6_phuong_thuc_thanh_toan,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat() if self.g6_ngay_tao else None,
        }


class G6ChiTietDonHang(db.Model):
    __tablename__ = 'G6ChiTietDonHang'

    g6_ma_chi_tiet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_don_hang = db.Column(db.Integer, db.ForeignKey('G6DonHang.g6_ma_don_hang', ondelete='CASCADE'),
                                 nullable=False)
    g6_ma_bien_the = db.Column(db.Integer, nullable=False)
    g6_ten_san_pham = db.Column(db.String(200), nullable=False)
    g6_sku = db.Column(db.String(100))
    g6_so_luong = db.Column(db.Integer, nullable=False)
    g6_don_gia = db.Column(db.Numeric(15, 0), nullable=False)
    g6_thanh_tien = db.Column(db.Numeric(15, 0), nullable=False)

    g6_don_hang = db.relationship('G6DonHang', back_populates='g6_chi_tiet')

    def g6_to_dict(self):
        return {
            'g6_ma_chi_tiet': self.g6_ma_chi_tiet,
            'g6_ma_bien_the': self.g6_ma_bien_the,
            'g6_ten_san_pham': self.g6_ten_san_pham,
            'g6_sku': self.g6_sku,
            'g6_so_luong': self.g6_so_luong,
            'g6_don_gia': float(self.g6_don_gia),
            'g6_thanh_tien': float(self.g6_thanh_tien),
        }


class G6LichSuDonHang(db.Model):
    __tablename__ = 'G6LichSuDonHang'

    g6_ma_lich_su = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_don_hang = db.Column(db.Integer, db.ForeignKey('G6DonHang.g6_ma_don_hang', ondelete='CASCADE'),
                                 nullable=False)
    g6_trang_thai_cu = db.Column(db.String(30))
    g6_trang_thai_moi = db.Column(db.String(30), nullable=False)
    g6_ghi_chu = db.Column(db.String(255))
    g6_nguoi_thay_doi = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_don_hang = db.relationship('G6DonHang', back_populates='g6_lich_su')

    def g6_to_dict(self):
        return {
            'g6_ma_lich_su': self.g6_ma_lich_su,
            'g6_trang_thai_cu': self.g6_trang_thai_cu,
            'g6_trang_thai_moi': self.g6_trang_thai_moi,
            'g6_ghi_chu': self.g6_ghi_chu,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat(),
        }
