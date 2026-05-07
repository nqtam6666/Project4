from backend.app import db
from datetime import datetime


class G6HuanLuyenVien(db.Model):
    __tablename__ = 'G6HuanLuyenVien'

    g6_ma_hlv = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_nhan_vien = db.Column(db.Integer, db.ForeignKey('G6NhanVien.g6_ma_nhan_vien'), nullable=False)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh'), nullable=False)
    g6_chuyen_mon = db.Column(db.Text)          # JSON: ["tang_co","giam_mo","yoga"]
    g6_cap_chung_chi = db.Column(db.String(50))  # 'ACE','NASM','REPs','ISSA'
    g6_so_nam_kinh_nghiem = db.Column(db.Integer, nullable=False, default=0)
    g6_tieu_su = db.Column(db.Text)
    g6_gia_theo_buoi = db.Column(db.Numeric(15, 0))
    g6_hinh_anh = db.Column(db.String(500))
    g6_thu_hang = db.Column(db.SmallInteger, nullable=False, default=5)  # 1-5 sao
    g6_so_hoi_vien_hien_tai = db.Column(db.Integer, nullable=False, default=0)
    g6_toi_da_hoi_vien = db.Column(db.Integer, nullable=False, default=20)
    g6_la_hien_thi_web = db.Column(db.Boolean, nullable=False, default=True)

    g6_nhan_vien = db.relationship('G6NhanVien', foreign_keys=[g6_ma_nhan_vien])
    g6_chi_nhanh = db.relationship('G6ChiNhanh', foreign_keys=[g6_ma_chi_nhanh])
    g6_goi_pt = db.relationship('G6GoiPT', back_populates='g6_hlv', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_hlv': self.g6_ma_hlv,
            'g6_ma_nhan_vien': self.g6_ma_nhan_vien,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_ho_ten': self.g6_nhan_vien.g6_ho_ten if self.g6_nhan_vien else None,
            'g6_so_dien_thoai': self.g6_nhan_vien.g6_so_dien_thoai if self.g6_nhan_vien else None,
            'g6_email': self.g6_nhan_vien.g6_email if self.g6_nhan_vien else None,
            'g6_chuyen_mon': self.g6_chuyen_mon,
            'g6_cap_chung_chi': self.g6_cap_chung_chi,
            'g6_so_nam_kinh_nghiem': self.g6_so_nam_kinh_nghiem,
            'g6_tieu_su': self.g6_tieu_su,
            'g6_gia_theo_buoi': float(self.g6_gia_theo_buoi) if self.g6_gia_theo_buoi else None,
            'g6_hinh_anh': self.g6_hinh_anh,
            'g6_thu_hang': self.g6_thu_hang,
            'g6_so_hoi_vien_hien_tai': self.g6_so_hoi_vien_hien_tai,
            'g6_toi_da_hoi_vien': self.g6_toi_da_hoi_vien,
            'g6_la_hien_thi_web': self.g6_la_hien_thi_web,
        }


class G6GoiPT(db.Model):
    __tablename__ = 'G6GoiPT'

    g6_ma_goi_pt = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_hlv = db.Column(db.Integer, db.ForeignKey('G6HuanLuyenVien.g6_ma_hlv'), nullable=False)
    g6_ten_goi = db.Column(db.String(100), nullable=False)
    g6_so_buoi = db.Column(db.Integer, nullable=False)
    g6_thoi_luong_buoi = db.Column(db.Integer, nullable=False)  # phút/buổi
    g6_gia = db.Column(db.Numeric(15, 0), nullable=False)
    g6_gia_khuyen_mai = db.Column(db.Numeric(15, 0))
    g6_hieu_luc_ngay = db.Column(db.Integer, nullable=False, default=90)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_hlv = db.relationship('G6HuanLuyenVien', back_populates='g6_goi_pt')
    g6_dang_ky = db.relationship('G6DangKyGoiPT', back_populates='g6_goi_pt', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_goi_pt': self.g6_ma_goi_pt,
            'g6_ma_hlv': self.g6_ma_hlv,
            'g6_ten_goi': self.g6_ten_goi,
            'g6_so_buoi': self.g6_so_buoi,
            'g6_thoi_luong_buoi': self.g6_thoi_luong_buoi,
            'g6_gia': float(self.g6_gia),
            'g6_gia_khuyen_mai': float(self.g6_gia_khuyen_mai) if self.g6_gia_khuyen_mai else None,
            'g6_hieu_luc_ngay': self.g6_hieu_luc_ngay,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat() if self.g6_ngay_tao else None,
        }


