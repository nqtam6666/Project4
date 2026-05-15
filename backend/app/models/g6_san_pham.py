from backend.app import db
from datetime import datetime


# ============================================================
# GROUP 9: DANH MỤC SẢN PHẨM
# ============================================================

class G6DanhMucSanPham(db.Model):
    __tablename__ = 'G6DanhMucSanPham'

    g6_ma_danh_muc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_danh_muc_cha = db.Column(db.Integer, db.ForeignKey('G6DanhMucSanPham.g6_ma_danh_muc'))
    g6_ten_danh_muc = db.Column(db.String(100), nullable=False)
    g6_slug = db.Column(db.String(100), nullable=False, unique=True)
    g6_mo_ta = db.Column(db.Text)
    g6_hinh_anh = db.Column(db.String(500))
    g6_thu_tu_hien_thi = db.Column(db.Integer, nullable=False, default=0)
    g6_la_hien_thi_menu = db.Column(db.Boolean, nullable=False, default=True)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)

    g6_danh_muc_con = db.relationship(
        'G6DanhMucSanPham',
        backref=db.backref('g6_danh_muc_cha_rel', remote_side='G6DanhMucSanPham.g6_ma_danh_muc'),
        foreign_keys=[g6_ma_danh_muc_cha],
    )
    g6_san_pham = db.relationship('G6SanPham', back_populates='g6_danh_muc')

    def g6_to_dict(self):
        return {
            'g6_ma_danh_muc': self.g6_ma_danh_muc,
            'g6_ma_danh_muc_cha': self.g6_ma_danh_muc_cha,
            'g6_ten_danh_muc': self.g6_ten_danh_muc,
            'g6_slug': self.g6_slug,
            'g6_mo_ta': self.g6_mo_ta,
            'g6_hinh_anh': self.g6_hinh_anh,
            'g6_thu_tu_hien_thi': self.g6_thu_tu_hien_thi,
            'g6_la_hien_thi_menu': self.g6_la_hien_thi_menu,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
        }


class G6MucTieuSucKhoe(db.Model):
    __tablename__ = 'G6MucTieuSucKhoe'

    g6_ma_muc_tieu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten_muc_tieu = db.Column(db.String(50), nullable=False)
    g6_slug = db.Column(db.String(50), nullable=False, unique=True)
    g6_bieu_tuong = db.Column(db.String(20))

    def g6_to_dict(self):
        return {
            'g6_ma_muc_tieu': self.g6_ma_muc_tieu,
            'g6_ten_muc_tieu': self.g6_ten_muc_tieu,
            'g6_slug': self.g6_slug,
            'g6_bieu_tuong': self.g6_bieu_tuong,
        }


class G6ThuongHieu(db.Model):
    __tablename__ = 'G6ThuongHieu'

    g6_ma_thuong_hieu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ten_thuong_hieu = db.Column(db.String(100), nullable=False)
    g6_slug = db.Column(db.String(100), nullable=False, unique=True)
    g6_nuoc_xuat_xu = db.Column(db.String(50))
    g6_logo = db.Column(db.String(500))
    g6_mo_ta = db.Column(db.Text)
    g6_website = db.Column(db.String(255))
    g6_la_noi_bat = db.Column(db.Boolean, nullable=False, default=False)
    g6_loai_tru_ma_giam = db.Column(db.Boolean, nullable=False, default=False)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_thu_tu_hien_thi = db.Column(db.Integer, nullable=False, default=0)

    g6_san_pham = db.relationship('G6SanPham', back_populates='g6_thuong_hieu')

    def g6_to_dict(self):
        return {
            'g6_ma_thuong_hieu': self.g6_ma_thuong_hieu,
            'g6_ten_thuong_hieu': self.g6_ten_thuong_hieu,
            'g6_slug': self.g6_slug,
            'g6_nuoc_xuat_xu': self.g6_nuoc_xuat_xu,
            'g6_logo': self.g6_logo,
            'g6_mo_ta': self.g6_mo_ta,
            'g6_website': self.g6_website,
            'g6_la_noi_bat': self.g6_la_noi_bat,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
            'g6_thu_tu_hien_thi': self.g6_thu_tu_hien_thi,
        }


