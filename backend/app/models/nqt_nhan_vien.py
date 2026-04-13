from backend.app import db
from datetime import datetime


class NqtNhanVien(db.Model):
    __tablename__ = 'NqtNhanVien'

    nqt_ma_nhan_vien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey('NqtNguoiDung.nqt_ma_nguoi_dung', ondelete='SET NULL'))
    nqt_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('NqtChiNhanh.nqt_ma_chi_nhanh'), nullable=False)
    nqt_ho_ten = db.Column(db.String(100), nullable=False)
    nqt_ngay_sinh = db.Column(db.Date)
    nqt_gioi_tinh = db.Column(db.String(10))
    nqt_so_dien_thoai = db.Column(db.String(15))
    nqt_email = db.Column(db.String(100))
    nqt_dia_chi = db.Column(db.String(255))
    nqt_so_cccd = db.Column(db.String(20))
    nqt_ngay_vao_lam = db.Column(db.Date, nullable=False)
    nqt_ngay_nghi_viec = db.Column(db.Date)
    nqt_luong_co_ban = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    nqt_trang_thai = db.Column(db.String(20), nullable=False, default='dang_lam')
    nqt_hinh_anh = db.Column(db.String(500))
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    nqt_nguoi_dung = db.relationship('NqtNguoiDung', foreign_keys=[nqt_ma_nguoi_dung])
    nqt_chi_nhanh = db.relationship('NqtChiNhanh', foreign_keys=[nqt_ma_chi_nhanh])
    nqt_lich_lam_viec = db.relationship('NqtLichLamViec', back_populates='nqt_nhan_vien', cascade='all, delete-orphan')

    def nqt_to_dict(self):
        return {
            'nqt_ma_nhan_vien': self.nqt_ma_nhan_vien,
            'nqt_ma_nguoi_dung': self.nqt_ma_nguoi_dung,
            'nqt_ma_chi_nhanh': self.nqt_ma_chi_nhanh,
            'nqt_ho_ten': self.nqt_ho_ten,
            'nqt_ngay_sinh': str(self.nqt_ngay_sinh) if self.nqt_ngay_sinh else None,
            'nqt_gioi_tinh': self.nqt_gioi_tinh,
            'nqt_so_dien_thoai': self.nqt_so_dien_thoai,
            'nqt_email': self.nqt_email,
            'nqt_ngay_vao_lam': str(self.nqt_ngay_vao_lam) if self.nqt_ngay_vao_lam else None,
            'nqt_trang_thai': self.nqt_trang_thai,
            'nqt_luong_co_ban': float(self.nqt_luong_co_ban) if self.nqt_luong_co_ban else 0,
        }


class NqtLichLamViec(db.Model):
    __tablename__ = 'NqtLichLamViec'

    nqt_ma_lich = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_nhan_vien = db.Column(db.Integer, db.ForeignKey('NqtNhanVien.nqt_ma_nhan_vien', ondelete='CASCADE'),
                                  nullable=False)
    nqt_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('NqtChiNhanh.nqt_ma_chi_nhanh'), nullable=False)
    nqt_thu_trong_tuan = db.Column(db.SmallInteger, nullable=False)
    nqt_gio_bat_dau = db.Column(db.Time, nullable=False)
    nqt_gio_ket_thuc = db.Column(db.Time, nullable=False)
    nqt_tuan_hieu_luc = db.Column(db.Date)

    nqt_nhan_vien = db.relationship('NqtNhanVien', back_populates='nqt_lich_lam_viec')

    def nqt_to_dict(self):
        return {
            'nqt_ma_lich': self.nqt_ma_lich,
            'nqt_ma_nhan_vien': self.nqt_ma_nhan_vien,
            'nqt_thu_trong_tuan': self.nqt_thu_trong_tuan,
            'nqt_gio_bat_dau': str(self.nqt_gio_bat_dau),
            'nqt_gio_ket_thuc': str(self.nqt_gio_ket_thuc),
            'nqt_tuan_hieu_luc': str(self.nqt_tuan_hieu_luc) if self.nqt_tuan_hieu_luc else None,
        }
