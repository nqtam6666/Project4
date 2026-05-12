from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import request
from backend.app.utils.g6_phan_hoi import nqt_loi
import json

def nqt_yeu_cau_dang_nhap(f):
    @wraps(f)
    def nqt_wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            nqt_claims = get_jwt()
            nqt_phien_id = nqt_claims.get('g6_phien_id')
            if nqt_phien_id:
                from backend.app.models.g6_xac_thuc import G6PhienDangNhap
                phien = G6PhienDangNhap.query.get(nqt_phien_id)
                if not phien or phien.g6_la_thu_hoi:
                    return nqt_loi('Phiên đăng nhập đã bị thu hồi', nqt_ma_trang=401)
        except Exception:
            return nqt_loi('Chưa đăng nhập hoặc phiên đã hết hạn', nqt_ma_trang=401)
        return f(*args, **kwargs)
    return nqt_wrapper


def nqt_yeu_cau_quyen(nqt_ten_quyen: str):
    def nqt_decorator(f):
        @wraps(f)
        def nqt_wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                nqt_claims = get_jwt()
                nqt_phien_id = nqt_claims.get('g6_phien_id')
                if nqt_phien_id:
                    from backend.app.models.g6_xac_thuc import G6PhienDangNhap
                    phien = G6PhienDangNhap.query.get(nqt_phien_id)
                    if not phien or phien.g6_la_thu_hoi:
                        return nqt_loi('Phiên đăng nhập đã bị thu hồi', nqt_ma_trang=401)
            except Exception:
                return nqt_loi('Chưa đăng nhập hoặc phiên đã hết hạn', nqt_ma_trang=401)
            nqt_claims = get_jwt()
            nqt_quyen_list = nqt_claims.get('g6_quyen', [])
            nqt_vai_tro = nqt_claims.get('g6_vai_tro', [])
            if 'G6QuanTri' in nqt_vai_tro:
                return f(*args, **kwargs)
            # Hỗ trợ cả 2 format: 'g6_xem_hoi_vien' và 'xem_hoi_vien'
            nqt_ten_quyen_goc = nqt_ten_quyen.replace('g6_', '', 1) if nqt_ten_quyen.startswith('g6_') else nqt_ten_quyen
            if nqt_ten_quyen not in nqt_quyen_list and nqt_ten_quyen_goc not in nqt_quyen_list:
                return nqt_loi('Không có quyền thực hiện', nqt_ma_trang=403)
            return f(*args, **kwargs)
        return nqt_wrapper
    return nqt_decorator


def nqt_ghi_nhat_ky(hanh_dong: str, ten_bang: str = None):
    """
    Decorator để ghi lại lịch sử thao tác của người dùng.
    Phải đặt SAU @nqt_yeu_cau_dang_nhap (để lấy được thông tin JWT).
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 1. Gọi hàm xử lý chính
            response = f(*args, **kwargs)
            
            # 2. Xử lý ghi log nếu thành công
            try:
                # Kiểm tra kết quả trả về có phải tuple (json, status_code) không
                # Flask jsonify() trả về Response object.
                # Response.get_json() lấy dữ liệu.
                if hasattr(response, 'get_json'):
                    data = response.get_json()
                elif isinstance(response, tuple) and len(response) > 0 and hasattr(response[0], 'get_json'):
                    data = response[0].get_json()
                else:
                    data = None

                # Chỉ log nếu kết quả thành công (nqt_thanh_cong = True)
                if data and data.get('nqt_thanh_cong') is True:
                    from backend.app.models.g6_xac_thuc import G6NhatKyHoatDong
                    from backend.app import db
                    
                    nqt_claims = get_jwt()
                    loai_nd = nqt_claims.get('g6_vai_tro', [''])[0] if nqt_claims.get('g6_vai_tro') else 'Unknown'
                    ma_nd = nqt_claims.get('sub') # sub is usually the user ID or identity

                    # Cố gắng lấy ID bị ảnh hưởng từ parameters URL
                    # VD: /api/nqt-san-pham/<int:nqt_id> -> kwargs có 'nqt_id'
                    ma_ban_ghi = None
                    for k, v in kwargs.items():
                        if k.endswith('_id') or k == 'nqt_id' or k == 'id':
                            ma_ban_ghi = v
                            break

                    nhat_ky = G6NhatKyHoatDong(
                        g6_loai_nguoi_dung=loai_nd,
                        g6_ma_nguoi_dung=ma_nd,
                        g6_hanh_dong=hanh_dong,
                        g6_ten_bang=ten_bang,
                        g6_ma_ban_ghi=ma_ban_ghi,
                        g6_dia_chi_ip=request.remote_addr,
                        g6_thiet_bi=request.user_agent.string[:200] if request.user_agent else None
                    )
                    db.session.add(nhat_ky)
                    db.session.commit()
            except Exception as e:
                # Không chặn lỗi chính nếu ghi log thất bại
                print(f"Lỗi ghi nhật ký hoạt động: {str(e)}")
                
            return response
        return wrapper
    return decorator
