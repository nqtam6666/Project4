from backend.app import db
from datetime import datetime


class NqtMaGiamGia(db.Model):
    __tablename__ = 'NqtMaGiamGia'

    nqt_ma_ma_giam_gia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma = db.Column(db.String(50), nullable=False, unique=True)
    nqt_loai = db.Column(db.String(20), nullable=False, default='phan_tram')
    nqt_gia_tri = db.Column(db.Numeric(15, 0), nullable=False)
    nqt_gia_tri_toi_da = db.Column(db.Numeric(15, 0))
    nqt_don_hang_toi_thieu = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    nqt_so_luong_tong = db.Column(db.Integer)
    nqt_so_luong_da_dung = db.Column(db.Integer, nullable=False, default=0)
    nqt_so_lan_moi_kh = db.Column(db.Integer, nullable=False, default=1)
    nqt_ngay_bat_dau = db.Column(db.DateTime, nullable=False)
    nqt_ngay_ket_thuc = db.Column(db.DateTime)
    nqt_yeu_cau_hang = db.Column(db.Integer, db.ForeignKey('NqtHangThanhVien.nqt_ma_hang', ondelete='SET NULL'))
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def nqt_to_dict(self):
        return {
            'nqt_ma_ma_giam_gia': self.nqt_ma_ma_giam_gia,
            'nqt_ma': self.nqt_ma,
            'nqt_loai': self.nqt_loai,
            'nqt_gia_tri': float(self.nqt_gia_tri),
            'nqt_don_hang_toi_thieu': float(self.nqt_don_hang_toi_thieu),
            'nqt_ngay_bat_dau': self.nqt_ngay_bat_dau.isoformat() if self.nqt_ngay_bat_dau else None,
            'nqt_ngay_ket_thuc': self.nqt_ngay_ket_thuc.isoformat() if self.nqt_ngay_ket_thuc else None,
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
        }


class NqtKhuyenMaiMuaKem(db.Model):
    __tablename__ = 'NqtKhuyenMaiMuaKem'

    nqt_ma_khuyen_mai = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ten = db.Column(db.String(200), nullable=False)
    nqt_ma_san_pham_chinh = db.Column(db.Integer, nullable=False)
    nqt_so_luong_mua = db.Column(db.Integer, nullable=False, default=1)
    nqt_ma_san_pham_tang = db.Column(db.Integer)
    nqt_so_luong_tang = db.Column(db.Integer, nullable=False, default=1)
    nqt_phan_tram_giam = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    nqt_ngay_bat_dau = db.Column(db.DateTime, nullable=False)
    nqt_ngay_ket_thuc = db.Column(db.DateTime)
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    def nqt_to_dict(self):
        return {
            'nqt_ma_khuyen_mai': self.nqt_ma_khuyen_mai,
            'nqt_ten': self.nqt_ten,
            'nqt_ma_san_pham_chinh': self.nqt_ma_san_pham_chinh,
            'nqt_phan_tram_giam': float(self.nqt_phan_tram_giam),
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
        }


class NqtBanner(db.Model):
    __tablename__ = 'NqtBanner'

    nqt_ma_banner = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_tieu_de = db.Column(db.String(200))
    nqt_hinh_anh = db.Column(db.String(500), nullable=False)
    nqt_duong_dan = db.Column(db.String(500))
    nqt_vi_tri = db.Column(db.String(30), nullable=False, default='slider')
    nqt_thu_tu = db.Column(db.Integer, nullable=False, default=0)
    nqt_ngay_bat_dau = db.Column(db.DateTime)
    nqt_ngay_ket_thuc = db.Column(db.DateTime)
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    def nqt_to_dict(self):
        return {
            'nqt_ma_banner': self.nqt_ma_banner,
            'nqt_tieu_de': self.nqt_tieu_de,
            'nqt_hinh_anh': self.nqt_hinh_anh,
            'nqt_duong_dan': self.nqt_duong_dan,
            'nqt_vi_tri': self.nqt_vi_tri,
            'nqt_thu_tu': self.nqt_thu_tu,
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
        }
