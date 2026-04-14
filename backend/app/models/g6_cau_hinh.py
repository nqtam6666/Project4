from backend.app import db
from datetime import datetime


class G6CauHinh(db.Model):
    __tablename__ = 'G6CauHinh'

    g6_ma_cau_hinh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_khoa = db.Column(db.String(100), nullable=False, unique=True)
    g6_gia_tri = db.Column(db.Text)
    g6_kieu_du_lieu = db.Column(db.String(20), nullable=False, default='string')
    g6_nhom = db.Column(db.String(50), nullable=False)
    g6_mo_ta = db.Column(db.String(255))
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False,
                                   default=datetime.utcnow, onupdate=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_cau_hinh': self.g6_ma_cau_hinh,
            'g6_khoa': self.g6_khoa,
            'g6_gia_tri': self.g6_gia_tri,
            'g6_kieu_du_lieu': self.g6_kieu_du_lieu,
            'g6_nhom': self.g6_nhom,
            'g6_mo_ta': self.g6_mo_ta,
            'g6_ngay_cap_nhat': self.g6_ngay_cap_nhat.isoformat() if self.g6_ngay_cap_nhat else None,
        }
