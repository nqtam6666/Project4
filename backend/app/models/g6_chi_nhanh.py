from backend.app import db
from datetime import datetime


class G6ChiNhanh(db.Model):
    __tablename__ = 'G6ChiNhanh'

    g6_ma_chi_nhanh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten_chi_nhanh = db.Column(db.String(100), nullable=False)
    g6_dia_chi = db.Column(db.String(255))
    g6_thanh_pho = db.Column(db.String(50))
    g6_tinh = db.Column(db.String(50))
    g6_hotline = db.Column(db.String(15))
    g6_email = db.Column(db.String(100))
    g6_gio_mo_cua = db.Column(db.Time)
    g6_gio_dong_cua = db.Column(db.Time)
    g6_gio_mo_lich = db.Column(db.JSON)
    g6_vi_do = db.Column(db.Numeric(9, 6))
    g6_kinh_do = db.Column(db.Numeric(9, 6))
    g6_google_maps_url = db.Column(db.String(500))
    g6_hinh_anh = db.Column(db.JSON)
    g6_suc_chua_toi_da = db.Column(db.Integer)
    g6_co_sauna = db.Column(db.Boolean, nullable=False, default=False)
    g6_co_ho_boi = db.Column(db.Boolean, nullable=False, default=False)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_thiet_bi = db.relationship('G6ThietBi', back_populates='g6_chi_nhanh', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_ten_chi_nhanh': self.g6_ten_chi_nhanh,
            'g6_dia_chi': self.g6_dia_chi,
            'g6_thanh_pho': self.g6_thanh_pho,
            'g6_tinh': self.g6_tinh,
            'g6_hotline': self.g6_hotline,
            'g6_email': self.g6_email,
            'g6_gio_mo_cua': str(self.g6_gio_mo_cua) if self.g6_gio_mo_cua else None,
            'g6_gio_dong_cua': str(self.g6_gio_dong_cua) if self.g6_gio_dong_cua else None,
            'g6_suc_chua_toi_da': self.g6_suc_chua_toi_da,
            'g6_co_sauna': self.g6_co_sauna,
            'g6_co_ho_boi': self.g6_co_ho_boi,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
            'g6_vi_do': float(self.g6_vi_do) if self.g6_vi_do else None,
            'g6_kinh_do': float(self.g6_kinh_do) if self.g6_kinh_do else None,
        }


class G6ThietBi(db.Model):
    __tablename__ = 'G6ThietBi'

    g6_ma_thiet_bi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh', ondelete='CASCADE'),
                                  nullable=False)
    g6_ten_thiet_bi = db.Column(db.String(100), nullable=False)
    g6_thuong_hieu = db.Column(db.String(100))
    g6_model = db.Column(db.String(100))
    g6_so_serie = db.Column(db.String(100))
    g6_ngay_mua = db.Column(db.Date)
    g6_ngay_bao_hanh_het = db.Column(db.Date)
    g6_ngay_bao_tri_cuoi = db.Column(db.Date)
    g6_ngay_bao_tri_tiep = db.Column(db.Date)
    g6_trang_thai = db.Column(db.String(20), nullable=False, default='hoat_dong')
    g6_hinh_anh = db.Column(db.String(500))
    g6_ghi_chu = db.Column(db.Text)

    g6_chi_nhanh = db.relationship('G6ChiNhanh', back_populates='g6_thiet_bi')

    def g6_to_dict(self):
        return {
            'g6_ma_thiet_bi': self.g6_ma_thiet_bi,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_ten_thiet_bi': self.g6_ten_thiet_bi,
            'g6_thuong_hieu': self.g6_thuong_hieu,
            'g6_model': self.g6_model,
            'g6_trang_thai': self.g6_trang_thai,
            'g6_ngay_bao_tri_tiep': str(self.g6_ngay_bao_tri_tiep) if self.g6_ngay_bao_tri_tiep else None,
        }
