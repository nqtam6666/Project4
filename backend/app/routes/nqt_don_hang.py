from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from backend.app import db
from backend.app.models.g6_san_pham import G6BienTheSanPham
from backend.app.models.g6_don_hang import (
    G6GioHang, G6ChiTietGioHang, G6DonHang, G6ChiTietDonHang, G6LichSuDonHang,
)
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_ghi_nhat_ky, nqt_yeu_cau_quyen

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
def nqt_lay_tat_ca_don_hang():
    nqt_identity = None
    nqt_claims = None
    try:
        verify_jwt_in_request(optional=True)
        nqt_identity = get_jwt_identity()
        nqt_claims = get_jwt()
        if nqt_claims:
            nqt_phien_id = nqt_claims.get('g6_phien_id')
            if nqt_phien_id:
                from backend.app.models.g6_xac_thuc import G6PhienDangNhap
                phien = G6PhienDangNhap.query.get(nqt_phien_id)
                if not phien or phien.g6_la_thu_hoi:
                    return nqt_loi('Phiên đăng nhập đã bị thu hồi', nqt_ma_trang=401)
    except Exception:
        pass

    nqt_q = G6DonHang.query

    # Phân quyền truy cập đơn hàng
    if nqt_identity:
        nqt_roles = nqt_claims.get('g6_vai_tro', [])
        nqt_loai = nqt_claims.get('g6_loai')
        
        # Nếu là nhân viên quản lý kho, admin hoặc quản trị viên thì được xem tất cả
        if 'QL_KHO' in nqt_roles or 'G6QuanTri' in nqt_roles or nqt_loai == 'admin':
            nqt_kh_id = request.args.get('g6_ma_khach_hang', type=int)
            if nqt_kh_id:
                nqt_q = nqt_q.filter_by(g6_ma_nguoi_dung=nqt_kh_id)
        else:
            # Thành viên thường chỉ được xem đơn hàng của chính mình
            try:
                nqt_ma = int(nqt_identity.split(':')[1])
                nqt_q = nqt_q.filter_by(g6_ma_nguoi_dung=nqt_ma)
            except Exception:
                return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)
    else:
        # Khách vãng lai: lọc theo danh sách ID đơn hàng từ localStorage hoặc số điện thoại
        nqt_id_list_str = request.args.get('g6_ma_don_hang_list')
        nqt_sdt = request.args.get('g6_so_dien_thoai')
        
        if nqt_id_list_str:
            try:
                nqt_ids = [int(x.strip()) for x in nqt_id_list_str.split(',') if x.strip()]
                nqt_q = nqt_q.filter(G6DonHang.g6_ma_don_hang.in_(nqt_ids))
            except ValueError:
                return nqt_loi('Mã đơn hàng không hợp lệ')
        elif nqt_sdt:
            nqt_q = nqt_q.filter_by(g6_so_dien_thoai=nqt_sdt)
        else:
            # Không cung cấp thông tin tra cứu -> trả về danh sách trống
            return nqt_ok({
                'g6_danh_sach': [],
                'g6_tong': 0,
                'g6_trang': 1,
            })

    nqt_trang = request.args.get('g6_trang', 1, type=int)
    nqt_gioi_han = request.args.get('g6_gioi_han', 20, type=int)
    nqt_trang_thai = request.args.get('g6_trang_thai')
    
    if nqt_trang_thai:
        nqt_q = nqt_q.filter_by(g6_trang_thai=nqt_trang_thai)
        
    nqt_phan_trang = nqt_q.order_by(G6DonHang.g6_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [d.g6_to_dict() for d in nqt_phan_trang.items],
        'g6_tong': nqt_phan_trang.total,
        'g6_trang': nqt_trang,
    })


@nqt_don_hang_bp.route('/nqt-don-hang/<int:nqt_id>', methods=['GET'])
def nqt_lay_don_hang(nqt_id):
    try:
        verify_jwt_in_request(optional=True)
        nqt_identity = get_jwt_identity()
        nqt_claims = get_jwt()
    except Exception:
        nqt_identity = None
        nqt_claims = None

    nqt_row = G6DonHang.query.get_or_404(nqt_id)
    
    # Kiểm tra quyền xem đơn hàng chi tiết
    if nqt_identity:
        nqt_roles = nqt_claims.get('g6_vai_tro', [])
        nqt_loai = nqt_claims.get('g6_loai')
        
        if 'QL_KHO' in nqt_roles or 'G6QuanTri' in nqt_roles or nqt_loai == 'admin':
            pass
        else:
            try:
                nqt_ma = int(nqt_identity.split(':')[1])
                if nqt_row.g6_ma_nguoi_dung != nqt_ma:
                    return nqt_loi('Bạn không có quyền xem đơn hàng này', nqt_ma_trang=403)
            except Exception:
                return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)

    nqt_result = nqt_row.g6_to_dict()
    nqt_result['g6_chi_tiet'] = [ct.g6_to_dict() for ct in nqt_row.g6_chi_tiet]
    nqt_result['g6_lich_su'] = [ls.g6_to_dict() for ls in nqt_row.g6_lich_su]
    return nqt_ok(nqt_result)


