from flask import Blueprint, jsonify
from sqlalchemy import func
from backend.app import db
from backend.app.models.g6_nguoi_dung import G6NguoiDung
from backend.app.models import (
    G6GoiTap, G6HuanLuyenVien, G6BaiViet,
    G6DichVuPhu, G6LopHoc, G6ChiNhanh
)
from backend.app.models.nxv_danh_gia import NxvDanhGiaHLV
from backend.app.models.g6_cau_hinh import G6CauHinh

nqt_public_bp = Blueprint('nqt_public', __name__)

@nqt_public_bp.route('/api/nqt-public/cau-hinh-ui', methods=['GET'])
def nqt_public_cau_hinh_ui():
    nqt_khoa_cho_phep = ['g6_mau_chu_dao', 'g6_mau_phu', 'g6_ten_website', 'g6_logo_url', 'g6_slogan', 'g6_favicon_url']
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


@nqt_public_bp.route('/api/nqt-public/stats', methods=['GET'])
def nqt_public_stats():
    nqt_total_members = G6NguoiDung.query.filter_by(g6_la_hoi_vien=True).count()
    nqt_total_trainers = G6HuanLuyenVien.query.count()
    nqt_avg_rating = db.session.query(func.avg(NxvDanhGiaHLV.nxv_sao)).scalar() or 5.0
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': {
            'total_members': nqt_total_members,
            'total_trainers': nqt_total_trainers,
            'avg_rating': round(float(nqt_avg_rating), 1)
        }
    })


@nqt_public_bp.route('/api/nqt-public/services', methods=['GET'])
def nqt_public_services():
    nqt_ds = G6DichVuPhu.query.all()
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': [s.g6_to_dict() for s in nqt_ds]
    })


@nqt_public_bp.route('/api/nqt-public/classes', methods=['GET'])
def nqt_public_classes():
    nqt_ds = G6LopHoc.query.limit(6).all()
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': [c.g6_to_dict() for c in nqt_ds]
    })


@nqt_public_bp.route('/api/nqt-public/testimonials', methods=['GET'])
def nqt_public_testimonials():
    nqt_ds = NxvDanhGiaHLV.query.filter_by(nxv_trang_thai='da_duyet').order_by(NxvDanhGiaHLV.nxv_ngay_tao.desc()).limit(10).all()
    nqt_result = []
    for t in nqt_ds:
        item = t.nxv_to_dict()
        if t.nxv_ma_hoi_vien:
            # Assuming G6HoiVien has g6_ho_ten via relationship or similar
            # In this project models usually have g6_nhan_vien or similar
            # Let's just use the content for now
            pass
        nqt_result.append(item)
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': nqt_result
    })


@nqt_public_bp.route('/api/nqt-public/branches', methods=['GET'])
def nqt_public_branches():
    nqt_ds = G6ChiNhanh.query.all()
    return jsonify({
        'nqt_thanh_cong': True,
        'nqt_du_lieu': [b.g6_to_dict() for b in nqt_ds]
    })
