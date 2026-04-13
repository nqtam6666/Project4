from backend.app import db
from datetime import datetime


class NqtVaiTro(db.Model):
    __tablename__ = 'NqtVaiTro'

    nqt_ma_vai_tro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ten_vai_tro = db.Column(db.String(50), nullable=False)
    nqt_mo_ta = db.Column(db.String(255))

    nqt_nguoi_dung = db.relationship('NqtNguoiDungVaiTro', back_populates='nqt_vai_tro', cascade='all, delete-orphan')
    nqt_quyen = db.relationship('NqtVaiTroQuyen', back_populates='nqt_vai_tro', cascade='all, delete-orphan')

    def nqt_to_dict(self):
        return {
            'nqt_ma_vai_tro': self.nqt_ma_vai_tro,
            'nqt_ten_vai_tro': self.nqt_ten_vai_tro,
            'nqt_mo_ta': self.nqt_mo_ta,
        }


class NqtQuyenHan(db.Model):
    __tablename__ = 'NqtQuyenHan'

    nqt_ma_quyen = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ten_quyen = db.Column(db.String(100), nullable=False)
    nqt_nhom_quyen = db.Column(db.String(50), nullable=False)

    nqt_vai_tro = db.relationship('NqtVaiTroQuyen', back_populates='nqt_quyen', cascade='all, delete-orphan')

    def nqt_to_dict(self):
        return {
            'nqt_ma_quyen': self.nqt_ma_quyen,
            'nqt_ten_quyen': self.nqt_ten_quyen,
            'nqt_nhom_quyen': self.nqt_nhom_quyen,
        }


class NqtNguoiDungVaiTro(db.Model):
    __tablename__ = 'NqtNguoiDungVaiTro'

    nqt_ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey('NqtNguoiDung.nqt_ma_nguoi_dung', ondelete='CASCADE'),
                                   primary_key=True)
    nqt_ma_vai_tro = db.Column(db.Integer, db.ForeignKey('NqtVaiTro.nqt_ma_vai_tro', ondelete='CASCADE'),
                                primary_key=True)

    nqt_nguoi_dung = db.relationship('NqtNguoiDung', back_populates='nqt_vai_tro')
    nqt_vai_tro = db.relationship('NqtVaiTro', back_populates='nqt_nguoi_dung')


class NqtVaiTroQuyen(db.Model):
    __tablename__ = 'NqtVaiTroQuyen'

    nqt_ma_vai_tro = db.Column(db.Integer, db.ForeignKey('NqtVaiTro.nqt_ma_vai_tro', ondelete='CASCADE'),
                                primary_key=True)
    nqt_ma_quyen = db.Column(db.Integer, db.ForeignKey('NqtQuyenHan.nqt_ma_quyen', ondelete='CASCADE'),
                              primary_key=True)

    nqt_vai_tro = db.relationship('NqtVaiTro', back_populates='nqt_quyen')
    nqt_quyen = db.relationship('NqtQuyenHan', back_populates='nqt_vai_tro')


class NqtNguoiDung(db.Model):
    __tablename__ = 'NqtNguoiDung'

    nqt_ma_nguoi_dung = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ten_dang_nhap = db.Column(db.String(50), nullable=False, unique=True)
    nqt_mat_khau = db.Column(db.String(255), nullable=False)
    nqt_ho_ten = db.Column(db.String(100), nullable=False)
    nqt_email = db.Column(db.String(100), unique=True)
    nqt_so_dien_thoai = db.Column(db.String(15))
    nqt_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('NqtChiNhanh.nqt_ma_chi_nhanh', ondelete='SET NULL'))
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    nqt_lan_dang_nhap_sai = db.Column(db.Integer, nullable=False, default=0)
    nqt_khoa_den = db.Column(db.DateTime)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nqt_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    nqt_chi_nhanh = db.relationship('NqtChiNhanh', foreign_keys=[nqt_ma_chi_nhanh])
    nqt_vai_tro = db.relationship('NqtNguoiDungVaiTro', back_populates='nqt_nguoi_dung', cascade='all, delete-orphan')

    def nqt_to_dict(self):
        return {
            'nqt_ma_nguoi_dung': self.nqt_ma_nguoi_dung,
            'nqt_ten_dang_nhap': self.nqt_ten_dang_nhap,
            'nqt_ho_ten': self.nqt_ho_ten,
            'nqt_email': self.nqt_email,
            'nqt_so_dien_thoai': self.nqt_so_dien_thoai,
            'nqt_ma_chi_nhanh': self.nqt_ma_chi_nhanh,
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat() if self.nqt_ngay_tao else None,
            'nqt_vai_tro': [ndvt.nqt_vai_tro.nqt_ten_vai_tro for ndvt in self.nqt_vai_tro],
        }
