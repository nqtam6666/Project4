# NQT - Dynamic Configuration System

Admin có thể chỉnh sửa TẤT CẢ cấu hình từ giao diện. Tất cả tên theo tiền tố **nqt**.

## Usage
/dynamic-config

## NGUYÊN TẮC: KHÔNG BAO GIỜ HARDCODE

```python
# ❌ SAI - KHÔNG BAO GIỜ LÀM THẾ NÀY
NQT_TEN_WEBSITE    = "Gym Pro"
NQT_JWT_HET_HAN    = 3600
NQT_NGAY_NHAC      = 3

# ✅ ĐÚNG - Luôn lấy từ NqtDichVuCauHinh
nqt_ten_website    = NqtDichVuCauHinh.nqt_lay('nqt_ten_website')
nqt_jwt_het_han    = NqtDichVuCauHinh.nqt_lay('nqt_jwt_thoi_gian_het_han', mac_dinh=3600)
nqt_ngay_nhac      = NqtDichVuCauHinh.nqt_lay('nqt_so_ngay_nhac_truoc_het_han', mac_dinh=3)
```

## Model

```python
# app/models/nqt_cau_hinh.py
from app import db
from datetime import datetime

class NqtCauHinh(db.Model):
    __tablename__ = 'NqtCauHinh'

    nqt_ma_cau_hinh      = db.Column(db.Integer, primary_key=True)
    nqt_khoa              = db.Column(db.String(100), unique=True, nullable=False, index=True)
    nqt_gia_tri           = db.Column(db.Text)
    nqt_kieu_du_lieu      = db.Column(db.String(20), default='string')
    nqt_nhom              = db.Column(db.String(50), nullable=False)
    nqt_ten_hien_thi      = db.Column(db.String(200))
    nqt_mo_ta             = db.Column(db.Text)
    nqt_la_bat_buoc       = db.Column(db.Boolean, default=False)
    nqt_la_cong_khai      = db.Column(db.Boolean, default=False)
    nqt_la_nhay_cam       = db.Column(db.Boolean, default=False)  # Ẩn khi hiển thị
    nqt_co_the_sua        = db.Column(db.Boolean, default=True)
    nqt_quy_tac_xac_thuc = db.Column(db.Text)   # JSON: {"min":1,"max":100}
    nqt_tuy_chon          = db.Column(db.Text)   # JSON cho select/dropdown
    nqt_thu_tu            = db.Column(db.Integer, default=0)
    nqt_cap_nhat_boi      = db.Column(db.Integer, db.ForeignKey('NqtNguoiDung.nqt_ma_nguoi_dung'))
    nqt_ngay_tao          = db.Column(db.DateTime, default=datetime.utcnow)
    nqt_ngay_cap_nhat     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def nqt_lay_gia_tri_dung_kieu(self):
        if self.nqt_gia_tri is None:
            return None
        if self.nqt_kieu_du_lieu == 'integer':
            return int(self.nqt_gia_tri)
        if self.nqt_kieu_du_lieu == 'float':
            return float(self.nqt_gia_tri)
        if self.nqt_kieu_du_lieu == 'boolean':
            return self.nqt_gia_tri.lower() in ('true', '1', 'yes')
        if self.nqt_kieu_du_lieu == 'json':
            import json
            return json.loads(self.nqt_gia_tri)
        return self.nqt_gia_tri


class NqtNhatKyDoiCauHinh(db.Model):
    """Ghi lại mọi thay đổi cấu hình."""
    __tablename__ = 'NqtNhatKyDoiCauHinh'

    nqt_ma_nhat_ky    = db.Column(db.Integer, primary_key=True)
    nqt_khoa          = db.Column(db.String(100), nullable=False)
    nqt_gia_tri_cu    = db.Column(db.Text)
    nqt_gia_tri_moi   = db.Column(db.Text)
    nqt_doi_boi       = db.Column(db.Integer, db.ForeignKey('NqtNguoiDung.nqt_ma_nguoi_dung'))
    nqt_thoi_diem_doi = db.Column(db.DateTime, default=datetime.utcnow)
    nqt_dia_chi_ip    = db.Column(db.String(50))
```

## Service với Caching

