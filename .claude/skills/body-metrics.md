# NQT - Body Metrics Time-Series

Theo dõi và vẽ biểu đồ chỉ số cơ thể hội viên. Tất cả tên theo tiền tố **nqt**.

## Usage
/body-metrics

## Model

```python
# app/models/nqt_chi_so_co_the.py
from app import db
from datetime import datetime

class NqtChiSoCoThe(db.Model):
    __tablename__ = 'NqtChiSoCoThe'

    nqt_ma_chi_so      = db.Column(db.Integer, primary_key=True)
    nqt_ma_hoi_vien    = db.Column(db.Integer, db.ForeignKey('NqtHoiVien.nqt_ma_hoi_vien'), nullable=False)

    # Chỉ số cốt lõi
    nqt_can_nang       = db.Column(db.Float)   # kg
    nqt_ti_le_mo       = db.Column(db.Float)   # %
    nqt_ti_le_co       = db.Column(db.Float)   # %

    # Chỉ số bổ sung
    nqt_vong_eo        = db.Column(db.Float)   # cm
    nqt_vong_nguc      = db.Column(db.Float)   # cm
    nqt_vong_hong      = db.Column(db.Float)   # cm

    nqt_ngay_do        = db.Column(db.Date, default=datetime.utcnow().date)
    nqt_ghi_chu        = db.Column(db.Text)
    nqt_ngay_tao       = db.Column(db.DateTime, default=datetime.utcnow)

    def nqt_chuyen_sang_dict(self) -> dict:
        return {
            'nqt_ma_chi_so':   self.nqt_ma_chi_so,
            'nqt_can_nang':    self.nqt_can_nang,
            'nqt_ti_le_mo':    self.nqt_ti_le_mo,
            'nqt_ti_le_co':    self.nqt_ti_le_co,
            'nqt_vong_eo':     self.nqt_vong_eo,
            'nqt_ngay_do':     self.nqt_ngay_do.isoformat(),
            'nqt_ghi_chu':     self.nqt_ghi_chu,
        }
```

## Service

```python
# app/services/nqt_dich_vu_chi_so.py
from app.models.nqt_chi_so_co_the import NqtChiSoCoThe
from app import db
from datetime import datetime, timedelta

class NqtDichVuChiSo:

    @staticmethod
    def nqt_ghi_nhan_chi_so(nqt_ma_hoi_vien: int, nqt_du_lieu: dict) -> NqtChiSoCoThe:
        nqt_chi_so = NqtChiSoCoThe(
            nqt_ma_hoi_vien = nqt_ma_hoi_vien,
            nqt_can_nang    = nqt_du_lieu.get('nqt_can_nang'),
            nqt_ti_le_mo    = nqt_du_lieu.get('nqt_ti_le_mo'),
            nqt_ti_le_co    = nqt_du_lieu.get('nqt_ti_le_co'),
            nqt_vong_eo     = nqt_du_lieu.get('nqt_vong_eo'),
            nqt_ngay_do     = nqt_du_lieu.get('nqt_ngay_do', datetime.now().date())
        )
        db.session.add(nqt_chi_so)
        db.session.commit()
        return nqt_chi_so

    @staticmethod
    def nqt_lay_lich_su(nqt_ma_hoi_vien: int, nqt_ngay_bat_dau=None, nqt_ngay_ket_thuc=None) -> dict:
        """Lấy dữ liệu time-series để vẽ biểu đồ."""
        nqt_truy_van = NqtChiSoCoThe.query.filter_by(nqt_ma_hoi_vien=nqt_ma_hoi_vien)

        if nqt_ngay_bat_dau:
            nqt_truy_van = nqt_truy_van.filter(NqtChiSoCoThe.nqt_ngay_do >= nqt_ngay_bat_dau)
        if nqt_ngay_ket_thuc:
            nqt_truy_van = nqt_truy_van.filter(NqtChiSoCoThe.nqt_ngay_do <= nqt_ngay_ket_thuc)

        nqt_danh_sach = nqt_truy_van.order_by(NqtChiSoCoThe.nqt_ngay_do).all()

        return {
            'nqt_nhan':      [cs.nqt_ngay_do.isoformat() for cs in nqt_danh_sach],
            'nqt_can_nang':  [cs.nqt_can_nang             for cs in nqt_danh_sach],
            'nqt_ti_le_mo':  [cs.nqt_ti_le_mo             for cs in nqt_danh_sach],
            'nqt_ti_le_co':  [cs.nqt_ti_le_co             for cs in nqt_danh_sach],
        }

    @staticmethod
    def nqt_tinh_tien_trinh(nqt_ma_hoi_vien: int, nqt_so_ngay: int = 30) -> dict:
        """Tính mức thay đổi trong khoảng thời gian."""
        nqt_ngay_ket_thuc  = datetime.now().date()
        nqt_ngay_bat_dau   = nqt_ngay_ket_thuc - timedelta(days=nqt_so_ngay)

        nqt_dau_ky = NqtChiSoCoThe.query.filter(
            NqtChiSoCoThe.nqt_ma_hoi_vien == nqt_ma_hoi_vien,
            NqtChiSoCoThe.nqt_ngay_do     >= nqt_ngay_bat_dau
        ).order_by(NqtChiSoCoThe.nqt_ngay_do).first()

        nqt_cuoi_ky = NqtChiSoCoThe.query.filter(
            NqtChiSoCoThe.nqt_ma_hoi_vien == nqt_ma_hoi_vien,
            NqtChiSoCoThe.nqt_ngay_do     <= nqt_ngay_ket_thuc
        ).order_by(NqtChiSoCoThe.nqt_ngay_do.desc()).first()

        if not nqt_dau_ky or not nqt_cuoi_ky:
            return None

        return {
            'nqt_thay_doi_can_nang': nqt_cuoi_ky.nqt_can_nang - nqt_dau_ky.nqt_can_nang,
            'nqt_thay_doi_ti_le_mo': nqt_cuoi_ky.nqt_ti_le_mo - nqt_dau_ky.nqt_ti_le_mo,
            'nqt_thay_doi_ti_le_co': nqt_cuoi_ky.nqt_ti_le_co - nqt_dau_ky.nqt_ti_le_co,
            'nqt_so_ngay':           nqt_so_ngay
        }
```

