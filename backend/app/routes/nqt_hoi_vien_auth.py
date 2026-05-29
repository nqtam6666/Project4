import uuid
import re
import bcrypt
from datetime import datetime, timedelta
from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    get_jwt_identity, get_jwt, verify_jwt_in_request
)
from backend.app import db
from backend.app.models.g6_nguoi_dung import G6NguoiDung
from backend.app.models.g6_hoi_vien import G6DangKyGoiTap, G6DiemDanh, G6ChiSoCoThe
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap
from backend.app.services.g6_dich_vu_cau_hinh import NqtDichVuCauHinh

nqt_hv_auth_bp = Blueprint('nqt_hv_auth', __name__, url_prefix='/api')


# ── Helpers ────────────────────────────────────────────────────────────────────
def _nqt_tao_jwt(nqt_ma_hoi_vien: int, nqt_ho_ten: str):
    nqt_jwt_giay = int(NqtDichVuCauHinh.g6_lay('nqt_jwt_hoi_vien_giay', nqt_mac_dinh=3600))
    nqt_refresh_ngay = int(NqtDichVuCauHinh.g6_lay('nqt_jwt_refresh_ngay', nqt_mac_dinh=7))
    return {
        'nqt_access_token': create_access_token(
            identity=f'hv:{nqt_ma_hoi_vien}',
            additional_claims={
                'g6_loai': 'hoi_vien',
                'g6_ho_ten': nqt_ho_ten,
            },
            expires_delta=timedelta(seconds=nqt_jwt_giay)
        ),
        'nqt_refresh_token': create_refresh_token(
            identity=f'hv:{nqt_ma_hoi_vien}',
            expires_delta=timedelta(days=nqt_refresh_ngay)
        ),
    }


# ── POST /api/nqt-hoi-vien/dang-ky ──────────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-hoi-vien/dang-ky', methods=['POST'])
def nqt_dang_ky_hoi_vien():
    nqt_data = request.get_json() or {}

    nqt_ho_ten = (nqt_data.get('nqt_ho_ten') or nqt_data.get('g6_ho_ten') or '').strip()
    nqt_sdt = (nqt_data.get('nqt_so_dien_thoai') or nqt_data.get('g6_so_dien_thoai') or '').strip()
    nqt_email = (nqt_data.get('nqt_email') or nqt_data.get('g6_email') or '').strip() or None
    nqt_mat_khau = nqt_data.get('nqt_mat_khau') or nqt_data.get('g6_mat_khau') or ''
    nqt_ma_chi_nhanh = nqt_data.get('nqt_ma_chi_nhanh') or 1

    # Validate
    if not nqt_ho_ten or len(nqt_ho_ten) < 2:
        return nqt_loi('Họ tên phải có ít nhất 2 ký tự', nqt_ma_trang=422)
    if not re.fullmatch(r'0\d{9,10}', nqt_sdt):
        return nqt_loi('Số điện thoại không hợp lệ (phải bắt đầu bằng 0, 10-11 số)', nqt_ma_trang=422)
    if len(nqt_mat_khau) < 6:
        return nqt_loi('Mật khẩu phải có ít nhất 6 ký tự', nqt_ma_trang=422)
    if nqt_email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', nqt_email):
        return nqt_loi('Email không hợp lệ', nqt_ma_trang=422)

    # Check duplicate SĐT
    if G6NguoiDung.query.filter_by(g6_so_dien_thoai=nqt_sdt).first():
        return nqt_loi('Số điện thoại đã được đăng ký', nqt_ma_trang=409)

    try:
        # Tạo G6NguoiDung (Hội viên)
        nqt_hoi_vien = G6NguoiDung(
            g6_ma_chi_nhanh=nqt_ma_chi_nhanh,
            g6_ho_ten=nqt_ho_ten,
            g6_so_dien_thoai=nqt_sdt,
            g6_email=nqt_email,
            g6_la_hoi_vien=True,
            g6_ngay_dang_ky=datetime.utcnow().date(),
            g6_ma_qr=str(uuid.uuid4())[:12].upper(),
        )
        nqt_hoi_vien.nqt_dat_mat_khau(nqt_mat_khau)
        db.session.add(nqt_hoi_vien)
        db.session.commit()

        # Trả JWT luôn
        from flask import make_response
        from flask_jwt_extended import set_access_cookies, set_refresh_cookies
        
        nqt_tokens = _nqt_tao_jwt(nqt_hoi_vien.g6_ma_nguoi_dung, nqt_hoi_vien.g6_ho_ten)
        
        nqt_response = make_response(nqt_ok({
            'nqt_hoi_vien': nqt_hoi_vien.g6_to_dict(),
            'nqt_access_token': nqt_tokens['nqt_access_token'],
            'nqt_refresh_token': nqt_tokens['nqt_refresh_token']
        }, 'Đăng ký thành công', nqt_ma_trang=201))
        
        set_access_cookies(nqt_response, nqt_tokens['nqt_access_token'])
        set_refresh_cookies(nqt_response, nqt_tokens['nqt_refresh_token'])
        
        return nqt_response

    except Exception as e:
        db.session.rollback()
        return nqt_loi(f'Lỗi đăng ký: {str(e)}', nqt_ma_trang=500)