```python
# app/services/nqt_dich_vu_cau_hinh.py
import json
from typing import Any
from app.models.nqt_cau_hinh import NqtCauHinh, NqtNhatKyDoCauHinh
from app import db

class NqtDichVuCauHinh:
    _nqt_bo_nho_dem: dict = {}

    @classmethod
    def nqt_lay(cls, nqt_khoa: str, mac_dinh: Any = None) -> Any:
        """Lấy giá trị config theo khóa. Có bộ nhớ đệm."""
        if nqt_khoa in cls._nqt_bo_nho_dem:
            return cls._nqt_bo_nho_dem[nqt_khoa]

        nqt_cau_hinh = NqtCauHinh.query.filter_by(nqt_khoa=nqt_khoa).first()
        if nqt_cau_hinh is None:
            return mac_dinh

        nqt_gia_tri = nqt_cau_hinh.nqt_lay_gia_tri_dung_kieu()
        cls._nqt_bo_nho_dem[nqt_khoa] = nqt_gia_tri
        return nqt_gia_tri

    @classmethod
    def nqt_dat(cls, nqt_khoa: str, nqt_gia_tri_moi: Any, nqt_ma_nguoi_dung: int = None) -> bool:
        """Cập nhật giá trị config và ghi nhật ký."""
        nqt_cau_hinh = NqtCauHinh.query.filter_by(nqt_khoa=nqt_khoa).first()
        if not nqt_cau_hinh:
            return False
        if not nqt_cau_hinh.nqt_co_the_sua:
            raise ValueError(f"Cấu hình '{nqt_khoa}' không được phép sửa")

        nqt_gia_tri_cu = nqt_cau_hinh.nqt_gia_tri

        if nqt_cau_hinh.nqt_kieu_du_lieu == 'json':
            nqt_gia_tri_luu = json.dumps(nqt_gia_tri_moi)
        elif nqt_cau_hinh.nqt_kieu_du_lieu == 'boolean':
            nqt_gia_tri_luu = 'true' if nqt_gia_tri_moi else 'false'
        else:
            nqt_gia_tri_luu = str(nqt_gia_tri_moi)

        cls._nqt_xac_thuc_gia_tri(nqt_cau_hinh, nqt_gia_tri_luu)

        nqt_cau_hinh.nqt_gia_tri    = nqt_gia_tri_luu
        nqt_cau_hinh.nqt_cap_nhat_boi = nqt_ma_nguoi_dung

        nqt_nhat_ky = NqtNhatKyDoCauHinh(
            nqt_khoa        = nqt_khoa,
            nqt_gia_tri_cu  = nqt_gia_tri_cu,
            nqt_gia_tri_moi = nqt_gia_tri_luu,
            nqt_doi_boi     = nqt_ma_nguoi_dung
        )
        db.session.add(nqt_nhat_ky)
        db.session.commit()

        cls._nqt_bo_nho_dem.pop(nqt_khoa, None)
        return True

    @classmethod
    def nqt_lay_theo_nhom(cls, nqt_nhom: str) -> list:
        """Lấy tất cả config theo nhóm cho Admin UI."""
        nqt_danh_sach = NqtCauHinh.query\
            .filter_by(nqt_nhom=nqt_nhom)\
            .order_by(NqtCauHinh.nqt_thu_tu).all()

        return [{
            'nqt_khoa':       c.nqt_khoa,
            'nqt_gia_tri':    c.nqt_gia_tri if not c.nqt_la_nhay_cam else '••••••••',
            'nqt_kieu':       c.nqt_kieu_du_lieu,
            'nqt_ten':        c.nqt_ten_hien_thi,
            'nqt_mo_ta':      c.nqt_mo_ta,
            'nqt_bat_buoc':   c.nqt_la_bat_buoc,
            'nqt_co_the_sua': c.nqt_co_the_sua,
            'nqt_tuy_chon':   json.loads(c.nqt_tuy_chon) if c.nqt_tuy_chon else None,
        } for c in nqt_danh_sach]

    @classmethod
    def nqt_lay_cong_khai(cls) -> dict:
        """Lấy các config public cho frontend."""
        nqt_danh_sach = NqtCauHinh.query.filter_by(nqt_la_cong_khai=True).all()
        return {c.nqt_khoa: c.nqt_lay_gia_tri_dung_kieu() for c in nqt_danh_sach}

    @classmethod
    def nqt_xoa_bo_nho_dem(cls):
        cls._nqt_bo_nho_dem.clear()

    @classmethod
    def _nqt_xac_thuc_gia_tri(cls, nqt_cau_hinh: NqtCauHinh, nqt_gia_tri: str):
        if nqt_cau_hinh.nqt_la_bat_buoc and not nqt_gia_tri:
            raise ValueError(f"{nqt_cau_hinh.nqt_ten_hien_thi} là bắt buộc")
        if nqt_cau_hinh.nqt_quy_tac_xac_thuc:
            nqt_quy_tac = json.loads(nqt_cau_hinh.nqt_quy_tac_xac_thuc)
            if nqt_cau_hinh.nqt_kieu_du_lieu in ('integer', 'float'):
                nqt_so = float(nqt_gia_tri)
                if 'min' in nqt_quy_tac and nqt_so < nqt_quy_tac['min']:
                    raise ValueError(f"{nqt_cau_hinh.nqt_ten_hien_thi} phải >= {nqt_quy_tac['min']}")
                if 'max' in nqt_quy_tac and nqt_so > nqt_quy_tac['max']:
                    raise ValueError(f"{nqt_cau_hinh.nqt_ten_hien_thi} phải <= {nqt_quy_tac['max']}")
```

