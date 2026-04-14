from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from backend.app.utils.g6_phan_hoi import nqt_loi


def nqt_yeu_cau_dang_nhap(f):
    @wraps(f)
    def nqt_wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception:
            return nqt_loi('Chưa đăng nhập', nqt_ma_trang=401)
        return f(*args, **kwargs)
    return nqt_wrapper


def nqt_yeu_cau_quyen(nqt_ten_quyen: str):
    def nqt_decorator(f):
        @wraps(f)
        def nqt_wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                return nqt_loi('Chưa đăng nhập', nqt_ma_trang=401)
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
