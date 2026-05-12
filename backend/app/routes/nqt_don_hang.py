from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from backend.app import db
from backend.app.models.g6_don_hang import (
    G6GioHang, G6ChiTietGioHang, G6DonHang, G6ChiTietDonHang, G6LichSuDonHang,
)
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_ghi_nhat_ky

nqt_don_hang_bp = Blueprint('g6_don_hang', __name__, url_prefix='/api')


# ---- GIỎ HÀNG ----

@nqt_don_hang_bp.route('/nqt-gio-hang', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_gio_hang():
    nqt_kh_id = request.args.get('g6_ma_khach_hang', type=int)
    nqt_phien = request.args.get('g6_phien_khach')
    nqt_q = G6GioHang.query
    if nqt_kh_id:
        nqt_q = nqt_q.filter_by(g6_ma_khach_hang=nqt_kh_id)
    elif nqt_phien:
        nqt_q = nqt_q.filter_by(g6_phien_khach=nqt_phien)
    else:
        return nqt_loi('Cần cung cấp mã khách hàng hoặc phiên')
    nqt_gio = nqt_q.first()
    return nqt_ok(nqt_gio.g6_to_dict() if nqt_gio else None)


@nqt_don_hang_bp.route('/nqt-gio-hang/nqt-them', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_them_vao_gio():
    nqt_data = request.get_json() or {}
    nqt_kh_id = nqt_data.get('g6_ma_khach_hang')
    nqt_phien = nqt_data.get('g6_phien_khach')
    nqt_bien_the = nqt_data.get('g6_ma_bien_the')
    nqt_so_luong = nqt_data.get('g6_so_luong', 1)
    nqt_don_gia = nqt_data.get('g6_don_gia', 0)

    if not nqt_bien_the:
        return nqt_loi('Thiếu mã biến thể sản phẩm')

    nqt_gio = None
    if nqt_kh_id:
        nqt_gio = G6GioHang.query.filter_by(g6_ma_khach_hang=nqt_kh_id).first()
    elif nqt_phien:
        nqt_gio = G6GioHang.query.filter_by(g6_phien_khach=nqt_phien).first()

    if not nqt_gio:
        nqt_gio = G6GioHang(g6_ma_khach_hang=nqt_kh_id, g6_phien_khach=nqt_phien)
        db.session.add(nqt_gio)
        db.session.flush()

    nqt_ct = G6ChiTietGioHang.query.filter_by(
        g6_ma_gio_hang=nqt_gio.g6_ma_gio_hang,
        g6_ma_bien_the=nqt_bien_the
    ).first()
    if nqt_ct:
        nqt_ct.g6_so_luong += nqt_so_luong
    else:
        nqt_ct = G6ChiTietGioHang(
            g6_ma_gio_hang=nqt_gio.g6_ma_gio_hang,
            g6_ma_bien_the=nqt_bien_the,
            g6_so_luong=nqt_so_luong,
            g6_don_gia=nqt_don_gia,
        )
        db.session.add(nqt_ct)
    db.session.commit()
    return nqt_ok(nqt_gio.g6_to_dict(), 'Đã thêm vào giỏ hàng')


@nqt_don_hang_bp.route('/nqt-gio-hang/nqt-xoa/<int:nqt_ct_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_khoi_gio(nqt_ct_id):
    nqt_ct = G6ChiTietGioHang.query.get_or_404(nqt_ct_id)
    db.session.delete(nqt_ct)
    db.session.commit()
    return nqt_ok(None, 'Đã xóa khỏi giỏ hàng')


# ---- ĐƠN HÀNG ----

@nqt_don_hang_bp.route('/nqt-don-hang', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_tat_ca_don_hang():
    nqt_trang = request.args.get('g6_trang', 1, type=int)
    nqt_gioi_han = request.args.get('g6_gioi_han', 20, type=int)
    nqt_trang_thai = request.args.get('g6_trang_thai')
    nqt_kh_id = request.args.get('g6_ma_khach_hang', type=int)
    nqt_q = G6DonHang.query
    if nqt_trang_thai:
        nqt_q = nqt_q.filter_by(g6_trang_thai=nqt_trang_thai)
    if nqt_kh_id:
        nqt_q = nqt_q.filter_by(g6_ma_khach_hang=nqt_kh_id)
    nqt_phan_trang = nqt_q.order_by(G6DonHang.g6_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [d.g6_to_dict() for d in nqt_phan_trang.items],
        'g6_tong': nqt_phan_trang.total,
        'g6_trang': nqt_trang,
    })


@nqt_don_hang_bp.route('/nqt-don-hang/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_don_hang(nqt_id):
    nqt_row = G6DonHang.query.get_or_404(nqt_id)
    nqt_result = nqt_row.g6_to_dict()
    nqt_result['g6_chi_tiet'] = [ct.g6_to_dict() for ct in nqt_row.g6_chi_tiet]
    nqt_result['g6_lich_su'] = [ls.g6_to_dict() for ls in nqt_row.g6_lich_su]
    return nqt_ok(nqt_result)


@nqt_don_hang_bp.route('/nqt-don-hang', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_ghi_nhat_ky('Tạo đơn hàng', 'G6DonHang')
def nqt_tao_don_hang():
    nqt_data = request.get_json() or {}
    nqt_san_pham = nqt_data.get('g6_san_pham', [])
    if not nqt_san_pham:
        return nqt_loi('Đơn hàng phải có ít nhất một sản phẩm')

    nqt_tong = sum(float(sp.get('g6_don_gia', 0)) * int(sp.get('g6_so_luong', 1)) for sp in nqt_san_pham)
    nqt_phi_vc = float(nqt_data.get('g6_phi_van_chuyen', 0))
    nqt_giam = float(nqt_data.get('g6_so_tien_giam', 0))

    nqt_don = G6DonHang(
        g6_ma_khach_hang=nqt_data.get('g6_ma_khach_hang'),
        g6_ho_ten_nguoi_nhan=nqt_data.get('g6_ho_ten_nguoi_nhan', ''),
        g6_so_dien_thoai=nqt_data.get('g6_so_dien_thoai', ''),
        g6_dia_chi_giao_hang=nqt_data.get('g6_dia_chi_giao_hang', ''),
        g6_tong_tien_hang=nqt_tong,
        g6_phi_van_chuyen=nqt_phi_vc,
        g6_so_tien_giam=nqt_giam,
        g6_tong_thanh_toan=nqt_tong + nqt_phi_vc - nqt_giam,
        g6_phuong_thuc_thanh_toan=nqt_data.get('g6_phuong_thuc_thanh_toan', 'cod'),
        g6_ghi_chu_khach=nqt_data.get('g6_ghi_chu_khach'),
        g6_ma_van_chuyen=nqt_data.get('g6_ma_van_chuyen'),
    )
    db.session.add(nqt_don)
    db.session.flush()

    for nqt_sp in nqt_san_pham:
        nqt_ct = G6ChiTietDonHang(
            g6_ma_don_hang=nqt_don.g6_ma_don_hang,
            g6_ma_bien_the=nqt_sp.get('g6_ma_bien_the'),
            g6_ten_san_pham=nqt_sp.get('g6_ten_san_pham', ''),
            g6_sku=nqt_sp.get('g6_sku'),
            g6_so_luong=nqt_sp.get('g6_so_luong', 1),
            g6_don_gia=nqt_sp.get('g6_don_gia', 0),
            g6_thanh_tien=float(nqt_sp.get('g6_don_gia', 0)) * int(nqt_sp.get('g6_so_luong', 1)),
        )
        db.session.add(nqt_ct)

    nqt_ls = G6LichSuDonHang(
        g6_ma_don_hang=nqt_don.g6_ma_don_hang,
        g6_trang_thai_moi='cho_xac_nhan',
        g6_ghi_chu='Đơn hàng mới',
    )
    db.session.add(nqt_ls)
    db.session.commit()
    return nqt_ok(nqt_don.g6_to_dict(), 'Đặt hàng thành công', 201)


@nqt_don_hang_bp.route('/nqt-don-hang/<int:nqt_id>/nqt-cap-nhat-trang-thai', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_ghi_nhat_ky('Cập nhật trạng thái đơn hàng', 'G6DonHang')
def nqt_cap_nhat_trang_thai(nqt_id):
    nqt_don = G6DonHang.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    nqt_tt_moi = nqt_data.get('g6_trang_thai')
    if not nqt_tt_moi:
        return nqt_loi('Thiếu trạng thái mới')
    nqt_tt_cu = nqt_don.g6_trang_thai
    nqt_don.g6_trang_thai = nqt_tt_moi
    nqt_ls = G6LichSuDonHang(
        g6_ma_don_hang=nqt_id,
        g6_trang_thai_cu=nqt_tt_cu,
        g6_trang_thai_moi=nqt_tt_moi,
        g6_ghi_chu=nqt_data.get('g6_ghi_chu'),
    )
    db.session.add(nqt_ls)
    db.session.commit()
    return nqt_ok(nqt_don.g6_to_dict())
