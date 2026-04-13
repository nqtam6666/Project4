from backend.app import db
from datetime import datetime


class NqtKhachHang(db.Model):
    __tablename__ = 'NqtKhachHang'

    nqt_ma_khach_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ho_ten = db.Column(db.String(100), nullable=False)
    nqt_email = db.Column(db.String(100), unique=True)
    nqt_so_dien_thoai = db.Column(db.String(15))
    nqt_mat_khau = db.Column(db.String(255))
    nqt_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('NqtHoiVien.nqt_ma_hoi_vien', ondelete='SET NULL'))
    nqt_la_xac_thuc_otp = db.Column(db.Boolean, nullable=False, default=False)
    nqt_google_id = db.Column(db.String(100))
    nqt_anh_dai_dien = db.Column(db.String(500))
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nqt_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    nqt_dia_chi = db.relationship('NqtDiaChiGiaoHang', back_populates='nqt_khach_hang', cascade='all, delete-orphan')
    nqt_diem = db.relationship('NqtDiemKhachHang', back_populates='nqt_khach_hang', uselist=False)

    def nqt_to_dict(self):
        return {
            'nqt_ma_khach_hang': self.nqt_ma_khach_hang,
            'nqt_ho_ten': self.nqt_ho_ten,
            'nqt_email': self.nqt_email,
            'nqt_so_dien_thoai': self.nqt_so_dien_thoai,
            'nqt_la_xac_thuc_otp': self.nqt_la_xac_thuc_otp,
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat() if self.nqt_ngay_tao else None,
        }


class NqtDiaChiGiaoHang(db.Model):
    __tablename__ = 'NqtDiaChiGiaoHang'

    nqt_ma_dia_chi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('NqtKhachHang.nqt_ma_khach_hang', ondelete='CASCADE'),
                                   nullable=False)
    nqt_ho_ten_nguoi_nhan = db.Column(db.String(100), nullable=False)
    nqt_so_dien_thoai = db.Column(db.String(15), nullable=False)
    nqt_dia_chi_chi_tiet = db.Column(db.String(255), nullable=False)
    nqt_phuong_xa = db.Column(db.String(100))
    nqt_quan_huyen = db.Column(db.String(100))
    nqt_tinh_thanh = db.Column(db.String(100))
    nqt_la_mac_dinh = db.Column(db.Boolean, nullable=False, default=False)

    nqt_khach_hang = db.relationship('NqtKhachHang', back_populates='nqt_dia_chi')

    def nqt_to_dict(self):
        return {
            'nqt_ma_dia_chi': self.nqt_ma_dia_chi,
            'nqt_ho_ten_nguoi_nhan': self.nqt_ho_ten_nguoi_nhan,
            'nqt_so_dien_thoai': self.nqt_so_dien_thoai,
            'nqt_dia_chi_chi_tiet': self.nqt_dia_chi_chi_tiet,
            'nqt_phuong_xa': self.nqt_phuong_xa,
            'nqt_quan_huyen': self.nqt_quan_huyen,
            'nqt_tinh_thanh': self.nqt_tinh_thanh,
            'nqt_la_mac_dinh': self.nqt_la_mac_dinh,
        }


class NqtHangThanhVien(db.Model):
    __tablename__ = 'NqtHangThanhVien'

    nqt_ma_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ten_hang = db.Column(db.String(50), nullable=False)
    nqt_diem_toi_thieu = db.Column(db.Integer, nullable=False, default=0)
    nqt_he_so_tich_diem = db.Column(db.Numeric(3, 2), nullable=False, default=1.0)
    nqt_mau_hien_thi = db.Column(db.String(20))
    nqt_icon = db.Column(db.String(100))

    def nqt_to_dict(self):
        return {
            'nqt_ma_hang': self.nqt_ma_hang,
            'nqt_ten_hang': self.nqt_ten_hang,
            'nqt_diem_toi_thieu': self.nqt_diem_toi_thieu,
            'nqt_he_so_tich_diem': float(self.nqt_he_so_tich_diem),
            'nqt_mau_hien_thi': self.nqt_mau_hien_thi,
        }


class NqtDiemKhachHang(db.Model):
    __tablename__ = 'NqtDiemKhachHang'

    nqt_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('NqtKhachHang.nqt_ma_khach_hang', ondelete='CASCADE'),
                                   primary_key=True)
    nqt_tong_diem = db.Column(db.Integer, nullable=False, default=0)
    nqt_diem_kha_dung = db.Column(db.Integer, nullable=False, default=0)
    nqt_ma_hang = db.Column(db.Integer, db.ForeignKey('NqtHangThanhVien.nqt_ma_hang'))
    nqt_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    nqt_khach_hang = db.relationship('NqtKhachHang', back_populates='nqt_diem')
    nqt_hang = db.relationship('NqtHangThanhVien')

    def nqt_to_dict(self):
        return {
            'nqt_tong_diem': self.nqt_tong_diem,
            'nqt_diem_kha_dung': self.nqt_diem_kha_dung,
            'nqt_hang': self.nqt_hang.nqt_ten_hang if self.nqt_hang else None,
        }


class NqtGiaoDichDiem(db.Model):
    __tablename__ = 'NqtGiaoDichDiem'

    nqt_ma_giao_dich = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('NqtKhachHang.nqt_ma_khach_hang', ondelete='CASCADE'),
                                   nullable=False)
    nqt_so_diem = db.Column(db.Integer, nullable=False)
    nqt_loai = db.Column(db.String(20), nullable=False)
    nqt_ly_do = db.Column(db.String(255))
    nqt_ma_don_hang = db.Column(db.Integer)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def nqt_to_dict(self):
        return {
            'nqt_ma_giao_dich': self.nqt_ma_giao_dich,
            'nqt_so_diem': self.nqt_so_diem,
            'nqt_loai': self.nqt_loai,
            'nqt_ly_do': self.nqt_ly_do,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat(),
        }
