from flask import Blueprint, request
from backend.app import db
from backend.app.models.nqt_chi_nhanh import NqtChiNhanh, NqtThietBi
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap

nqt_chi_nhanh_bp = Blueprint('nqt_chi_nhanh', __name__, url_prefix='/api')


@nqt_chi_nhanh_bp.route('/nqt-chi-nhanh', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_tat_ca_chi_nhanh():
    nqt_tat_ca = request.args.get('nqt_tat_ca', '0') == '1'
    nqt_q = NqtChiNhanh.query
    if not nqt_tat_ca:
        nqt_q = nqt_q.filter_by(nqt_la_hoat_dong=True)
    nqt_list = nqt_q.order_by(NqtChiNhanh.nqt_ma_chi_nhanh).all()
    return nqt_ok([c.nqt_to_dict() for c in nqt_list])


@nqt_chi_nhanh_bp.route('/nqt-chi-nhanh/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_chi_nhanh(nqt_id):
    nqt_row = NqtChiNhanh.query.get_or_404(nqt_id)
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_chi_nhanh_bp.route('/nqt-chi-nhanh', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_chi_nhanh():
    nqt_data = request.get_json() or {}
    nqt_ten = nqt_data.get('nqt_ten_chi_nhanh', '').strip()
    if not nqt_ten:
        return nqt_loi('Tên chi nhánh không được để trống')
    nqt_row = NqtChiNhanh(
        nqt_ten_chi_nhanh=nqt_ten,
        nqt_dia_chi=nqt_data.get('nqt_dia_chi'),
        nqt_thanh_pho=nqt_data.get('nqt_thanh_pho'),
        nqt_tinh=nqt_data.get('nqt_tinh'),
        nqt_hotline=nqt_data.get('nqt_hotline'),
        nqt_email=nqt_data.get('nqt_email'),
        nqt_suc_chua_toi_da=nqt_data.get('nqt_suc_chua_toi_da'),
        nqt_co_sauna=nqt_data.get('nqt_co_sauna', False),
        nqt_co_ho_boi=nqt_data.get('nqt_co_ho_boi', False),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Tạo chi nhánh thành công', 201)


@nqt_chi_nhanh_bp.route('/nqt-chi-nhanh/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_chi_nhanh(nqt_id):
    nqt_row = NqtChiNhanh.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    nqt_cap_nhat_fields = [
        'nqt_ten_chi_nhanh', 'nqt_dia_chi', 'nqt_thanh_pho', 'nqt_tinh',
        'nqt_hotline', 'nqt_email', 'nqt_suc_chua_toi_da', 'nqt_co_sauna',
        'nqt_co_ho_boi', 'nqt_la_hoat_dong', 'nqt_google_maps_url',
    ]
    for nqt_f in nqt_cap_nhat_fields:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Cập nhật thành công')


@nqt_chi_nhanh_bp.route('/nqt-chi-nhanh/<int:nqt_id>/nqt-thiet-bi', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_thiet_bi_chi_nhanh(nqt_id):
    NqtChiNhanh.query.get_or_404(nqt_id)
    nqt_list = NqtThietBi.query.filter_by(nqt_ma_chi_nhanh=nqt_id).all()
    return nqt_ok([t.nqt_to_dict() for t in nqt_list])


@nqt_chi_nhanh_bp.route('/nqt-thiet-bi', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_thiet_bi():
    nqt_data = request.get_json() or {}
    nqt_ten = nqt_data.get('nqt_ten_thiet_bi', '').strip()
    nqt_chi_nhanh_id = nqt_data.get('nqt_ma_chi_nhanh')
    if not nqt_ten or not nqt_chi_nhanh_id:
        return nqt_loi('Thiếu tên thiết bị hoặc mã chi nhánh')
    NqtChiNhanh.query.get_or_404(nqt_chi_nhanh_id)
    nqt_row = NqtThietBi(
        nqt_ma_chi_nhanh=nqt_chi_nhanh_id,
        nqt_ten_thiet_bi=nqt_ten,
        nqt_thuong_hieu=nqt_data.get('nqt_thuong_hieu'),
        nqt_model=nqt_data.get('nqt_model'),
        nqt_trang_thai=nqt_data.get('nqt_trang_thai', 'hoat_dong'),
        nqt_ghi_chu=nqt_data.get('nqt_ghi_chu'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Tạo thiết bị thành công', 201)


@nqt_chi_nhanh_bp.route('/nqt-thiet-bi/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_thiet_bi(nqt_id):
    nqt_row = NqtThietBi.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['nqt_ten_thiet_bi', 'nqt_trang_thai', 'nqt_ngay_bao_tri_tiep', 'nqt_ghi_chu']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict())
