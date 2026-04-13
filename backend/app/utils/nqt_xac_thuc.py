from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from backend.app.utils.nqt_phan_hoi import nqt_loi


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
            nqt_quyen_list = nqt_claims.get('nqt_quyen', [])
            nqt_vai_tro = nqt_claims.get('nqt_vai_tro', [])
            if 'NqtQuanTri' in nqt_vai_tro:
                return f(*args, **kwargs)
            if nqt_ten_quyen not in nqt_quyen_list:
                return nqt_loi('Không có quyền thực hiện', nqt_ma_trang=403)
            return f(*args, **kwargs)
        return nqt_wrapper
    return nqt_decorator
