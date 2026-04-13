from flask import Blueprint, request
from backend.app import db
from backend.app.models.nqt_blog import NqtDanhMucBaiViet, NqtBaiViet, NqtDanhGiaSanPham
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap

nqt_blog_bp = Blueprint('nqt_blog', __name__, url_prefix='/api')


@nqt_blog_bp.route('/nqt-danh-muc-bai-viet', methods=['GET'])
def nqt_lay_danh_muc():
    nqt_list = NqtDanhMucBaiViet.query.filter_by(nqt_la_hoat_dong=True).order_by(NqtDanhMucBaiViet.nqt_thu_tu).all()
    return nqt_ok([d.nqt_to_dict() for d in nqt_list])


@nqt_blog_bp.route('/nqt-bai-viet', methods=['GET'])
def nqt_lay_bai_viet():
    nqt_trang = request.args.get('nqt_trang', 1, type=int)
    nqt_gioi_han = request.args.get('nqt_gioi_han', 10, type=int)
    nqt_danh_muc = request.args.get('nqt_ma_danh_muc', type=int)
    nqt_q = NqtBaiViet.query.filter_by(nqt_trang_thai='xuat_ban')
    if nqt_danh_muc:
        nqt_q = nqt_q.filter_by(nqt_ma_danh_muc=nqt_danh_muc)
    nqt_phan_trang = nqt_q.order_by(NqtBaiViet.nqt_ngay_xuat_ban.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'nqt_danh_sach': [b.nqt_to_dict() for b in nqt_phan_trang.items],
        'nqt_tong': nqt_phan_trang.total,
        'nqt_trang': nqt_trang,
    })


@nqt_blog_bp.route('/nqt-bai-viet/<string:nqt_slug>', methods=['GET'])
def nqt_lay_chi_tiet_bai_viet(nqt_slug):
    nqt_row = NqtBaiViet.query.filter_by(nqt_slug=nqt_slug, nqt_trang_thai='xuat_ban').first_or_404()
    nqt_row.nqt_luot_xem += 1
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_blog_bp.route('/nqt-bai-viet', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_bai_viet():
    nqt_data = request.get_json() or {}
    nqt_row = NqtBaiViet(
        nqt_ma_danh_muc=nqt_data.get('nqt_ma_danh_muc'),
        nqt_tieu_de=nqt_data.get('nqt_tieu_de', ''),
        nqt_slug=nqt_data.get('nqt_slug', ''),
        nqt_mo_ta_ngan=nqt_data.get('nqt_mo_ta_ngan'),
        nqt_noi_dung=nqt_data.get('nqt_noi_dung'),
        nqt_hinh_dai_dien=nqt_data.get('nqt_hinh_dai_dien'),
        nqt_trang_thai=nqt_data.get('nqt_trang_thai', 'nhap'),
        nqt_tu_khoa_seo=nqt_data.get('nqt_tu_khoa_seo'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Tạo bài viết thành công', 201)


@nqt_blog_bp.route('/nqt-bai-viet/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_bai_viet(nqt_id):
    nqt_row = NqtBaiViet.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['nqt_tieu_de', 'nqt_noi_dung', 'nqt_trang_thai', 'nqt_mo_ta_ngan', 'nqt_ngay_xuat_ban']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict())


# ---- ĐÁNH GIÁ SẢN PHẨM ----

@nqt_blog_bp.route('/nqt-danh-gia/<int:nqt_san_pham_id>', methods=['GET'])
def nqt_lay_danh_gia(nqt_san_pham_id):
    nqt_trang = request.args.get('nqt_trang', 1, type=int)
    nqt_q = NqtDanhGiaSanPham.query.filter_by(
        nqt_ma_san_pham=nqt_san_pham_id, nqt_trang_thai='da_duyet'
    )
    nqt_phan_trang = nqt_q.order_by(NqtDanhGiaSanPham.nqt_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=10, error_out=False
    )
    return nqt_ok({
        'nqt_danh_sach': [d.nqt_to_dict() for d in nqt_phan_trang.items],
        'nqt_tong': nqt_phan_trang.total,
    })


@nqt_blog_bp.route('/nqt-danh-gia', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_danh_gia():
    nqt_data = request.get_json() or {}
    nqt_sao = nqt_data.get('nqt_sao', 5)
    if not (1 <= int(nqt_sao) <= 5):
        return nqt_loi('Số sao không hợp lệ (1-5)')
    nqt_row = NqtDanhGiaSanPham(
        nqt_ma_san_pham=nqt_data.get('nqt_ma_san_pham'),
        nqt_ma_khach_hang=nqt_data.get('nqt_ma_khach_hang'),
        nqt_sao=nqt_sao,
        nqt_noi_dung=nqt_data.get('nqt_noi_dung'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Cảm ơn bạn đã đánh giá', 201)