## Route

```python
# app/routes/nqt_chi_so_route.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.nqt_dich_vu_chi_so import NqtDichVuChiSo

nqt_chi_so_bp = Blueprint('nqt_chi_so', __name__)

@nqt_chi_so_bp.route('/nqt-chi-so', methods=['POST'])
@jwt_required()
def nqt_ghi_chi_so():
    nqt_ma_hoi_vien = get_jwt_identity()
    nqt_du_lieu     = request.get_json()
    nqt_chi_so      = NqtDichVuChiSo.nqt_ghi_nhan_chi_so(nqt_ma_hoi_vien, nqt_du_lieu)
    return jsonify({'nqt_thanh_cong': True, 'nqt_du_lieu': nqt_chi_so.nqt_chuyen_sang_dict()}), 201

@nqt_chi_so_bp.route('/nqt-chi-so/lich-su', methods=['GET'])
@jwt_required()
def nqt_lay_lich_su_chi_so():
    nqt_ma_hoi_vien  = get_jwt_identity()
    nqt_ngay_bat_dau = request.args.get('nqt_bat_dau')
    nqt_ngay_ket_thuc = request.args.get('nqt_ket_thuc')
    nqt_du_lieu      = NqtDichVuChiSo.nqt_lay_lich_su(nqt_ma_hoi_vien, nqt_ngay_bat_dau, nqt_ngay_ket_thuc)
    return jsonify({'nqt_thanh_cong': True, 'nqt_du_lieu': nqt_du_lieu})

@nqt_chi_so_bp.route('/nqt-chi-so/tien-trinh', methods=['GET'])
@jwt_required()
def nqt_lay_tien_trinh():
    nqt_ma_hoi_vien = get_jwt_identity()
    nqt_so_ngay     = request.args.get('nqt_so_ngay', 30, type=int)
    nqt_tien_trinh  = NqtDichVuChiSo.nqt_tinh_tien_trinh(nqt_ma_hoi_vien, nqt_so_ngay)
    return jsonify({'nqt_thanh_cong': True, 'nqt_du_lieu': nqt_tien_trinh})
```

## Frontend Chart

```javascript
// static/js/nqtBieuDoChiSo.js
class NqtBieuDoChiSo {

    async nqtTaiBieuDo(nqtNgayBatDau, nqtNgayKetThuc) {
        const nqtPhanHoi = await fetch(
            `/api/nqt-chi-so/lich-su?nqt_bat_dau=${nqtNgayBatDau}&nqt_ket_thuc=${nqtNgayKetThuc}`,
            { headers: { 'Authorization': `Bearer ${nqtLayToken()}` } }
        );
        const { nqt_du_lieu: nqtDuLieu } = await nqtPhanHoi.json();

        new Chart(document.getElementById('nqt-bieu-do-chi-so'), {
            type: 'line',
            data: {
                labels: nqtDuLieu.nqt_nhan,
                datasets: [
                    {
                        label: 'Cân nặng (kg)',
                        data: nqtDuLieu.nqt_can_nang,
                        borderColor: '#4CAF50',
                        tension: 0.1
                    },
                    {
                        label: 'Tỉ lệ mỡ (%)',
                        data: nqtDuLieu.nqt_ti_le_mo,
                        borderColor: '#FF5722',
                        tension: 0.1
                    },
                    {
                        label: 'Tỉ lệ cơ (%)',
                        data: nqtDuLieu.nqt_ti_le_co,
                        borderColor: '#2196F3',
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: { title: { display: true, text: 'Ngày' } },
                    y: { title: { display: true, text: 'Giá trị' } }
                }
            }
        });
    }
}

const nqtBieuDo = new NqtBieuDoChiSo();
```
