from flask import Blueprint, jsonify
from backend.app.models import G6GoiTap, G6HuanLuyenVien, G6BaiViet
from backend.app.models.g6_cau_hinh import G6CauHinh

nqt_public_bp = Blueprint('nqt_public', __name__)

@nqt_public_bp.route('/api/nqt-public/cau-hinh-ui', methods=['GET'])
def nqt_public_cau_hinh_ui():
    nqt_khoa_cho_phep = ['g6_mau_chu_dao', 'g6_mau_phu', 'g6_ten_website', 'g6_logo_url']
    nqt_ds = G6CauHinh.query.filter(G6CauHinh.g6_khoa.in_(nqt_khoa_cho_phep)).all()
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': [c.g6_to_dict() for c in nqt_ds]
    })


@nqt_public_bp.route('/api/nqt-public/goi-tap', methods=['GET'])
def nqt_public_goi_tap():
    nqt_ds = G6GoiTap.query.filter_by(g6_la_hoat_dong=True).order_by(G6GoiTap.g6_gia).all()
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': [nqt_g.g6_to_dict() for nqt_g in nqt_ds]
    })


@nqt_public_bp.route('/api/nqt-public/huan-luyen-vien', methods=['GET'])
def nqt_public_huan_luyen_vien():
    nqt_ds = (
        G6HuanLuyenVien.query
        .filter_by(g6_la_hien_thi_web=True)
        .order_by(G6HuanLuyenVien.g6_thu_hang.desc())
        .limit(8)
        .all()
    )
    nqt_result = []
    for nqt_hlv in nqt_ds:
        nqt_item = nqt_hlv.g6_to_dict()
        if nqt_hlv.g6_nhan_vien:
            nqt_item['g6_ho_ten'] = nqt_hlv.g6_nhan_vien.g6_ho_ten
            nqt_item['g6_anh_dai_dien'] = getattr(nqt_hlv.g6_nhan_vien, 'g6_anh_dai_dien', None)
        nqt_result.append(nqt_item)
    return jsonify({'nqt_thanh_cong': True, 'nqt_du_lieu': nqt_result})


@nqt_public_bp.route('/api/nqt-public/blog', methods=['GET'])
def nqt_public_blog():
    nqt_ds = (
        G6BaiViet.query
        .filter_by(g6_trang_thai='da_xuat_ban')
        .order_by(G6BaiViet.g6_ngay_xuat_ban.desc())
        .limit(6)
        .all()
    )
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': [nqt_b.g6_to_dict() for nqt_b in nqt_ds]
    })
