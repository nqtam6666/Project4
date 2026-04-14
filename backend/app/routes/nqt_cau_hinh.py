from flask import Blueprint, request
from backend.app import db
from backend.app.models.nqt_cau_hinh import NqtCauHinh
from backend.app.services.nqt_dich_vu_cau_hinh import NqtDichVuCauHinh
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen

nqt_cau_hinh_bp = Blueprint('nqt_cau_hinh', __name__, url_prefix='/api')


@nqt_cau_hinh_bp.route('/nqt-cau-hinh', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_xem_cau_hinh')
def nqt_lay_cau_hinh():
    nqt_nhom = request.args.get('nqt_nhom')
    nqt_q = NqtCauHinh.query
    if nqt_nhom:
        nqt_q = nqt_q.filter_by(nqt_nhom=nqt_nhom)
    nqt_list = nqt_q.order_by(NqtCauHinh.nqt_nhom, NqtCauHinh.nqt_khoa).all()
    return nqt_ok([c.nqt_to_dict() for c in nqt_list])


@nqt_cau_hinh_bp.route('/nqt-cau-hinh/<string:nqt_khoa>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_mot_cau_hinh(nqt_khoa):
    nqt_row = NqtCauHinh.query.filter_by(nqt_khoa=nqt_khoa).first()
    if not nqt_row:
        return nqt_loi('Không tìm thấy cấu hình', nqt_ma_trang=404)
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_cau_hinh_bp.route('/nqt-cau-hinh', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_sua_cau_hinh')
def nqt_cap_nhat_cau_hinh():
    nqt_data = request.get_json() or {}
    if not isinstance(nqt_data, dict):
        return nqt_loi('Dữ liệu không hợp lệ')
    nqt_nhom = nqt_data.pop('nqt_nhom', 'website')
    nqt_da_cap_nhat = []
    for nqt_khoa, nqt_gia_tri in nqt_data.items():
        NqtDichVuCauHinh.nqt_cap_nhat(nqt_khoa, nqt_gia_tri, nqt_nhom)
        nqt_da_cap_nhat.append(nqt_khoa)
    NqtDichVuCauHinh.nqt_xoa_cache()
    return nqt_ok({'nqt_da_cap_nhat': nqt_da_cap_nhat}, 'Cập nhật thành công')
