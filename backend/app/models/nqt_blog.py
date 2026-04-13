from backend.app import db
from datetime import datetime


class NqtDanhMucBaiViet(db.Model):
    __tablename__ = 'NqtDanhMucBaiViet'

    nqt_ma_danh_muc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ten = db.Column(db.String(100), nullable=False)
    nqt_slug = db.Column(db.String(120), nullable=False, unique=True)
    nqt_ma_cha = db.Column(db.Integer, db.ForeignKey('NqtDanhMucBaiViet.nqt_ma_danh_muc', ondelete='SET NULL'))
    nqt_thu_tu = db.Column(db.Integer, nullable=False, default=0)
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    nqt_bai_viet = db.relationship('NqtBaiViet', back_populates='nqt_danh_muc')

    def nqt_to_dict(self):
        return {
            'nqt_ma_danh_muc': self.nqt_ma_danh_muc,
            'nqt_ten': self.nqt_ten,
            'nqt_slug': self.nqt_slug,
            'nqt_ma_cha': self.nqt_ma_cha,
        }


class NqtBaiViet(db.Model):
    __tablename__ = 'NqtBaiViet'

    nqt_ma_bai_viet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_danh_muc = db.Column(db.Integer, db.ForeignKey('NqtDanhMucBaiViet.nqt_ma_danh_muc', ondelete='SET NULL'))
    nqt_tieu_de = db.Column(db.String(300), nullable=False)
    nqt_slug = db.Column(db.String(350), nullable=False, unique=True)
    nqt_mo_ta_ngan = db.Column(db.Text)
    nqt_noi_dung = db.Column(db.Text)
    nqt_hinh_dai_dien = db.Column(db.String(500))
    nqt_tac_gia = db.Column(db.Integer, db.ForeignKey('NqtNguoiDung.nqt_ma_nguoi_dung', ondelete='SET NULL'))
    nqt_trang_thai = db.Column(db.String(20), nullable=False, default='nhap')
    nqt_luot_xem = db.Column(db.Integer, nullable=False, default=0)
    nqt_tu_khoa_seo = db.Column(db.String(255))
    nqt_san_pham_lien_quan = db.Column(db.JSON)
    nqt_ngay_xuat_ban = db.Column(db.DateTime)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nqt_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    nqt_danh_muc = db.relationship('NqtDanhMucBaiViet', back_populates='nqt_bai_viet')

    def nqt_to_dict(self):
        return {
            'nqt_ma_bai_viet': self.nqt_ma_bai_viet,
            'nqt_ma_danh_muc': self.nqt_ma_danh_muc,
            'nqt_tieu_de': self.nqt_tieu_de,
            'nqt_slug': self.nqt_slug,
            'nqt_mo_ta_ngan': self.nqt_mo_ta_ngan,
            'nqt_hinh_dai_dien': self.nqt_hinh_dai_dien,
            'nqt_trang_thai': self.nqt_trang_thai,
            'nqt_luot_xem': self.nqt_luot_xem,
            'nqt_ngay_xuat_ban': self.nqt_ngay_xuat_ban.isoformat() if self.nqt_ngay_xuat_ban else None,
        }


class NqtDanhGiaSanPham(db.Model):
    __tablename__ = 'NqtDanhGiaSanPham'

    nqt_ma_danh_gia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_san_pham = db.Column(db.Integer, nullable=False)
    nqt_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('NqtKhachHang.nqt_ma_khach_hang', ondelete='SET NULL'))
    nqt_sao = db.Column(db.SmallInteger, nullable=False)
    nqt_noi_dung = db.Column(db.Text)
    nqt_hinh_anh = db.Column(db.JSON)
    nqt_trang_thai = db.Column(db.String(20), nullable=False, default='cho_duyet')
    nqt_phan_hoi_cua_shop = db.Column(db.Text)
    nqt_la_mua_hang_xac_nhan = db.Column(db.Boolean, nullable=False, default=False)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def nqt_to_dict(self):
        return {
            'nqt_ma_danh_gia': self.nqt_ma_danh_gia,
            'nqt_ma_san_pham': self.nqt_ma_san_pham,
            'nqt_sao': self.nqt_sao,
            'nqt_noi_dung': self.nqt_noi_dung,
            'nqt_trang_thai': self.nqt_trang_thai,
            'nqt_la_mua_hang_xac_nhan': self.nqt_la_mua_hang_xac_nhan,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat(),
        }
