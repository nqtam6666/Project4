from backend.app import db
from datetime import datetime


class NxvChuongTrinhTapLuyen(db.Model):
    __tablename__ = 'NxvChuongTrinhTapLuyen'

    nxv_ma_chuong_trinh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nxv_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('G6HoiVien.g6_ma_hoi_vien', ondelete='CASCADE'), nullable=False)
    nxv_ma_hlv = db.Column(db.Integer, db.ForeignKey('G6HuanLuyenVien.g6_ma_hlv', ondelete='SET NULL'))
    nxv_ten = db.Column(db.String(200), nullable=False)
    nxv_muc_tieu = db.Column(db.String(100))
    nxv_so_tuan = db.Column(db.Integer, nullable=False, default=4)
    nxv_ngay_bat_dau = db.Column(db.Date, nullable=False)
    nxv_ngay_ket_thuc = db.Column(db.Date)
    nxv_ghi_chu = db.Column(db.Text)
    nxv_trang_thai = db.Column(db.String(20), nullable=False, default='dang_thuc_hien')
    nxv_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    nxv_bai_tap = db.relationship('NxvBaiTapTrongNgay', back_populates='nxv_chuong_trinh', cascade='all, delete-orphan')

    def nxv_to_dict(self):
        return {
            'nxv_ma_chuong_trinh': self.nxv_ma_chuong_trinh,
            'nxv_ma_hoi_vien': self.nxv_ma_hoi_vien,
            'nxv_ma_hlv': self.nxv_ma_hlv,
            'nxv_ten': self.nxv_ten,
            'nxv_muc_tieu': self.nxv_muc_tieu,
            'nxv_so_tuan': self.nxv_so_tuan,
            'nxv_ngay_bat_dau': str(self.nxv_ngay_bat_dau) if self.nxv_ngay_bat_dau else None,
            'nxv_ngay_ket_thuc': str(self.nxv_ngay_ket_thuc) if self.nxv_ngay_ket_thuc else None,
            'nxv_trang_thai': self.nxv_trang_thai,
            'nxv_ngay_tao': self.nxv_ngay_tao.isoformat() if self.nxv_ngay_tao else None,
        }


class NxvBaiTapTrongNgay(db.Model):
    __tablename__ = 'NxvBaiTapTrongNgay'

    nxv_ma_bai_tap = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nxv_ma_chuong_trinh = db.Column(db.Integer, db.ForeignKey('NxvChuongTrinhTapLuyen.nxv_ma_chuong_trinh', ondelete='CASCADE'), nullable=False)
    nxv_tuan = db.Column(db.Integer, nullable=False)
    nxv_ngay_trong_tuan = db.Column(db.Integer, nullable=False)  # 1=Thứ 2 ... 7=Chủ nhật
    nxv_ten_bai_tap = db.Column(db.String(200), nullable=False)
    nxv_nhom_co = db.Column(db.String(100))
    nxv_so_hieu = db.Column(db.Integer)
    nxv_so_set = db.Column(db.Integer)
    nxv_so_rep = db.Column(db.Integer)
    nxv_trong_luong_kg = db.Column(db.Numeric(6, 2))
    nxv_thoi_gian_nghi_giay = db.Column(db.Integer)
    nxv_ghi_chu = db.Column(db.Text)
    nxv_la_hoan_thanh = db.Column(db.Boolean, nullable=False, default=False)
    g6_deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    nxv_chuong_trinh = db.relationship('NxvChuongTrinhTapLuyen', back_populates='nxv_bai_tap')

    def nxv_to_dict(self):
        return {
            'nxv_ma_bai_tap': self.nxv_ma_bai_tap,
            'nxv_ma_chuong_trinh': self.nxv_ma_chuong_trinh,
            'nxv_tuan': self.nxv_tuan,
            'nxv_ngay_trong_tuan': self.nxv_ngay_trong_tuan,
            'nxv_ten_bai_tap': self.nxv_ten_bai_tap,
            'nxv_nhom_co': self.nxv_nhom_co,
            'nxv_so_hieu': self.nxv_so_hieu,
            'nxv_so_set': self.nxv_so_set,
            'nxv_so_rep': self.nxv_so_rep,
            'nxv_trong_luong_kg': float(self.nxv_trong_luong_kg) if self.nxv_trong_luong_kg else None,
            'nxv_thoi_gian_nghi_giay': self.nxv_thoi_gian_nghi_giay,
            'nxv_la_hoan_thanh': self.nxv_la_hoan_thanh,
        }
