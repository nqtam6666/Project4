from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_khuyen_mai import G6MaGiamGia, G6KhuyenMaiMuaKem, G6Banner
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap

nqt_khuyen_mai_bp = Blueprint('g6_khuyen_mai', __name__, url_prefix='/api')


@nqt_khuyen_mai_bp.route('/nqt-ma-giam-gia', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_ma_giam_gia():
    nqt_list = G6MaGiamGia.query.order_by(G6MaGiamGia.g6_ngay_tao.desc()).all()
    return nqt_ok([m.g6_to_dict() for m in nqt_list])


@nqt_khuyen_mai_bp.route('/nqt-ma-giam-gia/nqt-kiem-tra', methods=['POST'])
def nqt_kiem_tra_ma_giam_gia():
    from datetime import datetime
    nqt_data = request.get_json() or {}
    nqt_ma = nqt_data.get('g6_ma', '').strip().upper()
    nqt_tong = float(nqt_data.get('g6_tong_tien', 0))
    nqt_row = G6MaGiamGia.query.filter_by(g6_ma=nqt_ma, g6_la_hoat_dong=True).first()
    if not nqt_row:
        return nqt_loi('Mã giảm giá không hợp lệ', nqt_ma_trang=404)
    nqt_now = datetime.utcnow()
    if nqt_row.g6_ngay_bat_dau > nqt_now:
        return nqt_loi('Mã giảm giá chưa có hiệu lực')
    if nqt_row.g6_ngay_ket_thuc and nqt_row.g6_ngay_ket_thuc < nqt_now:
        return nqt_loi('Mã giảm giá đã hết hạn')
    if nqt_row.g6_so_luong_tong and nqt_row.g6_so_luong_da_dung >= nqt_row.g6_so_luong_tong:
        return nqt_loi('Mã giảm giá đã hết lượt sử dụng')
    if nqt_tong < float(nqt_row.g6_don_hang_toi_thieu):
        return nqt_loi(f'Đơn hàng tối thiểu {int(nqt_row.g6_don_hang_toi_thieu):,}đ')
    nqt_giam = 0
    if nqt_row.g6_loai == 'phan_tram':
        nqt_giam = nqt_tong * float(nqt_row.g6_gia_tri) / 100
        if nqt_row.g6_gia_tri_toi_da:
            nqt_giam = min(nqt_giam, float(nqt_row.g6_gia_tri_toi_da))
    else:
        nqt_giam = float(nqt_row.g6_gia_tri)
    return nqt_ok({
        'g6_ma_ma_giam_gia': nqt_row.g6_ma_ma_giam_gia,
        'g6_so_tien_giam': round(nqt_giam),
        'g6_loai': nqt_row.g6_loai,
    })


@nqt_khuyen_mai_bp.route('/nqt-ma-giam-gia', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_ma_giam_gia():
    nqt_data = request.get_json() or {}
    nqt_row = G6MaGiamGia(
        g6_ma=nqt_data.get('g6_ma', '').upper(),
        g6_loai=nqt_data.get('g6_loai', 'phan_tram'),
        g6_gia_tri=nqt_data.get('g6_gia_tri', 0),
        g6_don_hang_toi_thieu=nqt_data.get('g6_don_hang_toi_thieu', 0),
        g6_so_luong_tong=nqt_data.get('g6_so_luong_tong'),
        g6_ngay_bat_dau=nqt_data.get('g6_ngay_bat_dau'),
        g6_ngay_ket_thuc=nqt_data.get('g6_ngay_ket_thuc'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo mã giảm giá thành công', 201)


@nqt_khuyen_mai_bp.route('/nqt-banner', methods=['GET'])
def nqt_lay_banner():
    nqt_vi_tri = request.args.get('g6_vi_tri', 'slider')
    nqt_list = G6Banner.query.filter_by(g6_la_hoat_dong=True, g6_vi_tri=nqt_vi_tri).order_by(
        G6Banner.g6_thu_tu
    ).all()
    return nqt_ok([b.g6_to_dict() for b in nqt_list])


@nqt_khuyen_mai_bp.route('/nqt-banner', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_banner():
    nqt_data = request.get_json() or {}
    nqt_row = G6Banner(
        g6_tieu_de=nqt_data.get('g6_tieu_de'),
        g6_hinh_anh=nqt_data.get('g6_hinh_anh', ''),
        g6_duong_dan=nqt_data.get('g6_duong_dan'),
        g6_vi_tri=nqt_data.get('g6_vi_tri', 'slider'),
        g6_thu_tu=nqt_data.get('g6_thu_tu', 0),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo banner thành công', 201)


@nqt_khuyen_mai_bp.route('/nqt-ma-giam-gia/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_ma_giam_gia(nqt_id):
    nqt_row = G6MaGiamGia.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in [
        'g6_gia_tri', 'g6_gia_tri_toi_da', 'g6_don_hang_toi_thieu',
        'g6_so_luong_tong', 'g6_ngay_bat_dau', 'g6_ngay_ket_thuc', 'g6_la_hoat_dong',
    ]:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Cập nhật mã giảm giá thành công')


@nqt_khuyen_mai_bp.route('/nqt-banner/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_banner(nqt_id):
    nqt_row = G6Banner.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['g6_tieu_de', 'g6_hinh_anh', 'g6_duong_dan', 'g6_vi_tri', 'g6_thu_tu', 'g6_la_hoat_dong']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Cập nhật banner thành công')


# ---- KHUYẾN MÃI MUA KÈM ----

@nqt_khuyen_mai_bp.route('/nqt-khuyen-mai-mua-kem', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_khuyen_mai_mua_kem():
    nqt_list = G6KhuyenMaiMuaKem.query.order_by(G6KhuyenMaiMuaKem.g6_ma_khuyen_mai.desc()).all()
    return nqt_ok([k.g6_to_dict() for k in nqt_list])


@nqt_khuyen_mai_bp.route('/nqt-khuyen-mai-mua-kem/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_khuyen_mai_chi_tiet(nqt_id):
    nqt_row = G6KhuyenMaiMuaKem.query.get_or_404(nqt_id)
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_khuyen_mai_bp.route('/nqt-khuyen-mai-mua-kem', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_khuyen_mai_mua_kem():
    from datetime import datetime
    nqt_data = request.get_json() or {}
    nqt_ten = nqt_data.get('g6_ten', '').strip()
    nqt_sp_chinh = nqt_data.get('g6_ma_san_pham_chinh')
    nqt_ngay_bat_dau = nqt_data.get('g6_ngay_bat_dau')
    if not nqt_ten or not nqt_sp_chinh or not nqt_ngay_bat_dau:
        return nqt_loi('Thiếu tên, sản phẩm chính hoặc ngày bắt đầu')
    nqt_row = G6KhuyenMaiMuaKem(
        g6_ten=nqt_ten,
        g6_ma_san_pham_chinh=nqt_sp_chinh,
        g6_so_luong_mua=nqt_data.get('g6_so_luong_mua', 1),
        g6_ma_san_pham_tang=nqt_data.get('g6_ma_san_pham_tang'),
        g6_so_luong_tang=nqt_data.get('g6_so_luong_tang', 1),
        g6_phan_tram_giam=nqt_data.get('g6_phan_tram_giam', 0),
        g6_ngay_bat_dau=nqt_ngay_bat_dau,
        g6_ngay_ket_thuc=nqt_data.get('g6_ngay_ket_thuc'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo khuyến mãi mua kèm thành công', 201)


@nqt_khuyen_mai_bp.route('/nqt-khuyen-mai-mua-kem/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_khuyen_mai_mua_kem(nqt_id):
    nqt_row = G6KhuyenMaiMuaKem.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in [
        'g6_ten', 'g6_so_luong_mua', 'g6_ma_san_pham_tang',
        'g6_so_luong_tang', 'g6_phan_tram_giam', 'g6_ngay_ket_thuc', 'g6_la_hoat_dong',
    ]:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Cập nhật khuyến mãi thành công')


@nqt_khuyen_mai_bp.route('/nqt-khuyen-mai-mua-kem/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_khuyen_mai_mua_kem(nqt_id):
    nqt_row = G6KhuyenMaiMuaKem.query.get_or_404(nqt_id)
    nqt_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã vô hiệu hóa khuyến mãi mua kèm')


@nqt_khuyen_mai_bp.route('/nqt-ma-giam-gia/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_ma_giam_gia(nqt_id):
    nqt_row = G6MaGiamGia.query.get_or_404(nqt_id)
    nqt_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã vô hiệu hóa mã giảm giá')


@nqt_khuyen_mai_bp.route('/nqt-banner/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_banner(nqt_id):
    nqt_row = G6Banner.query.get_or_404(nqt_id)
    nqt_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn banner')