## API Endpoints

```python
# app/routes/nqt_cau_hinh_route.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators import nqt_yeu_cau_quyen_quan_tri
from app.services.nqt_dich_vu_cau_hinh import NqtDichVuCauHinh
from app.models.nqt_cau_hinh import NqtNhatKyDoCauHinh

nqt_cau_hinh_bp = Blueprint('nqt_cau_hinh', __name__)

@nqt_cau_hinh_bp.route('/cong-khai', methods=['GET'])
def nqt_lay_cau_hinh_cong_khai():
    return jsonify({'nqt_thanh_cong': True, 'nqt_du_lieu': NqtDichVuCauHinh.nqt_lay_cong_khai()})

@nqt_cau_hinh_bp.route('/nhom/<nqt_nhom>', methods=['GET'])
@jwt_required()
@nqt_yeu_cau_quyen_quan_tri
def nqt_lay_cau_hinh_theo_nhom(nqt_nhom: str):
    nqt_du_lieu = NqtDichVuCauHinh.nqt_lay_theo_nhom(nqt_nhom)
    return jsonify({'nqt_thanh_cong': True, 'nqt_du_lieu': nqt_du_lieu})

@nqt_cau_hinh_bp.route('/', methods=['PUT'])
@jwt_required()
@nqt_yeu_cau_quyen_quan_tri
def nqt_cap_nhat_nhieu_cau_hinh():
    nqt_ma_nguoi_dung = get_jwt_identity()
    nqt_du_lieu       = request.get_json()
    nqt_da_cap_nhat, nqt_loi = [], []

    for nqt_khoa, nqt_gia_tri in nqt_du_lieu.items():
        try:
            NqtDichVuCauHinh.nqt_dat(nqt_khoa, nqt_gia_tri, nqt_ma_nguoi_dung)
            nqt_da_cap_nhat.append(nqt_khoa)
        except Exception as nqt_e:
            nqt_loi.append({'nqt_khoa': nqt_khoa, 'nqt_loi': str(nqt_e)})

    return jsonify({
        'nqt_thanh_cong': len(nqt_loi) == 0,
        'nqt_du_lieu':    {'nqt_da_cap_nhat': nqt_da_cap_nhat},
        'nqt_loi':        nqt_loi
    })

@nqt_cau_hinh_bp.route('/nhat-ky/<nqt_khoa>', methods=['GET'])
@jwt_required()
@nqt_yeu_cau_quyen_quan_tri
def nqt_lay_nhat_ky_thay_doi(nqt_khoa: str):
    nqt_danh_sach = NqtNhatKyDoCauHinh.query\
        .filter_by(nqt_khoa=nqt_khoa)\
        .order_by(NqtNhatKyDoCauHinh.nqt_thoi_diem_doi.desc())\
        .limit(50).all()
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': [{
            'nqt_gia_tri_cu':    l.nqt_gia_tri_cu,
            'nqt_gia_tri_moi':   l.nqt_gia_tri_moi,
            'nqt_doi_boi':       l.nqt_doi_boi,
            'nqt_thoi_diem_doi': l.nqt_thoi_diem_doi.isoformat()
        } for l in nqt_danh_sach]
    })
```

## Seed Data (Default Configs)