# ── POST /api/nqt-hoi-vien/dang-nhap ─────────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-hoi-vien/dang-nhap', methods=['POST'])
def nqt_dang_nhap_hoi_vien():
    nqt_data = request.get_json() or {}
    nqt_identifier = (nqt_data.get('nqt_so_dien_thoai') or nqt_data.get('g6_so_dien_thoai') or '').strip()
    nqt_mat_khau = nqt_data.get('nqt_mat_khau') or nqt_data.get('g6_mat_khau') or ''

    if not nqt_identifier or not nqt_mat_khau:
        return nqt_loi('Thiếu thông tin đăng nhập hoặc mật khẩu')

    # Tìm hội viên qua Số điện thoại, Email hoặc Tên đăng nhập
    nqt_hoi_vien = G6NguoiDung.query.filter(
        (G6NguoiDung.g6_so_dien_thoai == nqt_identifier) | 
        (db.func.lower(G6NguoiDung.g6_email) == nqt_identifier.lower()) | 
        (db.func.lower(G6NguoiDung.g6_ten_dang_nhap) == nqt_identifier.lower()),
        G6NguoiDung.g6_la_hoi_vien == True
    ).first()

    if not nqt_hoi_vien:
        return nqt_loi('Thông tin đăng nhập hoặc mật khẩu không đúng', nqt_ma_trang=401)

    # Kiểm tra khóa
    if nqt_hoi_vien.g6_khoa_den and nqt_hoi_vien.g6_khoa_den > datetime.utcnow():
        return nqt_loi('Tài khoản tạm thời bị khóa. Thử lại sau 30 phút.', nqt_ma_trang=403)

    if not nqt_hoi_vien.g6_la_hoat_dong:
        return nqt_loi('Tài khoản đã bị vô hiệu hóa', nqt_ma_trang=403)

    # Xác thực mật khẩu
    if not nqt_hoi_vien.nqt_kiem_tra_mat_khau(nqt_mat_khau):
        nqt_so_lan_sai = int(NqtDichVuCauHinh.g6_lay('nqt_so_lan_sai_hoi_vien', nqt_mac_dinh=5))
        nqt_hoi_vien.g6_lan_dang_nhap_sai += 1
        if nqt_hoi_vien.g6_lan_dang_nhap_sai >= nqt_so_lan_sai:
            nqt_hoi_vien.nqt_khoa_tai_khoan()
        db.session.commit()
        return nqt_loi('Thông tin đăng nhập hoặc mật khẩu không đúng', nqt_ma_trang=401)

    # Reset
    nqt_hoi_vien.g6_lan_dang_nhap_sai = 0
    nqt_hoi_vien.g6_khoa_den = None
    db.session.commit()

    from flask import make_response
    from flask_jwt_extended import set_access_cookies, set_refresh_cookies
    
    nqt_tokens = _nqt_tao_jwt(nqt_hoi_vien.g6_ma_nguoi_dung, nqt_hoi_vien.g6_ho_ten)
    
    nqt_response = make_response(nqt_ok({
        'nqt_hoi_vien': nqt_hoi_vien.g6_to_dict(),
        'nqt_access_token': nqt_tokens['nqt_access_token'],
        'nqt_refresh_token': nqt_tokens['nqt_refresh_token']
    }, 'Đăng nhập thành công'))
    
    set_access_cookies(nqt_response, nqt_tokens['nqt_access_token'])
    set_refresh_cookies(nqt_response, nqt_tokens['nqt_refresh_token'])
    
    return nqt_response