# ============================================================
# GROUP 10: SẢN PHẨM
# ============================================================

# Bảng trung gian SanPham ↔ MucTieu
g6_san_pham_muc_tieu = db.Table(
    'G6SanPhamMucTieu',
    db.Column('g6_ma_san_pham', db.Integer, db.ForeignKey('G6SanPham.g6_ma_san_pham', ondelete='CASCADE'), primary_key=True),
    db.Column('g6_ma_muc_tieu', db.Integer, db.ForeignKey('G6MucTieuSucKhoe.g6_ma_muc_tieu', ondelete='CASCADE'), primary_key=True),
)


class G6SanPham(db.Model):
    __tablename__ = 'G6SanPham'

    g6_ma_san_pham = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_danh_muc = db.Column(db.Integer, db.ForeignKey('G6DanhMucSanPham.g6_ma_danh_muc'), nullable=False)
    g6_ma_thuong_hieu = db.Column(db.Integer, db.ForeignKey('G6ThuongHieu.g6_ma_thuong_hieu'), nullable=False)
    g6_ten_san_pham = db.Column(db.String(255), nullable=False)
    g6_slug = db.Column(db.String(255), nullable=False, unique=True)
    g6_mo_ta_ngan = db.Column(db.String(500))
    g6_mo_ta_day_du = db.Column(db.Text)
    g6_cach_dung = db.Column(db.Text)
    g6_nuoc_xuat_xu = db.Column(db.String(50))
    g6_doi_tuong_dung = db.Column(db.String(100))  # 'nam','nu','nam_va_nu'
    g6_da_ban = db.Column(db.Integer, nullable=False, default=0)
    g6_luot_xem = db.Column(db.Integer, nullable=False, default=0)
    g6_thu_tu_hien_thi = db.Column(db.Integer, nullable=False, default=0)
    g6_la_noi_bat = db.Column(db.Boolean, nullable=False, default=False)
    g6_la_ban_chay = db.Column(db.Boolean, nullable=False, default=False)
    g6_la_hang_moi = db.Column(db.Boolean, nullable=False, default=False)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_seo_title = db.Column(db.String(255))
    g6_seo_mo_ta = db.Column(db.String(500))
    g6_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    g6_danh_muc = db.relationship('G6DanhMucSanPham', back_populates='g6_san_pham')
    g6_thuong_hieu = db.relationship('G6ThuongHieu', back_populates='g6_san_pham')
    g6_bien_the = db.relationship('G6BienTheSanPham', back_populates='g6_san_pham', cascade='all, delete-orphan')
    g6_hinh_anh = db.relationship('G6HinhAnhSanPham', back_populates='g6_san_pham', cascade='all, delete-orphan')
    g6_chung_nhan = db.relationship('G6ChungNhanSanPham', back_populates='g6_san_pham', cascade='all, delete-orphan')
    g6_muc_tieu = db.relationship('G6MucTieuSucKhoe', secondary=g6_san_pham_muc_tieu)

    def g6_to_dict(self):
        bt_mac_dinh = next((b for b in self.g6_bien_the if b.g6_la_mac_dinh), None)
        if not bt_mac_dinh and self.g6_bien_the:
            bt_mac_dinh = self.g6_bien_the[0]
            
        return {
            'g6_ma_san_pham': self.g6_ma_san_pham,
            'g6_ma_danh_muc': self.g6_ma_danh_muc,
            'g6_ma_thuong_hieu': self.g6_ma_thuong_hieu,
            'g6_ten_san_pham': self.g6_ten_san_pham,
            'g6_slug': self.g6_slug,
            'g6_mo_ta_ngan': self.g6_mo_ta_ngan,
            'g6_nuoc_xuat_xu': self.g6_nuoc_xuat_xu,
            'g6_doi_tuong_dung': self.g6_doi_tuong_dung,
            'g6_da_ban': self.g6_da_ban,
            'g6_luot_xem': self.g6_luot_xem,
            'g6_la_noi_bat': self.g6_la_noi_bat,
            'g6_la_ban_chay': self.g6_la_ban_chay,
            'g6_la_hang_moi': self.g6_la_hang_moi,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
            'g6_ngay_tao': self.g6_ngay_tao.isoformat() if self.g6_ngay_tao else None,
            'g6_gia_ban': float(bt_mac_dinh.g6_gia) if bt_mac_dinh else 0,
            'g6_gia_goc': float(bt_mac_dinh.g6_gia_so_sanh) if bt_mac_dinh and bt_mac_dinh.g6_gia_so_sanh else None,
            'g6_sku': bt_mac_dinh.g6_sku if bt_mac_dinh else None,
            'g6_ten_danh_muc': self.g6_danh_muc.g6_ten_danh_muc if self.g6_danh_muc else None,
            'g6_ten_thuong_hieu': self.g6_thuong_hieu.g6_ten_thuong_hieu if self.g6_thuong_hieu else None,
        }


