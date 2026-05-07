import bcrypt
from datetime import datetime, timezone, timedelta
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, verify_jwt_in_request
from backend.app import db
from backend.app.models.g6_nguoi_dung import G6NguoiDung, G6NguoiDungVaiTro, G6VaiTroQuyen
from backend.app.models.g6_xac_thuc import G6PhienDangNhap
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap
from backend.app.services.g6_dich_vu_cau_hinh import NqtDichVuCauHinh

nqt_auth_bp = Blueprint('g6_auth', __name__, url_prefix='/api')


@nqt_auth_bp.route('/nqt-dang-nhap', methods=['POST'])
def nqt_dang_nhap():
    nqt_data = request.get_json() or {}
    nqt_ten = nqt_data.get('g6_ten_dang_nhap', '').strip()
    nqt_mk = nqt_data.get('g6_mat_khau', '')

    if not nqt_ten or not nqt_mk:
        return nqt_loi('Thiếu tên đăng nhập hoặc mật khẩu')

    nqt_user = G6NguoiDung.query.filter(
        (G6NguoiDung.g6_ten_dang_nhap == nqt_ten) |
        (G6NguoiDung.g6_so_dien_thoai == nqt_ten) |
        (G6NguoiDung.g6_email == nqt_ten)
    ).first()
    if not nqt_user:
        return nqt_loi('Tên đăng nhập hoặc mật khẩu không đúng', nqt_ma_trang=401)

    # Kiểm tra khóa tài khoản
    if nqt_user.g6_khoa_den and nqt_user.g6_khoa_den > datetime.now(timezone.utc).replace(tzinfo=None):
        return nqt_loi('Tài khoản tạm thời bị khóa', nqt_ma_trang=403)

    if not nqt_user.g6_la_hoat_dong:
        return nqt_loi('Tài khoản đã bị vô hiệu hóa', nqt_ma_trang=403)

    # Xác thực mật khẩu
    if not bcrypt.checkpw(nqt_mk.encode(), nqt_user.g6_mat_khau.encode()):
        nqt_so_lan_sai_max = NqtDichVuCauHinh.g6_lay('g6_so_lan_dang_nhap_sai', nqt_mac_dinh=5)
        nqt_khoa_phut = NqtDichVuCauHinh.g6_lay('g6_khoa_tai_khoan_phut', nqt_mac_dinh=30)
        nqt_user.g6_lan_dang_nhap_sai += 1
        if nqt_user.g6_lan_dang_nhap_sai >= nqt_so_lan_sai_max:
            nqt_user.g6_khoa_den = datetime.utcnow() + timedelta(minutes=nqt_khoa_phut)
            nqt_user.g6_lan_dang_nhap_sai = 0
        db.session.commit()
        return nqt_loi('Tên đăng nhập hoặc mật khẩu không đúng', nqt_ma_trang=401)

    nqt_user.g6_lan_dang_nhap_sai = 0
    nqt_user.g6_khoa_den = None
    db.session.commit()

    # Lấy vai trò và quyền
    nqt_vai_tro_list = [ndvt.g6_vai_tro.g6_ten_vai_tro for ndvt in nqt_user.g6_vai_tro]
    nqt_quyen_list = []
    for ndvt in nqt_user.g6_vai_tro:
        for vtq in ndvt.g6_vai_tro.g6_quyen:
            nqt_quyen_list.append(vtq.g6_quyen.g6_ten_quyen)

    nqt_additional_claims = {
        'g6_vai_tro': nqt_vai_tro_list,
        'g6_quyen': list(set(nqt_quyen_list)),
        'g6_ho_ten': nqt_user.g6_ho_ten,
        'g6_loai': 'nhan_vien',
    }
    nqt_jwt_expiry = int(NqtDichVuCauHinh.g6_lay('g6_jwt_het_han_phut', nqt_mac_dinh=60)) * 60
    nqt_access_token = create_access_token(
        identity=str(nqt_user.g6_ma_nguoi_dung),
        additional_claims=nqt_additional_claims,
        expires_delta=timedelta(seconds=nqt_jwt_expiry)
    )
    nqt_refresh_expiry = int(NqtDichVuCauHinh.g6_lay('g6_jwt_refresh_ngay', nqt_mac_dinh=7))
    nqt_refresh_token = create_refresh_token(
        identity=str(nqt_user.g6_ma_nguoi_dung),
        expires_delta=timedelta(days=nqt_refresh_expiry)
    )

    return nqt_ok({
        'g6_access_token': nqt_access_token,
        'g6_refresh_token': nqt_refresh_token,
        'g6_nguoi_dung': nqt_user.g6_to_dict(),
    }, 'Đăng nhập thành công')


@nqt_auth_bp.route('/nqt-lam-moi-token', methods=['POST'])
def nqt_lam_moi_token():
    try:
        verify_jwt_in_request(refresh=True)
    except Exception:
        return nqt_loi('Refresh token không hợp lệ hoặc đã hết hạn', nqt_ma_trang=401)

    nqt_identity = get_jwt_identity()
    nqt_user = G6NguoiDung.query.get(int(nqt_identity))
    if not nqt_user or not nqt_user.g6_la_hoat_dong:
        return nqt_loi('Tài khoản không hợp lệ', nqt_ma_trang=401)

    nqt_vai_tro_list = [ndvt.g6_vai_tro.g6_ten_vai_tro for ndvt in nqt_user.g6_vai_tro]
    nqt_quyen_list = []
    for ndvt in nqt_user.g6_vai_tro:
        for vtq in ndvt.g6_vai_tro.g6_quyen:
            nqt_quyen_list.append(vtq.g6_quyen.g6_ten_quyen)

    nqt_jwt_expiry = int(NqtDichVuCauHinh.g6_lay('g6_jwt_het_han_phut', nqt_mac_dinh=60)) * 60
    nqt_access_token = create_access_token(
        identity=nqt_identity,
        additional_claims={
            'g6_vai_tro': nqt_vai_tro_list,
            'g6_quyen': list(set(nqt_quyen_list)),
            'g6_ho_ten': nqt_user.g6_ho_ten,
            'g6_loai': 'nhan_vien',
        },
        expires_delta=timedelta(seconds=nqt_jwt_expiry)
    )
    return nqt_ok({'g6_access_token': nqt_access_token})


@nqt_auth_bp.route('/nqt-dang-xuat', methods=['POST'])
def nqt_dang_xuat():
    try:
        verify_jwt_in_request(refresh=True)
        nqt_identity = get_jwt_identity()
        nqt_jti = get_jwt().get('jti')
        if nqt_jti:
            import hashlib
            nqt_jti_hash = hashlib.sha256(nqt_jti.encode()).hexdigest()
            nqt_phien = G6PhienDangNhap.query.filter_by(
                g6_ma_nguoi_dung=int(nqt_identity),
                g6_ma_refresh_token_hash=nqt_jti_hash,
                g6_la_thu_hoi=False,
            ).first()
            if nqt_phien:
                nqt_phien.g6_la_thu_hoi = True
                db.session.commit()
    except Exception:
        pass
    return nqt_ok(None, 'Đăng xuất thành công')


@nqt_auth_bp.route('/nqt-toi', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_thong_tin_toi():
    nqt_identity = get_jwt_identity()
    nqt_user = G6NguoiDung.query.get(int(nqt_identity))
    if not nqt_user:
        return nqt_loi('Không tìm thấy tài khoản', nqt_ma_trang=404)
    return nqt_ok(nqt_user.g6_to_dict())
