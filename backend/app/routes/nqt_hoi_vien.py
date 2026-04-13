import uuid
from datetime import date, timedelta
from flask import Blueprint, request
from sqlalchemy import func
from backend.app import db
from backend.app.models.nqt_hoi_vien import NqtHoiVien, NqtGoiTap, NqtDangKyGoiTap, NqtDiemDanh, NqtChiSoCoThe
from backend.app.models.nqt_thanh_toan import NqtThanhToan
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen

nqt_hoi_vien_bp = Blueprint('nqt_hoi_vien', __name__, url_prefix='/api')


# ---- HỘI VIÊN ----

@nqt_hoi_vien_bp.route('/nqt-hoi-vien', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_xem_hoi_vien')
def nqt_lay_tat_ca_hoi_vien():
    nqt_trang = request.args.get('nqt_trang', 1, type=int)
    nqt_gioi_han = request.args.get('nqt_gioi_han', 20, type=int)
    nqt_tim = request.args.get('nqt_tim_kiem', '').strip()
    nqt_chi_nhanh = request.args.get('nqt_ma_chi_nhanh', type=int)

    nqt_q = NqtHoiVien.query
    if nqt_chi_nhanh:
        nqt_q = nqt_q.filter_by(nqt_ma_chi_nhanh=nqt_chi_nhanh)
    if nqt_tim:
        nqt_q = nqt_q.filter(
            NqtHoiVien.nqt_ho_ten.ilike(f'%{nqt_tim}%') |
            NqtHoiVien.nqt_so_dien_thoai.ilike(f'%{nqt_tim}%')
        )
    nqt_phan_trang = nqt_q.order_by(NqtHoiVien.nqt_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'nqt_danh_sach': [h.nqt_to_dict() for h in nqt_phan_trang.items],
        'nqt_tong': nqt_phan_trang.total,
        'nqt_trang': nqt_trang,
        'nqt_tong_trang': nqt_phan_trang.pages,
    })