class G6DangKyGoiPT(db.Model):
    __tablename__ = 'G6DangKyGoiPT'

    g6_ma_dang_ky_pt = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('G6HoiVien.g6_ma_hoi_vien'), nullable=False)
    g6_ma_goi_pt = db.Column(db.Integer, db.ForeignKey('G6GoiPT.g6_ma_goi_pt'), nullable=False)
    g6_ma_hlv = db.Column(db.Integer, db.ForeignKey('G6HuanLuyenVien.g6_ma_hlv'), nullable=False)
    g6_ngay_mua = db.Column(db.Date, nullable=False)
    g6_ngay_het_han = db.Column(db.Date, nullable=False)
    g6_so_buoi_con_lai = db.Column(db.Integer, nullable=False)
    g6_gia_thuc_te = db.Column(db.Numeric(15, 0), nullable=False)
    g6_ma_thanh_toan = db.Column(db.Integer, db.ForeignKey('G6ThanhToan.g6_ma_thanh_toan', ondelete='SET NULL'))
    g6_trang_thai = db.Column(db.String(20), nullable=False, default='dang_dung')
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_goi_pt = db.relationship('G6GoiPT', back_populates='g6_dang_ky')
    g6_buoi_tap = db.relationship('G6BuoiTapPT', back_populates='g6_dang_ky_pt', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_dang_ky_pt': self.g6_ma_dang_ky_pt,
            'g6_ma_hoi_vien': self.g6_ma_hoi_vien,
            'g6_ma_goi_pt': self.g6_ma_goi_pt,
            'g6_ma_hlv': self.g6_ma_hlv,
            'g6_ngay_mua': str(self.g6_ngay_mua),
            'g6_ngay_het_han': str(self.g6_ngay_het_han),
            'g6_so_buoi_con_lai': self.g6_so_buoi_con_lai,
            'g6_gia_thuc_te': float(self.g6_gia_thuc_te),
            'g6_trang_thai': self.g6_trang_thai,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat() if self.g6_ngay_tao else None,
        }


class G6BuoiTapPT(db.Model):
    __tablename__ = 'G6BuoiTapPT'

    g6_ma_buoi_tap = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_dang_ky_pt = db.Column(db.Integer, db.ForeignKey('G6DangKyGoiPT.g6_ma_dang_ky_pt'), nullable=False)
    g6_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('G6HoiVien.g6_ma_hoi_vien'), nullable=False)
    g6_ma_hlv = db.Column(db.Integer, db.ForeignKey('G6HuanLuyenVien.g6_ma_hlv'), nullable=False)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh'), nullable=False)
    g6_ngay_tap = db.Column(db.DateTime, nullable=False)
    g6_thoi_luong = db.Column(db.Integer)  # phút thực tế
    g6_trang_thai = db.Column(db.String(20), nullable=False, default='cho_xac_nhan')
    g6_noi_dung_buoi_tap = db.Column(db.Text)
    g6_nhan_xet_hlv = db.Column(db.Text)
    g6_danh_gia_hoi_vien = db.Column(db.SmallInteger)  # 1-5 sao
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_dang_ky_pt = db.relationship('G6DangKyGoiPT', back_populates='g6_buoi_tap')

    def g6_to_dict(self):
        return {
            'g6_ma_buoi_tap': self.g6_ma_buoi_tap,
            'g6_ma_dang_ky_pt': self.g6_ma_dang_ky_pt,
            'g6_ma_hoi_vien': self.g6_ma_hoi_vien,
            'g6_ma_hlv': self.g6_ma_hlv,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_ngay_tap': self.g6_ngay_tap.isoformat() if self.g6_ngay_tap else None,
            'g6_thoi_luong': self.g6_thoi_luong,
            'g6_trang_thai': self.g6_trang_thai,
            'g6_noi_dung_buoi_tap': self.g6_noi_dung_buoi_tap,
            'g6_nhan_xet_hlv': self.g6_nhan_xet_hlv,
            'g6_danh_gia_hoi_vien': self.g6_danh_gia_hoi_vien,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat() if self.g6_ngay_tao else None,
        }
