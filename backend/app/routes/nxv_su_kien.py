from flask import Blueprint, request
from backend.app import db
from backend.app.models.nxv_su_kien import NxvSuKien, NxvDangKySuKien
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap
from datetime import datetime
import uuid

nxv_su_kien_bp = Blueprint('nxv_su_kien', __name__, url_prefix='/api')


# ---- SỰ KIỆN ----

@nxv_su_kien_bp.route('/nxv-su-kien', methods=['GET'])
def nxv_lay_su_kien():
    nxv_loai = request.args.get('nxv_loai')
    nxv_cn_id = request.args.get('nxv_ma_chi_nhanh', type=int)
    nxv_chi_hoat_dong = request.args.get('g6_hoat_dong', '1') == '1'
    nxv_trang = request.args.get('g6_trang', 1, type=int)

    nxv_q = NxvSuKien.query.filter(NxvSuKien.g6_deleted_at == None)
    if nxv_chi_hoat_dong:
        nxv_q = nxv_q.filter_by(nxv_la_hoat_dong=True)
    if nxv_loai:
        nxv_q = nxv_q.filter_by(nxv_loai=nxv_loai)
    if nxv_cn_id:
        nxv_q = nxv_q.filter_by(nxv_ma_chi_nhanh=nxv_cn_id)

    nxv_phan_trang = nxv_q.order_by(NxvSuKien.nxv_ngay_bat_dau.asc()).paginate(
        page=nxv_trang, per_page=20, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [s.nxv_to_dict() for s in nxv_phan_trang.items],
        'g6_tong': nxv_phan_trang.total,
        'g6_trang': nxv_trang,
    })


@nxv_su_kien_bp.route('/nxv-su-kien/<int:nxv_id>', methods=['GET'])
def nxv_lay_su_kien_chi_tiet(nxv_id):
    nxv_row = NxvSuKien.query.get_or_404(nxv_id)
    nxv_result = nxv_row.nxv_to_dict()
    nxv_result['nxv_so_dang_ky'] = NxvDangKySuKien.query.filter_by(
        nxv_ma_su_kien=nxv_id
    ).filter(NxvDangKySuKien.g6_deleted_at == None).count()
    return nqt_ok(nxv_result)


