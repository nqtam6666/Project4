from backend.app import db
from datetime import datetime


class G6MaGiamGia(db.Model):
    __tablename__ = 'G6MaGiamGia'

    g6_ma_ma_giam_gia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma = db.Column(db.String(50), nullable=False, unique=True)
    g6_loai = db.Column(db.String(20), nullable=False, default='phan_tram')
    g6_gia_tri = db.Column(db.Numeric(15, 0), nullable=False)
    g6_gia_tri_toi_da = db.Column(db.Numeric(15, 0))
    g6_don_hang_toi_thieu = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    g6_so_luong_tong = db.Column(db.Integer)
    g6_so_luong_da_dung = db.Column(db.Integer, nullable=False, default=0)
    g6_so_lan_moi_kh = db.Column(db.Integer, nullable=False, default=1)
    g6_ngay_bat_dau = db.Column(db.DateTime, nullable=False)
    g6_ngay_ket_thuc = db.Column(db.DateTime)
    g6_yeu_cau_hang = db.Column(db.Integer, db.ForeignKey('G6HangThanhVien.g6_ma_hang', ondelete='SET NULL'))
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_ma_giam_gia': self.g6_ma_ma_giam_gia,
            'g6_ma_id': self.g6_ma_ma_giam_gia,
            'g6_ma': self.g6_ma,
            'g6_ma_code': self.g6_ma,
            'g6_loai': self.g6_loai,
            'g6_loai_giam': self.g6_loai,
            'g6_gia_tri': float(self.g6_gia_tri),
            'g6_gia_tri_giam': float(self.g6_gia_tri),
            'g6_don_hang_toi_thieu': float(self.g6_don_hang_toi_thieu),
            'g6_so_luong_tong': self.g6_so_luong_tong,
            'g6_so_lan_su_dung_toi_da': self.g6_so_luong_tong,
            'g6_so_luong_da_dung': self.g6_so_luong_da_dung,
            'g6_so_lan_da_dung': self.g6_so_luong_da_dung,
            'g6_ngay_bat_dau': self.g6_ngay_bat_dau.isoformat() if self.g6_ngay_bat_dau else None,
            'g6_ngay_ket_thuc': self.g6_ngay_ket_thuc.isoformat() if self.g6_ngay_ket_thuc else None,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
        }


class G6KhuyenMaiMuaKem(db.Model):
    __tablename__ = 'G6KhuyenMaiMuaKem'

    g6_ma_khuyen_mai = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten = db.Column(db.String(200), nullable=False)
    g6_ma_san_pham_chinh = db.Column(db.Integer, nullable=False)
    g6_so_luong_mua = db.Column(db.Integer, nullable=False, default=1)
    g6_ma_san_pham_tang = db.Column(db.Integer)
    g6_so_luong_tang = db.Column(db.Integer, nullable=False, default=1)
    g6_phan_tram_giam = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    g6_ngay_bat_dau = db.Column(db.DateTime, nullable=False)
    g6_ngay_ket_thuc = db.Column(db.DateTime)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    def g6_to_dict(self):
        return {
            'g6_ma_khuyen_mai': self.g6_ma_khuyen_mai,
            'g6_ma_id': self.g6_ma_khuyen_mai,
            'g6_ten': self.g6_ten,
            'g6_ma_san_pham_chinh': self.g6_ma_san_pham_chinh,
            'g6_phan_tram_giam': float(self.g6_phan_tram_giam),
            'g6_dieu_kien': f'Mua {self.g6_so_luong_mua} sản phẩm #{self.g6_ma_san_pham_chinh}',
            'g6_qua_tang': f'Tặng {self.g6_so_luong_tang} sản phẩm, giảm {self.g6_phan_tram_giam}%',
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
        }


class G6Banner(db.Model):
    __tablename__ = 'G6Banner'

    g6_ma_banner = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_tieu_de = db.Column(db.String(200))
    g6_hinh_anh = db.Column(db.String(500), nullable=False)
    g6_duong_dan = db.Column(db.String(500))
    g6_vi_tri = db.Column(db.String(30), nullable=False, default='slider')
    g6_thu_tu = db.Column(db.Integer, nullable=False, default=0)
    g6_ngay_bat_dau = db.Column(db.DateTime)
    g6_ngay_ket_thuc = db.Column(db.DateTime)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    def g6_to_dict(self):
        return {
            'g6_ma_banner': self.g6_ma_banner,
            'g6_ma_id': self.g6_ma_banner,
            'g6_tieu_de': self.g6_tieu_de,
            'g6_hinh_anh': self.g6_hinh_anh,
            'g6_duong_dan': self.g6_duong_dan,
            'g6_vi_tri': self.g6_vi_tri,
            'g6_thu_tu': self.g6_thu_tu,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
        }
