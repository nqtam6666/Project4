from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_van_chuyen import G6DonViVanChuyen, G6VungVanChuyen
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap

nqt_van_chuyen_bp = Blueprint('g6_van_chuyen', __name__, url_prefix='/api')


@nqt_van_chuyen_bp.route('/nqt-van-chuyen', methods=['GET'])
def nqt_lay_don_vi_van_chuyen():
    nqt_list = G6DonViVanChuyen.query.filter_by(g6_la_hoat_dong=True).all()
    return nqt_ok([d.g6_to_dict() for d in nqt_list])


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
    nqt_row = G6DonViVanChuyen(
        g6_ten=nqt_data.get('g6_ten', ''),
        g6_ma=nqt_data.get('g6_ma', ''),
        g6_logo=nqt_data.get('g6_logo'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo thành công', 201)


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
