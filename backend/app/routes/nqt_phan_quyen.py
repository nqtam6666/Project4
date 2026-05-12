from flask import Blueprint, request
from backend.app.models.g6_nguoi_dung import G6VaiTro, G6QuyenHan, G6VaiTroQuyen, G6NguoiDungVaiTro, G6NguoiDung
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen
from backend.app import db

nqt_phan_quyen_bp = Blueprint('nqt_phan_quyen', __name__, url_prefix='/api')

# ==========================================
# 1. QUYỀN HẠN (PERMISSIONS)
# ==========================================

@nqt_phan_quyen_bp.route('/nqt-quyen-han', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_lay_danh_sach_quyen():
    nqt_danh_sach = G6QuyenHan.query.all()
    # Nhóm quyền theo g6_nhom_quyen để hiển thị trên frontend dễ dàng hơn
    nqt_ket_qua = {}
    for quyen in nqt_danh_sach:
        nhom = quyen.g6_nhom_quyen
        if nhom not in nqt_ket_qua:
            nqt_ket_qua[nhom] = []
        nqt_ket_qua[nhom].append(quyen.g6_to_dict())
    
    return nqt_ok({
        'g6_danh_sach_nhom': nqt_ket_qua,
        'g6_tong_so': len(nqt_danh_sach)
    }, 'Lấy danh sách quyền hạn thành công')


# ==========================================
# 2. VAI TRÒ (ROLES)
# ==========================================

@nqt_phan_quyen_bp.route('/nqt-vai-tro', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_lay_danh_sach_vai_tro():
    nqt_danh_sach = G6VaiTro.query.all()
    return nqt_ok([v.g6_to_dict() for v in nqt_danh_sach], 'Lấy danh sách vai trò thành công')

@nqt_phan_quyen_bp.route('/nqt-vai-tro', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_tao_vai_tro():
    nqt_data = request.get_json() or {}
    nqt_ten_vai_tro = nqt_data.get('g6_ten_vai_tro')
    nqt_mo_ta = nqt_data.get('g6_mo_ta')

    if not nqt_ten_vai_tro:
        return nqt_loi('Tên vai trò không được để trống')

    # Kiểm tra trùng tên
    if G6VaiTro.query.filter_by(g6_ten_vai_tro=nqt_ten_vai_tro).first():
        return nqt_loi('Tên vai trò đã tồn tại')

    nqt_vai_tro = G6VaiTro(g6_ten_vai_tro=nqt_ten_vai_tro, g6_mo_ta=nqt_mo_ta)
    db.session.add(nqt_vai_tro)
    db.session.commit()

    return nqt_ok(nqt_vai_tro.g6_to_dict(), 'Tạo vai trò thành công')

@nqt_phan_quyen_bp.route('/nqt-vai-tro/<int:nqt_ma_vai_tro>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_cap_nhat_vai_tro(nqt_ma_vai_tro):
    nqt_vai_tro = G6VaiTro.query.get(nqt_ma_vai_tro)
    if not nqt_vai_tro:
        return nqt_loi('Không tìm thấy vai trò', 404)

    # Không cho phép sửa vai trò G6QuanTri
    if nqt_vai_tro.g6_ten_vai_tro == 'G6QuanTri':
        return nqt_loi('Không thể chỉnh sửa vai trò Quản Trị hệ thống')

    nqt_data = request.get_json() or {}
    nqt_ten_vai_tro = nqt_data.get('g6_ten_vai_tro')
    nqt_mo_ta = nqt_data.get('g6_mo_ta')

    if nqt_ten_vai_tro:
        # Kiểm tra trùng tên với vai trò khác
        nqt_ton_tai = G6VaiTro.query.filter(
            G6VaiTro.g6_ten_vai_tro == nqt_ten_vai_tro,
            G6VaiTro.g6_ma_vai_tro != nqt_ma_vai_tro
        ).first()
        if nqt_ton_tai:
            return nqt_loi('Tên vai trò đã tồn tại')
        nqt_vai_tro.g6_ten_vai_tro = nqt_ten_vai_tro

    if nqt_mo_ta is not None:
        nqt_vai_tro.g6_mo_ta = nqt_mo_ta

    db.session.commit()
    return nqt_ok(nqt_vai_tro.g6_to_dict(), 'Cập nhật vai trò thành công')

@nqt_phan_quyen_bp.route('/nqt-vai-tro/<int:nqt_ma_vai_tro>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_xoa_vai_tro(nqt_ma_vai_tro):
    nqt_vai_tro = G6VaiTro.query.get(nqt_ma_vai_tro)
    if not nqt_vai_tro:
        return nqt_loi('Không tìm thấy vai trò', 404)

    if nqt_vai_tro.g6_ten_vai_tro == 'G6QuanTri':
        return nqt_loi('Không thể xoá vai trò Quản Trị hệ thống')

    db.session.delete(nqt_vai_tro)
    db.session.commit()
    return nqt_ok(None, 'Xoá vai trò thành công')


# ==========================================
# 3. GÁN QUYỀN CHO VAI TRÒ
# ==========================================

@nqt_phan_quyen_bp.route('/nqt-vai-tro/<int:nqt_ma_vai_tro>/nqt-quyen', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_lay_quyen_cua_vai_tro(nqt_ma_vai_tro):
    nqt_vai_tro = G6VaiTro.query.get(nqt_ma_vai_tro)
    if not nqt_vai_tro:
        return nqt_loi('Không tìm thấy vai trò', 404)
        
    nqt_danh_sach_quyen_id = [vtq.g6_ma_quyen for vtq in nqt_vai_tro.g6_quyen]
    
    # Lấy thông tin chi tiết các quyền
    nqt_quyen = G6QuyenHan.query.filter(G6QuyenHan.g6_ma_quyen.in_(nqt_danh_sach_quyen_id)).all() if nqt_danh_sach_quyen_id else []

    return nqt_ok({
        'g6_vai_tro': nqt_vai_tro.g6_to_dict(),
        'g6_danh_sach_quyen_id': nqt_danh_sach_quyen_id,
        'g6_chi_tiet_quyen': [q.g6_to_dict() for q in nqt_quyen]
    }, 'Lấy danh sách quyền của vai trò thành công')

@nqt_phan_quyen_bp.route('/nqt-vai-tro/<int:nqt_ma_vai_tro>/nqt-phan-quyen', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_phan_quyen_cho_vai_tro(nqt_ma_vai_tro):
    nqt_vai_tro = G6VaiTro.query.get(nqt_ma_vai_tro)
    if not nqt_vai_tro:
        return nqt_loi('Không tìm thấy vai trò', 404)
        
    if nqt_vai_tro.g6_ten_vai_tro == 'G6QuanTri':
        return nqt_loi('Vai trò G6QuanTri mặc định có toàn quyền, không cần thiết lập')

    nqt_data = request.get_json() or {}
    nqt_danh_sach_quyen = nqt_data.get('danh_sach_quyen', [])
    
    if not isinstance(nqt_danh_sach_quyen, list):
        return nqt_loi('danh_sach_quyen phải là một mảng (list)')

    # Xoá các quyền hiện có
    G6VaiTroQuyen.query.filter_by(g6_ma_vai_tro=nqt_ma_vai_tro).delete()
    
    # Thêm các quyền mới
    for ma_quyen in nqt_danh_sach_quyen:
        vtq = G6VaiTroQuyen(g6_ma_vai_tro=nqt_ma_vai_tro, g6_ma_quyen=ma_quyen)
        db.session.add(vtq)

    db.session.commit()
    return nqt_ok(None, 'Phân quyền cho vai trò thành công')


# ==========================================
# 4. GÁN VAI TRÒ CHO NGƯỜI DÙNG
# ==========================================

@nqt_phan_quyen_bp.route('/nqt-nguoi-dung/<int:nqt_ma_nguoi_dung>/nqt-gan-vai-tro', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_quan_tri_he_thong')
def nqt_gan_vai_tro_cho_nguoi_dung(nqt_ma_nguoi_dung):
    nqt_nguoi_dung = G6NguoiDung.query.get(nqt_ma_nguoi_dung)
    if not nqt_nguoi_dung:
        return nqt_loi('Không tìm thấy người dùng', 404)

    nqt_data = request.get_json() or {}
    nqt_danh_sach_vai_tro = nqt_data.get('danh_sach_vai_tro', [])
    
    if not isinstance(nqt_danh_sach_vai_tro, list):
        return nqt_loi('danh_sach_vai_tro phải là một mảng (list)')

    # Xoá các vai trò hiện tại của user
    G6NguoiDungVaiTro.query.filter_by(g6_ma_nguoi_dung=nqt_ma_nguoi_dung).delete()
    
    # Thêm các vai trò mới
    for ma_vai_tro in nqt_danh_sach_vai_tro:
        ndvt = G6NguoiDungVaiTro(g6_ma_nguoi_dung=nqt_ma_nguoi_dung, g6_ma_vai_tro=ma_vai_tro)
        db.session.add(ndvt)

    db.session.commit()
    return nqt_ok(None, 'Gán vai trò cho người dùng thành công')