@nqt_don_hang_bp.route('/nqt-don-hang', methods=['POST'])
@nqt_ghi_nhat_ky('Tạo đơn hàng', 'G6DonHang')
def nqt_tao_don_hang():
    try:
        verify_jwt_in_request(optional=True)
        nqt_identity = get_jwt_identity()
    except Exception:
        nqt_identity = None

    nqt_data = request.get_json() or {}
    
    # Hỗ trợ cả g6_san_pham (backend) và g6_chi_tiet (frontend)
    nqt_san_pham = nqt_data.get('g6_san_pham') or nqt_data.get('g6_chi_tiet') or []
    if not nqt_san_pham:
        return nqt_loi('Đơn hàng phải có ít nhất một sản phẩm')

    nqt_tong = sum(float(sp.get('g6_don_gia', 0)) * int(sp.get('g6_so_luong', 1)) for sp in nqt_san_pham)
    nqt_phi_vc = float(nqt_data.get('g6_phi_van_chuyen', 0))
    nqt_giam = float(nqt_data.get('g6_so_tien_giam', 0))

    # Xác định mã người dùng (hội viên)
    nqt_ma_nd = None
    if nqt_identity:
        try:
            nqt_ma_nd = int(nqt_identity.split(':')[1])
        except Exception:
            pass
    else:
        nqt_ma_nd = nqt_data.get('g6_ma_nguoi_dung') or nqt_data.get('g6_ma_khach_hang')

    nqt_ho_ten = nqt_data.get('g6_ho_ten_nguoi_nhan', '')
    nqt_sdt = nqt_data.get('g6_so_dien_thoai') or nqt_data.get('g6_so_dien_thoai_nguoi_nhan') or ''
    nqt_dia_chi = nqt_data.get('g6_dia_chi_giao_hang', '')
    nqt_ghi_chu = nqt_data.get('g6_ghi_chu_khach') or nqt_data.get('g6_ghi_chu') or ''

    if not nqt_ho_ten:
        return nqt_loi('Họ tên người nhận là bắt buộc')
    if not nqt_sdt:
        return nqt_loi('Số điện thoại người nhận là bắt buộc')
    if not nqt_dia_chi:
        return nqt_loi('Địa chỉ giao hàng là bắt buộc')

    nqt_ma_giam_gia = nqt_data.get('g6_ma_giam_gia')
    nqt_don = G6DonHang(
        g6_ma_nguoi_dung=nqt_ma_nd,
        g6_ho_ten_nguoi_nhan=nqt_ho_ten,
        g6_so_dien_thoai=nqt_sdt,
        g6_dia_chi_giao_hang=nqt_dia_chi,
        g6_tong_tien_hang=nqt_tong,
        g6_phi_van_chuyen=nqt_phi_vc,
        g6_so_tien_giam=nqt_giam,
        g6_tong_thanh_toan=nqt_tong + nqt_phi_vc - nqt_giam,
        g6_phuong_thuc_thanh_toan=nqt_data.get('g6_phuong_thuc_thanh_toan', 'cod'),
        g6_ghi_chu_khach=nqt_ghi_chu,
        g6_ma_van_chuyen=nqt_data.get('g6_ma_van_chuyen'),
    )
    if nqt_ma_giam_gia:
        from backend.app.models.g6_khuyen_mai import G6MaGiamGia
        nqt_coupon = G6MaGiamGia.query.get(nqt_ma_giam_gia)
        if nqt_coupon:
            nqt_don.g6_ma_giam_gia = nqt_coupon.g6_ma_ma_giam_gia
            nqt_coupon.g6_so_luong_da_dung = (nqt_coupon.g6_so_luong_da_dung or 0) + 1

    db.session.add(nqt_don)
    db.session.flush()

    for nqt_sp in nqt_san_pham:
        nqt_val = nqt_sp.get('g6_ma_bien_the')
        nqt_sku_val = nqt_sp.get('g6_sku')
        nqt_bt_id = None

        if nqt_val:
            if isinstance(nqt_val, str) and not nqt_val.isdigit():
                nqt_bt = G6BienTheSanPham.query.filter_by(g6_sku=nqt_val).first()
                if nqt_bt:
                    nqt_bt_id = nqt_bt.g6_ma_bien_the
                    nqt_sku_val = nqt_val
            else:
                try:
                    nqt_bt_id = int(nqt_val)
                except ValueError:
                    nqt_bt = G6BienTheSanPham.query.filter_by(g6_sku=str(nqt_val)).first()
                    if nqt_bt:
                        nqt_bt_id = nqt_bt.g6_ma_bien_the
                        nqt_sku_val = str(nqt_val)

        if nqt_bt_id and not nqt_sku_val:
            nqt_bt = G6BienTheSanPham.query.get(nqt_bt_id)
            if nqt_bt:
                nqt_sku_val = nqt_bt.g6_sku

        if nqt_bt_id is None:
            nqt_bt_id = 0

        nqt_ct = G6ChiTietDonHang(
            g6_ma_don_hang=nqt_don.g6_ma_don_hang,
            g6_ma_bien_the=nqt_bt_id,
            g6_ten_san_pham=nqt_sp.get('g6_ten_san_pham', ''),
            g6_sku=nqt_sku_val,
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
@nqt_yeu_cau_quyen('QL_KHO')
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
