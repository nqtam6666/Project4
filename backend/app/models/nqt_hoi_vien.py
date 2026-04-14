from backend.app import db
from datetime import datetime


class NqtHoiVien(db.Model):
    __tablename__ = 'NqtHoiVien'

    nqt_ma_hoi_vien = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('NqtChiNhanh.nqt_ma_chi_nhanh'), nullable=False)
    nqt_ho_ten = db.Column(db.String(100), nullable=False)
    nqt_ngay_sinh = db.Column(db.Date)
    nqt_gioi_tinh = db.Column(db.String(10))
    nqt_so_dien_thoai = db.Column(db.String(15), nullable=False, unique=True)
    nqt_email = db.Column(db.String(100))
    nqt_dia_chi = db.Column(db.String(255))
    nqt_so_cccd = db.Column(db.String(20))
    nqt_ngay_dang_ky = db.Column(db.Date, nullable=False)
    nqt_anh_the = db.Column(db.String(500))
    nqt_ma_qr = db.Column(db.String(100), nullable=False, unique=True)
    nqt_nguon_gioi_thieu = db.Column(db.String(100))
    nqt_ma_gioi_thieu = db.Column(db.Integer, db.ForeignKey('NqtHoiVien.nqt_ma_hoi_vien'))
    nqt_ghi_chu = db.Column(db.Text)
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nqt_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    nqt_chi_nhanh = db.relationship('NqtChiNhanh', foreign_keys=[nqt_ma_chi_nhanh])
    nqt_nguoi_gioi_thieu = db.relationship('NqtHoiVien', remote_side='NqtHoiVien.nqt_ma_hoi_vien',
                                            foreign_keys=[nqt_ma_gioi_thieu])
    nqt_dang_ky = db.relationship('NqtDangKyGoiTap', back_populates='nqt_hoi_vien', cascade='all, delete-orphan')
    nqt_diem_danh = db.relationship('NqtDiemDanh', back_populates='nqt_hoi_vien', cascade='all, delete-orphan')
    nqt_chi_so = db.relationship('NqtChiSoCoThe', back_populates='nqt_hoi_vien', cascade='all, delete-orphan')

    def nqt_to_dict(self):
        return {
            'nqt_ma_hoi_vien': self.nqt_ma_hoi_vien,
            'nqt_ma_chi_nhanh': self.nqt_ma_chi_nhanh,
            'nqt_ho_ten': self.nqt_ho_ten,
            'nqt_ngay_sinh': str(self.nqt_ngay_sinh) if self.nqt_ngay_sinh else None,
            'nqt_gioi_tinh': self.nqt_gioi_tinh,
            'nqt_so_dien_thoai': self.nqt_so_dien_thoai,
            'nqt_email': self.nqt_email,
            'nqt_ngay_dang_ky': str(self.nqt_ngay_dang_ky) if self.nqt_ngay_dang_ky else None,
            'nqt_ma_qr': self.nqt_ma_qr,
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat() if self.nqt_ngay_tao else None,
        }