class G6BienTheSanPham(db.Model):
    __tablename__ = 'G6BienTheSanPham'

    g6_ma_bien_the = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_san_pham = db.Column(db.Integer, db.ForeignKey('G6SanPham.g6_ma_san_pham', ondelete='CASCADE'), nullable=False)
    g6_sku = db.Column(db.String(100), nullable=False, unique=True)
    g6_ten_bien_the = db.Column(db.String(100), nullable=False)  # "5Lbs - Chocolate"
    g6_trong_luong = db.Column(db.String(30))                    # "5Lbs","2Lbs","500g"
    g6_trong_luong_gram = db.Column(db.Integer)
    g6_so_luot_dung = db.Column(db.Integer)
    g6_huong_vi = db.Column(db.String(50))                       # "Chocolate","Vanilla"
    g6_gia = db.Column(db.Numeric(15, 0), nullable=False)
    g6_gia_so_sanh = db.Column(db.Numeric(15, 0))
    g6_hinh_anh = db.Column(db.String(500))
    g6_la_mac_dinh = db.Column(db.Boolean, nullable=False, default=False)
    g6_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    g6_thu_tu = db.Column(db.Integer, nullable=False, default=0)

    g6_san_pham = db.relationship('G6SanPham', back_populates='g6_bien_the')
    g6_dinh_duong = db.relationship('G6ThanhPhanDinhDuong', back_populates='g6_bien_the', uselist=False, cascade='all, delete-orphan')
    g6_ton_kho = db.relationship('G6TonKho', back_populates='g6_bien_the', cascade='all, delete-orphan')

    def g6_to_dict(self):
        return {
            'g6_ma_bien_the': self.g6_ma_bien_the,
            'g6_ma_san_pham': self.g6_ma_san_pham,
            'g6_sku': self.g6_sku,
            'g6_ten_bien_the': self.g6_ten_bien_the,
            'g6_trong_luong': self.g6_trong_luong,
            'g6_trong_luong_gram': self.g6_trong_luong_gram,
            'g6_so_luot_dung': self.g6_so_luot_dung,
            'g6_huong_vi': self.g6_huong_vi,
            'g6_gia': float(self.g6_gia),
            'g6_gia_so_sanh': float(self.g6_gia_so_sanh) if self.g6_gia_so_sanh else None,
            'g6_hinh_anh': self.g6_hinh_anh,
            'g6_la_mac_dinh': self.g6_la_mac_dinh,
            'g6_la_hoat_dong': self.g6_la_hoat_dong,
            'g6_thu_tu': self.g6_thu_tu,
        }


