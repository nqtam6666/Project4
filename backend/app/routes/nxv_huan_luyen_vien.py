from datetime import date, timedelta
from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_huan_luyen_vien import (
    G6HuanLuyenVien, G6GoiPT, G6DangKyGoiPT, G6BuoiTapPT
)
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen

nxv_huan_luyen_vien_bp = Blueprint('nxv_huan_luyen_vien', __name__, url_prefix='/api')


# ============================================================
# HUẤN LUYỆN VIÊN (PT)
# ============================================================

@nxv_huan_luyen_vien_bp.route('/nxv-hlv', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_xem_nhan_vien')
def nxv_lay_tat_ca_hlv():
    nxv_chi_nhanh = request.args.get('g6_ma_chi_nhanh', type=int)
    nxv_hien_thi_web = request.args.get('g6_la_hien_thi_web', type=int)

    nxv_q = G6HuanLuyenVien.query
    if nxv_chi_nhanh:
        nxv_q = nxv_q.filter_by(g6_ma_chi_nhanh=nxv_chi_nhanh)
    if nxv_hien_thi_web is not None:
        nxv_q = nxv_q.filter_by(g6_la_hien_thi_web=bool(nxv_hien_thi_web))

    nxv_list = nxv_q.all()
    return nqt_ok([h.g6_to_dict() for h in nxv_list])


@nxv_huan_luyen_vien_bp.route('/nxv-hlv/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_xem_nhan_vien')
def nxv_lay_hlv(nxv_id):
    nxv_row = G6HuanLuyenVien.query.get_or_404(nxv_id)
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_huan_luyen_vien_bp.route('/nxv-hlv', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_tao_nhan_vien')
def nxv_tao_hlv():
    nxv_data = request.get_json() or {}
    nxv_ma_nv = nxv_data.get('g6_ma_nhan_vien')
    nxv_ma_cn = nxv_data.get('g6_ma_chi_nhanh')
    
    if not nxv_ma_cn:
        nxv_ma_cn = 1 # Default branch if missing
        
    if not nxv_ma_nv:
        nxv_ht = nxv_data.get('g6_ho_ten')
        if not nxv_ht:
            return nqt_loi('Thiếu họ tên nhân viên')
        from backend.app.models.g6_nhan_vien import G6NhanVien
        nxv_nv = G6NhanVien(
            g6_ho_ten=nxv_ht,
            g6_so_dien_thoai=nxv_data.get('g6_so_dien_thoai'),
            g6_ma_chi_nhanh=nxv_ma_cn,
            g6_trang_thai='dang_lam',
            g6_ngay_vao_lam=date.today()
        )
        db.session.add(nxv_nv)
        db.session.flush()
        nxv_ma_nv = nxv_nv.g6_ma_nhan_vien

    nxv_row = G6HuanLuyenVien(
        g6_ma_nhan_vien=nxv_ma_nv,
        g6_ma_chi_nhanh=nxv_ma_cn,
        g6_chuyen_mon=nxv_data.get('g6_chuyen_mon'),
        g6_cap_chung_chi=nxv_data.get('g6_cap_chung_chi'),
        g6_so_nam_kinh_nghiem=nxv_data.get('g6_so_nam_kinh_nghiem', 0),
        g6_tieu_su=nxv_data.get('g6_tieu_su'),
        g6_gia_theo_buoi=nxv_data.get('g6_gia_theo_buoi'),
        g6_hinh_anh=nxv_data.get('g6_hinh_anh'),
        g6_thu_hang=nxv_data.get('g6_thu_hang', 5),
        g6_toi_da_hoi_vien=nxv_data.get('g6_toi_da_hoi_vien', 20),
        g6_la_hien_thi_web=nxv_data.get('g6_la_hien_thi_web', True),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo huấn luyện viên thành công', 201)


@nxv_huan_luyen_vien_bp.route('/nxv-hlv/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_sua_nhan_vien')
def nxv_cap_nhat_hlv(nxv_id):
    nxv_row = G6HuanLuyenVien.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    
    if nxv_row.g6_nhan_vien:
        if 'g6_ho_ten' in nxv_data:
            nxv_row.g6_nhan_vien.g6_ho_ten = nxv_data['g6_ho_ten']
        if 'g6_so_dien_thoai' in nxv_data:
            nxv_row.g6_nhan_vien.g6_so_dien_thoai = nxv_data['g6_so_dien_thoai']
        if 'g6_ma_chi_nhanh' in nxv_data:
            nxv_row.g6_nhan_vien.g6_ma_chi_nhanh = nxv_data['g6_ma_chi_nhanh']

    for nxv_f in ['g6_chuyen_mon', 'g6_cap_chung_chi', 'g6_so_nam_kinh_nghiem',
                  'g6_tieu_su', 'g6_gia_theo_buoi', 'g6_hinh_anh', 'g6_ma_chi_nhanh',
                  'g6_thu_hang', 'g6_toi_da_hoi_vien', 'g6_la_hien_thi_web']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_huan_luyen_vien_bp.route('/nxv-hlv/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_xoa_nhan_vien')
def nxv_xoa_hlv(nxv_id):
    nxv_row = G6HuanLuyenVien.query.get_or_404(nxv_id)
    nxv_row.g6_la_hien_thi_web = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn huấn luyện viên')


# ============================================================
# GÓI PT
# ============================================================

@nxv_huan_luyen_vien_bp.route('/nxv-goi-pt', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_goi_pt():
    nxv_hlv_id = request.args.get('g6_ma_hlv', type=int)
    nxv_q = G6GoiPT.query.filter_by(g6_la_hoat_dong=True)
    if nxv_hlv_id:
        nxv_q = nxv_q.filter_by(g6_ma_hlv=nxv_hlv_id)
    return nqt_ok([g.g6_to_dict() for g in nxv_q.all()])


@nxv_huan_luyen_vien_bp.route('/nxv-goi-pt/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_chi_tiet_goi_pt(nxv_id):
    nxv_row = G6GoiPT.query.get_or_404(nxv_id)
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_huan_luyen_vien_bp.route('/nxv-goi-pt', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('QL_HOI_VIEN')
def nxv_tao_goi_pt():
    nxv_data = request.get_json() or {}
    nxv_hlv_id = nxv_data.get('g6_ma_hlv')
    if not nxv_hlv_id:
        return nqt_loi('Thiếu mã huấn luyện viên')
    G6HuanLuyenVien.query.get_or_404(nxv_hlv_id)

    nxv_row = G6GoiPT(
        g6_ma_hlv=nxv_hlv_id,
        g6_ten_goi=nxv_data.get('g6_ten_goi', ''),
        g6_so_buoi=nxv_data.get('g6_so_buoi', 10),
        g6_thoi_luong_buoi=nxv_data.get('g6_thoi_luong_buoi', 60),
        g6_gia=nxv_data.get('g6_gia', 0),
        g6_gia_khuyen_mai=nxv_data.get('g6_gia_khuyen_mai'),
        g6_hieu_luc_ngay=nxv_data.get('g6_hieu_luc_ngay', 90),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo gói PT thành công', 201)


@nxv_huan_luyen_vien_bp.route('/nxv-goi-pt/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_goi_pt(nxv_id):
    nxv_row = G6GoiPT.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['g6_ten_goi', 'g6_so_buoi', 'g6_thoi_luong_buoi',
                  'g6_gia', 'g6_gia_khuyen_mai', 'g6_hieu_luc_ngay', 'g6_la_hoat_dong']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_huan_luyen_vien_bp.route('/nxv-goi-pt/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_goi_pt(nxv_id):
    nxv_row = G6GoiPT.query.get_or_404(nxv_id)
    nxv_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn gói PT')


# ============================================================
# ĐĂNG KÝ GÓI PT
# ============================================================

@nxv_huan_luyen_vien_bp.route('/nxv-dang-ky-pt', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_dang_ky_pt():
    nxv_hv_id = request.args.get('g6_ma_hoi_vien', type=int)
    nxv_hlv_id = request.args.get('g6_ma_hlv', type=int)
    nxv_trang_thai = request.args.get('g6_trang_thai', '').strip()
    nxv_trang = request.args.get('g6_trang', 1, type=int)
    nxv_gioi_han = request.args.get('g6_gioi_han', 20, type=int)

    nxv_q = G6DangKyGoiPT.query
    if nxv_hv_id:
        nxv_q = nxv_q.filter_by(g6_ma_hoi_vien=nxv_hv_id)
    if nxv_hlv_id:
        nxv_q = nxv_q.filter_by(g6_ma_hlv=nxv_hlv_id)
    if nxv_trang_thai:
        nxv_q = nxv_q.filter_by(g6_trang_thai=nxv_trang_thai)

    nxv_pt = nxv_q.order_by(G6DangKyGoiPT.g6_ngay_tao.desc()).paginate(
        page=nxv_trang, per_page=nxv_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [d.g6_to_dict() for d in nxv_pt.items],
        'g6_tong': nxv_pt.total,
        'g6_trang': nxv_trang,
        'g6_tong_trang': nxv_pt.pages,
    })


@nxv_huan_luyen_vien_bp.route('/nxv-dang-ky-pt/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_chi_tiet_dang_ky_pt(nxv_id):
    nxv_row = G6DangKyGoiPT.query.get_or_404(nxv_id)
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_huan_luyen_vien_bp.route('/nxv-dang-ky-pt', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('QL_HOI_VIEN')
def nxv_tao_dang_ky_pt():
    nxv_data = request.get_json() or {}
    nxv_hv_id = nxv_data.get('g6_ma_hoi_vien')
    nxv_goi_id = nxv_data.get('g6_ma_goi_pt')
    if not nxv_hv_id or not nxv_goi_id:
        return nqt_loi('Thiếu mã hội viên hoặc gói PT')

    nxv_goi = G6GoiPT.query.get_or_404(nxv_goi_id)
    if not nxv_goi.g6_la_hoat_dong:
        return nqt_loi('Gói PT không còn hoạt động')

    # Kiểm tra HLV còn slot
    nxv_hlv = G6HuanLuyenVien.query.get_or_404(nxv_goi.g6_ma_hlv)
    if nxv_hlv.g6_so_hoi_vien_hien_tai >= nxv_hlv.g6_toi_da_hoi_vien:
        return nqt_loi('Huấn luyện viên đã đạt tối đa hội viên')

    nxv_ngay_mua = date.today()
    nxv_ngay_hh = nxv_ngay_mua + timedelta(days=nxv_goi.g6_hieu_luc_ngay)
    nxv_gia = float(nxv_goi.g6_gia_khuyen_mai or nxv_goi.g6_gia)

    nxv_row = G6DangKyGoiPT(
        g6_ma_hoi_vien=nxv_hv_id,
        g6_ma_goi_pt=nxv_goi_id,
        g6_ma_hlv=nxv_goi.g6_ma_hlv,
        g6_ngay_mua=nxv_ngay_mua,
        g6_ngay_het_han=nxv_ngay_hh,
        g6_so_buoi_con_lai=nxv_goi.g6_so_buoi,
        g6_gia_thuc_te=nxv_gia,
        g6_ma_thanh_toan=nxv_data.get('g6_ma_thanh_toan'),
    )
    db.session.add(nxv_row)
    # Tăng counter HLV
    nxv_hlv.g6_so_hoi_vien_hien_tai += 1
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Đăng ký gói PT thành công', 201)


@nxv_huan_luyen_vien_bp.route('/nxv-dang-ky-pt/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_dang_ky_pt(nxv_id):
    nxv_row = G6DangKyGoiPT.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    nxv_trang_thai_cu = nxv_row.g6_trang_thai
    for nxv_f in ['g6_trang_thai', 'g6_so_buoi_con_lai']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    # Khi hủy → giảm counter HLV
    if nxv_trang_thai_cu == 'dang_dung' and nxv_row.g6_trang_thai == 'huy':
        nxv_hlv = G6HuanLuyenVien.query.get(nxv_row.g6_ma_hlv)
        if nxv_hlv and nxv_hlv.g6_so_hoi_vien_hien_tai > 0:
            nxv_hlv.g6_so_hoi_vien_hien_tai -= 1
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_huan_luyen_vien_bp.route('/nxv-dang-ky-pt/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_huy_dang_ky_pt(nxv_id):
    nxv_row = G6DangKyGoiPT.query.get_or_404(nxv_id)
    if nxv_row.g6_trang_thai == 'huy':
        return nqt_loi('Đăng ký đã bị hủy trước đó')
    nxv_row.g6_trang_thai = 'huy'
    nxv_hlv = G6HuanLuyenVien.query.get(nxv_row.g6_ma_hlv)
    if nxv_hlv and nxv_hlv.g6_so_hoi_vien_hien_tai > 0:
        nxv_hlv.g6_so_hoi_vien_hien_tai -= 1
    db.session.commit()
    return nqt_ok(None, 'Đã hủy đăng ký gói PT')


# ============================================================
# BUỔI TẬP PT
# ============================================================

@nxv_huan_luyen_vien_bp.route('/nxv-buoi-tap-pt', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_buoi_tap():
    nxv_dk_id = request.args.get('g6_ma_dang_ky_pt', type=int)
    nxv_hv_id = request.args.get('g6_ma_hoi_vien', type=int)
    nxv_hlv_id = request.args.get('g6_ma_hlv', type=int)
    nxv_trang = request.args.get('g6_trang', 1, type=int)
    nxv_gioi_han = request.args.get('g6_gioi_han', 20, type=int)

    nxv_q = G6BuoiTapPT.query
    if nxv_dk_id:
        nxv_q = nxv_q.filter_by(g6_ma_dang_ky_pt=nxv_dk_id)
    if nxv_hv_id:
        nxv_q = nxv_q.filter_by(g6_ma_hoi_vien=nxv_hv_id)
    if nxv_hlv_id:
        nxv_q = nxv_q.filter_by(g6_ma_hlv=nxv_hlv_id)

    nxv_pt = nxv_q.order_by(G6BuoiTapPT.g6_ngay_tap.desc()).paginate(
        page=nxv_trang, per_page=nxv_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [b.g6_to_dict() for b in nxv_pt.items],
        'g6_tong': nxv_pt.total,
        'g6_trang': nxv_trang,
        'g6_tong_trang': nxv_pt.pages,
    })


@nxv_huan_luyen_vien_bp.route('/nxv-buoi-tap-pt', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_buoi_tap():
    nxv_data = request.get_json() or {}
    nxv_dk_id = nxv_data.get('g6_ma_dang_ky_pt')
    nxv_ngay_tap = nxv_data.get('g6_ngay_tap')
    if not nxv_dk_id or not nxv_ngay_tap:
        return nqt_loi('Thiếu mã đăng ký PT hoặc ngày tập')

    nxv_dk = G6DangKyGoiPT.query.get_or_404(nxv_dk_id)

    # Kiểm tra còn buổi và còn hiệu lực
    if nxv_dk.g6_so_buoi_con_lai <= 0:
        return nqt_loi('Gói PT đã hết buổi tập')
    if nxv_dk.g6_ngay_het_han < date.today():
        return nqt_loi('Gói PT đã hết hạn')
    if nxv_dk.g6_trang_thai != 'dang_dung':
        return nqt_loi('Gói PT không còn hoạt động')

    nxv_row = G6BuoiTapPT(
        g6_ma_dang_ky_pt=nxv_dk_id,
        g6_ma_hoi_vien=nxv_dk.g6_ma_hoi_vien,
        g6_ma_hlv=nxv_dk.g6_ma_hlv,
        g6_ma_chi_nhanh=nxv_data.get('g6_ma_chi_nhanh'),
        g6_ngay_tap=nxv_ngay_tap,
        g6_thoi_luong=nxv_data.get('g6_thoi_luong'),
        g6_trang_thai=nxv_data.get('g6_trang_thai', 'cho_xac_nhan'),
        g6_noi_dung_buoi_tap=nxv_data.get('g6_noi_dung_buoi_tap'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo buổi tập PT thành công', 201)


@nxv_huan_luyen_vien_bp.route('/nxv-buoi-tap-pt/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_buoi_tap(nxv_id):
    nxv_row = G6BuoiTapPT.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}

    nxv_trang_thai_cu = nxv_row.g6_trang_thai
    for nxv_f in ['g6_trang_thai', 'g6_thoi_luong', 'g6_noi_dung_buoi_tap',
                  'g6_nhan_xet_hlv', 'g6_danh_gia_hoi_vien']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])

    # Khi xác nhận buổi đã tập → trừ buổi còn lại
    if nxv_trang_thai_cu != 'da_tap' and nxv_row.g6_trang_thai == 'da_tap':
        nxv_dk = G6DangKyGoiPT.query.get(nxv_row.g6_ma_dang_ky_pt)
        if nxv_dk and nxv_dk.g6_so_buoi_con_lai > 0:
            nxv_dk.g6_so_buoi_con_lai -= 1
            if nxv_dk.g6_so_buoi_con_lai == 0:
                nxv_dk.g6_trang_thai = 'het_buoi'

    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_huan_luyen_vien_bp.route('/nxv-buoi-tap-pt/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_buoi_tap_theo_id(nxv_id):
    nxv_row = G6BuoiTapPT.query.get_or_404(nxv_id)
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_huan_luyen_vien_bp.route('/nxv-buoi-tap-pt/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_huy_buoi_tap(nxv_id):
    nxv_row = G6BuoiTapPT.query.get_or_404(nxv_id)
    if nxv_row.g6_trang_thai == 'da_tap':
        return nqt_loi('Không thể huỷ buổi đã tập', nqt_ma_trang=400)
    nxv_row.g6_trang_thai = 'da_huy'
    db.session.commit()
    return nqt_ok(None, 'Đã huỷ buổi tập PT')


from flask_jwt_extended import get_jwt_identity
from backend.app.models.g6_nhan_vien import G6NhanVien

@nxv_huan_luyen_vien_bp.route('/nxv-hlv/me', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_hlv_me():
    # Lấy thông tin user hiện tại
    user_id = int(get_jwt_identity())
    
    # Tìm NhanVien map với user
    nv = G6NhanVien.query.filter_by(g6_ma_nguoi_dung=user_id).first()
    if not nv:
        return nqt_loi('Bạn không phải là nhân viên', 403)
        
    # Tìm HuanLuyenVien map với NhanVien
    hlv = G6HuanLuyenVien.query.filter_by(g6_ma_nhan_vien=nv.g6_ma_nhan_vien).first()
    if not hlv:
        return nqt_loi('Bạn không phải là huấn luyện viên', 403)
        
    return nqt_ok(hlv.g6_to_dict())

@nxv_huan_luyen_vien_bp.route('/nxv-hlv/me/avatar', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_hlv_me_avatar():
    user_id = int(get_jwt_identity())
    
    nv = G6NhanVien.query.filter_by(g6_ma_nguoi_dung=user_id).first()
    if not nv:
        return nqt_loi('Bạn không phải là nhân viên', 403)
        
    hlv = G6HuanLuyenVien.query.filter_by(g6_ma_nhan_vien=nv.g6_ma_nhan_vien).first()
    if not hlv:
        return nqt_loi('Bạn không phải là huấn luyện viên', 403)
        
    data = request.get_json() or {}
    hinh_anh = data.get('g6_hinh_anh')
    if not hinh_anh:
        return nqt_loi('Vui lòng cung cấp link hình ảnh')
        
    hlv.g6_hinh_anh = hinh_anh
    # Đồng bộ avatar với G6NhanVien và G6NguoiDung nếu cần
    nv.g6_hinh_anh = hinh_anh
    if nv.g6_nguoi_dung:
        nv.g6_nguoi_dung.g6_anh_dai_dien = hinh_anh
        
    db.session.commit()
    return nqt_ok(hlv.g6_to_dict(), 'Cập nhật ảnh đại diện thành công')