```python
NQT_CAU_HINH_MAC_DINH = [
    # === WEBSITE ===
    {'khoa': 'nqt_ten_website',       'gia_tri': 'Gym Pro',         'kieu': 'string',  'nhom': 'website', 'ten': 'Tên Website',         'cong_khai': True,  'thu_tu': 1},
    {'khoa': 'nqt_logo',              'gia_tri': '/static/logo.png', 'kieu': 'string',  'nhom': 'website', 'ten': 'Logo',                'cong_khai': True,  'thu_tu': 2},
    {'khoa': 'nqt_slogan',            'gia_tri': '',                 'kieu': 'string',  'nhom': 'website', 'ten': 'Slogan',              'cong_khai': True,  'thu_tu': 3},
    {'khoa': 'nqt_so_dien_thoai',     'gia_tri': '',                 'kieu': 'string',  'nhom': 'website', 'ten': 'Số điện thoại',       'cong_khai': True,  'thu_tu': 4},
    {'khoa': 'nqt_email_lien_he',     'gia_tri': '',                 'kieu': 'email',   'nhom': 'website', 'ten': 'Email liên hệ',       'cong_khai': True,  'thu_tu': 5},
    {'khoa': 'nqt_dia_chi',           'gia_tri': '',                 'kieu': 'text',    'nhom': 'website', 'ten': 'Địa chỉ',             'cong_khai': True,  'thu_tu': 6},
    {'khoa': 'nqt_facebook',          'gia_tri': '',                 'kieu': 'url',     'nhom': 'website', 'ten': 'Facebook',            'cong_khai': True,  'thu_tu': 7},
    {'khoa': 'nqt_instagram',         'gia_tri': '',                 'kieu': 'url',     'nhom': 'website', 'ten': 'Instagram',           'cong_khai': True,  'thu_tu': 8},
    {'khoa': 'nqt_noi_dung_footer',   'gia_tri': '',                 'kieu': 'text',    'nhom': 'website', 'ten': 'Nội dung Footer',     'cong_khai': True,  'thu_tu': 9},

    # === KINH DOANH ===
    {'khoa': 'nqt_gio_mo_cua',                      'gia_tri': '06:00', 'kieu': 'string',  'nhom': 'kinh_doanh', 'ten': 'Giờ mở cửa',                          'cong_khai': True,  'thu_tu': 1},
    {'khoa': 'nqt_gio_dong_cua',                    'gia_tri': '22:00', 'kieu': 'string',  'nhom': 'kinh_doanh', 'ten': 'Giờ đóng cửa',                         'cong_khai': True,  'thu_tu': 2},
    {'khoa': 'nqt_so_ngay_nhac_truoc_het_han',      'gia_tri': '3',     'kieu': 'integer', 'nhom': 'kinh_doanh', 'ten': 'Số ngày nhắc trước hết hạn',           'quy_tac': '{"min":1,"max":30}', 'thu_tu': 3},
    {'khoa': 'nqt_thoi_luong_dat_lich_toi_thieu',   'gia_tri': '30',    'kieu': 'integer', 'nhom': 'kinh_doanh', 'ten': 'Thời gian booking tối thiểu (phút)',   'thu_tu': 4},
    {'khoa': 'nqt_thoi_luong_dat_lich_toi_da',      'gia_tri': '120',   'kieu': 'integer', 'nhom': 'kinh_doanh', 'ten': 'Thời gian booking tối đa (phút)',       'thu_tu': 5},
    {'khoa': 'nqt_so_ngay_dat_truoc_toi_da',        'gia_tri': '30',    'kieu': 'integer', 'nhom': 'kinh_doanh', 'ten': 'Đặt lịch trước tối đa (ngày)',         'thu_tu': 6},
    {'khoa': 'nqt_suc_chua_toi_da_phong',           'gia_tri': '100',   'kieu': 'integer', 'nhom': 'kinh_doanh', 'ten': 'Sức chứa tối đa phòng tập',            'thu_tu': 7},

    # === BẢO MẬT ===
    {'khoa': 'nqt_jwt_thoi_gian_het_han',     'gia_tri': '86400', 'kieu': 'integer', 'nhom': 'bao_mat', 'ten': 'Thời gian hết hạn token (giây)',    'thu_tu': 1},
    {'khoa': 'nqt_so_lan_dang_nhap_sai_toi_da','gia_tri': '5',   'kieu': 'integer', 'nhom': 'bao_mat', 'ten': 'Số lần đăng nhập sai tối đa',       'thu_tu': 2},
    {'khoa': 'nqt_thoi_gian_khoa_tai_khoan',  'gia_tri': '30',   'kieu': 'integer', 'nhom': 'bao_mat', 'ten': 'Thời gian khóa tài khoản (phút)',   'thu_tu': 3},
    {'khoa': 'nqt_do_dai_mat_khau_toi_thieu', 'gia_tri': '8',    'kieu': 'integer', 'nhom': 'bao_mat', 'ten': 'Độ dài mật khẩu tối thiểu',         'thu_tu': 4},
    {'khoa': 'nqt_yeu_cau_ky_tu_dac_biet',   'gia_tri': 'true', 'kieu': 'boolean', 'nhom': 'bao_mat', 'ten': 'Yêu cầu ký tự đặc biệt trong MK',  'thu_tu': 5},
    {'khoa': 'nqt_gioi_han_yeu_cau_moi_phut', 'gia_tri': '60',  'kieu': 'integer', 'nhom': 'bao_mat', 'ten': 'Rate limit (requests/phút)',         'thu_tu': 6},

    # === EMAIL ===
    {'khoa': 'nqt_smtp_may_chu',     'gia_tri': '',    'kieu': 'string',   'nhom': 'email', 'ten': 'SMTP Server',       'thu_tu': 1},
    {'khoa': 'nqt_smtp_cong',        'gia_tri': '587', 'kieu': 'integer',  'nhom': 'email', 'ten': 'SMTP Port',         'thu_tu': 2},
    {'khoa': 'nqt_smtp_tai_khoan',   'gia_tri': '',    'kieu': 'string',   'nhom': 'email', 'ten': 'SMTP Username',     'thu_tu': 3},
    {'khoa': 'nqt_smtp_mat_khau',    'gia_tri': '',    'kieu': 'password', 'nhom': 'email', 'ten': 'SMTP Password',     'nhay_cam': True, 'thu_tu': 4},
    {'khoa': 'nqt_ten_nguoi_gui',    'gia_tri': 'Gym Pro', 'kieu': 'string', 'nhom': 'email', 'ten': 'Tên người gửi', 'thu_tu': 5},

    # === THANH TOÁN ===
    {'khoa': 'nqt_don_vi_tien_te',      'gia_tri': 'VND',  'kieu': 'string', 'nhom': 'thanh_toan', 'ten': 'Đơn vị tiền tệ', 'cong_khai': True, 'thu_tu': 1},
    {'khoa': 'nqt_thue_vat',            'gia_tri': '10',   'kieu': 'float',  'nhom': 'thanh_toan', 'ten': 'Thuế VAT (%)',    'thu_tu': 2},
    {'khoa': 'nqt_phuong_thuc_thanh_toan','gia_tri': '["tien_mat","chuyen_khoan","momo"]', 'kieu': 'json', 'nhom': 'thanh_toan', 'ten': 'Phương thức thanh toán', 'thu_tu': 3},

    # === GIAO DIỆN ===
    {'khoa': 'nqt_mau_chu_dao',      'gia_tri': '#4CAF50', 'kieu': 'color',   'nhom': 'giao_dien', 'ten': 'Màu chủ đạo',        'cong_khai': True, 'thu_tu': 1},
    {'khoa': 'nqt_mau_phu',          'gia_tri': '#2196F3', 'kieu': 'color',   'nhom': 'giao_dien', 'ten': 'Màu phụ',            'cong_khai': True, 'thu_tu': 2},
    {'khoa': 'nqt_cho_phep_dark_mode','gia_tri': 'true',   'kieu': 'boolean', 'nhom': 'giao_dien', 'ten': 'Cho phép Dark Mode', 'cong_khai': True, 'thu_tu': 3},
]
```