@nxv_su_kien_bp.route('/nxv-su-kien', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_su_kien():
    nxv_data = request.get_json() or {}
    nxv_ten = nxv_data.get('nxv_ten', '').strip()
    nxv_ngay_bd = nxv_data.get('nxv_ngay_bat_dau')
    nxv_ngay_kt = nxv_data.get('nxv_ngay_ket_thuc')
    
    try:
        if nxv_ngay_bd and isinstance(nxv_ngay_bd, str):
            nxv_ngay_bd = datetime.fromisoformat(nxv_ngay_bd.replace('Z', ''))
        if nxv_ngay_kt and isinstance(nxv_ngay_kt, str):
            nxv_ngay_kt = datetime.fromisoformat(nxv_ngay_kt.replace('Z', ''))
    except ValueError:
        return nqt_loi('Định dạng thời gian không hợp lệ')

    if not nxv_ten or not nxv_ngay_bd or not nxv_ngay_kt:
        return nqt_loi('Thiếu tên, ngày bắt đầu hoặc ngày kết thúc')
        
    nxv_row = NxvSuKien(
        nxv_ma_chi_nhanh=nxv_data.get('nxv_ma_chi_nhanh'),
        nxv_ten=nxv_ten,
        nxv_mo_ta=nxv_data.get('nxv_mo_ta'),
        nxv_loai=nxv_data.get('nxv_loai', 'su_kien'),
        nxv_hinh_anh=nxv_data.get('nxv_hinh_anh'),
        nxv_ngay_bat_dau=nxv_ngay_bd,
        nxv_ngay_ket_thuc=nxv_ngay_kt,
        nxv_dia_diem=nxv_data.get('nxv_dia_diem'),
        nxv_suc_chua=nxv_data.get('nxv_suc_chua'),
        nxv_gia_ve=nxv_data.get('nxv_gia_ve', 0),
        nxv_gia_giam=nxv_data.get('nxv_gia_giam'),
        nxv_ma_goi_ap_dung=nxv_data.get('nxv_ma_goi_ap_dung'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Tạo sự kiện thành công', 201)


@nxv_su_kien_bp.route('/nxv-su-kien/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_su_kien(nxv_id):
    nxv_row = NxvSuKien.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    
    try:
        for f in ['nxv_ngay_bat_dau', 'nxv_ngay_ket_thuc']:
            if nxv_data.get(f) and isinstance(nxv_data[f], str):
                nxv_data[f] = datetime.fromisoformat(nxv_data[f].replace('Z', ''))
    except ValueError:
        return nqt_loi('Định dạng thời gian không hợp lệ')
        
    for nxv_f in [
        'nxv_ten', 'nxv_mo_ta', 'nxv_hinh_anh', 'nxv_ngay_bat_dau', 'nxv_ngay_ket_thuc',
        'nxv_dia_diem', 'nxv_suc_chua', 'nxv_gia_ve', 'nxv_gia_giam', 'nxv_la_hoat_dong',
    ]:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Cập nhật sự kiện thành công')


@nxv_su_kien_bp.route('/nxv-su-kien/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_su_kien(nxv_id):
    nxv_row = NxvSuKien.query.get_or_404(nxv_id)
    nxv_row.g6_deleted_at = datetime.utcnow()
    nxv_row.nxv_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã xoá sự kiện')


# ---- ĐĂNG KÝ SỰ KIỆN ----

@nxv_su_kien_bp.route('/nxv-su-kien/<int:nxv_sk_id>/nxv-dang-ky', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_dang_ky_su_kien(nxv_sk_id):
    NxvSuKien.query.get_or_404(nxv_sk_id)
    nxv_trang_thai = request.args.get('nxv_trang_thai')
    nxv_q = NxvDangKySuKien.query.filter_by(nxv_ma_su_kien=nxv_sk_id).filter(
        NxvDangKySuKien.g6_deleted_at == None
    )
    if nxv_trang_thai:
        nxv_q = nxv_q.filter_by(nxv_trang_thai=nxv_trang_thai)
    nxv_list = nxv_q.order_by(NxvDangKySuKien.nxv_ngay_tao.desc()).all()
    return nqt_ok([d.nxv_to_dict() for d in nxv_list])


@nxv_su_kien_bp.route('/nxv-dang-ky-su-kien', methods=['POST'])
def nxv_dang_ky_su_kien():
    nxv_data = request.get_json() or {}
    nxv_sk_id = nxv_data.get('nxv_ma_su_kien')
    nxv_ho_ten = nxv_data.get('nxv_ho_ten', '').strip()
    if not nxv_sk_id or not nxv_ho_ten:
        return nqt_loi('Thiếu mã sự kiện hoặc họ tên')

    nxv_sk = NxvSuKien.query.get_or_404(nxv_sk_id)
    if not nxv_sk.nxv_la_hoat_dong:
        return nqt_loi('Sự kiện không còn hoạt động')

    nxv_so_ve = nxv_data.get('nxv_so_ve', 1)
    if nxv_sk.nxv_suc_chua:
        nxv_so_dky = NxvDangKySuKien.query.filter_by(nxv_ma_su_kien=nxv_sk_id).filter(
            NxvDangKySuKien.g6_deleted_at == None,
            NxvDangKySuKien.nxv_trang_thai != 'da_huy',
        ).count()
        if nxv_so_dky >= nxv_sk.nxv_suc_chua:
            return nqt_loi('Sự kiện đã hết chỗ')

    nxv_gia = float(nxv_sk.nxv_gia_giam or nxv_sk.nxv_gia_ve)
    nxv_row = NxvDangKySuKien(
        nxv_ma_su_kien=nxv_sk_id,
        nxv_ma_hoi_vien=nxv_data.get('nxv_ma_hoi_vien'),
        nxv_ma_khach_hang=nxv_data.get('nxv_ma_khach_hang'),
        nxv_ho_ten=nxv_ho_ten,
        nxv_so_dien_thoai=nxv_data.get('nxv_so_dien_thoai'),
        nxv_email=nxv_data.get('nxv_email'),
        nxv_so_ve=nxv_so_ve,
        nxv_tong_tien=nxv_gia * nxv_so_ve,
        nxv_ma_qr=str(uuid.uuid4())[:12].upper(),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict(), 'Đăng ký sự kiện thành công', 201)


@nxv_su_kien_bp.route('/nxv-dang-ky-su-kien/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_dang_ky(nxv_id):
    nxv_row = NxvDangKySuKien.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['nxv_trang_thai', 'nxv_so_ve', 'nxv_tong_tien']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.nxv_to_dict())


@nxv_su_kien_bp.route('/nxv-dang-ky-su-kien/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_huy_dang_ky(nxv_id):
    nxv_row = NxvDangKySuKien.query.get_or_404(nxv_id)
    nxv_row.nxv_trang_thai = 'da_huy'
    nxv_row.g6_deleted_at = datetime.utcnow()
    db.session.commit()
    return nqt_ok(None, 'Đã huỷ đăng ký sự kiện')