@nqt_hv_auth_bp.route('/nqt-hoi-vien/google-login', methods=['POST'])
def nqt_dang_nhap_google():
    import urllib.request
    import json
    import os
    import random
    import string
    
    nqt_data = request.get_json() or {}
    nqt_token = nqt_data.get('nqt_google_token') or nqt_data.get('credential')
    
    if not nqt_token:
        return nqt_loi('Thiếu Google Token')
        
    try:
        # Gọi API của Google để verify token
        nqt_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={nqt_token}"
        nqt_req = urllib.request.Request(nqt_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(nqt_req, timeout=10) as nqt_response:
            nqt_res_data = json.loads(nqt_response.read().decode('utf-8'))
            
        if 'error_description' in nqt_res_data or 'sub' not in nqt_res_data:
            return nqt_loi('Token Google không hợp lệ hoặc đã hết hạn', nqt_ma_trang=400)
            
        nqt_google_id = nqt_res_data.get('sub')
        nqt_email = nqt_res_data.get('email')
        nqt_name = nqt_res_data.get('name')
        nqt_picture = nqt_res_data.get('picture')
        
        # Kiểm tra aud có khớp với GOOGLE_CLIENT_ID không
        nqt_client_id = os.environ.get('GOOGLE_CLIENT_ID')
        if nqt_client_id and nqt_res_data.get('aud') != nqt_client_id:
            # Nếu chạy local và client ID khớp với placeholder, bỏ qua check aud để tiện test
            if nqt_client_id != 'your-google-client-id-here.apps.googleusercontent.com':
                return nqt_loi('Ứng dụng Client ID không khớp', nqt_ma_trang=400)
            
        # Tìm người dùng trong database
        nqt_user = G6NguoiDung.query.filter(
            (G6NguoiDung.g6_google_id == nqt_google_id) |
            ((G6NguoiDung.g6_email == nqt_email) & (G6NguoiDung.g6_email.isnot(None)))
        ).first()
        
        if nqt_user:
            # Nếu tìm thấy nhưng chưa gán google_id, gán luôn
            if not nqt_user.g6_google_id:
                nqt_user.g6_google_id = nqt_google_id
            # Cập nhật avatar nếu có
            if nqt_picture and not nqt_user.g6_anh_dai_dien:
                nqt_user.g6_anh_dai_dien = nqt_picture
            db.session.commit()
        else:
            # Tạo người dùng mới (Hội viên mới)
            nqt_user = G6NguoiDung(
                g6_ho_ten=nqt_name,
                g6_email=nqt_email,
                g6_google_id=nqt_google_id,
                g6_anh_dai_dien=nqt_picture,
                g6_la_hoi_vien=True,
                g6_la_hoat_dong=True,
                g6_ngay_dang_ky=datetime.utcnow().date(),
                g6_ma_qr=str(uuid.uuid4())[:12].upper(),
                g6_so_dien_thoai=f"00{str(uuid.uuid4().fields[0])[:8]}"
            )
            # Đặt mật khẩu ngẫu nhiên
            nqt_rand_pw = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            nqt_user.nqt_dat_mat_khau(nqt_rand_pw)
            
            db.session.add(nqt_user)
            db.session.commit()
            
        # Tạo JWT tokens
        from flask import make_response
        from flask_jwt_extended import set_access_cookies, set_refresh_cookies
        
        nqt_tokens = _nqt_tao_jwt(nqt_user.g6_ma_nguoi_dung, nqt_user.g6_ho_ten)
        
        nqt_response = make_response(nqt_ok({
            'nqt_hoi_vien': nqt_user.g6_to_dict(),
            'nqt_access_token': nqt_tokens['nqt_access_token'],
            'nqt_refresh_token': nqt_tokens['nqt_refresh_token']
        }, 'Đăng nhập Google thành công'))
        
        set_access_cookies(nqt_response, nqt_tokens['nqt_access_token'])
        set_refresh_cookies(nqt_response, nqt_tokens['nqt_refresh_token'])
        
        return nqt_response
        
    except Exception as e:
        db.session.rollback()
        return nqt_loi(f'Lỗi đăng nhập bằng Google: {str(e)}', nqt_ma_trang=500)


# ── GET /api/nqt-hoi-vien/toi ────────────────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-hoi-vien/toi', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_profile_hoi_vien():
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)

    nqt_hoi_vien = G6NguoiDung.query.filter_by(g6_ma_nguoi_dung=nqt_ma, g6_la_hoi_vien=True).first()
    if not nqt_hoi_vien:
        return nqt_loi('Không tìm thấy hội viên', nqt_ma_trang=404)

    # Lấy gói đang hoạt động
    nqt_dang_ky_hd = None
    for dk in (nqt_hoi_vien.g6_dang_ky or []):
        if dk.g6_trang_thai == 'dang_hoat_dong':
            nqt_dang_ky_hd = dk
            break

    return nqt_ok({
        'nqt_hoi_vien': nqt_hoi_vien.g6_to_dict(),
        'nqt_goi_hien_tai': nqt_dang_ky_hd.g6_to_dict() if nqt_dang_ky_hd else None,
    })


# ── PUT /api/nqt-hoi-vien/toi ─────────────────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-hoi-vien/toi', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_profile_hoi_vien():
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)

    nqt_hoi_vien = G6NguoiDung.query.filter_by(g6_ma_nguoi_dung=nqt_ma, g6_la_hoi_vien=True).first()
    if not nqt_hoi_vien:
        return nqt_loi('Không tìm thấy hội viên', nqt_ma_trang=404)

    nqt_data = request.get_json() or {}
    nqt_ho_ten = (nqt_data.get('g6_ho_ten') or '').strip()
    nqt_email = (nqt_data.get('g6_email') or '').strip() or None
    nqt_dia_chi = (nqt_data.get('g6_dia_chi') or '').strip() or None
    nqt_ngay_sinh = nqt_data.get('g6_ngay_sinh') or None
    nqt_gioi_tinh = nqt_data.get('g6_gioi_tinh') or None
    nqt_anh_the = nqt_data.get('g6_anh_the')

    if nqt_ho_ten and len(nqt_ho_ten) < 2:
        return nqt_loi('Họ tên phải có ít nhất 2 ký tự', nqt_ma_trang=422)
    if nqt_email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', nqt_email):
        return nqt_loi('Email không hợp lệ', nqt_ma_trang=422)

    if nqt_ho_ten:
        nqt_hoi_vien.g6_ho_ten = nqt_ho_ten
    nqt_hoi_vien.g6_email = nqt_email
    nqt_hoi_vien.g6_dia_chi = nqt_dia_chi
    nqt_hoi_vien.g6_gioi_tinh = nqt_gioi_tinh
    if 'g6_anh_the' in nqt_data:
        nqt_hoi_vien.g6_anh_the = nqt_anh_the
    if nqt_ngay_sinh:
        try:
            from datetime import date
            nqt_hoi_vien.g6_ngay_sinh = date.fromisoformat(nqt_ngay_sinh)
        except ValueError:
            pass

    db.session.commit()
    return nqt_ok({'nqt_hoi_vien': nqt_hoi_vien.g6_to_dict()}, 'Cập nhật thông tin thành công')


