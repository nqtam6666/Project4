from backend.app import db
from datetime import datetime


class G6KhachHang(db.Model):
    __tablename__ = 'G6KhachHang'

    g6_ma_khach_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ho_ten = db.Column(db.String(100), nullable=False)
    g6_email = db.Column(db.String(100), unique=True)
    g6_so_dien_thoai = db.Column(db.String(15))
    g6_mat_khau = db.Column(db.String(255))
    g6_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('G6HoiVien.g6_ma_hoi_vien', ondelete='SET NULL'))
    g6_la_xac_thuc_otp = db.Column(db.Boolean, nullable=False, default=False)
    g6_google_id = db.Column(db.String(100))
    g6_anh_dai_dien = db.Column(db.String(500))
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    g6_dia_chi = db.relationship('G6DiaChiGiaoHang', back_populates='g6_khach_hang', cascade='all, delete-orphan')
    g6_diem = db.relationship('G6DiemKhachHang', back_populates='g6_khach_hang', uselist=False)

    def g6_to_dict(self):
        return {
            'g6_ma_khach_hang': self.g6_ma_khach_hang,
            'g6_ho_ten': self.g6_ho_ten,
            'g6_email': self.g6_email,
            'g6_so_dien_thoai': self.g6_so_dien_thoai,
            'g6_la_xac_thuc_otp': self.g6_la_xac_thuc_otp,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat() if self.g6_ngay_tao else None,
        }


class G6DiaChiGiaoHang(db.Model):
    __tablename__ = 'G6DiaChiGiaoHang'

    g6_ma_dia_chi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('G6KhachHang.g6_ma_khach_hang', ondelete='CASCADE'),
                                   nullable=False)
    g6_ho_ten_nguoi_nhan = db.Column(db.String(100), nullable=False)
    g6_so_dien_thoai = db.Column(db.String(15), nullable=False)
    g6_dia_chi_chi_tiet = db.Column(db.String(255), nullable=False)
    g6_phuong_xa = db.Column(db.String(100))
    g6_quan_huyen = db.Column(db.String(100))
    g6_tinh_thanh = db.Column(db.String(100))
    g6_la_mac_dinh = db.Column(db.Boolean, nullable=False, default=False)

    g6_khach_hang = db.relationship('G6KhachHang', back_populates='g6_dia_chi')

    def g6_to_dict(self):
        return {
            'g6_ma_dia_chi': self.g6_ma_dia_chi,
            'g6_ho_ten_nguoi_nhan': self.g6_ho_ten_nguoi_nhan,
            'g6_so_dien_thoai': self.g6_so_dien_thoai,
            'g6_dia_chi_chi_tiet': self.g6_dia_chi_chi_tiet,
            'g6_phuong_xa': self.g6_phuong_xa,
            'g6_quan_huyen': self.g6_quan_huyen,
            'g6_tinh_thanh': self.g6_tinh_thanh,
            'g6_la_mac_dinh': self.g6_la_mac_dinh,
        }


class G6HangThanhVien(db.Model):
    __tablename__ = 'G6HangThanhVien'

    g6_ma_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten_hang = db.Column(db.String(50), nullable=False)
    g6_diem_toi_thieu = db.Column(db.Integer, nullable=False, default=0)
    g6_he_so_tich_diem = db.Column(db.Numeric(3, 2), nullable=False, default=1.0)
    g6_mau_hien_thi = db.Column(db.String(20))
    g6_icon = db.Column(db.String(100))

    def g6_to_dict(self):
        return {
            'g6_ma_hang': self.g6_ma_hang,
            'g6_ten_hang': self.g6_ten_hang,
            'g6_diem_toi_thieu': self.g6_diem_toi_thieu,
            'g6_he_so_tich_diem': float(self.g6_he_so_tich_diem),
            'g6_mau_hien_thi': self.g6_mau_hien_thi,
        }


class G6DiemKhachHang(db.Model):
    __tablename__ = 'G6DiemKhachHang'

    g6_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('G6KhachHang.g6_ma_khach_hang', ondelete='CASCADE'),
                                   primary_key=True)
    g6_tong_diem = db.Column(db.Integer, nullable=False, default=0)
    g6_diem_kha_dung = db.Column(db.Integer, nullable=False, default=0)
    g6_ma_hang = db.Column(db.Integer, db.ForeignKey('G6HangThanhVien.g6_ma_hang'))
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    g6_khach_hang = db.relationship('G6KhachHang', back_populates='g6_diem')
    g6_hang = db.relationship('G6HangThanhVien')

    def g6_to_dict(self):
        return {
            'g6_tong_diem': self.g6_tong_diem,
            'g6_diem_kha_dung': self.g6_diem_kha_dung,
            'g6_hang': self.g6_hang.g6_ten_hang if self.g6_hang else None,
        }


class G6GiaoDichDiem(db.Model):
    __tablename__ = 'G6GiaoDichDiem'

    g6_ma_giao_dich = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('G6KhachHang.g6_ma_khach_hang', ondelete='CASCADE'),
                                   nullable=False)
    g6_so_diem = db.Column(db.Integer, nullable=False)
    g6_loai = db.Column(db.String(20), nullable=False)
    g6_ly_do = db.Column(db.String(255))
    g6_ma_don_hang = db.Column(db.Integer)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_giao_dich': self.g6_ma_giao_dich,
            'g6_so_diem': self.g6_so_diem,
            'g6_loai': self.g6_loai,
            'g6_ly_do': self.g6_ly_do,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat(),
        }