class NqtGoiTap(db.Model):
    __tablename__ = 'NqtGoiTap'

    nqt_ma_goi_tap = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('NqtChiNhanh.nqt_ma_chi_nhanh', ondelete='SET NULL'))
    nqt_ten_goi = db.Column(db.String(100), nullable=False)
    nqt_mo_ta = db.Column(db.Text)
    nqt_so_ngay = db.Column(db.Integer, nullable=False)
    nqt_gia = db.Column(db.Numeric(15, 0), nullable=False)
    nqt_gia_khuyen_mai = db.Column(db.Numeric(15, 0))
    nqt_so_luot_checkin_ngay = db.Column(db.Integer, nullable=False, default=1)
    nqt_duoc_dua_khach = db.Column(db.Boolean, nullable=False, default=False)
    nqt_so_khach_duoc_dua = db.Column(db.Integer, nullable=False, default=0)
    nqt_co_pt = db.Column(db.Boolean, nullable=False, default=False)
    nqt_so_buoi_pt = db.Column(db.Integer, nullable=False, default=0)
    nqt_co_sauna = db.Column(db.Boolean, nullable=False, default=False)
    nqt_mau_hien_thi = db.Column(db.String(20))
    nqt_la_noi_bat = db.Column(db.Boolean, nullable=False, default=False)
    nqt_thu_tu_hien_thi = db.Column(db.Integer, nullable=False, default=0)
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def nqt_to_dict(self):
        return {
            'nqt_ma_goi_tap': self.nqt_ma_goi_tap,
            'nqt_ten_goi': self.nqt_ten_goi,
            'nqt_mo_ta': self.nqt_mo_ta,
            'nqt_so_ngay': self.nqt_so_ngay,
            'nqt_gia': float(self.nqt_gia),
            'nqt_gia_khuyen_mai': float(self.nqt_gia_khuyen_mai) if self.nqt_gia_khuyen_mai else None,
            'nqt_co_pt': self.nqt_co_pt,
            'nqt_so_buoi_pt': self.nqt_so_buoi_pt,
            'nqt_co_sauna': self.nqt_co_sauna,
            'nqt_la_noi_bat': self.nqt_la_noi_bat,
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
        }


class NqtDangKyGoiTap(db.Model):
    __tablename__ = 'NqtDangKyGoiTap'

    nqt_ma_dang_ky = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('NqtHoiVien.nqt_ma_hoi_vien'), nullable=False)
    nqt_ma_goi_tap = db.Column(db.Integer, db.ForeignKey('NqtGoiTap.nqt_ma_goi_tap'), nullable=False)
    nqt_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('NqtChiNhanh.nqt_ma_chi_nhanh'), nullable=False)
    nqt_ngay_bat_dau = db.Column(db.Date, nullable=False)
    nqt_ngay_het_han = db.Column(db.Date, nullable=False)
    nqt_gia_thuc_te = db.Column(db.Numeric(15, 0), nullable=False)
    nqt_ma_thanh_toan = db.Column(db.Integer, db.ForeignKey('NqtThanhToan.nqt_ma_thanh_toan', ondelete='SET NULL'))
    nqt_trang_thai = db.Column(db.String(20), nullable=False, default='dang_hoat_dong')
    nqt_ly_do_tam_dung = db.Column(db.String(255))
    nqt_ngay_tam_dung = db.Column(db.Date)
    nqt_ngay_tiep_tuc = db.Column(db.Date)
    nqt_tu_dong_gia_han = db.Column(db.Boolean, nullable=False, default=False)
    nqt_ghi_chu = db.Column(db.Text)
    nqt_nguoi_tao = db.Column(db.Integer, db.ForeignKey('NqtNguoiDung.nqt_ma_nguoi_dung', ondelete='SET NULL'))
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    nqt_hoi_vien = db.relationship('NqtHoiVien', back_populates='nqt_dang_ky')
    nqt_goi_tap = db.relationship('NqtGoiTap')

    def nqt_to_dict(self):
        return {
            'nqt_ma_dang_ky': self.nqt_ma_dang_ky,
            'nqt_ma_hoi_vien': self.nqt_ma_hoi_vien,
            'nqt_ma_goi_tap': self.nqt_ma_goi_tap,
            'nqt_ngay_bat_dau': str(self.nqt_ngay_bat_dau),
            'nqt_ngay_het_han': str(self.nqt_ngay_het_han),
            'nqt_gia_thuc_te': float(self.nqt_gia_thuc_te),
            'nqt_trang_thai': self.nqt_trang_thai,
        }


