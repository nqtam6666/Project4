from flask import Blueprint, request
from backend.app.models.g6_xac_thuc import G6NhatKyHoatDong, G6PhienDangNhap
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen
from backend.app import db

nqt_quan_tri_bp = Blueprint('nqt_quan_tri', __name__, url_prefix='/api')


# ---- NHẬT KÝ HOẠT ĐỘNG ----

@nqt_quan_tri_bp.route('/nqt-nhat-ky-hoat-dong', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_lay_nhat_ky():
    nqt_trang = request.args.get('g6_trang', 1, type=int)
    nqt_gioi_han = request.args.get('g6_gioi_han', 50, type=int)
    nqt_hanh_dong = request.args.get('g6_hanh_dong')
    nqt_ten_bang = request.args.get('g6_ten_bang')
    nqt_nd_id = request.args.get('g6_ma_nguoi_dung', type=int)

    nqt_q = G6NhatKyHoatDong.query
    if nqt_hanh_dong:
        nqt_q = nqt_q.filter_by(g6_hanh_dong=nqt_hanh_dong)
    if nqt_ten_bang:
        nqt_q = nqt_q.filter_by(g6_ten_bang=nqt_ten_bang)
    if nqt_nd_id:
        nqt_q = nqt_q.filter_by(g6_ma_nguoi_dung=nqt_nd_id)

    nqt_phan_trang = nqt_q.order_by(G6NhatKyHoatDong.g6_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [n.g6_to_dict() for n in nqt_phan_trang.items],
        'g6_tong': nqt_phan_trang.total,
        'g6_trang': nqt_trang,
        'g6_tong_trang': nqt_phan_trang.pages,
    })


# ---- PHIÊN ĐĂNG NHẬP ----

@nqt_quan_tri_bp.route('/nqt-phien-dang-nhap', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_lay_phien_dang_nhap():
    nqt_trang = request.args.get('g6_trang', 1, type=int)
    nqt_gioi_han = request.args.get('g6_gioi_han', 20, type=int)
    nqt_loai = request.args.get('g6_loai_nguoi_dung')
    nqt_nd_id = request.args.get('g6_ma_nguoi_dung', type=int)
    nqt_con_hieu_luc = request.args.get('g6_con_hieu_luc', type=int)

    nqt_q = G6PhienDangNhap.query
    if nqt_loai:
        nqt_q = nqt_q.filter_by(g6_loai_nguoi_dung=nqt_loai)
    if nqt_nd_id:
        nqt_q = nqt_q.filter_by(g6_ma_nguoi_dung=nqt_nd_id)
    if nqt_con_hieu_luc == 1:
        nqt_q = nqt_q.filter_by(g6_la_thu_hoi=False)

    nqt_phan_trang = nqt_q.order_by(G6PhienDangNhap.g6_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [p.g6_to_dict() for p in nqt_phan_trang.items],
        'g6_tong': nqt_phan_trang.total,
        'g6_trang': nqt_trang,
    })


@nqt_quan_tri_bp.route('/nqt-phien-dang-nhap/<int:nqt_id>/nqt-thu-hoi', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_thu_hoi_phien(nqt_id):
    nqt_row = G6PhienDangNhap.query.get_or_404(nqt_id)
    nqt_row.g6_la_thu_hoi = True
    db.session.commit()
    return nqt_ok(None, 'Đã thu hồi phiên đăng nhập')


@nqt_quan_tri_bp.route('/nqt-phien-dang-nhap/nqt-thu-hoi-tat-ca', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_thu_hoi_tat_ca_phien():
    nqt_data = request.get_json() or {}
    nqt_nd_id = nqt_data.get('g6_ma_nguoi_dung')
    nqt_loai = nqt_data.get('g6_loai_nguoi_dung')
    if not nqt_nd_id or not nqt_loai:
        return nqt_loi('Thiếu mã người dùng hoặc loại')
    nqt_so_luong = G6PhienDangNhap.query.filter_by(
        g6_ma_nguoi_dung=nqt_nd_id,
        g6_loai_nguoi_dung=nqt_loai,
        g6_la_thu_hoi=False,
    ).update({'g6_la_thu_hoi': True})
    db.session.commit()
    return nqt_ok({'g6_so_phien_thu_hoi': nqt_so_luong}, 'Đã thu hồi tất cả phiên')