@nqt_hv_auth_bp.route('/nqt-hoi-vien/dang-xuat', methods=['POST'])
def nqt_dang_xuat_hoi_vien():
    from flask_jwt_extended import unset_jwt_cookies
    from flask import make_response
    nqt_response = make_response(nqt_ok(None, 'Đăng xuất thành công'))
    unset_jwt_cookies(nqt_response)
    return nqt_response


# ── PUT /api/nqt-hoi-vien/doi-mat-khau ───────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-hoi-vien/doi-mat-khau', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_doi_mat_khau_hoi_vien():
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)

    nqt_data = request.get_json() or {}
    nqt_mk_cu = nqt_data.get('nqt_mat_khau_cu') or ''
    nqt_mk_moi = nqt_data.get('nqt_mat_khau_moi') or ''

    if len(nqt_mk_moi) < 6:
        return nqt_loi('Mật khẩu mới phải có ít nhất 6 ký tự', nqt_ma_trang=422)

    nqt_hoi_vien = G6NguoiDung.query.filter_by(g6_ma_nguoi_dung=nqt_ma, g6_la_hoi_vien=True).first()
    if not nqt_hoi_vien:
        return nqt_loi('Không tìm thấy tài khoản', nqt_ma_trang=404)

    if not nqt_hoi_vien.nqt_kiem_tra_mat_khau(nqt_mk_cu):
        return nqt_loi('Mật khẩu hiện tại không đúng', nqt_ma_trang=401)

    nqt_hoi_vien.nqt_dat_mat_khau(nqt_mk_moi)
    db.session.commit()
    return nqt_ok(None, 'Đổi mật khẩu thành công')


# ── GET /api/nqt-dang-ky-goi-tap (member tự xem gói của mình) ────────────────
@nqt_hv_auth_bp.route('/nqt-dang-ky-goi-tap', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_dang_ky_goi_tap_cua_toi():
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)

    nqt_list = G6DangKyGoiTap.query.filter_by(g6_ma_nguoi_dung=nqt_ma)\
        .order_by(G6DangKyGoiTap.g6_ngay_bat_dau.desc()).all()
    return nqt_ok([d.g6_to_dict() for d in nqt_list])


# ── GET /api/nqt-hoi-vien/diem-danh (member xem lịch sử check-in) ────────────
@nqt_hv_auth_bp.route('/nqt-hoi-vien/diem-danh', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_diem_danh_cua_toi():
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)

    nqt_gioi_han = request.args.get('g6_gioi_han', 20, type=int)
    nqt_list = G6DiemDanh.query.filter_by(g6_ma_nguoi_dung=nqt_ma)\
        .order_by(G6DiemDanh.g6_thoi_gian_vao.desc())\
        .limit(nqt_gioi_han).all()
    return nqt_ok([d.g6_to_dict() for d in nqt_list])


# ── GET /api/nqt-hoi-vien/toi/nqt-chi-so ─────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-hoi-vien/toi/nqt-chi-so', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_chi_so_cua_toi():
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)

    nqt_gioi_han = request.args.get('g6_gioi_han', 10, type=int)
    nqt_list = G6ChiSoCoThe.query.filter_by(g6_ma_nguoi_dung=nqt_ma)\
        .order_by(G6ChiSoCoThe.g6_ngay_do.desc())\
        .limit(nqt_gioi_han).all()
    return nqt_ok([c.g6_to_dict() for c in nqt_list])


# ── POST /api/nqt-hoi-vien/quen-mat-khau ─────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-hoi-vien/quen-mat-khau', methods=['POST'])
def nqt_quen_mat_khau():
    import random
    from backend.app.utils.nqt_email import nqt_gui_email

    nqt_data = request.get_json() or {}
    nqt_email = (nqt_data.get('g6_email') or '').strip()
    nqt_sdt = (nqt_data.get('g6_so_dien_thoai') or '').strip()

    if not nqt_email and not nqt_sdt:
        return nqt_loi('Vui lòng cung cấp địa chỉ Email hoặc Số điện thoại', nqt_ma_trang=400)

    nqt_hoi_vien = None
    if nqt_email:
        nqt_hoi_vien = G6NguoiDung.query.filter(db.func.lower(G6NguoiDung.g6_email) == nqt_email.lower(), G6NguoiDung.g6_la_hoi_vien == True).first()
    elif nqt_sdt:
        nqt_hoi_vien = G6NguoiDung.query.filter(G6NguoiDung.g6_so_dien_thoai == nqt_sdt, G6NguoiDung.g6_la_hoi_vien == True).first()

    if not nqt_hoi_vien:
        return nqt_loi('Không tìm thấy tài khoản đã đăng ký', nqt_ma_trang=404)

    nqt_email_gui = nqt_hoi_vien.g6_email or nqt_email
    if not nqt_email_gui:
        return nqt_loi('Tài khoản này chưa đăng ký địa chỉ Email để khôi phục mật khẩu. Vui lòng liên hệ quầy lễ tân.', nqt_ma_trang=400)

    try:
        # Tạo OTP ngẫu nhiên gồm 6 chữ số
        nqt_otp = f"{random.randint(100000, 999999)}"
        nqt_hoi_vien.g6_reset_token = nqt_otp
        nqt_hoi_vien.g6_reset_token_het_han = datetime.utcnow() + timedelta(minutes=10)
        db.session.commit()

        # Gửi email qua SMTP
        nqt_tieu_de = "🔑 Mã khôi phục mật khẩu - G6 Gym Portal"
        nqt_html_noi_dung = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f8fafc; padding: 20px;">
            <div style="max-width: 550px; margin: 0 auto; background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: #C9A84C; margin: 0;">G6 Gym Portal</h2>
                    <p style="font-size: 13px; color: #64748b; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px;">Khôi phục mật khẩu</p>
                </div>
                <hr style="border: none; border-top: 1px solid #f1f5f9; margin-bottom: 25px;">
                <p>Xin chào <strong>{nqt_hoi_vien.g6_ho_ten}</strong>,</p>
                <p>Chúng tôi đã nhận được yêu cầu khôi phục mật khẩu cho tài khoản của bạn. Vui lòng sử dụng mã xác minh dưới đây để thiết lập mật khẩu mới (Mã có hiệu lực trong vòng <strong>10 phút</strong>):</p>
                <div style="text-align: center; margin: 30px 0;">
                    <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; padding: 12px 30px; background-color: #f8fafc; border-radius: 12px; color: #1e293b; border: 1px solid #cbd5e1; display: inline-block;">{nqt_otp}</span>
                </div>
                <p style="font-size: 13px; color: #64748b; text-align: center; margin-top: 25px;">Nếu bạn không thực hiện yêu cầu này, bạn có thể bỏ qua email này một cách an toàn.</p>
                <hr style="border: none; border-top: 1px solid #f1f5f9; margin-top: 30px; margin-bottom: 20px;">
                <p style="font-size: 12px; color: #94a3b8; text-align: center; margin: 0;">&copy; 2026 G6 Gym Luxury Center. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        nqt_gui_email(nqt_email_gui, nqt_tieu_de, nqt_html_noi_dung)
        return nqt_ok(None, 'Mã xác nhận khôi phục mật khẩu đã được gửi đến email của bạn')

    except Exception as e:
        db.session.rollback()
        return nqt_loi(f'Lỗi khi gửi email khôi phục: {str(e)}', nqt_ma_trang=500)


