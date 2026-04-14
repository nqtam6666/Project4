from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_chi_nhanh import G6ChiNhanh, G6ThietBi
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap

nqt_chi_nhanh_bp = Blueprint('g6_chi_nhanh', __name__, url_prefix='/api')


@nqt_chi_nhanh_bp.route('/nqt-chi-nhanh', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_tat_ca_chi_nhanh():
    nqt_tat_ca = request.args.get('g6_tat_ca', '0') == '1'
    nqt_q = G6ChiNhanh.query
    if not nqt_tat_ca:
        nqt_q = nqt_q.filter_by(g6_la_hoat_dong=True)
    nqt_list = nqt_q.order_by(G6ChiNhanh.g6_ma_chi_nhanh).all()
    return nqt_ok([c.g6_to_dict() for c in nqt_list])


@nqt_chi_nhanh_bp.route('/nqt-chi-nhanh/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_chi_nhanh(nqt_id):
    nqt_row = G6ChiNhanh.query.get_or_404(nqt_id)
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_chi_nhanh_bp.route('/nqt-chi-nhanh', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_chi_nhanh():
    nqt_data = request.get_json() or {}
    nqt_ten = nqt_data.get('g6_ten_chi_nhanh', '').strip()
    if not nqt_ten:
        return nqt_loi('Tên chi nhánh không được để trống')
    nqt_row = G6ChiNhanh(
        g6_ten_chi_nhanh=nqt_ten,
        g6_dia_chi=nqt_data.get('g6_dia_chi'),
        g6_thanh_pho=nqt_data.get('g6_thanh_pho'),
        g6_tinh=nqt_data.get('g6_tinh'),
        g6_hotline=nqt_data.get('g6_hotline'),
        g6_email=nqt_data.get('g6_email'),
        g6_suc_chua_toi_da=nqt_data.get('g6_suc_chua_toi_da'),
        g6_co_sauna=nqt_data.get('g6_co_sauna', False),
        g6_co_ho_boi=nqt_data.get('g6_co_ho_boi', False),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo chi nhánh thành công', 201)


@nqt_chi_nhanh_bp.route('/nqt-chi-nhanh/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_chi_nhanh(nqt_id):
    nqt_row = G6ChiNhanh.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    nqt_cap_nhat_fields = [
        'g6_ten_chi_nhanh', 'g6_dia_chi', 'g6_thanh_pho', 'g6_tinh',
        'g6_hotline', 'g6_email', 'g6_suc_chua_toi_da', 'g6_co_sauna',
        'g6_co_ho_boi', 'g6_la_hoat_dong', 'g6_google_maps_url',
    ]
    for nqt_f in nqt_cap_nhat_fields:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Cập nhật thành công')


@nqt_chi_nhanh_bp.route('/nqt-chi-nhanh/<int:nqt_id>/nqt-thiet-bi', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_thiet_bi_chi_nhanh(nqt_id):
    G6ChiNhanh.query.get_or_404(nqt_id)
    nqt_list = G6ThietBi.query.filter_by(g6_ma_chi_nhanh=nqt_id).all()
    return nqt_ok([t.g6_to_dict() for t in nqt_list])


@nqt_chi_nhanh_bp.route('/nqt-thiet-bi', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_thiet_bi():
    nqt_data = request.get_json() or {}
    nqt_ten = nqt_data.get('g6_ten_thiet_bi', '').strip()
    nqt_chi_nhanh_id = nqt_data.get('g6_ma_chi_nhanh')
    if not nqt_ten or not nqt_chi_nhanh_id:
        return nqt_loi('Thiếu tên thiết bị hoặc mã chi nhánh')
    G6ChiNhanh.query.get_or_404(nqt_chi_nhanh_id)
    nqt_row = G6ThietBi(
        g6_ma_chi_nhanh=nqt_chi_nhanh_id,
        g6_ten_thiet_bi=nqt_ten,
        g6_thuong_hieu=nqt_data.get('g6_thuong_hieu'),
        g6_model=nqt_data.get('g6_model'),
        g6_trang_thai=nqt_data.get('g6_trang_thai', 'hoat_dong'),
        g6_ghi_chu=nqt_data.get('g6_ghi_chu'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo thiết bị thành công', 201)


@nqt_chi_nhanh_bp.route('/nqt-thiet-bi/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_thiet_bi(nqt_id):
    nqt_row = G6ThietBi.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['g6_ten_thiet_bi', 'g6_trang_thai', 'g6_ngay_bao_tri_tiep', 'g6_ghi_chu']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict())
