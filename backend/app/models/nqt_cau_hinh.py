from backend.app import db
from datetime import datetime


class NqtCauHinh(db.Model):
    __tablename__ = 'NqtCauHinh'

    nqt_ma_cau_hinh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_khoa = db.Column(db.String(100), nullable=False, unique=True)
    nqt_gia_tri = db.Column(db.Text)
    nqt_kieu_du_lieu = db.Column(db.String(20), nullable=False, default='string')
    nqt_nhom = db.Column(db.String(50), nullable=False)
    nqt_mo_ta = db.Column(db.String(255))
    nqt_ngay_cap_nhat = db.Column(db.DateTime, nullable=False,
                                   default=datetime.utcnow, onupdate=datetime.utcnow)

    def nqt_to_dict(self):
        return {
            'nqt_ma_cau_hinh': self.nqt_ma_cau_hinh,
            'nqt_khoa': self.nqt_khoa,
            'nqt_gia_tri': self.nqt_gia_tri,
            'nqt_kieu_du_lieu': self.nqt_kieu_du_lieu,
            'nqt_nhom': self.nqt_nhom,
            'nqt_mo_ta': self.nqt_mo_ta,
            'nqt_ngay_cap_nhat': self.nqt_ngay_cap_nhat.isoformat() if self.nqt_ngay_cap_nhat else None,
        }
