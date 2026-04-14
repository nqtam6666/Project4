from backend.app import db
from datetime import datetime


class G6OtpXacThuc(db.Model):
    __tablename__ = 'G6OtpXacThuc'

    g6_ma_otp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('G6KhachHang.g6_ma_khach_hang', ondelete='CASCADE'))
    g6_dien_thoai_hoac_email = db.Column(db.String(100), nullable=False)
    g6_ma_otp_hash = db.Column(db.String(255), nullable=False)
    g6_muc_dich = db.Column(db.String(30), nullable=False)
    g6_het_han_luc = db.Column(db.DateTime, nullable=False)
    g6_so_lan_sai = db.Column(db.Integer, nullable=False, default=0)
    g6_la_da_dung = db.Column(db.Boolean, nullable=False, default=False)
    g6_dia_chi_ip = db.Column(db.String(45))
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_otp': self.g6_ma_otp,
            'g6_muc_dich': self.g6_muc_dich,
            'g6_het_han_luc': self.g6_het_han_luc.isoformat(),
            'g6_la_da_dung': self.g6_la_da_dung,
        }


class G6PhienDangNhap(db.Model):
    __tablename__ = 'G6PhienDangNhap'

    g6_ma_phien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_loai_nguoi_dung = db.Column(db.String(20), nullable=False)
    g6_ma_nguoi_dung = db.Column(db.Integer, nullable=False)
    g6_ma_refresh_token_hash = db.Column(db.String(255), nullable=False)
    g6_thiet_bi = db.Column(db.String(200))
    g6_dia_chi_ip = db.Column(db.String(45))
    g6_het_han_luc = db.Column(db.DateTime, nullable=False)
    g6_la_thu_hoi = db.Column(db.Boolean, nullable=False, default=False)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_phien': self.g6_ma_phien,
            'g6_loai_nguoi_dung': self.g6_loai_nguoi_dung,
            'g6_thiet_bi': self.g6_thiet_bi,
            'g6_dia_chi_ip': self.g6_dia_chi_ip,
            'g6_het_han_luc': self.g6_het_han_luc.isoformat(),
            'g6_la_thu_hoi': self.g6_la_thu_hoi,
        }


class G6NhatKyHoatDong(db.Model):
    __tablename__ = 'G6NhatKyHoatDong'

    g6_ma_nhat_ky = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_loai_nguoi_dung = db.Column(db.String(20))
    g6_ma_nguoi_dung = db.Column(db.Integer)
    g6_hanh_dong = db.Column(db.String(100), nullable=False)
    g6_ten_bang = db.Column(db.String(100))
    g6_ma_ban_ghi = db.Column(db.Integer)
    g6_du_lieu_cu = db.Column(db.JSON)
    g6_du_lieu_moi = db.Column(db.JSON)
    g6_dia_chi_ip = db.Column(db.String(45))
    g6_thiet_bi = db.Column(db.String(200))
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_nhat_ky': self.g6_ma_nhat_ky,
            'g6_loai_nguoi_dung': self.g6_loai_nguoi_dung,
            'g6_ma_nguoi_dung': self.g6_ma_nguoi_dung,
            'g6_hanh_dong': self.g6_hanh_dong,
            'g6_ten_bang': self.g6_ten_bang,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat(),
        }
