from backend.app import db
from datetime import datetime


class NxvLichSuBaoTri(db.Model):
    __tablename__ = 'NxvLichSuBaoTri'

    nxv_ma_bao_tri = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nxv_ma_thiet_bi = db.Column(db.Integer, db.ForeignKey('G6ThietBi.g6_ma_thiet_bi', ondelete='CASCADE'), nullable=False)
    nxv_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh', ondelete='NO ACTION'))
    nxv_loai = db.Column(db.String(30), nullable=False, default='dinh_ky')  # dinh_ky, dot_xuat, sua_chua
    nxv_ngay_bao_tri = db.Column(db.Date, nullable=False)
    nxv_ngay_hoan_thanh = db.Column(db.Date)
    nxv_nguoi_thuc_hien = db.Column(db.String(100))
    nxv_noi_dung = db.Column(db.Text, nullable=False)
    nxv_chi_phi = db.Column(db.Numeric(15, 0), nullable=False, default=0)
    nxv_ket_qua = db.Column(db.String(30), nullable=False, default='cho_xu_ly')  # cho_xu_ly, hoan_thanh, huy
    nxv_ghi_chu = db.Column(db.Text)
    nxv_ngay_bao_tri_tiep_theo = db.Column(db.Date)
    nxv_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    def nxv_to_dict(self):
        return {
            'nxv_ma_bao_tri': self.nxv_ma_bao_tri,
            'nxv_ma_thiet_bi': self.nxv_ma_thiet_bi,
            'nxv_ma_chi_nhanh': self.nxv_ma_chi_nhanh,
            'nxv_loai': self.nxv_loai,
            'nxv_ngay_bao_tri': str(self.nxv_ngay_bao_tri) if self.nxv_ngay_bao_tri else None,
            'nxv_ngay_hoan_thanh': str(self.nxv_ngay_hoan_thanh) if self.nxv_ngay_hoan_thanh else None,
            'nxv_nguoi_thuc_hien': self.nxv_nguoi_thuc_hien,
            'nxv_noi_dung': self.nxv_noi_dung,
            'nxv_chi_phi': float(self.nxv_chi_phi),
            'nxv_ket_qua': self.nxv_ket_qua,
            'nxv_ngay_bao_tri_tiep_theo': str(self.nxv_ngay_bao_tri_tiep_theo) if self.nxv_ngay_bao_tri_tiep_theo else None,
            'nxv_ngay_tao': self.nxv_ngay_tao.isoformat() if self.nxv_ngay_tao else None,
        }


class NxvPhieuSuaChua(db.Model):
    __tablename__ = 'NxvPhieuSuaChua'

    nxv_ma_phieu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nxv_ma_thiet_bi = db.Column(db.Integer, db.ForeignKey('G6ThietBi.g6_ma_thiet_bi', ondelete='CASCADE'), nullable=False)
    nxv_ma_chi_nhanh = db.Column(db.Integer, db.ForeignKey('G6ChiNhanh.g6_ma_chi_nhanh', ondelete='NO ACTION'))
    nxv_so_phieu = db.Column(db.String(30), nullable=False, unique=True)
    nxv_ngay_tao_phieu = db.Column(db.Date, nullable=False)
    nxv_mo_ta_su_co = db.Column(db.Text, nullable=False)
    nxv_don_vi_sua_chua = db.Column(db.String(200))
    nxv_chi_phi_du_kien = db.Column(db.Numeric(15, 0))
    nxv_chi_phi_thuc_te = db.Column(db.Numeric(15, 0))
    nxv_ngay_gui_sua = db.Column(db.Date)
    nxv_ngay_nhan_lai = db.Column(db.Date)
    nxv_trang_thai = db.Column(db.String(30), nullable=False, default='cho_xu_ly')
    nxv_ket_qua_sua_chua = db.Column(db.Text)
    nxv_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    g6_deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    def nxv_to_dict(self):
        return {
            'nxv_ma_phieu': self.nxv_ma_phieu,
            'nxv_ma_thiet_bi': self.nxv_ma_thiet_bi,
            'nxv_ma_chi_nhanh': self.nxv_ma_chi_nhanh,
            'nxv_so_phieu': self.nxv_so_phieu,
            'nxv_ngay_tao_phieu': str(self.nxv_ngay_tao_phieu) if self.nxv_ngay_tao_phieu else None,
            'nxv_mo_ta_su_co': self.nxv_mo_ta_su_co,
            'nxv_don_vi_sua_chua': self.nxv_don_vi_sua_chua,
            'nxv_chi_phi_du_kien': float(self.nxv_chi_phi_du_kien) if self.nxv_chi_phi_du_kien else None,
            'nxv_chi_phi_thuc_te': float(self.nxv_chi_phi_thuc_te) if self.nxv_chi_phi_thuc_te else None,
            'nxv_ngay_gui_sua': str(self.nxv_ngay_gui_sua) if self.nxv_ngay_gui_sua else None,
            'nxv_ngay_nhan_lai': str(self.nxv_ngay_nhan_lai) if self.nxv_ngay_nhan_lai else None,
            'nxv_trang_thai': self.nxv_trang_thai,
            'nxv_ket_qua_sua_chua': self.nxv_ket_qua_sua_chua,
            'nxv_ngay_tao': self.nxv_ngay_tao.isoformat() if self.nxv_ngay_tao else None,
        }
