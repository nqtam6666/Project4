from backend.app import db
from datetime import datetime


class G6LopHoc(db.Model):
    __tablename__ = 'G6LopHoc'

    g6_ma_lop_hoc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh'), nullable=False)
    g6_ten_lop = db.Column(db.String(100), nullable=False)
    g6_loai_lop = db.Column(db.String(50), nullable=False)  # 'yoga','spinning','boxing','zumba','aerobic'
    g6_mo_ta = db.Column(db.Text)
    g6_hinh_anh = db.Column(db.String(500))
    g6_do_kho = db.Column(db.String(20), nullable=False, default='co_ban')  # 'co_ban','trung_binh','nang_cao'
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    g6_chi_nhanh = db.relationship('G6ChiNhanh', foreign_keys=[g6_ma_chi_nhanh])
    g6_lich_lop = db.relationship('G6LichLopHoc', back_populates='g6_lop_hoc', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_lop_hoc': self.g6_ma_lop_hoc,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_ten_lop': self.g6_ten_lop,
            'g6_loai_lop': self.g6_loai_lop,
            'g6_mo_ta': self.g6_mo_ta,
            'g6_hinh_anh': self.g6_hinh_anh,
            'g6_do_kho': self.g6_do_kho,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
        }


class G6LichLopHoc(db.Model):
    __tablename__ = 'G6LichLopHoc'

    g6_ma_lich_lop = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_lop_hoc = db.Column(db.Integer, db.ForeignKey('G6LopHoc.g6_ma_lop_hoc', ondelete='CASCADE'), nullable=False)
    g6_ma_hlv = db.Column(db.Integer, db.ForeignKey('G6HuanLuyenVien.g6_ma_hlv'), nullable=False)
    g6_thu_trong_tuan = db.Column(db.SmallInteger, nullable=False)  # 1=T2 ... 7=CN
    g6_gio_bat_dau = db.Column(db.Time, nullable=False)
    g6_thoi_luong = db.Column(db.Integer, nullable=False)  # phút
    g6_suc_chua_toi_da = db.Column(db.Integer, nullable=False, default=20)
    g6_phong_tap = db.Column(db.String(50))
    g6_ngay_ap_dung_tu = db.Column(db.Date, nullable=False)
    g6_ngay_ap_dung_den = db.Column(db.Date)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    g6_lop_hoc = db.relationship('G6LopHoc', back_populates='g6_lich_lop')
    g6_hlv = db.relationship('G6HuanLuyenVien', foreign_keys=[g6_ma_hlv])
    g6_dat_cho = db.relationship('G6DatChoLopHoc', back_populates='g6_lich_lop', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_lich_lop': self.g6_ma_lich_lop,
            'g6_ma_lop_hoc': self.g6_ma_lop_hoc,
            'g6_ten_lop': self.g6_lop_hoc.g6_ten_lop if self.g6_lop_hoc else None,
            'g6_loai_lop': self.g6_lop_hoc.g6_loai_lop if self.g6_lop_hoc else None,
            'g6_ma_hlv': self.g6_ma_hlv,
            'g6_ten_hlv': self.g6_hlv.g6_nhan_vien.g6_ho_ten if self.g6_hlv and self.g6_hlv.g6_nhan_vien else None,
            'g6_thu_trong_tuan': self.g6_thu_trong_tuan,
            'g6_gio_bat_dau': str(self.g6_gio_bat_dau) if self.g6_gio_bat_dau else None,
            'g6_thoi_luong': self.g6_thoi_luong,
            'g6_suc_chua_toi_da': self.g6_suc_chua_toi_da,
            'g6_phong_tap': self.g6_phong_tap,
            'g6_ngay_ap_dung_tu': str(self.g6_ngay_ap_dung_tu) if self.g6_ngay_ap_dung_tu else None,
            'g6_ngay_ap_dung_den': str(self.g6_ngay_ap_dung_den) if self.g6_ngay_ap_dung_den else None,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
        }


class G6DatChoLopHoc(db.Model):
    __tablename__ = 'G6DatChoLopHoc'

    g6_ma_dat_cho = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_lich_lop = db.Column(db.Integer, db.ForeignKey('G6LichLopHoc.g6_ma_lich_lop'), nullable=False)
    g6_ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung'), nullable=False)
    g6_ngay_tap = db.Column(db.Date, nullable=False)
    g6_trang_thai = db.Column(db.String(20), nullable=False, default='dat_cho')  # 'dat_cho','da_den','vang_mat','da_huy'
    g6_thoi_gian_dat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_thoi_gian_huy = db.Column(db.DateTime)
    g6_ly_do_huy = db.Column(db.String(255))

    g6_lich_lop = db.relationship('G6LichLopHoc', back_populates='g6_dat_cho')

    def g6_to_dict(self):
        return {
            'g6_ma_dat_cho': self.g6_ma_dat_cho,
            'g6_ma_lich_lop': self.g6_ma_lich_lop,
            'g6_ma_nguoi_dung': self.g6_ma_nguoi_dung,
            'g6_ngay_tap': str(self.g6_ngay_tap) if self.g6_ngay_tap else None,
            'g6_trang_thai': self.g6_trang_thai,
            'g6_thoi_gian_dat': self.g6_thoi_gian_dat.isoformat() if self.g6_thoi_gian_dat else None,
            'g6_thoi_gian_huy': self.g6_thoi_gian_huy.isoformat() if self.g6_thoi_gian_huy else None,
            'g6_ly_do_huy': self.g6_ly_do_huy,
        }
