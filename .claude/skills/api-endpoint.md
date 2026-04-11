# NQT - API Endpoint Generator

Tạo Flask RESTful API endpoint với đầy đủ CRUD, đặt tên theo chuẩn tiền tố **nqt**.

## Usage
/api-endpoint <ten_tai_nguyen>

## Quy tắc đặt tên bắt buộc

```python
# ✅ ĐÚNG
class NqtHoiVien(db.Model):           # Class: NqtPascalCase
    nqt_ma_hoi_vien = db.Column(...)   # Column: nqt_snake_case
    nqt_ho_ten = db.Column(...)

def nqt_lay_tat_ca_hoi_vien():         # Hàm: nqt_snake_case
def nqt_lay_hoi_vien_theo_id(nqt_ma):
def nqt_tao_hoi_vien():
def nqt_cap_nhat_hoi_vien(nqt_ma):
def nqt_xoa_hoi_vien(nqt_ma):

nqt_hoi_vien_bp = Blueprint(...)       # Blueprint: nqt_snake_case

# ❌ SAI - Thiếu tiền tố
class HoiVien():
def lay_tat_ca():
ho_ten = db.Column(...)
```

## Model Template

```python
# app/models/nqt_hoi_vien.py
from app import db
from datetime import datetime

class NqtHoiVien(db.Model):
    __tablename__ = 'NqtHoiVien'

    nqt_ma_hoi_vien = db.Column(db.Integer, primary_key=True)
    nqt_ho_ten      = db.Column(db.String(100), nullable=False)
    nqt_email       = db.Column(db.String(150), unique=True)
    nqt_so_dien_thoai = db.Column(db.String(15))
    nqt_trang_thai  = db.Column(db.Boolean, default=True)
    nqt_ngay_tao    = db.Column(db.DateTime, default=datetime.utcnow)
    nqt_ngay_cap_nhat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    nqt_da_xoa      = db.Column(db.Boolean, default=False)  # soft delete

    def nqt_chuyen_sang_dict(self) -> dict:
        return {
            'nqt_ma_hoi_vien':     self.nqt_ma_hoi_vien,
            'nqt_ho_ten':          self.nqt_ho_ten,
            'nqt_email':           self.nqt_email,
            'nqt_so_dien_thoai':   self.nqt_so_dien_thoai,
            'nqt_trang_thai':      self.nqt_trang_thai,
            'nqt_ngay_tao':        self.nqt_ngay_tao.isoformat(),
        }
```

## Service Template

```python
# app/services/nqt_dich_vu_hoi_vien.py
from app.models.nqt_hoi_vien import NqtHoiVien
from app import db

class NqtDichVuHoiVien:

    @staticmethod
    def nqt_lay_tat_ca(nqt_trang: int = 1, nqt_gioi_han: int = 20) -> list:
        return NqtHoiVien.query\
            .filter_by(nqt_da_xoa=False)\
            .paginate(page=nqt_trang, per_page=nqt_gioi_han)

    @staticmethod
    def nqt_lay_theo_ma(nqt_ma: int) -> NqtHoiVien:
        return NqtHoiVien.query.filter_by(
            nqt_ma_hoi_vien=nqt_ma,
            nqt_da_xoa=False
        ).first_or_404()

    @staticmethod
    def nqt_tao_moi(nqt_du_lieu: dict) -> NqtHoiVien:
        nqt_hoi_vien = NqtHoiVien(**nqt_du_lieu)
        db.session.add(nqt_hoi_vien)
        db.session.commit()
        return nqt_hoi_vien

    @staticmethod
    def nqt_cap_nhat(nqt_ma: int, nqt_du_lieu: dict) -> NqtHoiVien:
        nqt_hoi_vien = NqtDichVuHoiVien.nqt_lay_theo_ma(nqt_ma)
        for nqt_truong, nqt_gia_tri in nqt_du_lieu.items():
            setattr(nqt_hoi_vien, nqt_truong, nqt_gia_tri)
        db.session.commit()
        return nqt_hoi_vien

    @staticmethod
    def nqt_xoa_mem(nqt_ma: int) -> bool:
        nqt_hoi_vien = NqtDichVuHoiVien.nqt_lay_theo_ma(nqt_ma)
        nqt_hoi_vien.nqt_da_xoa = True
        db.session.commit()
        return True
```

## Route Template

```python
# app/routes/nqt_hoi_vien_route.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.nqt_dich_vu_hoi_vien import NqtDichVuHoiVien

nqt_hoi_vien_bp = Blueprint('nqt_hoi_vien', __name__)

@nqt_hoi_vien_bp.route('/', methods=['GET'])
@jwt_required()
def nqt_lay_tat_ca_hoi_vien():
    nqt_trang     = request.args.get('trang', 1, type=int)
    nqt_gioi_han  = request.args.get('gioi_han', 20, type=int)
    nqt_ket_qua   = NqtDichVuHoiVien.nqt_lay_tat_ca(nqt_trang, nqt_gioi_han)
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': [hv.nqt_chuyen_sang_dict() for hv in nqt_ket_qua.items],
        'nqt_tong': nqt_ket_qua.total
    })

@nqt_hoi_vien_bp.route('/<int:nqt_ma>', methods=['GET'])
@jwt_required()
def nqt_lay_hoi_vien_theo_ma(nqt_ma: int):
    nqt_hoi_vien = NqtDichVuHoiVien.nqt_lay_theo_ma(nqt_ma)
    return jsonify({'nqt_thanh_cong': True, 'nqt_du_lieu': nqt_hoi_vien.nqt_chuyen_sang_dict()})

@nqt_hoi_vien_bp.route('/', methods=['POST'])
@jwt_required()
def nqt_tao_hoi_vien():
    nqt_du_lieu  = request.get_json()
    nqt_hoi_vien = NqtDichVuHoiVien.nqt_tao_moi(nqt_du_lieu)
    return jsonify({'nqt_thanh_cong': True, 'nqt_du_lieu': nqt_hoi_vien.nqt_chuyen_sang_dict()}), 201

@nqt_hoi_vien_bp.route('/<int:nqt_ma>', methods=['PUT'])
@jwt_required()
def nqt_cap_nhat_hoi_vien(nqt_ma: int):
    nqt_du_lieu  = request.get_json()
    nqt_hoi_vien = NqtDichVuHoiVien.nqt_cap_nhat(nqt_ma, nqt_du_lieu)
    return jsonify({'nqt_thanh_cong': True, 'nqt_du_lieu': nqt_hoi_vien.nqt_chuyen_sang_dict()})

@nqt_hoi_vien_bp.route('/<int:nqt_ma>', methods=['DELETE'])
@jwt_required()
def nqt_xoa_hoi_vien(nqt_ma: int):
    NqtDichVuHoiVien.nqt_xoa_mem(nqt_ma)
    return jsonify({'nqt_thanh_cong': True, 'nqt_thong_diep': 'Đã xoá hội viên'})
```

## API Response Format chuẩn nqt
```json
{
  "nqt_thanh_cong": true,
  "nqt_du_lieu": {},
  "nqt_thong_diep": "Thành công",
  "nqt_loi": []
}
```
