from backend.app import db
from datetime import datetime


class NqtThongBao(db.Model):
    __tablename__ = 'NqtThongBao'

    nqt_ma_thong_bao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_tieu_de = db.Column(db.String(200), nullable=False)
    nqt_noi_dung = db.Column(db.Text, nullable=False)
    nqt_loai = db.Column(db.String(20), nullable=False, default='in_app')
    nqt_la_quang_ba = db.Column(db.Boolean, nullable=False, default=False)
    nqt_ma_nguoi_nhan = db.Column(db.Integer)
    nqt_loai_nguoi_nhan = db.Column(db.String(20))
    nqt_la_da_doc = db.Column(db.Boolean, nullable=False, default=False)
    nqt_du_lieu_them = db.Column(db.JSON)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def nqt_to_dict(self):
        return {
            'nqt_ma_thong_bao': self.nqt_ma_thong_bao,
            'nqt_tieu_de': self.nqt_tieu_de,
            'nqt_noi_dung': self.nqt_noi_dung,
            'nqt_loai': self.nqt_loai,
            'nqt_la_quang_ba': self.nqt_la_quang_ba,
            'nqt_la_da_doc': self.nqt_la_da_doc,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat(),
        }


class NqtLichGuiThongBao(db.Model):
    __tablename__ = 'NqtLichGuiThongBao'

    nqt_ma_lich = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ten = db.Column(db.String(200), nullable=False)
    nqt_loai_su_kien = db.Column(db.String(50), nullable=False)
    nqt_bieu_thuc_cron = db.Column(db.String(100))
    nqt_tieu_de_mau = db.Column(db.String(200), nullable=False)
    nqt_noi_dung_mau = db.Column(db.Text, nullable=False)
    nqt_kenh = db.Column(db.String(20), nullable=False, default='in_app')
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    nqt_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def nqt_to_dict(self):
        return {
            'nqt_ma_lich': self.nqt_ma_lich,
            'nqt_ten': self.nqt_ten,
            'nqt_loai_su_kien': self.nqt_loai_su_kien,
            'nqt_bieu_thuc_cron': self.nqt_bieu_thuc_cron,
            'nqt_tieu_de_mau': self.nqt_tieu_de_mau,
            'nqt_kenh': self.nqt_kenh,
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
        }
