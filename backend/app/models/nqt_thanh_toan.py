from backend.app import db
from datetime import datetime


class NqtThanhToan(db.Model):
    __tablename__ = 'NqtThanhToan'

    nqt_ma_thanh_toan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('NqtKhachHang.nqt_ma_khach_hang', ondelete='SET NULL'))
    nqt_loai_giao_dich = db.Column(db.String(30), nullable=False)
    nqt_so_tien = db.Column(db.Numeric(15, 0), nullable=False)
    nqt_phuong_thuc = db.Column(db.String(30), nullable=False, default='cod')
    nqt_trang_thai = db.Column(db.String(20), nullable=False, default='cho_xu_ly')
    nqt_ma_giao_dich_cong = db.Column(db.String(100))
    nqt_du_lieu_tra_ve = db.Column(db.JSON)
    nqt_ngay_thanh_toan = db.Column(db.DateTime)
    nqt_ghi_chu = db.Column(db.String(255))
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    nqt_hoa_don = db.relationship('NqtHoaDon', back_populates='nqt_thanh_toan', uselist=False)

    def nqt_to_dict(self):
        return {
            'nqt_ma_thanh_toan': self.nqt_ma_thanh_toan,
            'nqt_loai_giao_dich': self.nqt_loai_giao_dich,
            'nqt_so_tien': float(self.nqt_so_tien),
            'nqt_phuong_thuc': self.nqt_phuong_thuc,
            'nqt_trang_thai': self.nqt_trang_thai,
            'nqt_ngay_thanh_toan': self.nqt_ngay_thanh_toan.isoformat() if self.nqt_ngay_thanh_toan else None,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat(),
        }


class NqtHoaDon(db.Model):
    __tablename__ = 'NqtHoaDon'

    nqt_ma_hoa_don = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_thanh_toan = db.Column(db.Integer, db.ForeignKey('NqtThanhToan.nqt_ma_thanh_toan', ondelete='CASCADE'),
                                   nullable=False, unique=True)
    nqt_so_hoa_don = db.Column(db.String(30), nullable=False, unique=True)
    nqt_tien_truoc_thue = db.Column(db.Numeric(15, 0), nullable=False)
    nqt_tien_thue = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    nqt_tong_cong = db.Column(db.Numeric(15, 0), nullable=False)
    nqt_thong_tin_mst = db.Column(db.String(255))
    nqt_ngay_xuat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    nqt_thanh_toan = db.relationship('NqtThanhToan', back_populates='nqt_hoa_don')

    def nqt_to_dict(self):
        return {
            'nqt_ma_hoa_don': self.nqt_ma_hoa_don,
            'nqt_so_hoa_don': self.nqt_so_hoa_don,
            'nqt_tien_truoc_thue': float(self.nqt_tien_truoc_thue),
            'nqt_tien_thue': float(self.nqt_tien_thue),
            'nqt_tong_cong': float(self.nqt_tong_cong),
            'nqt_ngay_xuat': self.nqt_ngay_xuat.isoformat(),
        }