## Frontend Admin UI

```javascript
// static/js/nqtQuanLyCauHinh.js
class NqtQuanLyCauHinh {

    async nqtTaiDanhSachNhom() {
        const nqtCacNhom = [
            { nqtKhoa: 'website',     nqtTen: 'Website',       nqtBieuTuong: 'globe' },
            { nqtKhoa: 'kinh_doanh',  nqtTen: 'Kinh doanh',    nqtBieuTuong: 'briefcase' },
            { nqtKhoa: 'bao_mat',     nqtTen: 'Bảo mật',       nqtBieuTuong: 'shield-lock' },
            { nqtKhoa: 'email',       nqtTen: 'Email',          nqtBieuTuong: 'envelope' },
            { nqtKhoa: 'thanh_toan',  nqtTen: 'Thanh toán',    nqtBieuTuong: 'credit-card' },
            { nqtKhoa: 'giao_dien',   nqtTen: 'Giao diện',     nqtBieuTuong: 'palette' },
        ];

        const nqtContainer = document.getElementById('nqt-danh-sach-nhom');
        nqtContainer.innerHTML = nqtCacNhom.map(nqtNhom => `
            <a href="#" class="list-group-item list-group-item-action"
               onclick="nqtQuanLyCauHinh.nqtTaiCauHinhTheoNhom('${nqtNhom.nqtKhoa}')">
                <i class="bi bi-${nqtNhom.nqtBieuTuong} me-2"></i>${nqtNhom.nqtTen}
            </a>
        `).join('');
    }

    async nqtTaiCauHinhTheoNhom(nqtNhom) {
        const nqtPhanHoi = await fetch(`/api/nqt-cau-hinh/nhom/${nqtNhom}`, {
            headers: { 'Authorization': `Bearer ${nqtLayToken()}` }
        });
        const { nqt_du_lieu: nqtDuLieu } = await nqtPhanHoi.json();

        document.getElementById('nqt-cac-truong').innerHTML =
            nqtDuLieu.map(nqtCfg => this.nqtVeTruongNhap(nqtCfg)).join('');
    }

    nqtVeTruongNhap(nqtCauHinh) {
        const nqtNhap = this._nqtChonLoaiInput(nqtCauHinh);
        return `
            <div class="mb-3">
                <label class="form-label fw-semibold">
                    ${nqtCauHinh.nqt_ten}
                    ${nqtCauHinh.nqt_bat_buoc ? '<span class="text-danger">*</span>' : ''}
                </label>
                ${nqtNhap}
                ${nqtCauHinh.nqt_mo_ta ? `<div class="form-text">${nqtCauHinh.nqt_mo_ta}</div>` : ''}
            </div>`;
    }

    _nqtChonLoaiInput(nqtCfg) {
        switch (nqtCfg.nqt_kieu) {
            case 'boolean':
                return `<div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox"
                           name="${nqtCfg.nqt_khoa}" ${nqtCfg.nqt_gia_tri === 'true' ? 'checked' : ''}
                           ${!nqtCfg.nqt_co_the_sua ? 'disabled' : ''}>
                </div>`;
            case 'text':
                return `<textarea class="form-control" name="${nqtCfg.nqt_khoa}" rows="3"
                                  ${!nqtCfg.nqt_co_the_sua ? 'disabled' : ''}>${nqtCfg.nqt_gia_tri || ''}</textarea>`;
            case 'color':
                return `<input type="color" class="form-control form-control-color"
                               name="${nqtCfg.nqt_khoa}" value="${nqtCfg.nqt_gia_tri || '#000000'}"
                               ${!nqtCfg.nqt_co_the_sua ? 'disabled' : ''}>`;
            case 'password':
                return `<input type="password" class="form-control"
                               name="${nqtCfg.nqt_khoa}" placeholder="••••••••"
                               ${!nqtCfg.nqt_co_the_sua ? 'disabled' : ''}>`;
            default:
                const nqtLoai = nqtCfg.nqt_kieu === 'integer' || nqtCfg.nqt_kieu === 'float' ? 'number'
                               : nqtCfg.nqt_kieu === 'email' ? 'email'
                               : nqtCfg.nqt_kieu === 'url'   ? 'url' : 'text';
                return `<input type="${nqtLoai}" class="form-control"
                               name="${nqtCfg.nqt_khoa}" value="${nqtCfg.nqt_gia_tri || ''}"
                               ${!nqtCfg.nqt_co_the_sua ? 'disabled' : ''}>`;
        }
    }

    async nqtLuuCauHinh(nqtForm) {
        const nqtDuLieu = Object.fromEntries(new FormData(nqtForm));

        const nqtPhanHoi = await fetch('/api/nqt-cau-hinh/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${nqtLayToken()}`
            },
            body: JSON.stringify(nqtDuLieu)
        });

        const nqtKetQua = await nqtPhanHoi.json();
        nqtKetQua.nqt_thanh_cong
            ? nqtHienThiThongBao('Đã lưu cấu hình thành công!', 'success')
            : nqtHienThiThongBao('Lỗi: ' + nqtKetQua.nqt_loi.map(e => e.nqt_loi).join(', '), 'error');
    }
}

const nqtQuanLyCauHinh = new NqtQuanLyCauHinh();
nqtQuanLyCauHinh.nqtTaiDanhSachNhom();

document.getElementById('nqt-form-cau-hinh').addEventListener('submit', async (nqtSuKien) => {
    nqtSuKien.preventDefault();
    await nqtQuanLyCauHinh.nqtLuuCauHinh(nqtSuKien.target);
});
```