# ── POST /api/nqt-hoi-vien/dat-lai-mat-khau ──────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-hoi-vien/dat-lai-mat-khau', methods=['POST'])
def nqt_dat_lai_mat_khau():
    nqt_data = request.get_json() or {}
    nqt_email = (nqt_data.get('g6_email') or '').strip()
    nqt_sdt = (nqt_data.get('g6_so_dien_thoai') or '').strip()
    nqt_otp = (nqt_data.get('g6_reset_token') or nqt_data.get('g6_token') or '').strip()
    nqt_mk_moi = nqt_data.get('g6_mat_khau_moi') or ''

    if not nqt_otp or not nqt_mk_moi:
        return nqt_loi('Vui lòng cung cấp mã xác nhận và mật khẩu mới', nqt_ma_trang=400)

    if len(nqt_mk_moi) < 6:
        return nqt_loi('Mật khẩu mới phải có ít nhất 6 ký tự', nqt_ma_trang=422)

    nqt_hoi_vien = None
    if nqt_email:
        nqt_hoi_vien = G6NguoiDung.query.filter(db.func.lower(G6NguoiDung.g6_email) == nqt_email.lower(), G6NguoiDung.g6_la_hoi_vien == True).first()
    elif nqt_sdt:
        nqt_hoi_vien = G6NguoiDung.query.filter(G6NguoiDung.g6_so_dien_thoai == nqt_sdt, G6NguoiDung.g6_la_hoi_vien == True).first()
    else:
        nqt_hoi_vien = G6NguoiDung.query.filter(G6NguoiDung.g6_reset_token == nqt_otp, G6NguoiDung.g6_la_hoi_vien == True).first()

    if not nqt_hoi_vien:
        return nqt_loi('Không tìm thấy tài khoản phù hợp', nqt_ma_trang=404)

    if not nqt_hoi_vien.g6_reset_token or nqt_hoi_vien.g6_reset_token != nqt_otp:
        return nqt_loi('Mã xác nhận không chính xác', nqt_ma_trang=400)

    if nqt_hoi_vien.g6_reset_token_het_han and nqt_hoi_vien.g6_reset_token_het_han < datetime.utcnow():
        return nqt_loi('Mã xác nhận đã hết hạn', nqt_ma_trang=400)

    try:
        nqt_hoi_vien.nqt_dat_mat_khau(nqt_mk_moi)
        nqt_hoi_vien.g6_reset_token = None
        nqt_hoi_vien.g6_reset_token_het_han = None
        nqt_hoi_vien.g6_lan_dang_nhap_sai = 0
        nqt_hoi_vien.g6_khoa_den = None
        db.session.commit()
        return nqt_ok(None, 'Đặt lại mật khẩu thành công')
    except Exception as e:
        db.session.rollback()
        return nqt_loi(f'Lỗi khi cập nhật mật khẩu: {str(e)}', nqt_ma_trang=500)

