from backend.app import db
from datetime import datetime


class NqtOtpXacThuc(db.Model):
    __tablename__ = 'NqtOtpXacThuc'

    nqt_ma_otp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('NqtKhachHang.nqt_ma_khach_hang', ondelete='CASCADE'))
    nqt_dien_thoai_hoac_email = db.Column(db.String(100), nullable=False)
    nqt_ma_otp_hash = db.Column(db.String(255), nullable=False)
    nqt_muc_dich = db.Column(db.String(30), nullable=False)
    nqt_het_han_luc = db.Column(db.DateTime, nullable=False)
    nqt_so_lan_sai = db.Column(db.Integer, nullable=False, default=0)
    nqt_la_da_dung = db.Column(db.Boolean, nullable=False, default=False)
    nqt_dia_chi_ip = db.Column(db.String(45))
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def nqt_to_dict(self):
        return {
            'nqt_ma_otp': self.nqt_ma_otp,
            'nqt_muc_dich': self.nqt_muc_dich,
            'nqt_het_han_luc': self.nqt_het_han_luc.isoformat(),
            'nqt_la_da_dung': self.nqt_la_da_dung,
        }


class NqtPhienDangNhap(db.Model):
    __tablename__ = 'NqtPhienDangNhap'

    nqt_ma_phien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_loai_nguoi_dung = db.Column(db.String(20), nullable=False)
    nqt_ma_nguoi_dung = db.Column(db.Integer, nullable=False)
    nqt_ma_refresh_token_hash = db.Column(db.String(255), nullable=False)
    nqt_thiet_bi = db.Column(db.String(200))
    nqt_dia_chi_ip = db.Column(db.String(45))
    nqt_het_han_luc = db.Column(db.DateTime, nullable=False)
    nqt_la_thu_hoi = db.Column(db.Boolean, nullable=False, default=False)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def nqt_to_dict(self):
        return {
            'nqt_ma_phien': self.nqt_ma_phien,
            'nqt_loai_nguoi_dung': self.nqt_loai_nguoi_dung,
            'nqt_thiet_bi': self.nqt_thiet_bi,
            'nqt_dia_chi_ip': self.nqt_dia_chi_ip,
            'nqt_het_han_luc': self.nqt_het_han_luc.isoformat(),
            'nqt_la_thu_hoi': self.nqt_la_thu_hoi,
        }


class NqtNhatKyHoatDong(db.Model):
    __tablename__ = 'NqtNhatKyHoatDong'

    nqt_ma_nhat_ky = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_loai_nguoi_dung = db.Column(db.String(20))
    nqt_ma_nguoi_dung = db.Column(db.Integer)
    nqt_hanh_dong = db.Column(db.String(100), nullable=False)
    nqt_ten_bang = db.Column(db.String(100))
    nqt_ma_ban_ghi = db.Column(db.Integer)
    nqt_du_lieu_cu = db.Column(db.JSON)
    nqt_du_lieu_moi = db.Column(db.JSON)
    nqt_dia_chi_ip = db.Column(db.String(45))
    nqt_thiet_bi = db.Column(db.String(200))
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def nqt_to_dict(self):
        return {
            'nqt_ma_nhat_ky': self.nqt_ma_nhat_ky,
            'nqt_loai_nguoi_dung': self.nqt_loai_nguoi_dung,
            'nqt_ma_nguoi_dung': self.nqt_ma_nguoi_dung,
            'nqt_hanh_dong': self.nqt_hanh_dong,
            'nqt_ten_bang': self.nqt_ten_bang,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat(),
        }
