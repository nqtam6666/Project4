from backend.app import db
from datetime import datetime


class G6HoiVien(db.Model):
    __tablename__ = 'G6HoiVien'

    g6_ma_hoi_vien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh'), nullable=False)
    g6_ho_ten = db.Column(db.String(100), nullable=False)
    g6_ngay_sinh = db.Column(db.Date)
    g6_gioi_tinh = db.Column(db.String(10))
    g6_so_dien_thoai = db.Column(db.String(15), nullable=False, unique=True)
    g6_email = db.Column(db.String(100))
    g6_dia_chi = db.Column(db.String(255))
    g6_so_cccd = db.Column(db.String(20))
    g6_ngay_dang_ky = db.Column(db.Date, nullable=False)
    g6_anh_the = db.Column(db.String(500))
    g6_ma_qr = db.Column(db.String(100), nullable=False, unique=True)
    g6_nguon_gioi_thieu = db.Column(db.String(100))
    g6_ma_gioi_thieu = db.Column(db.Integer, db.ForeignKey('G6HoiVien.g6_ma_hoi_vien'))
    g6_ghi_chu = db.Column(db.Text)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    g6_chi_nhanh = db.relationship('G6ChiNhanh', foreign_keys=[g6_ma_chi_nhanh])
    g6_nguoi_gioi_thieu = db.relationship('G6HoiVien', remote_side='G6HoiVien.g6_ma_hoi_vien',
                                            foreign_keys=[g6_ma_gioi_thieu])
    g6_dang_ky = db.relationship('G6DangKyGoiTap', back_populates='g6_hoi_vien', cascade='all, delete-orphan')
    g6_diem_danh = db.relationship('G6DiemDanh', back_populates='g6_hoi_vien', cascade='all, delete-orphan')
    g6_chi_so = db.relationship('G6ChiSoCoThe', back_populates='g6_hoi_vien', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_hoi_vien': self.g6_ma_hoi_vien,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_ho_ten': self.g6_ho_ten,
            'g6_ngay_sinh': str(self.g6_ngay_sinh) if self.g6_ngay_sinh else None,
            'g6_gioi_tinh': self.g6_gioi_tinh,
            'g6_so_dien_thoai': self.g6_so_dien_thoai,
            'g6_email': self.g6_email,
            'g6_ngay_dang_ky': str(self.g6_ngay_dang_ky) if self.g6_ngay_dang_ky else None,
            'g6_ma_qr': self.g6_ma_qr,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat() if self.g6_ngay_tao else None,
        }


class G6GoiTap(db.Model):
    __tablename__ = 'G6GoiTap'

    g6_ma_goi_tap = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh', ondelete='SET NULL'))
    g6_ten_goi = db.Column(db.String(100), nullable=False)
    g6_mo_ta = db.Column(db.Text)
    g6_so_ngay = db.Column(db.Integer, nullable=False)
    g6_gia = db.Column(db.Numeric(15, 0), nullable=False)
    g6_gia_khuyen_mai = db.Column(db.Numeric(15, 0))
    g6_so_luot_checkin_ngay = db.Column(db.Integer, nullable=False, default=1)
    g6_duoc_dua_khach = db.Column(db.Boolean, nullable=False, default=False)
    g6_so_khach_duoc_dua = db.Column(db.Integer, nullable=False, default=0)
    g6_co_pt = db.Column(db.Boolean, nullable=False, default=False)
    g6_so_buoi_pt = db.Column(db.Integer, nullable=False, default=0)
    g6_co_sauna = db.Column(db.Boolean, nullable=False, default=False)
    g6_mau_hien_thi = db.Column(db.String(20))
    g6_la_noi_bat = db.Column(db.Boolean, nullable=False, default=False)
    g6_thu_tu_hien_thi = db.Column(db.Integer, nullable=False, default=0)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_goi_tap': self.g6_ma_goi_tap,
            'g6_ten_goi': self.g6_ten_goi,
            'g6_mo_ta': self.g6_mo_ta,
            'g6_so_ngay': self.g6_so_ngay,
            'g6_gia': float(self.g6_gia),
            'g6_gia_khuyen_mai': float(self.g6_gia_khuyen_mai) if self.g6_gia_khuyen_mai else None,
            'g6_co_pt': self.g6_co_pt,
            'g6_so_buoi_pt': self.g6_so_buoi_pt,
            'g6_co_sauna': self.g6_co_sauna,
            'g6_la_noi_bat': self.g6_la_noi_bat,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
        }


