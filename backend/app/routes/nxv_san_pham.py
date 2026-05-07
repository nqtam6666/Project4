from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_san_pham import (
    G6DanhMucSanPham, G6MucTieuSucKhoe, G6ThuongHieu,
    G6SanPham, G6BienTheSanPham, G6HinhAnhSanPham,
    G6ThanhPhanDinhDuong, G6ChungNhanSanPham,
    G6TonKho, G6LichSuTonKho,
)
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap

nxv_san_pham_bp = Blueprint('nxv_san_pham', __name__, url_prefix='/api')


# ============================================================
# DANH MỤC SẢN PHẨM
# ============================================================

@nxv_san_pham_bp.route('/nxv-danh-muc', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_danh_muc():
    nxv_chi = request.args.get('g6_ma_danh_muc_cha', type=int)
    nxv_q = G6DanhMucSanPham.query.filter_by(g6_la_hoat_dong=True)
    if nxv_chi is not None:
        nxv_q = nxv_q.filter_by(g6_ma_danh_muc_cha=nxv_chi if nxv_chi else None)
    return nqt_ok([d.g6_to_dict() for d in nxv_q.order_by(G6DanhMucSanPham.g6_thu_tu_hien_thi).all()])


@nxv_san_pham_bp.route('/nxv-danh-muc/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_chi_tiet_dm(nxv_id):
    return nqt_ok(G6DanhMucSanPham.query.get_or_404(nxv_id).g6_to_dict())


@nxv_san_pham_bp.route('/nxv-danh-muc', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_danh_muc():
    nxv_data = request.get_json() or {}
    nxv_ten = nxv_data.get('g6_ten_danh_muc', '').strip()
    nxv_slug = nxv_data.get('g6_slug', '').strip()
    if not nxv_ten or not nxv_slug:
        return nqt_loi('Thiếu tên hoặc slug danh mục')
    if G6DanhMucSanPham.query.filter_by(g6_slug=nxv_slug).first():
        return nqt_loi('Slug đã tồn tại')

    nxv_row = G6DanhMucSanPham(
        g6_ten_danh_muc=nxv_ten,
        g6_slug=nxv_slug,
        g6_ma_danh_muc_cha=nxv_data.get('g6_ma_danh_muc_cha'),
        g6_mo_ta=nxv_data.get('g6_mo_ta'),
        g6_hinh_anh=nxv_data.get('g6_hinh_anh'),
        g6_thu_tu_hien_thi=nxv_data.get('g6_thu_tu_hien_thi', 0),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo danh mục thành công', 201)


@nxv_san_pham_bp.route('/nxv-danh-muc/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_dm(nxv_id):
    nxv_row = G6DanhMucSanPham.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['g6_ten_danh_muc', 'g6_mo_ta', 'g6_hinh_anh',
                  'g6_thu_tu_hien_thi', 'g6_la_hien_thi_menu', 'g6_la_hoat_dong']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_san_pham_bp.route('/nxv-danh-muc/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_dm(nxv_id):
    nxv_row = G6DanhMucSanPham.query.get_or_404(nxv_id)
    nxv_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn danh mục')


# ============================================================
# MỤC TIÊU SỨC KHỎE
# ============================================================

@nxv_san_pham_bp.route('/nxv-muc-tieu', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_muc_tieu():
    return nqt_ok([m.g6_to_dict() for m in G6MucTieuSucKhoe.query.all()])


@nxv_san_pham_bp.route('/nxv-muc-tieu', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_muc_tieu():
    nxv_data = request.get_json() or {}
    nxv_ten = nxv_data.get('g6_ten_muc_tieu', '').strip()
    nxv_slug = nxv_data.get('g6_slug', '').strip()
    if not nxv_ten or not nxv_slug:
        return nqt_loi('Thiếu tên hoặc slug mục tiêu')

    nxv_row = G6MucTieuSucKhoe(
        g6_ten_muc_tieu=nxv_ten,
        g6_slug=nxv_slug,
        g6_bieu_tuong=nxv_data.get('g6_bieu_tuong'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo mục tiêu thành công', 201)


@nxv_san_pham_bp.route('/nxv-muc-tieu/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_muc_tieu(nxv_id):
    nxv_row = G6MucTieuSucKhoe.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['g6_ten_muc_tieu', 'g6_bieu_tuong']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_san_pham_bp.route('/nxv-muc-tieu/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_muc_tieu(nxv_id):
    nxv_row = G6MucTieuSucKhoe.query.get_or_404(nxv_id)
    db.session.delete(nxv_row)
    db.session.commit()
    return nqt_ok(None, 'Xóa mục tiêu thành công')


# ============================================================
# THƯƠNG HIỆU
# ============================================================

@nxv_san_pham_bp.route('/nxv-thuong-hieu', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_thuong_hieu():
    nxv_q = G6ThuongHieu.query.filter_by(g6_la_hoat_dong=True)
    nxv_noi_bat = request.args.get('g6_la_noi_bat', type=int)
    if nxv_noi_bat is not None:
        nxv_q = nxv_q.filter_by(g6_la_noi_bat=bool(nxv_noi_bat))
    return nqt_ok([t.g6_to_dict() for t in nxv_q.order_by(G6ThuongHieu.g6_thu_tu_hien_thi).all()])


@nxv_san_pham_bp.route('/nxv-thuong-hieu/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_chi_tiet_th(nxv_id):
    return nqt_ok(G6ThuongHieu.query.get_or_404(nxv_id).g6_to_dict())


@nxv_san_pham_bp.route('/nxv-thuong-hieu', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_thuong_hieu():
    nxv_data = request.get_json() or {}
    nxv_ten = nxv_data.get('g6_ten_thuong_hieu', '').strip()
    nxv_slug = nxv_data.get('g6_slug', '').strip()
    if not nxv_ten or not nxv_slug:
        return nqt_loi('Thiếu tên hoặc slug thương hiệu')
    if G6ThuongHieu.query.filter_by(g6_slug=nxv_slug).first():
        return nqt_loi('Slug đã tồn tại')

    nxv_row = G6ThuongHieu(
        g6_ten_thuong_hieu=nxv_ten,
        g6_slug=nxv_slug,
        g6_nuoc_xuat_xu=nxv_data.get('g6_nuoc_xuat_xu'),
        g6_logo=nxv_data.get('g6_logo'),
        g6_mo_ta=nxv_data.get('g6_mo_ta'),
        g6_website=nxv_data.get('g6_website'),
        g6_la_noi_bat=nxv_data.get('g6_la_noi_bat', False),
        g6_thu_tu_hien_thi=nxv_data.get('g6_thu_tu_hien_thi', 0),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo thương hiệu thành công', 201)


@nxv_san_pham_bp.route('/nxv-thuong-hieu/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_th(nxv_id):
    nxv_row = G6ThuongHieu.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['g6_ten_thuong_hieu', 'g6_nuoc_xuat_xu', 'g6_logo', 'g6_mo_ta',
                  'g6_website', 'g6_la_noi_bat', 'g6_thu_tu_hien_thi', 'g6_la_hoat_dong']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_san_pham_bp.route('/nxv-thuong-hieu/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_th(nxv_id):
    nxv_row = G6ThuongHieu.query.get_or_404(nxv_id)
    nxv_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn thương hiệu')


# ============================================================
# SẢN PHẨM
# ============================================================

@nxv_san_pham_bp.route('/nxv-san-pham', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_san_pham():
    nxv_trang = request.args.get('g6_trang', 1, type=int)
    nxv_gioi_han = request.args.get('g6_gioi_han', 20, type=int)
    nxv_dm_id = request.args.get('g6_ma_danh_muc', type=int)
    nxv_th_id = request.args.get('g6_ma_thuong_hieu', type=int)
    nxv_tim = request.args.get('g6_tim_kiem', '').strip()
    nxv_noi_bat = request.args.get('g6_la_noi_bat', type=int)

    nxv_q = G6SanPham.query.filter_by(g6_la_hoat_dong=True)
    if nxv_dm_id:
        nxv_q = nxv_q.filter_by(g6_ma_danh_muc=nxv_dm_id)
    if nxv_th_id:
        nxv_q = nxv_q.filter_by(g6_ma_thuong_hieu=nxv_th_id)
    if nxv_tim:
        nxv_q = nxv_q.filter(G6SanPham.g6_ten_san_pham.ilike(f'%{nxv_tim}%'))
    if nxv_noi_bat is not None:
        nxv_q = nxv_q.filter_by(g6_la_noi_bat=bool(nxv_noi_bat))

    nxv_pt = nxv_q.order_by(G6SanPham.g6_thu_tu_hien_thi, G6SanPham.g6_ngay_tao.desc()).paginate(
        page=nxv_trang, per_page=nxv_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [s.g6_to_dict() for s in nxv_pt.items],
        'g6_tong': nxv_pt.total,
        'g6_trang': nxv_trang,
        'g6_tong_trang': nxv_pt.pages,
    })


@nxv_san_pham_bp.route('/nxv-san-pham/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_chi_tiet_sp(nxv_id):
    nxv_row = G6SanPham.query.get_or_404(nxv_id)
    nxv_row.g6_luot_xem += 1
    db.session.commit()
    nxv_dict = nxv_row.g6_to_dict()
    nxv_dict['g6_bien_the'] = [b.g6_to_dict() for b in nxv_row.g6_bien_the]
    nxv_dict['g6_hinh_anh'] = [h.g6_to_dict() for h in nxv_row.g6_hinh_anh]
    nxv_dict['g6_chung_nhan'] = [c.g6_to_dict() for c in nxv_row.g6_chung_nhan]
    nxv_dict['g6_muc_tieu'] = [m.g6_to_dict() for m in nxv_row.g6_muc_tieu]
    return nqt_ok(nxv_dict)


@nxv_san_pham_bp.route('/nxv-san-pham', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_san_pham():
    nxv_data = request.get_json() or {}
    nxv_ten = nxv_data.get('g6_ten_san_pham', '').strip()
    nxv_slug = nxv_data.get('g6_slug', '').strip()
    nxv_dm = nxv_data.get('g6_ma_danh_muc')
    nxv_th = nxv_data.get('g6_ma_thuong_hieu')
    if not nxv_ten or not nxv_slug or not nxv_dm or not nxv_th:
        return nqt_loi('Thiếu tên, slug, danh mục hoặc thương hiệu')
    if G6SanPham.query.filter_by(g6_slug=nxv_slug).first():
        return nqt_loi('Slug đã tồn tại')

    nxv_row = G6SanPham(
        g6_ma_danh_muc=nxv_dm,
        g6_ma_thuong_hieu=nxv_th,
        g6_ten_san_pham=nxv_ten,
        g6_slug=nxv_slug,
        g6_mo_ta_ngan=nxv_data.get('g6_mo_ta_ngan'),
        g6_mo_ta_day_du=nxv_data.get('g6_mo_ta_day_du'),
        g6_cach_dung=nxv_data.get('g6_cach_dung'),
        g6_nuoc_xuat_xu=nxv_data.get('g6_nuoc_xuat_xu'),
        g6_doi_tuong_dung=nxv_data.get('g6_doi_tuong_dung'),
        g6_la_noi_bat=nxv_data.get('g6_la_noi_bat', False),
        g6_la_ban_chay=nxv_data.get('g6_la_ban_chay', False),
        g6_la_hang_moi=nxv_data.get('g6_la_hang_moi', False),
        g6_seo_title=nxv_data.get('g6_seo_title'),
        g6_seo_mo_ta=nxv_data.get('g6_seo_mo_ta'),
    )
    db.session.add(nxv_row)
    db.session.flush()

    nxv_gia = nxv_data.get('g6_gia_ban')
    if nxv_gia is not None:
        nxv_bt = G6BienTheSanPham(
            g6_ma_san_pham=nxv_row.g6_ma_san_pham,
            g6_sku=f"{nxv_slug}-default",
            g6_ten_bien_the="Mặc định",
            g6_gia=nxv_gia,
            g6_gia_so_sanh=nxv_data.get('g6_gia_goc'),
            g6_la_mac_dinh=True
        )
        db.session.add(nxv_bt)

    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo sản phẩm thành công', 201)


@nxv_san_pham_bp.route('/nxv-san-pham/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_sp(nxv_id):
    nxv_row = G6SanPham.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['g6_ten_san_pham', 'g6_mo_ta_ngan', 'g6_mo_ta_day_du', 'g6_cach_dung',
                  'g6_nuoc_xuat_xu', 'g6_doi_tuong_dung', 'g6_la_noi_bat', 'g6_la_ban_chay',
                  'g6_la_hang_moi', 'g6_la_hoat_dong', 'g6_seo_title', 'g6_seo_mo_ta',
                  'g6_thu_tu_hien_thi', 'g6_ma_danh_muc', 'g6_ma_thuong_hieu']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])

    # Cập nhật mục tiêu sức khỏe
    nxv_mt_ids = nxv_data.get('g6_ma_muc_tieu_ids')
    if nxv_mt_ids is not None:
        nxv_mts = G6MucTieuSucKhoe.query.filter(G6MucTieuSucKhoe.g6_ma_muc_tieu.in_(nxv_mt_ids)).all()
        nxv_row.g6_muc_tieu = nxv_mts

    if 'g6_gia_ban' in nxv_data or 'g6_gia_goc' in nxv_data:
        nxv_bt = G6BienTheSanPham.query.filter_by(g6_ma_san_pham=nxv_id, g6_la_mac_dinh=True).first()
        if not nxv_bt:
            nxv_bt = G6BienTheSanPham.query.filter_by(g6_ma_san_pham=nxv_id).first()
        if nxv_bt:
            if 'g6_gia_ban' in nxv_data: nxv_bt.g6_gia = nxv_data['g6_gia_ban']
            if 'g6_gia_goc' in nxv_data: nxv_bt.g6_gia_so_sanh = nxv_data['g6_gia_goc']
        elif 'g6_gia_ban' in nxv_data:
            nxv_bt = G6BienTheSanPham(
                g6_ma_san_pham=nxv_id,
                g6_sku=f"sp-{nxv_id}-default",
                g6_ten_bien_the="Mặc định",
                g6_gia=nxv_data['g6_gia_ban'],
                g6_gia_so_sanh=nxv_data.get('g6_gia_goc'),
                g6_la_mac_dinh=True
            )
            db.session.add(nxv_bt)

    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_san_pham_bp.route('/nxv-san-pham/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_sp(nxv_id):
    nxv_row = G6SanPham.query.get_or_404(nxv_id)
    nxv_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn sản phẩm')


# ============================================================
# BIẾN THỂ SẢN PHẨM
# ============================================================

@nxv_san_pham_bp.route('/nxv-san-pham/<int:nxv_sp_id>/bien-the', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_bien_the(nxv_sp_id):
    G6SanPham.query.get_or_404(nxv_sp_id)
    nxv_list = G6BienTheSanPham.query.filter_by(g6_ma_san_pham=nxv_sp_id, g6_la_hoat_dong=True).all()
    return nqt_ok([b.g6_to_dict() for b in nxv_list])


@nxv_san_pham_bp.route('/nxv-san-pham/<int:nxv_sp_id>/bien-the', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_bien_the(nxv_sp_id):
    G6SanPham.query.get_or_404(nxv_sp_id)
    nxv_data = request.get_json() or {}
    nxv_sku = nxv_data.get('g6_sku', '').strip()
    nxv_ten = nxv_data.get('g6_ten_bien_the', '').strip()
    nxv_gia = nxv_data.get('g6_gia')
    if not nxv_sku or not nxv_ten or nxv_gia is None:
        return nqt_loi('Thiếu SKU, tên biến thể hoặc giá')
    if G6BienTheSanPham.query.filter_by(g6_sku=nxv_sku).first():
        return nqt_loi('SKU đã tồn tại')

    nxv_row = G6BienTheSanPham(
        g6_ma_san_pham=nxv_sp_id,
        g6_sku=nxv_sku,
        g6_ten_bien_the=nxv_ten,
        g6_gia=nxv_gia,
        g6_gia_so_sanh=nxv_data.get('g6_gia_so_sanh'),
        g6_trong_luong=nxv_data.get('g6_trong_luong'),
        g6_trong_luong_gram=nxv_data.get('g6_trong_luong_gram'),
        g6_so_luot_dung=nxv_data.get('g6_so_luot_dung'),
        g6_huong_vi=nxv_data.get('g6_huong_vi'),
        g6_hinh_anh=nxv_data.get('g6_hinh_anh'),
        g6_la_mac_dinh=nxv_data.get('g6_la_mac_dinh', False),
        g6_thu_tu=nxv_data.get('g6_thu_tu', 0),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo biến thể thành công', 201)


@nxv_san_pham_bp.route('/nxv-bien-the/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_bien_the(nxv_id):
    nxv_row = G6BienTheSanPham.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['g6_ten_bien_the', 'g6_gia', 'g6_gia_so_sanh', 'g6_trong_luong',
                  'g6_trong_luong_gram', 'g6_so_luot_dung', 'g6_huong_vi',
                  'g6_hinh_anh', 'g6_la_mac_dinh', 'g6_la_hoat_dong', 'g6_thu_tu']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_san_pham_bp.route('/nxv-bien-the/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_bien_the(nxv_id):
    nxv_row = G6BienTheSanPham.query.get_or_404(nxv_id)
    nxv_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn biến thể')


# ============================================================
# HÌNH ẢNH SẢN PHẨM
# ============================================================

@nxv_san_pham_bp.route('/nxv-san-pham/<int:nxv_sp_id>/hinh-anh', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_hinh_anh(nxv_sp_id):
    G6SanPham.query.get_or_404(nxv_sp_id)
    nxv_list = G6HinhAnhSanPham.query.filter_by(g6_ma_san_pham=nxv_sp_id).order_by(G6HinhAnhSanPham.g6_thu_tu).all()
    return nqt_ok([h.g6_to_dict() for h in nxv_list])


@nxv_san_pham_bp.route('/nxv-san-pham/<int:nxv_sp_id>/hinh-anh', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_them_hinh_anh(nxv_sp_id):
    G6SanPham.query.get_or_404(nxv_sp_id)
    nxv_data = request.get_json() or {}
    nxv_duong_dan = nxv_data.get('g6_duong_dan', '').strip()
    if not nxv_duong_dan:
        return nqt_loi('Thiếu đường dẫn hình ảnh')

    nxv_row = G6HinhAnhSanPham(
        g6_ma_san_pham=nxv_sp_id,
        g6_ma_bien_the=nxv_data.get('g6_ma_bien_the'),
        g6_duong_dan=nxv_duong_dan,
        g6_alt_text=nxv_data.get('g6_alt_text'),
        g6_thu_tu=nxv_data.get('g6_thu_tu', 0),
        g6_la_anh_chinh=nxv_data.get('g6_la_anh_chinh', False),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Thêm hình ảnh thành công', 201)


@nxv_san_pham_bp.route('/nxv-hinh-anh/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_hinh_anh(nxv_id):
    nxv_row = G6HinhAnhSanPham.query.get_or_404(nxv_id)
    db.session.delete(nxv_row)
    db.session.commit()
    return nqt_ok(None, 'Xóa hình ảnh thành công')


# ============================================================
# THÀNH PHẦN DINH DƯỠNG
# ============================================================

@nxv_san_pham_bp.route('/nxv-bien-the/<int:nxv_bt_id>/dinh-duong', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_dinh_duong(nxv_bt_id):
    G6BienTheSanPham.query.get_or_404(nxv_bt_id)
    nxv_row = G6ThanhPhanDinhDuong.query.filter_by(g6_ma_bien_the=nxv_bt_id).first()
    return nqt_ok(nxv_row.g6_to_dict() if nxv_row else None)


@nxv_san_pham_bp.route('/nxv-bien-the/<int:nxv_bt_id>/dinh-duong', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_luu_dinh_duong(nxv_bt_id):
    G6BienTheSanPham.query.get_or_404(nxv_bt_id)
    nxv_data = request.get_json() or {}

    nxv_row = G6ThanhPhanDinhDuong.query.filter_by(g6_ma_bien_the=nxv_bt_id).first()
    if nxv_row:
        # Cập nhật nếu đã tồn tại
        for nxv_f in ['g6_khau_phan', 'g6_calo', 'g6_protein', 'g6_tinh_bot',
                      'g6_chat_beo', 'g6_duong', 'g6_chat_xo', 'g6_bcaa',
                      'g6_glutamine', 'g6_creatine', 'g6_caffeine', 'g6_thanh_phan_khac']:
            if nxv_f in nxv_data:
                setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    else:
        nxv_row = G6ThanhPhanDinhDuong(
            g6_ma_bien_the=nxv_bt_id,
            g6_khau_phan=nxv_data.get('g6_khau_phan'),
            g6_calo=nxv_data.get('g6_calo'),
            g6_protein=nxv_data.get('g6_protein'),
            g6_tinh_bot=nxv_data.get('g6_tinh_bot'),
            g6_chat_beo=nxv_data.get('g6_chat_beo'),
            g6_duong=nxv_data.get('g6_duong'),
            g6_chat_xo=nxv_data.get('g6_chat_xo'),
            g6_bcaa=nxv_data.get('g6_bcaa'),
            g6_glutamine=nxv_data.get('g6_glutamine'),
            g6_creatine=nxv_data.get('g6_creatine'),
            g6_caffeine=nxv_data.get('g6_caffeine'),
            g6_thanh_phan_khac=nxv_data.get('g6_thanh_phan_khac'),
        )
        db.session.add(nxv_row)

    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Lưu dinh dưỡng thành công')


# ============================================================
# CHỨNG NHẬN SẢN PHẨM
# ============================================================

@nxv_san_pham_bp.route('/nxv-san-pham/<int:nxv_sp_id>/chung-nhan', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_chung_nhan(nxv_sp_id):
    G6SanPham.query.get_or_404(nxv_sp_id)
    nxv_list = G6ChungNhanSanPham.query.filter_by(g6_ma_san_pham=nxv_sp_id).all()
    return nqt_ok([c.g6_to_dict() for c in nxv_list])


@nxv_san_pham_bp.route('/nxv-san-pham/<int:nxv_sp_id>/chung-nhan', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_them_chung_nhan(nxv_sp_id):
    G6SanPham.query.get_or_404(nxv_sp_id)
    nxv_data = request.get_json() or {}
    nxv_loai = nxv_data.get('g6_loai', '').strip()
    if not nxv_loai:
        return nqt_loi('Thiếu loại chứng nhận')

    nxv_row = G6ChungNhanSanPham(
        g6_ma_san_pham=nxv_sp_id,
        g6_loai=nxv_loai,
        g6_so_chung_nhan=nxv_data.get('g6_so_chung_nhan'),
        g6_ngay_cap=nxv_data.get('g6_ngay_cap'),
        g6_hinh_anh=nxv_data.get('g6_hinh_anh'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Thêm chứng nhận thành công', 201)


@nxv_san_pham_bp.route('/nxv-chung-nhan/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_chung_nhan(nxv_id):
    nxv_row = G6ChungNhanSanPham.query.get_or_404(nxv_id)
    db.session.delete(nxv_row)
    db.session.commit()
    return nqt_ok(None, 'Xóa chứng nhận thành công')


# ============================================================
# TỒN KHO
# ============================================================

@nxv_san_pham_bp.route('/nxv-ton-kho', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_ton_kho():
    nxv_bt_id = request.args.get('g6_ma_bien_the', type=int)
    nxv_cn_id = request.args.get('g6_ma_chi_nhanh', type=int)
    nxv_canh_bao = request.args.get('g6_canh_bao', type=int)  # 1=chỉ hiển thị sắp hết

    nxv_q = G6TonKho.query
    if nxv_bt_id:
        nxv_q = nxv_q.filter_by(g6_ma_bien_the=nxv_bt_id)
    if nxv_cn_id:
        nxv_q = nxv_q.filter_by(g6_ma_chi_nhanh=nxv_cn_id)
    if nxv_canh_bao:
        nxv_q = nxv_q.filter(G6TonKho.g6_so_luong <= G6TonKho.g6_nguong_canh_bao)

    return nqt_ok([t.g6_to_dict() for t in nxv_q.all()])


@nxv_san_pham_bp.route('/nxv-ton-kho', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_ton_kho():
    nxv_data = request.get_json() or {}
    nxv_bt_id = nxv_data.get('g6_ma_bien_the')
    if not nxv_bt_id:
        return nqt_loi('Thiếu mã biến thể')

    nxv_row = G6TonKho.query.filter_by(
        g6_ma_bien_the=nxv_bt_id,
        g6_ma_chi_nhanh=nxv_data.get('g6_ma_chi_nhanh'),
    ).first()

    if nxv_row:
        nxv_row.g6_so_luong = nxv_data.get('g6_so_luong', nxv_row.g6_so_luong)
        nxv_row.g6_nguong_canh_bao = nxv_data.get('g6_nguong_canh_bao', nxv_row.g6_nguong_canh_bao)
    else:
        nxv_row = G6TonKho(
            g6_ma_bien_the=nxv_bt_id,
            g6_ma_chi_nhanh=nxv_data.get('g6_ma_chi_nhanh'),
            g6_so_luong=nxv_data.get('g6_so_luong', 0),
            g6_nguong_canh_bao=nxv_data.get('g6_nguong_canh_bao', 10),
        )
        db.session.add(nxv_row)

    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Cập nhật tồn kho thành công')


@nxv_san_pham_bp.route('/nxv-ton-kho/<int:nxv_id>/nhap-hang', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_nhap_hang(nxv_id):
    nxv_row = G6TonKho.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    nxv_so_luong = nxv_data.get('g6_so_luong', 0)
    if nxv_so_luong <= 0:
        return nqt_loi('Số lượng nhập phải lớn hơn 0')

    nxv_so_cu = nxv_row.g6_so_luong
    nxv_row.g6_so_luong += nxv_so_luong

    nxv_ls = G6LichSuTonKho(
        g6_ma_bien_the=nxv_row.g6_ma_bien_the,
        g6_ma_chi_nhanh=nxv_row.g6_ma_chi_nhanh,
        g6_loai_giao_dich='nhap',
        g6_so_luong_thay_doi=nxv_so_luong,
        g6_so_luong_truoc=nxv_so_cu,
        g6_so_luong_sau=nxv_row.g6_so_luong,
        g6_ghi_chu=nxv_data.get('g6_ghi_chu'),
        g6_nguoi_thuc_hien=nxv_data.get('g6_nguoi_thuc_hien'),
    )
    db.session.add(nxv_ls)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), f'Nhập {nxv_so_luong} sản phẩm thành công')


@nxv_san_pham_bp.route('/nxv-ton-kho/<int:nxv_id>/xuat-hang', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_xuat_hang(nxv_id):
    nxv_row = G6TonKho.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    nxv_so_luong = nxv_data.get('g6_so_luong', 0)
    if nxv_so_luong <= 0:
        return nqt_loi('Số lượng xuất phải lớn hơn 0')
    if nxv_so_luong > nxv_row.g6_so_luong:
        return nqt_loi(f'Không đủ tồn kho (hiện có: {nxv_row.g6_so_luong})')

    nxv_so_cu = nxv_row.g6_so_luong
    nxv_row.g6_so_luong -= nxv_so_luong

    nxv_ls = G6LichSuTonKho(
        g6_ma_bien_the=nxv_row.g6_ma_bien_the,
        g6_ma_chi_nhanh=nxv_row.g6_ma_chi_nhanh,
        g6_loai_giao_dich='xuat',
        g6_so_luong_thay_doi=-nxv_so_luong,
        g6_so_luong_truoc=nxv_so_cu,
        g6_so_luong_sau=nxv_row.g6_so_luong,
        g6_ghi_chu=nxv_data.get('g6_ghi_chu'),
        g6_nguoi_thuc_hien=nxv_data.get('g6_nguoi_thuc_hien'),
    )
    db.session.add(nxv_ls)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), f'Xuất {nxv_so_luong} sản phẩm thành công')


# ============================================================
# LỊCH SỬ TỒN KHO
# ============================================================

@nxv_san_pham_bp.route('/nxv-lich-su-ton-kho', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_lich_su_ton_kho():
    nxv_bt_id = request.args.get('g6_ma_bien_the', type=int)
    nxv_cn_id = request.args.get('g6_ma_chi_nhanh', type=int)
    nxv_loai = request.args.get('g6_loai_giao_dich', '').strip()
    nxv_trang = request.args.get('g6_trang', 1, type=int)

    nxv_q = G6LichSuTonKho.query
    if nxv_bt_id:
        nxv_q = nxv_q.filter_by(g6_ma_bien_the=nxv_bt_id)
    if nxv_cn_id:
        nxv_q = nxv_q.filter_by(g6_ma_chi_nhanh=nxv_cn_id)
    if nxv_loai:
        nxv_q = nxv_q.filter_by(g6_loai_giao_dich=nxv_loai)

    nxv_pt = nxv_q.order_by(G6LichSuTonKho.g6_thoi_gian.desc()).paginate(
        page=nxv_trang, per_page=20, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [l.g6_to_dict() for l in nxv_pt.items],
        'g6_tong': nxv_pt.total,
        'g6_trang': nxv_trang,
        'g6_tong_trang': nxv_pt.pages,
    })
