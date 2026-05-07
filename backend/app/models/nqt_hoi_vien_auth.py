import bcrypt
from datetime import datetime, timedelta, timezone
from backend.app import db
from backend.app.services.g6_dich_vu_cau_hinh import NqtDichVuCauHinh


class NqtHoiVienAuth(db.Model):
    """Bảng xác thực hội viên — tách riêng khỏi G6HoiVien (thông tin cá nhân)."""
    __tablename__ = 'NqtHoiVienAuth'

    nqt_ma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nqt_ma_hoi_vien = db.Column(
        db.Integer,
        db.ForeignKey('G6HoiVien.g6_ma_hoi_vien', ondelete='CASCADE'),
        nullable=False, unique=True
    )
    nqt_mat_khau_hash = db.Column(db.String(255), nullable=False)
    nqt_la_hoat_dong = db.Column(db.Boolean, nullable=False, default=True)
    nqt_lan_dang_nhap_sai = db.Column(db.Integer, nullable=False, default=0)
    nqt_khoa_den = db.Column(db.DateTime, nullable=True)
    nqt_reset_token = db.Column(db.String(8), nullable=True)
    nqt_reset_token_het_han = db.Column(db.DateTime, nullable=True)
    nqt_ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    nqt_ngay_cap_nhat = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship
    nqt_hoi_vien = db.relationship('G6HoiVien', backref=db.backref('nqt_xac_thuc', uselist=False))

    # ── Password helpers ─────────────────────────────────────────────────────
    def nqt_dat_mat_khau(self, nqt_mat_khau_plain: str):
        self.nqt_mat_khau_hash = bcrypt.hashpw(
            nqt_mat_khau_plain.encode(), bcrypt.gensalt()
        ).decode()

    def nqt_kiem_tra_mat_khau(self, nqt_mat_khau_plain: str) -> bool:
        return bcrypt.checkpw(
            nqt_mat_khau_plain.encode(),
            self.nqt_mat_khau_hash.encode()
        )

    # ── Lockout helpers ─────────────────────────────────────────────────────
    def nqt_khoa_tai_khoan(self):
        nqt_phut = int(NqtDichVuCauHinh.g6_lay('nqt_khoa_hoi_vien_phut', nqt_mac_dinh=30))
        self.nqt_khoa_den = datetime.utcnow() + timedelta(minutes=nqt_phut)
        self.nqt_lan_dang_nhap_sai = 0

    def nqt_mo_khoa(self):
        self.nqt_khoa_den = None
        self.nqt_lan_dang_nhap_sai = 0

    # ── Serialize ────────────────────────────────────────────────────────────
    def nqt_to_dict(self):
        return {
            'nqt_ma': self.nqt_ma,
            'nqt_ma_hoi_vien': self.nqt_ma_hoi_vien,
            'nqt_la_hoat_dong': self.nqt_la_hoat_dong,
            'nqt_ngay_tao': self.nqt_ngay_tao.isoformat() if self.nqt_ngay_tao else None,
        }
