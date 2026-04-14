from backend.app import db
from datetime import datetime


class G6VaiTro(db.Model):
    __tablename__ = 'G6VaiTro'

    g6_ma_vai_tro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten_vai_tro = db.Column(db.String(50), nullable=False)
    g6_mo_ta = db.Column(db.String(255))

    g6_nguoi_dung = db.relationship('G6NguoiDungVaiTro', back_populates='g6_vai_tro', cascade='all, delete-orphan')
    g6_quyen = db.relationship('G6VaiTroQuyen', back_populates='g6_vai_tro', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_vai_tro': self.g6_ma_vai_tro,
            'g6_ten_vai_tro': self.g6_ten_vai_tro,
            'g6_mo_ta': self.g6_mo_ta,
        }


class G6QuyenHan(db.Model):
    __tablename__ = 'G6QuyenHan'

    g6_ma_quyen = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten_quyen = db.Column(db.String(100), nullable=False)
    g6_nhom_quyen = db.Column(db.String(50), nullable=False)

    g6_vai_tro = db.relationship('G6VaiTroQuyen', back_populates='g6_quyen', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_quyen': self.g6_ma_quyen,
            'g6_ten_quyen': self.g6_ten_quyen,
            'g6_nhom_quyen': self.g6_nhom_quyen,
        }


class G6NguoiDungVaiTro(db.Model):
    __tablename__ = 'G6NguoiDungVaiTro'

    g6_ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='CASCADE'),
                                   primary_key=True)
    g6_ma_vai_tro = db.Column(db.Integer, db.ForeignKey('G6VaiTro.g6_ma_vai_tro', ondelete='CASCADE'),
                                primary_key=True)

    g6_nguoi_dung = db.relationship('G6NguoiDung', back_populates='g6_vai_tro')
    g6_vai_tro = db.relationship('G6VaiTro', back_populates='g6_nguoi_dung')


class G6VaiTroQuyen(db.Model):
    __tablename__ = 'G6VaiTroQuyen'

    g6_ma_vai_tro = db.Column(db.Integer, db.ForeignKey('G6VaiTro.g6_ma_vai_tro', ondelete='CASCADE'),
                                primary_key=True)
    g6_ma_quyen = db.Column(db.Integer, db.ForeignKey('G6QuyenHan.g6_ma_quyen', ondelete='CASCADE'),
                              primary_key=True)

    g6_vai_tro = db.relationship('G6VaiTro', back_populates='g6_quyen')
    g6_quyen = db.relationship('G6QuyenHan', back_populates='g6_vai_tro')


class G6NguoiDung(db.Model):
    __tablename__ = 'G6NguoiDung'

    g6_ma_nguoi_dung = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten_dang_nhap = db.Column(db.String(50), nullable=False, unique=True)
    g6_mat_khau = db.Column(db.String(255), nullable=False)
    g6_ho_ten = db.Column(db.String(100), nullable=False)
    g6_email = db.Column(db.String(100), unique=True)
    g6_so_dien_thoai = db.Column(db.String(15))
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh', ondelete='SET NULL'))
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_lan_dang_nhap_sai = db.Column(db.Integer, nullable=False, default=0)
    g6_khoa_den = db.Column(db.DateTime)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    g6_chi_nhanh = db.relationship('G6ChiNhanh', foreign_keys=[g6_ma_chi_nhanh])
    g6_vai_tro = db.relationship('G6NguoiDungVaiTro', back_populates='g6_nguoi_dung', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_nguoi_dung': self.g6_ma_nguoi_dung,
            'g6_ten_dang_nhap': self.g6_ten_dang_nhap,
            'g6_ho_ten': self.g6_ho_ten,
            'g6_email': self.g6_email,
            'g6_so_dien_thoai': self.g6_so_dien_thoai,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat() if self.g6_ngay_tao else None,
            'g6_vai_tro': [ndvt.g6_vai_tro.g6_ten_vai_tro for ndvt in self.g6_vai_tro],
        }
