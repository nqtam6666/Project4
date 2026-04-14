from backend.app import db
from datetime import datetime


class G6ThanhToan(db.Model):
    __tablename__ = 'G6ThanhToan'

    g6_ma_thanh_toan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_khach_hang = db.Column(db.Integer, db.ForeignKey('G6KhachHang.g6_ma_khach_hang', ondelete='SET NULL'))
    g6_loai_giao_dich = db.Column(db.String(30), nullable=False)
    g6_so_tien = db.Column(db.Numeric(15, 0), nullable=False)
    g6_phuong_thuc = db.Column(db.String(30), nullable=False, default='cod')
    g6_trang_thai = db.Column(db.String(20), nullable=False, default='cho_xu_ly')
    g6_ma_giao_dich_cong = db.Column(db.String(100))
    g6_du_lieu_tra_ve = db.Column(db.JSON)
    g6_ngay_thanh_toan = db.Column(db.DateTime)
    g6_ghi_chu = db.Column(db.String(255))
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_hoa_don = db.relationship('G6HoaDon', back_populates='g6_thanh_toan', uselist=False)

    def g6_to_dict(self):
        return {
            'g6_ma_thanh_toan': self.g6_ma_thanh_toan,
            'g6_loai_giao_dich': self.g6_loai_giao_dich,
            'g6_so_tien': float(self.g6_so_tien),
            'g6_phuong_thuc': self.g6_phuong_thuc,
            'g6_trang_thai': self.g6_trang_thai,
            'g6_ngay_thanh_toan': self.g6_ngay_thanh_toan.isoformat() if self.g6_ngay_thanh_toan else None,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat(),
        }


class G6HoaDon(db.Model):
    __tablename__ = 'G6HoaDon'

    g6_ma_hoa_don = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_thanh_toan = db.Column(db.Integer, db.ForeignKey('G6ThanhToan.g6_ma_thanh_toan', ondelete='CASCADE'),
                                   nullable=False, unique=True)
    g6_so_hoa_don = db.Column(db.String(30), nullable=False, unique=True)
    g6_tien_truoc_thue = db.Column(db.Numeric(15, 0), nullable=False)
    g6_tien_thue = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    g6_tong_cong = db.Column(db.Numeric(15, 0), nullable=False)
    g6_thong_tin_mst = db.Column(db.String(255))
    g6_ngay_xuat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_thanh_toan = db.relationship('G6ThanhToan', back_populates='g6_hoa_don')

    def g6_to_dict(self):
        return {
            'g6_ma_hoa_don': self.g6_ma_hoa_don,
            'g6_so_hoa_don': self.g6_so_hoa_don,
            'g6_tien_truoc_thue': float(self.g6_tien_truoc_thue),
            'g6_tien_thue': float(self.g6_tien_thue),
            'g6_tong_cong': float(self.g6_tong_cong),
            'g6_ngay_xuat': self.g6_ngay_xuat.isoformat(),
        }
