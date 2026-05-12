from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_van_chuyen import G6DonViVanChuyen, G6VungVanChuyen
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap

nqt_van_chuyen_bp = Blueprint('g6_van_chuyen', __name__, url_prefix='/api')


@nqt_van_chuyen_bp.route('/nqt-van-chuyen', methods=['GET'])
def nqt_lay_don_vi_van_chuyen():
    nqt_tat_ca = request.args.get('g6_tat_ca', '0') == '1'
    nqt_q = G6DonViVanChuyen.query
    if not nqt_tat_ca:
        nqt_q = nqt_q.filter_by(g6_la_hoat_dong=True)
    nqt_list = nqt_q.all()
    return nqt_ok([d.g6_to_dict() for d in nqt_list])


@nqt_van_chuyen_bp.route('/nqt-van-chuyen/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_don_vi(nqt_id):
    nqt_row = G6DonViVanChuyen.query.get_or_404(nqt_id)
    nqt_result = nqt_row.g6_to_dict()
    nqt_result['g6_vung'] = [v.g6_to_dict() for v in nqt_row.g6_vung]
    return nqt_ok(nqt_result)


@nqt_van_chuyen_bp.route('/nqt-van-chuyen/nqt-tinh-phi', methods=['POST'])
def nqt_tinh_phi_van_chuyen():
    nqt_data = request.get_json() or {}
    nqt_tinh = nqt_data.get('g6_tinh_thanh', '')
    nqt_don_vi_id = nqt_data.get('g6_ma_don_vi')
    nqt_trong_luong = float(nqt_data.get('g6_trong_luong_kg', 0))
    nqt_gia_tri_dh = float(nqt_data.get('g6_gia_tri_don_hang', 0))

    nqt_q = G6VungVanChuyen.query.filter(
        G6VungVanChuyen.g6_tinh_thanh.ilike(f'%{nqt_tinh}%')
    )
    if nqt_don_vi_id:
        nqt_q = nqt_q.filter_by(g6_ma_don_vi=nqt_don_vi_id)
    nqt_vung = nqt_q.first()
    if not nqt_vung:
        return nqt_ok({'g6_phi': 0, 'g6_mien_phi': False, 'g6_thong_bao': 'Chưa hỗ trợ khu vực này'})

    nqt_mien_phi = nqt_vung.g6_mien_phi_tu and nqt_gia_tri_dh >= float(nqt_vung.g6_mien_phi_tu)
    nqt_phi = 0 if nqt_mien_phi else float(nqt_vung.g6_phi_co_ban) + nqt_trong_luong * float(nqt_vung.g6_phi_theo_kg)
    return nqt_ok({
        'g6_phi': round(nqt_phi),
        'g6_mien_phi': nqt_mien_phi,
        'g6_thoi_gian_du_kien': nqt_vung.g6_thoi_gian_du_kien,
    })


@nqt_van_chuyen_bp.route('/nqt-van-chuyen', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_don_vi():
    nqt_data = request.get_json() or {}
    nqt_ten = nqt_data.get('g6_ten', '').strip()
    nqt_ma = nqt_data.get('g6_ma', '').strip().upper()
    if not nqt_ten or not nqt_ma:
        return nqt_loi('Thiếu tên hoặc mã đơn vị vận chuyển')
    nqt_row = G6DonViVanChuyen(
        g6_ten=nqt_ten,
        g6_ma=nqt_ma,
        g6_logo=nqt_data.get('g6_logo'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo thành công', 201)


@nqt_van_chuyen_bp.route('/nqt-van-chuyen/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_don_vi(nqt_id):
    nqt_row = G6DonViVanChuyen.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['g6_ten', 'g6_logo', 'g6_la_hoat_dong']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Cập nhật thành công')


@nqt_van_chuyen_bp.route('/nqt-van-chuyen/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_don_vi(nqt_id):
    nqt_row = G6DonViVanChuyen.query.get_or_404(nqt_id)
    nqt_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã vô hiệu hóa đơn vị vận chuyển')


@nqt_van_chuyen_bp.route('/nqt-van-chuyen/<int:nqt_id>/nqt-vung', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_vung_van_chuyen(nqt_id):
    G6DonViVanChuyen.query.get_or_404(nqt_id)
    nqt_list = G6VungVanChuyen.query.filter_by(g6_ma_don_vi=nqt_id).all()
    return nqt_ok([v.g6_to_dict() for v in nqt_list])


@nqt_van_chuyen_bp.route('/nqt-van-chuyen/<int:nqt_id>/nqt-vung', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_them_vung(nqt_id):
    G6DonViVanChuyen.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    nqt_row = G6VungVanChuyen(
        g6_ma_don_vi=nqt_id,
        g6_tinh_thanh=nqt_data.get('g6_tinh_thanh', ''),
        g6_phi_co_ban=nqt_data.get('g6_phi_co_ban', 0),
        g6_phi_theo_kg=nqt_data.get('g6_phi_theo_kg', 0),
        g6_mien_phi_tu=nqt_data.get('g6_mien_phi_tu'),
        g6_thoi_gian_du_kien=nqt_data.get('g6_thoi_gian_du_kien'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Thêm vùng thành công', 201)


@nqt_van_chuyen_bp.route('/nqt-vung-van-chuyen/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_vung(nqt_id):
    nqt_row = G6VungVanChuyen.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['g6_tinh_thanh', 'g6_phi_co_ban', 'g6_phi_theo_kg', 'g6_mien_phi_tu', 'g6_thoi_gian_du_kien']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Cập nhật vùng thành công')


@nqt_van_chuyen_bp.route('/nqt-vung-van-chuyen/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_vung(nqt_id):
    nqt_row = G6VungVanChuyen.query.get_or_404(nqt_id)
    db.session.delete(nqt_row)
    db.session.commit()
    return nqt_ok(None, 'Đã xoá vùng vận chuyển')

