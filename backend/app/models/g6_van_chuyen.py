from backend.app import db
from datetime import datetime


class G6DonViVanChuyen(db.Model):
    __tablename__ = 'G6DonViVanChuyen'

    g6_ma_don_vi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten = db.Column(db.String(100), nullable=False)
    g6_ma = db.Column(db.String(20), nullable=False, unique=True)
    g6_logo = db.Column(db.String(500))
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    g6_vung = db.relationship('G6VungVanChuyen', back_populates='g6_don_vi', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_don_vi': self.g6_ma_don_vi,
            'g6_ten': self.g6_ten,
            'g6_ma': self.g6_ma,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
        }


class G6VungVanChuyen(db.Model):
    __tablename__ = 'G6VungVanChuyen'

    g6_ma_vung = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_don_vi = db.Column(db.Integer, db.ForeignKey('G6DonViVanChuyen.g6_ma_don_vi', ondelete='CASCADE'),
                               nullable=False)
    g6_tinh_thanh = db.Column(db.String(100), nullable=False)
    g6_phi_co_ban = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    g6_phi_theo_kg = db.Column(db.Numeric(10, 0), nullable=False, default=0)
    g6_mien_phi_tu = db.Column(db.Numeric(15, 0))
    g6_thoi_gian_du_kien = db.Column(db.String(50))

    g6_don_vi = db.relationship('G6DonViVanChuyen', back_populates='g6_vung')

    def g6_to_dict(self):
        return {
            'g6_ma_vung': self.g6_ma_vung,
            'g6_ma_don_vi': self.g6_ma_don_vi,
            'g6_tinh_thanh': self.g6_tinh_thanh,
            'g6_phi_co_ban': float(self.g6_phi_co_ban),
            'g6_mien_phi_tu': float(self.g6_mien_phi_tu) if self.g6_mien_phi_tu else None,
            'g6_thoi_gian_du_kien': self.g6_thoi_gian_du_kien,
        }