class G6HinhAnhSanPham(db.Model):
    __tablename__ = 'G6HinhAnhSanPham'

    g6_ma_hinh_anh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_san_pham = db.Column(db.Integer, db.ForeignKey('G6SanPham.g6_ma_san_pham', ondelete='NO ACTION'), nullable=False)
    g6_ma_bien_the = db.Column(db.Integer, db.ForeignKey('G6BienTheSanPham.g6_ma_bien_the', ondelete='NO ACTION'), nullable=True)
    g6_duong_dan = db.Column(db.String(500), nullable=False)
    g6_alt_text = db.Column(db.String(255))
    g6_thu_tu = db.Column(db.Integer, nullable=False, default=0)
    g6_la_anh_chinh = db.Column(db.Boolean, nullable=False, default=False)

    g6_san_pham = db.relationship('G6SanPham', back_populates='g6_hinh_anh')

    def g6_to_dict(self):
        return {
            'g6_ma_hinh_anh': self.g6_ma_hinh_anh,
            'g6_ma_san_pham': self.g6_ma_san_pham,
            'g6_ma_bien_the': self.g6_ma_bien_the,
            'g6_duong_dan': self.g6_duong_dan,
            'g6_alt_text': self.g6_alt_text,
            'g6_thu_tu': self.g6_thu_tu,
            'g6_la_anh_chinh': self.g6_la_anh_chinh,
        }


class G6ThanhPhanDinhDuong(db.Model):
    __tablename__ = 'G6ThanhPhanDinhDuong'

    g6_ma_dinh_duong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_bien_the = db.Column(db.Integer, db.ForeignKey('G6BienTheSanPham.g6_ma_bien_the', ondelete='CASCADE'), nullable=False, unique=True)
    g6_khau_phan = db.Column(db.Integer)
    g6_calo = db.Column(db.Integer)
    g6_protein = db.Column(db.Numeric(6, 2))
    g6_tinh_bot = db.Column(db.Numeric(6, 2))
    g6_chat_beo = db.Column(db.Numeric(6, 2))
    g6_duong = db.Column(db.Numeric(6, 2))
    g6_chat_xo = db.Column(db.Numeric(6, 2))
    g6_bcaa = db.Column(db.Numeric(6, 2))
    g6_glutamine = db.Column(db.Numeric(6, 2))
    g6_creatine = db.Column(db.Numeric(6, 2))
    g6_caffeine = db.Column(db.Numeric(6, 2))   # mg
    g6_thanh_phan_khac = db.Column(db.Text)      # JSON

    g6_bien_the = db.relationship('G6BienTheSanPham', back_populates='g6_dinh_duong')

    def g6_to_dict(self):
        def g6_f(v):
            return float(v) if v is not None else None
        return {
            'g6_ma_dinh_duong': self.g6_ma_dinh_duong,
            'g6_ma_bien_the': self.g6_ma_bien_the,
            'g6_khau_phan': self.g6_khau_phan,
            'g6_calo': self.g6_calo,
            'g6_protein': g6_f(self.g6_protein),
            'g6_tinh_bot': g6_f(self.g6_tinh_bot),
            'g6_chat_beo': g6_f(self.g6_chat_beo),
            'g6_duong': g6_f(self.g6_duong),
            'g6_chat_xo': g6_f(self.g6_chat_xo),
            'g6_bcaa': g6_f(self.g6_bcaa),
            'g6_glutamine': g6_f(self.g6_glutamine),
            'g6_creatine': g6_f(self.g6_creatine),
            'g6_caffeine': g6_f(self.g6_caffeine),
        }


class G6ChungNhanSanPham(db.Model):
    __tablename__ = 'G6ChungNhanSanPham'

    g6_ma_chung_nhan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_san_pham = db.Column(db.Integer, db.ForeignKey('G6SanPham.g6_ma_san_pham', ondelete='CASCADE'), nullable=False)
    g6_loai = db.Column(db.String(30), nullable=False)  # 'GMP','Halal','Kosher','FDA','DAVN'
    g6_so_chung_nhan = db.Column(db.String(100))
    g6_ngay_cap = db.Column(db.Date)
    g6_hinh_anh = db.Column(db.String(500))

    g6_san_pham = db.relationship('G6SanPham', back_populates='g6_chung_nhan')

    def g6_to_dict(self):
        return {
            'g6_ma_chung_nhan': self.g6_ma_chung_nhan,
            'g6_ma_san_pham': self.g6_ma_san_pham,
            'g6_loai': self.g6_loai,
            'g6_so_chung_nhan': self.g6_so_chung_nhan,
            'g6_ngay_cap': str(self.g6_ngay_cap) if self.g6_ngay_cap else None,
            'g6_hinh_anh': self.g6_hinh_anh,
        }


