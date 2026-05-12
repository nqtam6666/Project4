from backend.app import db
from datetime import datetime, date


class G6NhanVien(db.Model):
    __tablename__ = 'G6NhanVien'

    g6_ma_nhan_vien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh'), nullable=False)
    g6_ho_ten = db.Column(db.String(100), nullable=False)
    g6_ngay_sinh = db.Column(db.Date)
    g6_gioi_tinh = db.Column(db.String(10))
    g6_so_dien_thoai = db.Column(db.String(15))
    g6_email = db.Column(db.String(100))
    g6_dia_chi = db.Column(db.String(255))
    g6_so_cccd = db.Column(db.String(20))
    g6_ngay_vao_lam = db.Column(db.Date, nullable=False, default=date.today)
    g6_ngay_nghi_viec = db.Column(db.Date)
    g6_luong_co_ban = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    g6_trang_thai = db.Column(db.String(20), nullable=False, default='dang_lam')
    g6_hinh_anh = db.Column(db.String(500))
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_nguoi_dung = db.relationship('G6NguoiDung', foreign_keys=[g6_ma_nguoi_dung])
    g6_chi_nhanh = db.relationship('G6ChiNhanh', foreign_keys=[g6_ma_chi_nhanh])
    g6_lich_lam_viec = db.relationship('G6LichLamViec', back_populates='g6_nhan_vien', cascade='all, delete-orphan')

    def g6_to_dict(self):
        res = {
            'g6_ma_nhan_vien': self.g6_ma_nhan_vien,
            'g6_ma_nguoi_dung': self.g6_ma_nguoi_dung,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_ho_ten': self.g6_ho_ten,
            'g6_ngay_sinh': str(self.g6_ngay_sinh) if self.g6_ngay_sinh else None,
            'g6_gioi_tinh': self.g6_gioi_tinh,
            'g6_so_dien_thoai': self.g6_so_dien_thoai,
            'g6_email': self.g6_email,
            'g6_ngay_vao_lam': str(self.g6_ngay_vao_lam) if self.g6_ngay_vao_lam else None,
            'g6_trang_thai': self.g6_trang_thai,
            'g6_luong_co_ban': float(self.g6_luong_co_ban) if self.g6_luong_co_ban else 0,
        }
        if self.g6_nguoi_dung:
            res['g6_ten_dang_nhap'] = self.g6_nguoi_dung.g6_ten_dang_nhap
            res['g6_vai_tro'] = [vt.g6_vai_tro.g6_ten_vai_tro for vt in self.g6_nguoi_dung.g6_vai_tro]
        else:
            res['g6_ten_dang_nhap'] = '—'
            res['g6_vai_tro'] = []
        return res


class G6LichLamViec(db.Model):
    __tablename__ = 'G6LichLamViec'

    g6_ma_lich = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_nhan_vien = db.Column(db.Integer, db.ForeignKey('G6NhanVien.g6_ma_nhan_vien', ondelete='CASCADE'),
                                  nullable=False)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh'), nullable=False)
    g6_thu_trong_tuan = db.Column(db.SmallInteger, nullable=False)
    g6_gio_bat_dau = db.Column(db.Time, nullable=False)
    g6_gio_ket_thuc = db.Column(db.Time, nullable=False)
    g6_tuan_hieu_luc = db.Column(db.Date)

    g6_nhan_vien = db.relationship('G6NhanVien', back_populates='g6_lich_lam_viec')

    def g6_to_dict(self):
        return {
            'g6_ma_lich': self.g6_ma_lich,
            'g6_ma_nhan_vien': self.g6_ma_nhan_vien,
            'g6_thu_trong_tuan': self.g6_thu_trong_tuan,
            'g6_gio_bat_dau': str(self.g6_gio_bat_dau),
            'g6_gio_ket_thuc': str(self.g6_gio_ket_thuc),
            'g6_tuan_hieu_luc': str(self.g6_tuan_hieu_luc) if self.g6_tuan_hieu_luc else None,
        }