class G6DangKyGoiTap(db.Model):
    __tablename__ = 'G6DangKyGoiTap'

    g6_ma_dang_ky = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('G6HoiVien.g6_ma_hoi_vien'), nullable=False)
    g6_ma_goi_tap = db.Column(db.Integer, db.ForeignKey('G6GoiTap.g6_ma_goi_tap'), nullable=False)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh'), nullable=False)
    g6_ngay_bat_dau = db.Column(db.Date, nullable=False)
    g6_ngay_het_han = db.Column(db.Date, nullable=False)
    g6_gia_thuc_te = db.Column(db.Numeric(15, 0), nullable=False)
    g6_ma_thanh_toan = db.Column(db.Integer, db.ForeignKey('G6ThanhToan.g6_ma_thanh_toan', ondelete='SET NULL'))
    g6_trang_thai = db.Column(db.String(20), nullable=False, default='dang_hoat_dong')
    g6_ly_do_tam_dung = db.Column(db.String(255))
    g6_ngay_tam_dung = db.Column(db.Date)
    g6_ngay_tiep_tuc = db.Column(db.Date)
    g6_tu_dong_gia_han = db.Column(db.Boolean, nullable=False, default=False)
    g6_ghi_chu = db.Column(db.Text)
    g6_nguoi_tao = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_hoi_vien = db.relationship('G6HoiVien', back_populates='g6_dang_ky')
    g6_goi_tap = db.relationship('G6GoiTap')

    def g6_to_dict(self):
        return {
            'g6_ma_dang_ky': self.g6_ma_dang_ky,
            'g6_ma_hoi_vien': self.g6_ma_hoi_vien,
            'g6_ma_goi_tap': self.g6_ma_goi_tap,
            'g6_ngay_bat_dau': str(self.g6_ngay_bat_dau),
            'g6_ngay_het_han': str(self.g6_ngay_het_han),
            'g6_gia_thuc_te': float(self.g6_gia_thuc_te),
            'g6_trang_thai': self.g6_trang_thai,
        }


class G6DiemDanh(db.Model):
    __tablename__ = 'G6DiemDanh'

    g6_ma_diem_danh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_dang_ky = db.Column(db.Integer, db.ForeignKey('G6DangKyGoiTap.g6_ma_dang_ky'), nullable=False)
    g6_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('G6HoiVien.g6_ma_hoi_vien'), nullable=False)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh'), nullable=False)
    g6_thoi_gian_vao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_thoi_gian_ra = db.Column(db.DateTime)
    g6_phuong_thuc = db.Column(db.String(20), nullable=False, default='qr')
    g6_nguoi_xac_nhan = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    g6_ghi_chu = db.Column(db.String(255))

    g6_hoi_vien = db.relationship('G6HoiVien', back_populates='g6_diem_danh')

    def g6_to_dict(self):
        return {
            'g6_ma_diem_danh': self.g6_ma_diem_danh,
            'g6_ma_hoi_vien': self.g6_ma_hoi_vien,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_thoi_gian_vao': self.g6_thoi_gian_vao.isoformat(),
            'g6_thoi_gian_ra': self.g6_thoi_gian_ra.isoformat() if self.g6_thoi_gian_ra else None,
            'g6_phuong_thuc': self.g6_phuong_thuc,
        }


class G6ChiSoCoThe(db.Model):
    __tablename__ = 'G6ChiSoCoThe'

    g6_ma_chi_so = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('G6HoiVien.g6_ma_hoi_vien', ondelete='CASCADE'),
                                 nullable=False)
    g6_ngay_do = db.Column(db.Date, nullable=False)
    g6_can_nang = db.Column(db.Numeric(5, 2))
    g6_chieu_cao = db.Column(db.Numeric(5, 2))
    g6_chi_so_bmi = db.Column(db.Numeric(5, 2))
    g6_ti_le_mo = db.Column(db.Numeric(5, 2))
    g6_ti_le_co = db.Column(db.Numeric(5, 2))
    g6_ti_le_nuoc = db.Column(db.Numeric(5, 2))
    g6_khoi_luong_co = db.Column(db.Numeric(5, 2))
    g6_vong_nguc = db.Column(db.Numeric(5, 2))
    g6_vong_eo = db.Column(db.Numeric(5, 2))
    g6_vong_hong = db.Column(db.Numeric(5, 2))
    g6_vong_tay_trai = db.Column(db.Numeric(5, 2))
    g6_vong_dui_trai = db.Column(db.Numeric(5, 2))
    g6_nguoi_do = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    g6_ghi_chu = db.Column(db.Text)
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    g6_hoi_vien = db.relationship('G6HoiVien', back_populates='g6_chi_so')

    def g6_to_dict(self):
        def g6_f(v):
            return float(v) if v is not None else None
        return {
            'g6_ma_chi_so': self.g6_ma_chi_so,
            'g6_ma_hoi_vien': self.g6_ma_hoi_vien,
            'g6_ngay_do': str(self.g6_ngay_do),
            'g6_can_nang': g6_f(self.g6_can_nang),
            'g6_chieu_cao': g6_f(self.g6_chieu_cao),
            'g6_chi_so_bmi': g6_f(self.g6_chi_so_bmi),
            'g6_ti_le_mo': g6_f(self.g6_ti_le_mo),
            'g6_ti_le_co': g6_f(self.g6_ti_le_co),
            'g6_vong_eo': g6_f(self.g6_vong_eo),
        }
