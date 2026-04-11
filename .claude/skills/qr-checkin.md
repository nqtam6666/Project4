# NQT - QR Code Check-in System

Tạo và xác thực QR check-in cho hội viên. Tất cả tên theo tiền tố **nqt**.

## Usage
/qr-checkin

## 1. Tạo mã QR

```python
# app/services/nqt_dich_vu_qr.py
import qrcode, io, base64, hashlib
from datetime import datetime

class NqtDichVuQR:

    @staticmethod
    def nqt_tao_ma_qr_hoi_vien(nqt_ma_hoi_vien: int, nqt_khoa_bi_mat: str) -> str:
        """Tạo mã QR duy nhất cho hội viên (hết hạn theo ngày)."""

        nqt_ngay_hom_nay  = datetime.now().strftime('%Y%m%d')
        nqt_chuoi_goc     = f"{nqt_ma_hoi_vien}:{nqt_ngay_hom_nay}:{nqt_khoa_bi_mat}"
        nqt_ma_bam        = hashlib.sha256(nqt_chuoi_goc.encode()).hexdigest()[:16]
        nqt_noi_dung_qr   = f"NQT:{nqt_ma_hoi_vien}:{nqt_ma_bam}"

        nqt_qr = qrcode.QRCode(version=1, box_size=10, border=5)
        nqt_qr.add_data(nqt_noi_dung_qr)
        nqt_qr.make(fit=True)

        nqt_anh    = nqt_qr.make_image(fill_color='black', back_color='white')
        nqt_buffer = io.BytesIO()
        nqt_anh.save(nqt_buffer, format='PNG')

        return base64.b64encode(nqt_buffer.getvalue()).decode()

    @staticmethod
    def nqt_xac_thuc_ma_qr(nqt_noi_dung: str, nqt_khoa_bi_mat: str) -> bool:
        """Xác thực mã QR còn hiệu lực trong ngày."""
        try:
            nqt_phan       = nqt_noi_dung.split(':')
            if len(nqt_phan) != 3 or nqt_phan[0] != 'NQT':
                return False

            nqt_ma_hoi_vien   = nqt_phan[1]
            nqt_ma_bam_nhan   = nqt_phan[2]

            nqt_ngay_hom_nay  = datetime.now().strftime('%Y%m%d')
            nqt_chuoi_goc     = f"{nqt_ma_hoi_vien}:{nqt_ngay_hom_nay}:{nqt_khoa_bi_mat}"
            nqt_ma_bam_du_kien = hashlib.sha256(nqt_chuoi_goc.encode()).hexdigest()[:16]

            return nqt_ma_bam_nhan == nqt_ma_bam_du_kien
        except Exception:
            return False
```

## 2. Xử lý Check-in

```python
# app/services/nqt_dich_vu_diem_danh.py
from app.models.nqt_hoi_vien  import NqtHoiVien
from app.models.nqt_diem_danh import NqtDiemDanh
from app.models.nqt_goi_tap   import NqtGoiTap
from app.services.nqt_dich_vu_qr import NqtDichVuQR
from app import db
from datetime import datetime
from flask import current_app

class NqtDichVuDiemDanh:

    @staticmethod
    def nqt_xu_ly_diem_danh(nqt_noi_dung_qr: str) -> dict:
        """
        Xác thực QR và ghi nhận điểm danh.
        Returns: dict với nqt_thanh_cong, nqt_hoi_vien, nqt_thong_diep
        """
        nqt_khoa_bi_mat = current_app.config['NQT_QR_SECRET_KEY']

        # Xác thực mã QR
        if not NqtDichVuQR.nqt_xac_thuc_ma_qr(nqt_noi_dung_qr, nqt_khoa_bi_mat):
            return {'nqt_thanh_cong': False, 'nqt_thong_diep': 'Mã QR không hợp lệ hoặc đã hết hạn'}

        nqt_ma_hoi_vien = int(nqt_noi_dung_qr.split(':')[1])
        nqt_hoi_vien    = NqtHoiVien.query.get(nqt_ma_hoi_vien)

        if not nqt_hoi_vien:
            return {'nqt_thanh_cong': False, 'nqt_thong_diep': 'Không tìm thấy hội viên'}

        # Kiểm tra gói tập còn hạn
        nqt_goi_tap_hien_tai = NqtGoiTap.query.filter(
            NqtGoiTap.nqt_ma_hoi_vien == nqt_ma_hoi_vien,
            NqtGoiTap.nqt_trang_thai  == True,
            NqtGoiTap.nqt_ngay_het_han >= datetime.now().date()
        ).first()

        if not nqt_goi_tap_hien_tai:
            return {
                'nqt_thanh_cong':   False,
                'nqt_hoi_vien':     nqt_hoi_vien.nqt_chuyen_sang_dict(),
                'nqt_thong_diep':   'Gói tập đã hết hạn',
                'nqt_trang_thai_goi': 'het_han'
            }

        # Ghi nhận điểm danh
        nqt_diem_danh = NqtDiemDanh(
            nqt_ma_hoi_vien      = nqt_ma_hoi_vien,
            nqt_thoi_gian_vao    = datetime.now()
        )
        db.session.add(nqt_diem_danh)
        db.session.commit()

        nqt_so_ngay_con_lai = (nqt_goi_tap_hien_tai.nqt_ngay_het_han - datetime.now().date()).days

        return {
            'nqt_thanh_cong':     True,
            'nqt_hoi_vien':       nqt_hoi_vien.nqt_chuyen_sang_dict(),
            'nqt_thong_diep':     f'Chào mừng, {nqt_hoi_vien.nqt_ho_ten}!',
            'nqt_trang_thai_goi': 'hoat_dong',
            'nqt_so_ngay_con_lai': nqt_so_ngay_con_lai
        }
```