# ── POST /api/nqt-mua-goi-tap ────────────────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-mua-goi-tap', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_mua_goi_tap_cua_toi():
    from backend.app.models.g6_hoi_vien import G6GoiTap, G6DangKyGoiTap
    from datetime import date, timedelta
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)
    
    nqt_data = request.get_json() or {}
    nqt_gt_id = nqt_data.get('g6_ma_goi_tap')
    if not nqt_gt_id:
        return nqt_loi('Thiếu mã gói tập')
        
    nqt_gt = G6GoiTap.query.get_or_404(nqt_gt_id)
    nqt_hv = G6NguoiDung.query.get_or_404(nqt_ma)
    
    nqt_ngay_bd = date.today()
    nqt_ngay_hh = nqt_ngay_bd + timedelta(days=nqt_gt.g6_so_ngay)
    nqt_gia = float(nqt_gt.g6_gia_khuyen_mai or nqt_gt.g6_gia)
    
    nqt_row = G6DangKyGoiTap(
        g6_ma_nguoi_dung=nqt_ma,
        g6_ma_goi_tap=nqt_gt_id,
        g6_ma_chi_nhanh=nqt_hv.g6_ma_chi_nhanh,
        g6_ngay_bat_dau=nqt_ngay_bd,
        g6_ngay_het_han=nqt_ngay_hh,
        g6_gia_thuc_te=nqt_gia,
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Mua gói tập thành công', 201)

# ── POST /api/nqt-mua-goi-pt ─────────────────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-mua-goi-pt', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_mua_goi_pt_cua_toi():
    from backend.app.models.g6_huan_luyen_vien import G6GoiPT, G6DangKyGoiPT, G6HuanLuyenVien
    from datetime import date, timedelta
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)
    
    nqt_data = request.get_json() or {}
    nqt_hlv_id = nqt_data.get('g6_ma_hlv')
    nqt_goi_id = nqt_data.get('g6_ma_goi_pt')
    
    if nqt_hlv_id:
        nxv_goi = G6GoiPT.query.filter_by(g6_ma_hlv=nqt_hlv_id, g6_la_hoat_dong=True).first()
        if not nxv_goi:
            return nqt_loi('Huấn luyện viên chưa có gói PT nào')
    elif nqt_goi_id:
        nxv_goi = G6GoiPT.query.get_or_404(nqt_goi_id)
    else:
        return nqt_loi('Thiếu thông tin gói PT hoặc HLV')
    if not nxv_goi.g6_la_hoat_dong:
        return nqt_loi('Gói PT không còn hoạt động')
        
    nxv_hlv = G6HuanLuyenVien.query.get_or_404(nxv_goi.g6_ma_hlv)
    if nxv_hlv.g6_so_hoi_vien_hien_tai >= nxv_hlv.g6_toi_da_hoi_vien:
        return nqt_loi('Huấn luyện viên đã đạt tối đa hội viên')
        
    nxv_ngay_mua = date.today()
    nxv_ngay_hh = nxv_ngay_mua + timedelta(days=nxv_goi.g6_hieu_luc_ngay)
    nxv_gia = float(nxv_goi.g6_gia_khuyen_mai or nxv_goi.g6_gia)
    
    nxv_row = G6DangKyGoiPT(
        g6_ma_nguoi_dung=nqt_ma,
        g6_ma_goi_pt=nxv_goi.g6_ma_goi_pt,
        g6_ma_hlv=nxv_goi.g6_ma_hlv,
        g6_ngay_mua=nxv_ngay_mua,
        g6_ngay_het_han=nxv_ngay_hh,
        g6_so_buoi_con_lai=nxv_goi.g6_so_buoi,
        g6_gia_thuc_te=nxv_gia,
    )
    db.session.add(nxv_row)
    nxv_hlv.g6_so_hoi_vien_hien_tai += 1
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Đăng ký PT thành công', 201)

