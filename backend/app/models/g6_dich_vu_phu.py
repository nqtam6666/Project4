from backend.app import db
from datetime import datetime


class G6DichVuPhu(db.Model):
    __tablename__ = 'G6DichVuPhu'

    g6_ma_dich_vu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh'), nullable=False)
    g6_ten_dich_vu = db.Column(db.String(100), nullable=False)  # 'Sauna','Hồ bơi','Massage'
    g6_loai_dich_vu = db.Column(db.String(50), nullable=False)
    g6_mo_ta = db.Column(db.Text)
    g6_gia_theo_luot = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    g6_thoi_luong_phut = db.Column(db.Integer, nullable=False, default=60)
    g6_suc_chua = db.Column(db.Integer)
    g6_la_mien_phi_goi = db.Column(db.Boolean, nullable=False, default=False)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    g6_chi_nhanh = db.relationship('G6ChiNhanh', foreign_keys=[g6_ma_chi_nhanh])
    g6_dat_dich_vu = db.relationship('G6DatDichVu', back_populates='g6_dich_vu', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_dich_vu': self.g6_ma_dich_vu,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_ten_dich_vu': self.g6_ten_dich_vu,
            'g6_loai_dich_vu': self.g6_loai_dich_vu,
            'g6_mo_ta': self.g6_mo_ta,
            'g6_gia_theo_luot': float(self.g6_gia_theo_luot),
            'g6_thoi_luong_phut': self.g6_thoi_luong_phut,
            'g6_suc_chua': self.g6_suc_chua,
            'g6_la_mien_phi_goi': self.g6_la_mien_phi_goi,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
        }


class G6DatDichVu(db.Model):
    __tablename__ = 'G6DatDichVu'

    g6_ma_dat_dich_vu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_dich_vu = db.Column(db.Integer, db.ForeignKey('G6DichVuPhu.g6_ma_dich_vu'), nullable=False)
    g6_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('G6HoiVien.g6_ma_hoi_vien'), nullable=False)
    g6_thoi_gian_bat_dau = db.Column(db.DateTime, nullable=False)
    g6_thoi_gian_ket_thuc = db.Column(db.DateTime, nullable=False)
    g6_trang_thai = db.Column(db.String(20), nullable=False, default='da_dat')  # 'da_dat','da_dung','da_huy'
    g6_la_mien_phi = db.Column(db.Boolean, nullable=False, default=False)
    g6_ma_thanh_toan = db.Column(db.Integer, db.ForeignKey('G6ThanhToan.g6_ma_thanh_toan', ondelete='SET NULL'))
    g6_ghi_chu = db.Column(db.String(255))
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_dich_vu = db.relationship('G6DichVuPhu', back_populates='g6_dat_dich_vu')

    def g6_to_dict(self):
        return {
            'g6_ma_dat_dich_vu': self.g6_ma_dat_dich_vu,
            'g6_ma_dich_vu': self.g6_ma_dich_vu,
            'g6_ma_hoi_vien': self.g6_ma_hoi_vien,
            'g6_thoi_gian_bat_dau': self.g6_thoi_gian_bat_dau.isoformat() if self.g6_thoi_gian_bat_dau else None,
            'g6_thoi_gian_ket_thuc': self.g6_thoi_gian_ket_thuc.isoformat() if self.g6_thoi_gian_ket_thuc else None,
            'g6_trang_thai': self.g6_trang_thai,
            'g6_la_mien_phi': self.g6_la_mien_phi,
            'g6_ghi_chu': self.g6_ghi_chu,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat() if self.g6_ngay_tao else None,
        }
