from backend.app import db
from datetime import datetime


class NqtDonViVanChuyen(db.Model):
    __tablename__ = 'NqtDonViVanChuyen'

    nqt_ma_don_vi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ten = db.Column(db.String(100), nullable=False)
    nqt_ma = db.Column(db.String(20), nullable=False, unique=True)
    nqt_logo = db.Column(db.String(500))
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    nqt_vung = db.relationship('NqtVungVanChuyen', back_populates='nqt_don_vi', cascade='all, delete-orphan')

    def nqt_to_dict(self):
        return {
            'nqt_ma_don_vi': self.nqt_ma_don_vi,
            'nqt_ten': self.nqt_ten,
            'nqt_ma': self.nqt_ma,
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
        }


class NqtVungVanChuyen(db.Model):
    __tablename__ = 'NqtVungVanChuyen'

    nqt_ma_vung = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_don_vi = db.Column(db.Integer, db.ForeignKey('NqtDonViVanChuyen.nqt_ma_don_vi', ondelete='CASCADE'),
                               nullable=False)
    nqt_tinh_thanh = db.Column(db.String(100), nullable=False)
    nqt_phi_co_ban = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    nqt_phi_theo_kg = db.Column(db.Numeric(10, 0), nullable=False, default=0)
    nqt_mien_phi_tu = db.Column(db.Numeric(15, 0))
    nqt_thoi_gian_du_kien = db.Column(db.String(50))

    nqt_don_vi = db.relationship('NqtDonViVanChuyen', back_populates='nqt_vung')

    def nqt_to_dict(self):
        return {
            'nqt_ma_vung': self.nqt_ma_vung,
            'nqt_ma_don_vi': self.nqt_ma_don_vi,
            'nqt_tinh_thanh': self.nqt_tinh_thanh,
            'nqt_phi_co_ban': float(self.nqt_phi_co_ban),
            'nqt_mien_phi_tu': float(self.nqt_mien_phi_tu) if self.nqt_mien_phi_tu else None,
            'nqt_thoi_gian_du_kien': self.nqt_thoi_gian_du_kien,
        }
