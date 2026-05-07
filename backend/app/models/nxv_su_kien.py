from backend.app import db
from datetime import datetime


class NxvSuKien(db.Model):
    __tablename__ = 'NxvSuKien'

    nxv_ma_su_kien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nxv_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh', ondelete='SET NULL'))
    nxv_ten = db.Column(db.String(200), nullable=False)
    nxv_mo_ta = db.Column(db.Text)
    nxv_loai = db.Column(db.String(30), nullable=False, default='su_kien')  # su_kien, flash_sale, khuyen_mai
    nxv_hinh_anh = db.Column(db.String(500))
    nxv_ngay_bat_dau = db.Column(db.DateTime, nullable=False)
    nxv_ngay_ket_thuc = db.Column(db.DateTime, nullable=False)
    nxv_dia_diem = db.Column(db.String(255))
    nxv_suc_chua = db.Column(db.Integer)
    nxv_gia_ve = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    nxv_gia_giam = db.Column(db.Numeric(15, 0))
    nxv_ma_goi_ap_dung = db.Column(db.Integer, db.ForeignKey('G6GoiTap.g6_ma_goi_tap', ondelete='SET NULL'))
    nxv_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    nxv_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    nxv_dang_ky = db.relationship('NxvDangKySuKien', back_populates='nxv_su_kien', cascade='all, delete-orphan')

    def nxv_to_dict(self):
        return {
            'nxv_ma_su_kien': self.nxv_ma_su_kien,
            'nxv_ma_chi_nhanh': self.nxv_ma_chi_nhanh,
            'nxv_ten': self.nxv_ten,
            'nxv_mo_ta': self.nxv_mo_ta,
            'nxv_loai': self.nxv_loai,
            'nxv_hinh_anh': self.nxv_hinh_anh,
            'nxv_ngay_bat_dau': self.nxv_ngay_bat_dau.isoformat() if self.nxv_ngay_bat_dau else None,
            'nxv_ngay_ket_thuc': self.nxv_ngay_ket_thuc.isoformat() if self.nxv_ngay_ket_thuc else None,
            'nxv_dia_diem': self.nxv_dia_diem,
            'nxv_suc_chua': self.nxv_suc_chua,
            'nxv_gia_ve': float(self.nxv_gia_ve),
            'nxv_gia_giam': float(self.nxv_gia_giam) if self.nxv_gia_giam else None,
            'nxv_la_hoat_dong': self.nxv_la_hoat_dong,
            'nxv_ngay_tao': self.nxv_ngay_tao.isoformat() if self.nxv_ngay_tao else None,
        }


class NxvDangKySuKien(db.Model):
    __tablename__ = 'NxvDangKySuKien'

    nxv_ma_dang_ky = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nxv_ma_su_kien = db.Column(db.Integer, db.ForeignKey('NxvSuKien.nxv_ma_su_kien', ondelete='CASCADE'), nullable=False)
    nxv_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('G6HoiVien.g6_ma_hoi_vien', ondelete='SET NULL'))
    nxv_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('G6KhachHang.g6_ma_khach_hang', ondelete='SET NULL'))
    nxv_ho_ten = db.Column(db.String(100), nullable=False)
    nxv_so_dien_thoai = db.Column(db.String(15))
    nxv_email = db.Column(db.String(100))
    nxv_so_ve = db.Column(db.Integer, nullable=False, default=1)
    nxv_tong_tien = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    nxv_trang_thai = db.Column(db.String(20), nullable=False, default='cho_xac_nhan')
    nxv_ma_qr = db.Column(db.String(100), unique=True)
    nxv_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    nxv_su_kien = db.relationship('NxvSuKien', back_populates='nxv_dang_ky')

    def nxv_to_dict(self):
        return {
            'nxv_ma_dang_ky': self.nxv_ma_dang_ky,
            'nxv_ma_su_kien': self.nxv_ma_su_kien,
            'nxv_ma_hoi_vien': self.nxv_ma_hoi_vien,
            'nxv_ma_khach_hang': self.nxv_ma_khach_hang,
            'nxv_ho_ten': self.nxv_ho_ten,
            'nxv_so_dien_thoai': self.nxv_so_dien_thoai,
            'nxv_email': self.nxv_email,
            'nxv_so_ve': self.nxv_so_ve,
            'nxv_tong_tien': float(self.nxv_tong_tien),
            'nxv_trang_thai': self.nxv_trang_thai,
            'nxv_ma_qr': self.nxv_ma_qr,
            'nxv_ngay_tao': self.nxv_ngay_tao.isoformat() if self.nxv_ngay_tao else None,
        }
