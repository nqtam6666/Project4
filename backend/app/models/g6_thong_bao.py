from backend.app import db
from datetime import datetime


class G6ThongBao(db.Model):
    __tablename__ = 'G6ThongBao'

    g6_ma_thong_bao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_tieu_de = db.Column(db.String(200), nullable=False)
    g6_noi_dung = db.Column(db.Text, nullable=False)
    g6_loai = db.Column(db.String(20), nullable=False, default='in_app')
    g6_la_quang_ba = db.Column(db.Boolean, nullable=False, default=False)
    g6_ma_nguoi_nhan = db.Column(db.Integer)
    g6_loai_nguoi_nhan = db.Column(db.String(20))
    g6_la_da_doc = db.Column(db.Boolean, nullable=False, default=False)
    g6_du_lieu_them = db.Column(db.JSON)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_thong_bao': self.g6_ma_thong_bao,
            'g6_tieu_de': self.g6_tieu_de,
            'g6_noi_dung': self.g6_noi_dung,
            'g6_loai': self.g6_loai,
            'g6_la_quang_ba': self.g6_la_quang_ba,
            'g6_la_da_doc': self.g6_la_da_doc,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat(),
        }


class G6LichGuiThongBao(db.Model):
    __tablename__ = 'G6LichGuiThongBao'

    g6_ma_lich = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten = db.Column(db.String(200), nullable=False)
    g6_loai_su_kien = db.Column(db.String(50), nullable=False)
    g6_bieu_thuc_cron = db.Column(db.String(100))
    g6_tieu_de_mau = db.Column(db.String(200), nullable=False)
    g6_noi_dung_mau = db.Column(db.Text, nullable=False)
    g6_kenh = db.Column(db.String(20), nullable=False, default='in_app')
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_lich': self.g6_ma_lich,
            'g6_ten': self.g6_ten,
            'g6_loai_su_kien': self.g6_loai_su_kien,
            'g6_bieu_thuc_cron': self.g6_bieu_thuc_cron,
            'g6_tieu_de_mau': self.g6_tieu_de_mau,
            'g6_kenh': self.g6_kenh,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
        }