## 3. Route

```python
# app/routes/nqt_diem_danh_route.py
from flask import Blueprint, request, jsonify
from app.services.nqt_dich_vu_diem_danh import NqtDichVuDiemDanh
from app.services.nqt_dich_vu_qr        import NqtDichVuQR
from flask_jwt_extended import jwt_required, get_jwt_identity

nqt_diem_danh_bp = Blueprint('nqt_diem_danh', __name__)

@nqt_diem_danh_bp.route('/nqt-diem-danh', methods=['POST'])
def nqt_ghi_nhan_diem_danh():
    nqt_du_lieu   = request.get_json()
    nqt_noi_dung  = nqt_du_lieu.get('nqt_noi_dung_qr')
    nqt_ket_qua   = NqtDichVuDiemDanh.nqt_xu_ly_diem_danh(nqt_noi_dung)
    nqt_ma_http   = 200 if nqt_ket_qua['nqt_thanh_cong'] else 400
    return jsonify(nqt_ket_qua), nqt_ma_http

@nqt_diem_danh_bp.route('/nqt-ma-qr', methods=['GET'])
@jwt_required()
def nqt_lay_ma_qr_ca_nhan():
    """Hội viên lấy mã QR của mình."""
    from flask import current_app
    nqt_ma_hoi_vien = get_jwt_identity()
    nqt_anh_qr      = NqtDichVuQR.nqt_tao_ma_qr_hoi_vien(
        nqt_ma_hoi_vien,
        current_app.config['NQT_QR_SECRET_KEY']
    )
    return jsonify({'nqt_thanh_cong': True, 'nqt_anh_qr_base64': nqt_anh_qr})
```

## 4. Frontend Scanner

```javascript
// static/js/nqtDiemDanh.js
class NqtQuanLyDiemDanh {
    constructor() {
        this.nqtMayQuet = new Html5Qrcode('nqt-khung-quet');
    }

    async nqtBatDauQuet() {
        await this.nqtMayQuet.start(
            { facingMode: 'environment' },
            { fps: 10, qrbox: 250 },
            async (nqtNoiDungQr) => {
                await this.nqtXuLyKetQuaQet(nqtNoiDungQr);
            }
        );
    }

    async nqtXuLyKetQuaQet(nqtNoiDungQr) {
        const nqtPhanHoi = await fetch('/api/nqt-diem-danh', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nqt_noi_dung_qr: nqtNoiDungQr })
        });

        const nqtKetQua = await nqtPhanHoi.json();
        this.nqtHienThiKetQua(nqtKetQua);
    }

    nqtHienThiKetQua(nqtKetQua) {
        const nqtKhungKetQua = document.getElementById('nqt-ket-qua');
        nqtKhungKetQua.className = nqtKetQua.nqt_thanh_cong ? 'alert alert-success' : 'alert alert-danger';
        nqtKhungKetQua.textContent = nqtKetQua.nqt_thong_diep;
    }
}

const nqtDiemDanh = new NqtQuanLyDiemDanh();
```