class NqtDiemDanh(db.Model):
    __tablename__ = 'NqtDiemDanh'

    nqt_ma_diem_danh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_dang_ky = db.Column(db.Integer, db.ForeignKey('NqtDangKyGoiTap.nqt_ma_dang_ky'), nullable=False)
    nqt_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('NqtHoiVien.nqt_ma_hoi_vien'), nullable=False)
    nqt_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('NqtChiNhanh.nqt_ma_chi_nhanh'), nullable=False)
    nqt_thoi_gian_vao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nqt_thoi_gian_ra = db.Column(db.DateTime)
    nqt_phuong_thuc = db.Column(db.String(20), nullable=False, default='qr')
    nqt_nguoi_xac_nhan = db.Column(db.Integer, db.ForeignKey('NqtNguoiDung.nqt_ma_nguoi_dung', ondelete='SET NULL'))
    nqt_ghi_chu = db.Column(db.String(255))

    nqt_hoi_vien = db.relationship('NqtHoiVien', back_populates='nqt_diem_danh')

    def nqt_to_dict(self):
        return {
            'nqt_ma_diem_danh': self.nqt_ma_diem_danh,
            'nqt_ma_hoi_vien': self.nqt_ma_hoi_vien,
            'nqt_ma_chi_nhanh': self.nqt_ma_chi_nhanh,
            'nqt_thoi_gian_vao': self.nqt_thoi_gian_vao.isoformat(),
            'nqt_thoi_gian_ra': self.nqt_thoi_gian_ra.isoformat() if self.nqt_thoi_gian_ra else None,
            'nqt_phuong_thuc': self.nqt_phuong_thuc,
        }


class NqtChiSoCoThe(db.Model):
    __tablename__ = 'NqtChiSoCoThe'

    nqt_ma_chi_so = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_hoi_vien = db.Column(db.Integer, db.ForeignKey('NqtHoiVien.nqt_ma_hoi_vien', ondelete='CASCADE'),
                                 nullable=False)
    nqt_ngay_do = db.Column(db.Date, nullable=False)
    nqt_can_nang = db.Column(db.Numeric(5, 2))
    nqt_chieu_cao = db.Column(db.Numeric(5, 2))
    nqt_chi_so_bmi = db.Column(db.Numeric(5, 2))
    nqt_ti_le_mo = db.Column(db.Numeric(5, 2))
    nqt_ti_le_co = db.Column(db.Numeric(5, 2))
    nqt_ti_le_nuoc = db.Column(db.Numeric(5, 2))
    nqt_khoi_luong_co = db.Column(db.Numeric(5, 2))
    nqt_vong_nguc = db.Column(db.Numeric(5, 2))
    nqt_vong_eo = db.Column(db.Numeric(5, 2))
    nqt_vong_hong = db.Column(db.Numeric(5, 2))
    nqt_vong_tay_trai = db.Column(db.Numeric(5, 2))
    nqt_vong_dui_trai = db.Column(db.Numeric(5, 2))
    nqt_nguoi_do = db.Column(db.Integer, db.ForeignKey('NqtNguoiDung.nqt_ma_nguoi_dung', ondelete='SET NULL'))
    nqt_ghi_chu = db.Column(db.Text)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    nqt_hoi_vien = db.relationship('NqtHoiVien', back_populates='nqt_chi_so')

    def nqt_to_dict(self):
        def nqt_f(v):
            return float(v) if v is not None else None
        return {
            'nqt_ma_chi_so': self.nqt_ma_chi_so,
            'nqt_ma_hoi_vien': self.nqt_ma_hoi_vien,
            'nqt_ngay_do': str(self.nqt_ngay_do),
            'nqt_can_nang': nqt_f(self.nqt_can_nang),
            'nqt_chieu_cao': nqt_f(self.nqt_chieu_cao),
            'nqt_chi_so_bmi': nqt_f(self.nqt_chi_so_bmi),
            'nqt_ti_le_mo': nqt_f(self.nqt_ti_le_mo),
            'nqt_ti_le_co': nqt_f(self.nqt_ti_le_co),
            'nqt_vong_eo': nqt_f(self.nqt_vong_eo),
        }
