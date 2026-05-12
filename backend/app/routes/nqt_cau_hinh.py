from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_cau_hinh import G6CauHinh
from backend.app.services.g6_dich_vu_cau_hinh import NqtDichVuCauHinh
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen, nqt_ghi_nhat_ky

nqt_cau_hinh_bp = Blueprint('g6_cau_hinh', __name__, url_prefix='/api')


@nqt_cau_hinh_bp.route('/nqt-cau-hinh', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_xem_cau_hinh')
def nqt_lay_cau_hinh():
    nqt_nhom = request.args.get('g6_nhom')
    nqt_q = G6CauHinh.query
    if nqt_nhom:
        nqt_q = nqt_q.filter_by(g6_nhom=nqt_nhom)
    nqt_list = nqt_q.order_by(G6CauHinh.g6_nhom, G6CauHinh.g6_khoa).all()
    return nqt_ok([c.g6_to_dict() for c in nqt_list])


@nqt_cau_hinh_bp.route('/nqt-cau-hinh/<string:nqt_khoa>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_mot_cau_hinh(nqt_khoa):
    nqt_row = G6CauHinh.query.filter_by(g6_khoa=nqt_khoa).first()
    if not nqt_row:
        return nqt_loi('Không tìm thấy cấu hình', nqt_ma_trang=404)
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_cau_hinh_bp.route('/nqt-cau-hinh', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_sua_cau_hinh')
@nqt_ghi_nhat_ky('Cập nhật cấu hình', 'G6CauHinh')
def nqt_cap_nhat_cau_hinh():
    nqt_data = request.get_json() or {}
    if not isinstance(nqt_data, dict):
        return nqt_loi('Dữ liệu không hợp lệ')
    nqt_nhom = nqt_data.pop('g6_nhom', 'website')
    nqt_da_cap_nhat = []
    for nqt_khoa, nqt_gia_tri in nqt_data.items():
        NqtDichVuCauHinh.g6_cap_nhat(nqt_khoa, nqt_gia_tri, nqt_nhom)
        nqt_da_cap_nhat.append(nqt_khoa)
    NqtDichVuCauHinh.g6_xoa_cache()
    return nqt_ok({'g6_da_cap_nhat': nqt_da_cap_nhat}, 'Cập nhật thành công')