# ============================================================
# GROUP 11: KHO HÀNG
# ============================================================

class G6TonKho(db.Model):
    __tablename__ = 'G6TonKho'

    g6_ma_ton_kho = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_bien_the = db.Column(db.Integer, db.ForeignKey('G6BienTheSanPham.g6_ma_bien_the'), nullable=False)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh', ondelete='SET NULL'))
    g6_so_luong = db.Column(db.Integer, nullable=False, default=0)
    g6_so_luong_dat_truoc = db.Column(db.Integer, nullable=False, default=0)
    g6_nguong_canh_bao = db.Column(db.Integer, nullable=False, default=10)
    g6_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    g6_bien_the = db.relationship('G6BienTheSanPham', back_populates='g6_ton_kho')
    g6_chi_nhanh = db.relationship('G6ChiNhanh', backref='g6_ton_kho')

    def g6_to_dict(self):
        return {
            'g6_ma_ton_kho': self.g6_ma_ton_kho,
            'g6_ma_bien_the': self.g6_ma_bien_the,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_so_luong': self.g6_so_luong,
            'g6_so_luong_dat_truoc': self.g6_so_luong_dat_truoc,
            'g6_nguong_canh_bao': self.g6_nguong_canh_bao,
            'g6_ngay_cap_nhat': self.g6_ngay_cap_nhat.isoformat() if self.g6_ngay_cap_nhat else None,
            'g6_ten_san_pham': self.g6_bien_the.g6_san_pham.g6_ten_san_pham if self.g6_bien_the and self.g6_bien_the.g6_san_pham else None,
            'g6_ten_bien_the': self.g6_bien_the.g6_ten_bien_the if self.g6_bien_the else None,
            'g6_ten_chi_nhanh': self.g6_chi_nhanh.g6_ten_chi_nhanh if self.g6_chi_nhanh else None,
            'g6_so_luong_toi_thieu': self.g6_nguong_canh_bao
        }


class G6LichSuTonKho(db.Model):
    __tablename__ = 'G6LichSuTonKho'

    g6_ma_lich_su = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g6_ma_bien_the = db.Column(db.Integer, db.ForeignKey('G6BienTheSanPham.g6_ma_bien_the'), nullable=False)
    g6_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh', ondelete='SET NULL'))
    g6_loai_giao_dich = db.Column(db.String(20), nullable=False)  # 'nhap','xuat','dieu_chuyen','tra_hang','kiem_ke'
    g6_so_luong_thay_doi = db.Column(db.Integer, nullable=False)  # âm=xuất, dương=nhập
    g6_so_luong_truoc = db.Column(db.Integer, nullable=False)
    g6_so_luong_sau = db.Column(db.Integer, nullable=False)
    g6_ma_don_hang = db.Column(db.Integer, db.ForeignKey('G6DonHang.g6_ma_don_hang', ondelete='SET NULL'))
    g6_ghi_chu = db.Column(db.String(255))
    g6_nguoi_thuc_hien = db.Column(db.Integer, db.ForeignKey('G6NguoiDung.g6_ma_nguoi_dung', ondelete='SET NULL'))
    g6_thoi_gian = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def g6_to_dict(self):
        return {
            'g6_ma_lich_su': self.g6_ma_lich_su,
            'g6_ma_bien_the': self.g6_ma_bien_the,
            'g6_ma_chi_nhanh': self.g6_ma_chi_nhanh,
            'g6_loai_giao_dich': self.g6_loai_giao_dich,
            'g6_so_luong_thay_doi': self.g6_so_luong_thay_doi,
            'g6_so_luong_truoc': self.g6_so_luong_truoc,
            'g6_so_luong_sau': self.g6_so_luong_sau,
            'g6_ma_don_hang': self.g6_ma_don_hang,
            'g6_ghi_chu': self.g6_ghi_chu,
            'g6_thoi_gian': self.g6_thoi_gian.isoformat() if self.g6_thoi_gian else None,
        }