@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_xem_hoi_vien')
def nqt_lay_hoi_vien(nqt_id):
    nqt_row = NqtHoiVien.query.get_or_404(nqt_id)
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_hoi_vien_bp.route('/nqt-hoi-vien', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_tao_hoi_vien')
def nqt_tao_hoi_vien():
    nqt_data = request.get_json() or {}
    nqt_ho_ten = nqt_data.get('nqt_ho_ten', '').strip()
    nqt_sdt = nqt_data.get('nqt_so_dien_thoai', '').strip()
    nqt_chi_nhanh = nqt_data.get('nqt_ma_chi_nhanh')

    if not nqt_ho_ten or not nqt_sdt or not nqt_chi_nhanh:
        return nqt_loi('Thiếu họ tên, số điện thoại hoặc chi nhánh')
    if NqtHoiVien.query.filter_by(nqt_so_dien_thoai=nqt_sdt).first():
        return nqt_loi('Số điện thoại đã được đăng ký')

    nqt_row = NqtHoiVien(
        nqt_ho_ten=nqt_ho_ten,
        nqt_so_dien_thoai=nqt_sdt,
        nqt_ma_chi_nhanh=nqt_chi_nhanh,
        nqt_ngay_dang_ky=date.today(),
        nqt_ma_qr=str(uuid.uuid4()),
        nqt_email=nqt_data.get('nqt_email'),
        nqt_ngay_sinh=nqt_data.get('nqt_ngay_sinh'),
        nqt_gioi_tinh=nqt_data.get('nqt_gioi_tinh'),
        nqt_dia_chi=nqt_data.get('nqt_dia_chi'),
        nqt_nguon_gioi_thieu=nqt_data.get('nqt_nguon_gioi_thieu'),
        nqt_ma_gioi_thieu=nqt_data.get('nqt_ma_gioi_thieu'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Tạo hội viên thành công', 201)


@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_sua_hoi_vien')
def nqt_cap_nhat_hoi_vien(nqt_id):
    nqt_row = NqtHoiVien.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['nqt_ho_ten', 'nqt_email', 'nqt_dia_chi', 'nqt_la_hoat_dong', 'nqt_ghi_chu']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_xoa_hoi_vien')
def nqt_xoa_hoi_vien(nqt_id):
    nqt_row = NqtHoiVien.query.get_or_404(nqt_id)
    db.session.delete(nqt_row)
    db.session.commit()
    return nqt_ok(None, 'Xóa hội viên thành công')


# ---- GÓI TẬP ----

@nqt_hoi_vien_bp.route('/nqt-goi-tap', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_goi_tap():
    nqt_list = NqtGoiTap.query.filter_by(nqt_la_hoat_dong=True).order_by(NqtGoiTap.nqt_thu_tu_hien_thi).all()
    return nqt_ok([g.nqt_to_dict() for g in nqt_list])


@nqt_hoi_vien_bp.route('/nqt-goi-tap', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_goi_tap():
    nqt_data = request.get_json() or {}
    nqt_row = NqtGoiTap(
        nqt_ten_goi=nqt_data.get('nqt_ten_goi', ''),
        nqt_mo_ta=nqt_data.get('nqt_mo_ta'),
        nqt_so_ngay=nqt_data.get('nqt_so_ngay', 30),
        nqt_gia=nqt_data.get('nqt_gia', 0),
        nqt_gia_khuyen_mai=nqt_data.get('nqt_gia_khuyen_mai'),
        nqt_co_pt=nqt_data.get('nqt_co_pt', False),
        nqt_so_buoi_pt=nqt_data.get('nqt_so_buoi_pt', 0),
        nqt_co_sauna=nqt_data.get('nqt_co_sauna', False),
        nqt_la_noi_bat=nqt_data.get('nqt_la_noi_bat', False),
        nqt_ma_chi_nhanh=nqt_data.get('nqt_ma_chi_nhanh'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Tạo gói tập thành công', 201)


@nqt_hoi_vien_bp.route('/nqt-goi-tap/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_goi_tap(nqt_id):
    nqt_row = NqtGoiTap.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['nqt_ten_goi', 'nqt_gia', 'nqt_gia_khuyen_mai', 'nqt_la_hoat_dong', 'nqt_la_noi_bat']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_hoi_vien_bp.route('/nqt-goi-tap/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_goi_tap(nqt_id):
    nqt_row = NqtGoiTap.query.get_or_404(nqt_id)
    nqt_row.nqt_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn gói tập thành công')


# ---- ĐĂNG KÝ GÓI TẬP ----

@nqt_hoi_vien_bp.route('/nqt-dang-ky-goi-tap', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_tao_hoi_vien')
def nqt_dang_ky_goi_tap():
    from datetime import timedelta
    nqt_data = request.get_json() or {}
    nqt_hv_id = nqt_data.get('nqt_ma_hoi_vien')
    nqt_gt_id = nqt_data.get('nqt_ma_goi_tap')
    if not nqt_hv_id or not nqt_gt_id:
        return nqt_loi('Thiếu mã hội viên hoặc gói tập')
    nqt_hv = NqtHoiVien.query.get_or_404(nqt_hv_id)
    nqt_gt = NqtGoiTap.query.get_or_404(nqt_gt_id)
    nqt_ngay_bd = date.today()
    nqt_ngay_hh = nqt_ngay_bd + date.resolution.__class__(days=nqt_gt.nqt_so_ngay)
    from datetime import timedelta
    nqt_ngay_hh = nqt_ngay_bd + timedelta(days=nqt_gt.nqt_so_ngay)
    nqt_gia = float(nqt_gt.nqt_gia_khuyen_mai or nqt_gt.nqt_gia)
    nqt_row = NqtDangKyGoiTap(
        nqt_ma_hoi_vien=nqt_hv_id,
        nqt_ma_goi_tap=nqt_gt_id,
        nqt_ma_chi_nhanh=nqt_hv.nqt_ma_chi_nhanh,
        nqt_ngay_bat_dau=nqt_ngay_bd,
        nqt_ngay_het_han=nqt_ngay_hh,
        nqt_gia_thuc_te=nqt_gia,
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Đăng ký gói tập thành công', 201)


@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>/nqt-dang-ky', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_dang_ky(nqt_id):
    NqtHoiVien.query.get_or_404(nqt_id)
    nqt_list = NqtDangKyGoiTap.query.filter_by(nqt_ma_hoi_vien=nqt_id).all()
    return nqt_ok([d.nqt_to_dict() for d in nqt_list])


# ---- CHECK-IN ----

@nqt_hoi_vien_bp.route('/nqt-diem-danh/qr', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('nqt_checkin_hoi_vien')
def nqt_checkin_qr():
    nqt_data = request.get_json() or {}
    nqt_qr = nqt_data.get('nqt_ma_qr', '').strip()
    nqt_chi_nhanh = nqt_data.get('nqt_ma_chi_nhanh')
    if not nqt_qr or not nqt_chi_nhanh:
        return nqt_loi('Thiếu mã QR hoặc chi nhánh')
    nqt_hv = NqtHoiVien.query.filter_by(nqt_ma_qr=nqt_qr, nqt_la_hoat_dong=True).first()
    if not nqt_hv:
        return nqt_loi('Mã QR không hợp lệ', nqt_ma_trang=404)
    nqt_dang_ky = NqtDangKyGoiTap.query.filter_by(
        nqt_ma_hoi_vien=nqt_hv.nqt_ma_hoi_vien,
        nqt_trang_thai='dang_hoat_dong'
    ).filter(NqtDangKyGoiTap.nqt_ngay_het_han >= date.today()).first()
    if not nqt_dang_ky:
        return nqt_loi('Hội viên không có gói tập đang hoạt động', nqt_ma_trang=403)
    nqt_dd = NqtDiemDanh(
        nqt_ma_dang_ky=nqt_dang_ky.nqt_ma_dang_ky,
        nqt_ma_hoi_vien=nqt_hv.nqt_ma_hoi_vien,
        nqt_ma_chi_nhanh=nqt_chi_nhanh,
        nqt_phuong_thuc='qr',
    )
    db.session.add(nqt_dd)
    db.session.commit()
    return nqt_ok({'nqt_diem_danh': nqt_dd.nqt_to_dict(), 'nqt_hoi_vien': nqt_hv.nqt_to_dict()},
                  f'Chào mừng {nqt_hv.nqt_ho_ten}!')


# ---- CHỈ SỐ CƠ THỂ ----

@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>/nqt-chi-so', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_chi_so(nqt_id):
    NqtHoiVien.query.get_or_404(nqt_id)
    nqt_list = NqtChiSoCoThe.query.filter_by(nqt_ma_hoi_vien=nqt_id).order_by(
        NqtChiSoCoThe.nqt_ngay_do.desc()
    ).all()
    return nqt_ok([c.nqt_to_dict() for c in nqt_list])


@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>/nqt-chi-so', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_them_chi_so(nqt_id):
    NqtHoiVien.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    nqt_can = nqt_data.get('nqt_can_nang')
    nqt_cao = nqt_data.get('nqt_chieu_cao')
    nqt_bmi = None
    if nqt_can and nqt_cao:
        nqt_bmi = round(float(nqt_can) / ((float(nqt_cao) / 100) ** 2), 2)
    nqt_row = NqtChiSoCoThe(
        nqt_ma_hoi_vien=nqt_id,
        nqt_ngay_do=nqt_data.get('nqt_ngay_do', str(date.today())),
        nqt_can_nang=nqt_can,
        nqt_chieu_cao=nqt_cao,
        nqt_chi_so_bmi=nqt_bmi,
        nqt_ti_le_mo=nqt_data.get('nqt_ti_le_mo'),
        nqt_ti_le_co=nqt_data.get('nqt_ti_le_co'),
        nqt_vong_eo=nqt_data.get('nqt_vong_eo'),
        nqt_ghi_chu=nqt_data.get('nqt_ghi_chu'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Đã lưu chỉ số', 201)


# ---- THỐNG KÊ DASHBOARD ----

@nqt_hoi_vien_bp.route('/nqt-thong-ke-dashboard', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_thong_ke_dashboard():
    nqt_hom_nay = date.today()
    nqt_dau_thang = nqt_hom_nay.replace(day=1)
    nqt_7_ngay_toi = nqt_hom_nay + timedelta(days=7)

    # Tổng hội viên
    nqt_tong_hv = NqtHoiVien.query.filter_by(nqt_la_hoat_dong=True).count()

    # Đang tập luyện (check-in vào hôm nay, chưa ra)
    nqt_dang_tap = NqtDiemDanh.query.filter(
        func.cast(NqtDiemDanh.nqt_thoi_gian_vao, db.Date) == nqt_hom_nay,
        NqtDiemDanh.nqt_thoi_gian_ra.is_(None)
    ).count()

    # Gói tập sắp hết hạn trong 7 ngày
    nqt_sap_het_han = NqtDangKyGoiTap.query.filter(
        NqtDangKyGoiTap.nqt_trang_thai == 'dang_hoat_dong',
        NqtDangKyGoiTap.nqt_ngay_het_han >= nqt_hom_nay,
        NqtDangKyGoiTap.nqt_ngay_het_han <= nqt_7_ngay_toi,
    ).count()

    # Doanh thu tháng hiện tại (thanh toán đã hoàn thành)
    nqt_doanh_thu = db.session.query(func.sum(NqtThanhToan.nqt_so_tien)).filter(
        NqtThanhToan.nqt_trang_thai == 'hoan_thanh',
        func.cast(NqtThanhToan.nqt_ngay_thanh_toan, db.Date) >= nqt_dau_thang,
    ).scalar() or 0

    # Hội viên mới đăng ký tháng này
    nqt_hv_moi = NqtHoiVien.query.filter(
        NqtHoiVien.nqt_ngay_dang_ky >= nqt_dau_thang
    ).count()

    return nqt_ok({
        'nqt_tong_hoi_vien': nqt_tong_hv,
        'nqt_dang_tap_luyen': nqt_dang_tap,
        'nqt_sap_het_han': nqt_sap_het_han,
        'nqt_doanh_thu_thang': float(nqt_doanh_thu),
        'nqt_hoi_vien_moi_thang': nqt_hv_moi,
    })
