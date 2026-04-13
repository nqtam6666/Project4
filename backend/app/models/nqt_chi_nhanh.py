from backend.app import db
from datetime import datetime


class NqtChiNhanh(db.Model):
    __tablename__ = 'NqtChiNhanh'

    nqt_ma_chi_nhanh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ten_chi_nhanh = db.Column(db.String(100), nullable=False)
    nqt_dia_chi = db.Column(db.String(255))
    nqt_thanh_pho = db.Column(db.String(50))
    nqt_tinh = db.Column(db.String(50))
    nqt_hotline = db.Column(db.String(15))
    nqt_email = db.Column(db.String(100))
    nqt_gio_mo_cua = db.Column(db.Time)
    nqt_gio_dong_cua = db.Column(db.Time)
    nqt_gio_mo_lich = db.Column(db.JSON)
    nqt_vi_do = db.Column(db.Numeric(9, 6))
    nqt_kinh_do = db.Column(db.Numeric(9, 6))
    nqt_google_maps_url = db.Column(db.String(500))
    nqt_hinh_anh = db.Column(db.JSON)
    nqt_suc_chua_toi_da = db.Column(db.Integer)
    nqt_co_sauna = db.Column(db.Boolean, nullable=False, default=False)
    nqt_co_ho_boi = db.Column(db.Boolean, nullable=False, default=False)
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    nqt_thiet_bi = db.relationship('NqtThietBi', back_populates='nqt_chi_nhanh', cascade='all, delete-orphan')

    def nqt_to_dict(self):
        return {
            'nqt_ma_chi_nhanh': self.nqt_ma_chi_nhanh,
            'nqt_ten_chi_nhanh': self.nqt_ten_chi_nhanh,
            'nqt_dia_chi': self.nqt_dia_chi,
            'nqt_thanh_pho': self.nqt_thanh_pho,
            'nqt_tinh': self.nqt_tinh,
            'nqt_hotline': self.nqt_hotline,
            'nqt_email': self.nqt_email,
            'nqt_gio_mo_cua': str(self.nqt_gio_mo_cua) if self.nqt_gio_mo_cua else None,
            'nqt_gio_dong_cua': str(self.nqt_gio_dong_cua) if self.nqt_gio_dong_cua else None,
            'nqt_suc_chua_toi_da': self.nqt_suc_chua_toi_da,
            'nqt_co_sauna': self.nqt_co_sauna,
            'nqt_co_ho_boi': self.nqt_co_ho_boi,
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
            'nqt_vi_do': float(self.nqt_vi_do) if self.nqt_vi_do else None,
            'nqt_kinh_do': float(self.nqt_kinh_do) if self.nqt_kinh_do else None,
        }


class NqtThietBi(db.Model):
    __tablename__ = 'NqtThietBi'

    nqt_ma_thiet_bi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('NqtChiNhanh.nqt_ma_chi_nhanh', ondelete='CASCADE'),
                                  nullable=False)
    nqt_ten_thiet_bi = db.Column(db.String(100), nullable=False)
    nqt_thuong_hieu = db.Column(db.String(100))
    nqt_model = db.Column(db.String(100))
    nqt_so_serie = db.Column(db.String(100))
    nqt_ngay_mua = db.Column(db.Date)
    nqt_ngay_bao_hanh_het = db.Column(db.Date)
    nqt_ngay_bao_tri_cuoi = db.Column(db.Date)
    nqt_ngay_bao_tri_tiep = db.Column(db.Date)
    nqt_trang_thai = db.Column(db.String(20), nullable=False, default='hoat_dong')
    nqt_hinh_anh = db.Column(db.String(500))
    nqt_ghi_chu = db.Column(db.Text)

    nqt_chi_nhanh = db.relationship('NqtChiNhanh', back_populates='nqt_thiet_bi')

    def nqt_to_dict(self):
        return {
            'nqt_ma_thiet_bi': self.nqt_ma_thiet_bi,
            'nqt_ma_chi_nhanh': self.nqt_ma_chi_nhanh,
            'nqt_ten_thiet_bi': self.nqt_ten_thiet_bi,
            'nqt_thuong_hieu': self.nqt_thuong_hieu,
            'nqt_model': self.nqt_model,
            'nqt_trang_thai': self.nqt_trang_thai,
            'nqt_ngay_bao_tri_tiep': str(self.nqt_ngay_bao_tri_tiep) if self.nqt_ngay_bao_tri_tiep else None,
        }