# ── POST /api/nqt-dat-cho-lop ────────────────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-dat-cho-lop', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_dat_cho_lop_cua_toi():
    from backend.app.models.g6_lop_hoc import G6LichLopHoc, G6DatChoLopHoc
    from datetime import date
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)
        
    nqt_data = request.get_json() or {}
    nxv_lop_id = nqt_data.get('g6_ma_lop_hoc')
    nxv_lich_id = nqt_data.get('g6_ma_lich_lop')
    nxv_ngay = nqt_data.get('g6_ngay_tap') or str(date.today())
    
    if nxv_lop_id:
        nxv_lich = G6LichLopHoc.query.filter_by(g6_ma_lop_hoc=nxv_lop_id, g6_la_hoat_dong=True).first()
        if not nxv_lich:
            return nqt_loi('Lớp học chưa có lịch xếp sẵn')
        nxv_lich_id = nxv_lich.g6_ma_lich_lop
    elif nxv_lich_id:
        nxv_lich = G6LichLopHoc.query.get_or_404(nxv_lich_id)
    else:
        return nqt_loi('Thiếu thông tin lịch lớp')
        
    nxv_trung = G6DatChoLopHoc.query.filter_by(
        g6_ma_lich_lop=nxv_lich_id,
        g6_ma_nguoi_dung=nqt_ma,
        g6_ngay_tap=nxv_ngay,
    ).filter(G6DatChoLopHoc.g6_trang_thai != 'da_huy').first()
    if nxv_trung:
        return nqt_loi('Bạn đã đặt chỗ cho lớp này rồi')
        
    nxv_so_dat = G6DatChoLopHoc.query.filter_by(
        g6_ma_lich_lop=nxv_lich_id,
        g6_ngay_tap=nxv_ngay,
    ).filter(G6DatChoLopHoc.g6_trang_thai.in_(['dat_cho', 'da_den'])).count()
    if nxv_so_dat >= nxv_lich.g6_suc_chua_toi_da:
        return nqt_loi('Lớp học đã đầy chỗ')

    nxv_row = G6DatChoLopHoc(
        g6_ma_lich_lop=nxv_lich_id,
        g6_ma_nguoi_dung=nqt_ma,
        g6_ngay_tap=nxv_ngay,
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Đặt chỗ thành công', 201)

# ── POST /api/nqt-dat-lich-pt ────────────────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-dat-lich-pt', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_dat_lich_pt_cua_toi():
    from backend.app.models.g6_huan_luyen_vien import G6DangKyGoiPT, G6BuoiTapPT
    from datetime import date
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)
        
    nqt_data = request.get_json() or {}
    nxv_dk_id = nqt_data.get('g6_ma_dang_ky_pt')
    nxv_ngay_tap = nqt_data.get('g6_ngay_tap') or str(date.today())
    if not nxv_dk_id:
        return nqt_loi('Thiếu mã đăng ký PT')

    nxv_dk = G6DangKyGoiPT.query.filter_by(g6_ma_dang_ky_pt=nxv_dk_id, g6_ma_nguoi_dung=nqt_ma).first_or_404()

    if nxv_dk.g6_so_buoi_con_lai <= 0:
        return nqt_loi('Gói PT đã hết buổi tập')
    if nxv_dk.g6_ngay_het_han < date.today():
        return nqt_loi('Gói PT đã hết hạn')
    if nxv_dk.g6_trang_thai != 'dang_dung':
        return nqt_loi('Gói PT không còn hoạt động')

    nqt_hv = G6NguoiDung.query.get(nqt_ma)

    nxv_row = G6BuoiTapPT(
        g6_ma_dang_ky_pt=nxv_dk_id,
        g6_ma_nguoi_dung=nqt_ma,
        g6_ma_hlv=nxv_dk.g6_ma_hlv,
        g6_ma_chi_nhanh=nqt_hv.g6_ma_chi_nhanh,
        g6_ngay_tap=nxv_ngay_tap,
        g6_thoi_luong=60,
        g6_trang_thai='cho_xac_nhan',
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Đặt lịch PT thành công', 201)


# ── POST /api/nqt-chatbot ───────────────────────────────────────────────────
@nqt_hv_auth_bp.route('/nqt-chatbot', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_chatbot_assistant():
    from backend.app.models.g6_hoi_vien import G6GoiTap, G6DangKyGoiTap
    from backend.app.models.g6_huan_luyen_vien import G6HuanLuyenVien, G6DangKyGoiPT
    from backend.app.models.g6_san_pham import G6SanPham
    from backend.app.models.g6_nguoi_dung import G6NguoiDung
    from datetime import date
    
    nqt_identity = get_jwt_identity()
    try:
        nqt_ma = int(nqt_identity.split(':')[1])
    except Exception:
        return nqt_loi('Token không hợp lệ', nqt_ma_trang=401)
        
    nqt_data = request.get_json() or {}
    message = nqt_data.get('message', '').strip()
    if not message:
        return nqt_loi('Vui lòng gửi câu hỏi')
        
    user = G6NguoiDung.query.get(nqt_ma)
    user_name = user.g6_ho_ten if user else "Hội viên"
    user_first_name = user_name.split()[-1] if user_name else "bạn"
    
    lower_msg = message.lower()
    
    response_text = ""
    action = None
    
    # 1. Gói tập của tôi / Gói đang sử dụng
    if any(k in lower_msg for k in ["gói của tôi", "goi cua toi", "gói đang dùng", "gói đang sử dụng", "gói của em", "lịch tập của tôi", "lịch sử tập"]):
        active_taps = G6DangKyGoiTap.query.filter_by(g6_ma_nguoi_dung=nqt_ma).filter(G6DangKyGoiTap.g6_ngay_het_han >= date.today()).all()
        active_pts = G6DangKyGoiPT.query.filter_by(g6_ma_nguoi_dung=nqt_ma).filter(G6DangKyGoiPT.g6_ngay_het_han >= date.today()).all()
        
        parts = [f"Dạ {user_first_name}, đây là thông tin gói dịch vụ hiện tại của bạn:"]
        
        if active_taps:
            parts.append("\n**Gói thành viên:**")
            for tap in active_taps:
                parts.append(f"- Gói: {tap.g6_goi_tap.g6_ten_goi if tap.g6_goi_tap else 'Gói Tập'} (Hạn dùng: {tap.g6_ngay_het_han.strftime('%d/%m/%Y')})")
        else:
            parts.append("\n- Bạn chưa đăng ký gói tập thành viên nào đang hoạt động.")
            
        if active_pts:
            parts.append("\n**Gói Huấn luyện viên PT:**")
            for pt in active_pts:
                parts.append(f"- HLV: {pt.g6_goi_pt.g6_hlv.g6_nhan_vien.g6_ho_ten if pt.g6_goi_pt and pt.g6_goi_pt.g6_hlv else 'PT'} (Còn lại: {pt.g6_so_buoi_con_lai} buổi, Hạn dùng: {pt.g6_ngay_het_han.strftime('%d/%m/%Y')})")
        else:
            parts.append("\n- Bạn chưa đăng ký gói tập với Huấn luyện viên PT.")
            
        response_text = "\n".join(parts)
        
    # 2. Xem các gói tập (Mua gói tập)
    elif any(k in lower_msg for k in ["gói tập", "goi tap", "mua gói", "gói gym"]):
        goi_taps = G6GoiTap.query.filter_by(g6_la_hoat_dong=True).all()
        parts = [f"Hiện tại G6 Gym đang cung cấp các gói tập thành viên cao cấp sau:"]
        for g in goi_taps:
            gia_ban = g.g6_gia_khuyen_mai or g.g6_gia
            parts.append(f"- **{g.g6_ten_goi}**: {int(gia_ban):,} VNĐ / {g.g6_so_ngay} ngày. ({g.g6_mo_ta or ''})")
        
        response_text = "\n".join(parts)
        action = {
            "label": "Xem các Gói Tập 🛒",
            "type": "tab",
            "target": "goi-tap"
        }
        
    # 3. Tìm huấn luyện viên
    elif any(k in lower_msg for k in ["huấn luyện viên", "huan luyen vien", "pt", "hlv", "thuê pt"]):
        hlvs = G6HuanLuyenVien.query.filter_by(g6_la_hien_thi_web=True).limit(5).all()
        parts = [f"Dạ {user_first_name}, đây là danh sách các Huấn luyện viên cá nhân (PT) nổi bật tại chi nhánh:"]
        for h in hlvs:
            chuyen_mon = h.g6_chuyen_mon or "Tăng cơ, giảm mỡ"
            if isinstance(chuyen_mon, str) and (chuyen_mon.startswith('[') or chuyen_mon.startswith('{')):
                import json
                try:
                    cm_list = json.loads(chuyen_mon)
                    chuyen_mon = ", ".join(cm_list) if isinstance(cm_list, list) else chuyen_mon
                except:
                    pass
            parts.append(f"- **HLV {h.g6_nhan_vien.g6_ho_ten if h.g6_nhan_vien else 'PT'}**: {h.g6_so_nam_kinh_nghiem} năm kinh nghiệm. Chuyên môn: {chuyen_mon}.")
            
        response_text = "\n".join(parts)
        action = {
            "label": "Gặp Huấn Luyện Viên 📅",
            "type": "tab",
            "target": "pt"
        }
        
    # 4. Tìm sản phẩm / thực phẩm bổ sung
    elif any(k in lower_msg for k in ["sản phẩm", "san pham", "cửa hàng", "cua hang", "mua đồ", "whey", "bcaa", "creatine", "nước uống", "dinh dưỡng", "calo", "protein", "ăn gì"]):
        sp = G6SanPham.query.filter_by(g6_la_hoat_dong=True).limit(5).all()
        parts = [f"Danh sách sản phẩm bổ sung thể hình & phụ kiện đang bán chạy tại G6 Shop:"]
        for s in sp:
            gia_sp = s.g6_to_dict().get('g6_gia_ban') or s.g6_gia if hasattr(s, 'g6_gia') else 0
            parts.append(f"- **{s.g6_ten_san_pham}**: {int(gia_sp):,} VNĐ.")
            
        response_text = "\n".join(parts)
        action = {
            "label": "Ghé Cửa Hàng 🍏",
            "type": "tab",
            "target": "shop"
        }
        
    # 5. Chào hỏi
    elif any(k in lower_msg for k in ["chào", "hello", "hi"]):
        response_text = f"Xin chào {user_name}! Tôi là Trợ lý ảo AI của G6 Gym. Hôm nay tôi có thể giúp gì cho bạn? Bạn có thể hỏi tôi về: Gói tập, Đặt lịch PT, Cửa hàng hoặc Lịch tập của bạn."
        
    # 6. Giờ mở cửa / địa chỉ
    elif any(k in lower_msg for k in ["giờ mở cửa", "gio mo cua", "mấy giờ"]):
        mo_cua = NqtDichVuCauHinh.g6_lay("g6_gio_mo_cua", nqt_mac_dinh="05:00")
        dong_cua = NqtDichVuCauHinh.g6_lay("g6_gio_dong_cua", nqt_mac_dinh="23:00")
        response_text = f"G6 Gym Luxury Center mở cửa hoạt động từ **{mo_cua} - {dong_cua}** tất cả các ngày trong tuần (kể cả ngày nghỉ, lễ). Rất hân hạnh được đón tiếp bạn!"
    elif any(k in lower_msg for k in ["địa chỉ", "dia chi", "ở đâu"]):
        dia_chi = NqtDichVuCauHinh.g6_lay("g6_dia_chi_tru_so", nqt_mac_dinh="Xã Đại Thanh, Hà Nội")
        hotline = NqtDichVuCauHinh.g6_lay("g6_so_dien_thoai_hotline", nqt_mac_dinh="096 1138 440")
        response_text = f"G6 Gym Luxury Center tọa lạc tại {dia_chi}. Hotline hỗ trợ: {hotline}."
        
    # 7. Fallback
    else:
        response_text = f"Cảm ơn câu hỏi của bạn. Câu hỏi của bạn đã được chuyển đến bộ phận hỗ trợ khách hàng của G6 Gym. Chúng tôi sẽ liên hệ lại qua SĐT {user.g6_so_dien_thoai if user else ''} trong giây lát! Bạn cũng có thể thử hỏi tôi các câu hỏi như: 'gói của tôi', 'gói tập', 'danh sách pt', hoặc 'sản phẩm shop'."
        
    return nqt_ok({
        "text": response_text,
        "action": action
    })

