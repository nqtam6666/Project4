from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_blog import G6DanhMucBaiViet, G6BaiViet, G6DanhGiaSanPham
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap

nqt_blog_bp = Blueprint('g6_blog', __name__, url_prefix='/api')


@nqt_blog_bp.route('/nqt-danh-muc-bai-viet', methods=['GET'])
def nqt_lay_danh_muc():
    nqt_list = G6DanhMucBaiViet.query.filter_by(g6_la_hoat_dong=True).order_by(G6DanhMucBaiViet.g6_thu_tu).all()
    return nqt_ok([d.g6_to_dict() for d in nqt_list])


@nqt_blog_bp.route('/nqt-bai-viet', methods=['GET'])
def nqt_lay_bai_viet():
    nqt_trang = request.args.get('g6_trang', 1, type=int)
    nqt_gioi_han = request.args.get('g6_gioi_han', 10, type=int)
    nqt_danh_muc = request.args.get('g6_ma_danh_muc', type=int)
    nqt_q = G6BaiViet.query.filter_by(g6_trang_thai='xuat_ban')
    if nqt_danh_muc:
        nqt_q = nqt_q.filter_by(g6_ma_danh_muc=nqt_danh_muc)
    nqt_phan_trang = nqt_q.order_by(G6BaiViet.g6_ngay_xuat_ban.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [b.g6_to_dict() for b in nqt_phan_trang.items],
        'g6_tong': nqt_phan_trang.total,
        'g6_trang': nqt_trang,
    })


@nqt_blog_bp.route('/nqt-bai-viet/<string:nqt_slug>', methods=['GET'])
def nqt_lay_chi_tiet_bai_viet(nqt_slug):
    nqt_row = G6BaiViet.query.filter_by(g6_slug=nqt_slug, g6_trang_thai='xuat_ban').first_or_404()
    nqt_row.g6_luot_xem += 1
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_blog_bp.route('/nqt-bai-viet', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_bai_viet():
    nqt_data = request.get_json() or {}
    nqt_row = G6BaiViet(
        g6_ma_danh_muc=nqt_data.get('g6_ma_danh_muc'),
        g6_tieu_de=nqt_data.get('g6_tieu_de', ''),
        g6_slug=nqt_data.get('g6_slug', ''),
        g6_mo_ta_ngan=nqt_data.get('g6_mo_ta_ngan'),
        g6_noi_dung=nqt_data.get('g6_noi_dung'),
        g6_hinh_dai_dien=nqt_data.get('g6_hinh_dai_dien'),
        g6_trang_thai=nqt_data.get('g6_trang_thai', 'nhap'),
        g6_tu_khoa_seo=nqt_data.get('g6_tu_khoa_seo'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo bài viết thành công', 201)


@nqt_blog_bp.route('/nqt-bai-viet/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_bai_viet(nqt_id):
    nqt_row = G6BaiViet.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['g6_tieu_de', 'g6_noi_dung', 'g6_trang_thai', 'g6_mo_ta_ngan', 'g6_ngay_xuat_ban']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict())


# ---- ĐÁNH GIÁ SẢN PHẨM ----

@nqt_blog_bp.route('/nqt-danh-gia/<int:nqt_san_pham_id>', methods=['GET'])
def nqt_lay_danh_gia(nqt_san_pham_id):
    nqt_trang = request.args.get('g6_trang', 1, type=int)
    nqt_q = G6DanhGiaSanPham.query.filter_by(
        g6_ma_san_pham=nqt_san_pham_id, g6_trang_thai='da_duyet'
    )
    nqt_phan_trang = nqt_q.order_by(G6DanhGiaSanPham.g6_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=10, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [d.g6_to_dict() for d in nqt_phan_trang.items],
        'g6_tong': nqt_phan_trang.total,
    })


@nqt_blog_bp.route('/nqt-danh-gia', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_danh_gia():
    nqt_data = request.get_json() or {}
    nqt_sao = nqt_data.get('g6_sao', 5)
    if not (1 <= int(nqt_sao) <= 5):
        return nqt_loi('Số sao không hợp lệ (1-5)')
    nqt_row = G6DanhGiaSanPham(
        g6_ma_san_pham=nqt_data.get('g6_ma_san_pham'),
        g6_ma_khach_hang=nqt_data.get('g6_ma_khach_hang'),
        g6_sao=nqt_sao,
        g6_noi_dung=nqt_data.get('g6_noi_dung'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Cảm ơn bạn đã đánh giá', 201)


@nqt_blog_bp.route('/nqt-bai-viet/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_bai_viet(nqt_id):
    nqt_row = G6BaiViet.query.get_or_404(nqt_id)
    nqt_row.g6_trang_thai = 'an'
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn bài viết')


@nqt_blog_bp.route('/nqt-danh-muc-bai-viet/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_danh_muc(nqt_id):
    nqt_row = G6DanhMucBaiViet.query.get_or_404(nqt_id)
    nqt_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã vô hiệu hóa danh mục')
