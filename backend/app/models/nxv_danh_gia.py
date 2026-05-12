from backend.app import db
from datetime import datetime


class NxvDanhGiaHLV(db.Model):
    __tablename__ = 'NxvDanhGiaHLV'

    nxv_ma_danh_gia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nxv_ma_hlv = db.Column(db.Integer, db.ForeignKey('G6HuanLuyenVien.g6_ma_hlv', ondelete='CASCADE'), nullable=False)
    nxv_ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    nxv_ma_dang_ky_pt = db.Column(db.Integer, db.ForeignKey('G6DangKyGoiPT.g6_ma_dang_ky_pt', ondelete='SET NULL'))
    nxv_sao = db.Column(db.SmallInteger, nullable=False)
    nxv_noi_dung = db.Column(db.Text)
    nxv_phan_hoi_hlv = db.Column(db.Text)
    nxv_trang_thai = db.Column(db.String(20), nullable=False, default='cho_duyet')
    nxv_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    def nxv_to_dict(self):
        return {
            'nxv_ma_danh_gia': self.nxv_ma_danh_gia,
            'nxv_ma_hlv': self.nxv_ma_hlv,
            'nxv_ma_nguoi_dung': self.nxv_ma_nguoi_dung,
            'nxv_ma_dang_ky_pt': self.nxv_ma_dang_ky_pt,
            'nxv_sao': self.nxv_sao,
            'nxv_noi_dung': self.nxv_noi_dung,
            'nxv_phan_hoi_hlv': self.nxv_phan_hoi_hlv,
            'nxv_trang_thai': self.nxv_trang_thai,
            'nxv_ngay_tao': self.nxv_ngay_tao.isoformat() if self.nxv_ngay_tao else None,
        }


class NxvDanhGiaLopHoc(db.Model):
    __tablename__ = 'NxvDanhGiaLopHoc'

    nxv_ma_danh_gia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nxv_ma_lop_hoc = db.Column(db.Integer, db.ForeignKey('G6LopHoc.g6_ma_lop_hoc', ondelete='CASCADE'), nullable=False)
    nxv_ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    nxv_ma_dat_cho = db.Column(db.Integer, db.ForeignKey('G6DatChoLopHoc.g6_ma_dat_cho', ondelete='SET NULL'))
    nxv_sao = db.Column(db.SmallInteger, nullable=False)
    nxv_noi_dung = db.Column(db.Text)
    nxv_phan_hoi_hlv = db.Column(db.Text)
    nxv_trang_thai = db.Column(db.String(20), nullable=False, default='cho_duyet')
    nxv_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    def nxv_to_dict(self):
        return {
            'nxv_ma_danh_gia': self.nxv_ma_danh_gia,
            'nxv_ma_lop_hoc': self.nxv_ma_lop_hoc,
            'nxv_ma_nguoi_dung': self.nxv_ma_nguoi_dung,
            'nxv_ma_dat_cho': self.nxv_ma_dat_cho,
            'nxv_sao': self.nxv_sao,
            'nxv_noi_dung': self.nxv_noi_dung,
            'nxv_phan_hoi_hlv': self.nxv_phan_hoi_hlv,
            'nxv_trang_thai': self.nxv_trang_thai,
            'nxv_ngay_tao': self.nxv_ngay_tao.isoformat() if self.nxv_ngay_tao else None,
        }
