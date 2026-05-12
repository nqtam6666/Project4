from backend.app import db
from datetime import datetime


class G6DanhMucBaiViet(db.Model):
    __tablename__ = 'G6DanhMucBaiViet'

    g6_ma_danh_muc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten = db.Column(db.String(100), nullable=False)
    g6_slug = db.Column(db.String(120), nullable=False, unique=True)
    g6_ma_cha = db.Column(db.Integer, db.ForeignKey('G6DanhMucBaiViet.g6_ma_danh_muc'))
    g6_thu_tu = db.Column(db.Integer, nullable=False, default=0)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    g6_bai_viet = db.relationship('G6BaiViet', back_populates='g6_danh_muc')

    def g6_to_dict(self):
        return {
            'g6_ma_danh_muc': self.g6_ma_danh_muc,
            'g6_ten': self.g6_ten,
            'g6_slug': self.g6_slug,
            'g6_ma_cha': self.g6_ma_cha,
        }


class G6BaiViet(db.Model):
    __tablename__ = 'G6BaiViet'

    g6_ma_bai_viet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_danh_muc = db.Column(db.Integer, db.ForeignKey('G6DanhMucBaiViet.g6_ma_danh_muc', ondelete='SET NULL'))
    g6_tieu_de = db.Column(db.String(300), nullable=False)
    g6_slug = db.Column(db.String(350), nullable=False, unique=True)
    g6_mo_ta_ngan = db.Column(db.Text)
    g6_noi_dung = db.Column(db.Text)
    g6_hinh_dai_dien = db.Column(db.String(500))
    g6_tac_gia = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    g6_trang_thai = db.Column(db.String(20), nullable=False, default='nhap')
    g6_luot_xem = db.Column(db.Integer, nullable=False, default=0)
    g6_tu_khoa_seo = db.Column(db.String(255))
    g6_san_pham_lien_quan = db.Column(db.JSON)
    g6_ngay_xuat_ban = db.Column(db.DateTime)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    g6_danh_muc = db.relationship('G6DanhMucBaiViet', back_populates='g6_bai_viet')

    def g6_to_dict(self):
        return {
            'g6_ma_bai_viet': self.g6_ma_bai_viet,
            'g6_ma_danh_muc': self.g6_ma_danh_muc,
            'g6_tieu_de': self.g6_tieu_de,
            'g6_slug': self.g6_slug,
            'g6_mo_ta_ngan': self.g6_mo_ta_ngan,
            'g6_hinh_dai_dien': self.g6_hinh_dai_dien,
            'g6_trang_thai': self.g6_trang_thai,
            'g6_luot_xem': self.g6_luot_xem,
            'g6_ngay_xuat_ban': self.g6_ngay_xuat_ban.isoformat() if self.g6_ngay_xuat_ban else None,
        }


class G6DanhGiaSanPham(db.Model):
    __tablename__ = 'G6DanhGiaSanPham'

    g6_ma_danh_gia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_san_pham = db.Column(db.Integer, nullable=False)
    g6_ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    g6_sao = db.Column(db.SmallInteger, nullable=False)
    g6_noi_dung = db.Column(db.Text)
    g6_hinh_anh = db.Column(db.JSON)
    g6_trang_thai = db.Column(db.String(20), nullable=False, default='cho_duyet')
    g6_phan_hoi_cua_shop = db.Column(db.Text)
    g6_la_mua_hang_xac_nhan = db.Column(db.Boolean, nullable=False, default=False)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_danh_gia': self.g6_ma_danh_gia,
            'g6_ma_san_pham': self.g6_ma_san_pham,
            'g6_sao': self.g6_sao,
            'g6_noi_dung': self.g6_noi_dung,
            'g6_trang_thai': self.g6_trang_thai,
            'g6_la_mua_hang_xac_nhan': self.g6_la_mua_hang_xac_nhan,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat(),
        }
