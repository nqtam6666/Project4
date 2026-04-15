import uuid
from datetime import date, timedelta
from flask import Blueprint, request
from sqlalchemy import func, cast, Date
from backend.app import db
from backend.app.models.g6_hoi_vien import G6HoiVien, G6GoiTap, G6DangKyGoiTap, G6DiemDanh, G6ChiSoCoThe
from backend.app.models.g6_thanh_toan import G6ThanhToan
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap, nqt_yeu_cau_quyen

nqt_hoi_vien_bp = Blueprint('g6_hoi_vien', __name__, url_prefix='/api')


# ---- HỘI VIÊN ----

@nqt_hoi_vien_bp.route('/nqt-hoi-vien', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_xem_hoi_vien')
def nqt_lay_tat_ca_hoi_vien():
    nqt_trang = request.args.get('g6_trang', 1, type=int)
    nqt_gioi_han = request.args.get('g6_gioi_han', 20, type=int)
    nqt_tim = request.args.get('g6_tim_kiem', '').strip()
    nqt_chi_nhanh = request.args.get('g6_ma_chi_nhanh', type=int)
    nqt_trang_thai = request.args.get('g6_trang_thai', '').strip()    # 'true' / 'false'
    nqt_sap_het_han = request.args.get('g6_sap_het_han', type=int)    # số ngày, ví dụ 7

    nqt_q = G6HoiVien.query
    if nqt_chi_nhanh:
        nqt_q = nqt_q.filter_by(g6_ma_chi_nhanh=nqt_chi_nhanh)
    if nqt_trang_thai == 'true':
        nqt_q = nqt_q.filter_by(g6_la_hoat_dong=True)
    elif nqt_trang_thai == 'false':
        nqt_q = nqt_q.filter_by(g6_la_hoat_dong=False)
    if nqt_tim:
        nqt_q = nqt_q.filter(
            G6HoiVien.g6_ho_ten.ilike(f'%{nqt_tim}%') |
            G6HoiVien.g6_so_dien_thoai.ilike(f'%{nqt_tim}%')
        )
    if nqt_sap_het_han:
        # Lọc hội viên có gói tập sắp hết hạn trong N ngày
        nqt_han = date.today() + timedelta(days=nqt_sap_het_han)
        nqt_ids_sq = db.session.query(G6DangKyGoiTap.g6_ma_hoi_vien).filter(
            G6DangKyGoiTap.g6_trang_thai == 'dang_hoat_dong',
            G6DangKyGoiTap.g6_ngay_het_han >= date.today(),
            G6DangKyGoiTap.g6_ngay_het_han <= nqt_han,
        ).scalar_subquery()
        nqt_q = nqt_q.filter(G6HoiVien.g6_ma_hoi_vien.in_(nqt_ids_sq))

    nqt_phan_trang = nqt_q.order_by(G6HoiVien.g6_ngay_tao.desc()).paginate(
        page=nqt_trang, per_page=nqt_gioi_han, error_out=False
    )
    return nqt_ok({
        'g6_danh_sach': [h.g6_to_dict() for h in nqt_phan_trang.items],
        'g6_tong': nqt_phan_trang.total,
        'g6_trang': nqt_trang,
        'g6_tong_trang': nqt_phan_trang.pages,
    })


@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_xem_hoi_vien')
def nqt_lay_hoi_vien(nqt_id):
    nqt_row = G6HoiVien.query.get_or_404(nqt_id)
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_hoi_vien_bp.route('/nqt-hoi-vien', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_tao_hoi_vien')
def nqt_tao_hoi_vien():
    nqt_data = request.get_json() or {}
    nqt_ho_ten = nqt_data.get('g6_ho_ten', '').strip()
    nqt_sdt = nqt_data.get('g6_so_dien_thoai', '').strip()
    nqt_chi_nhanh = nqt_data.get('g6_ma_chi_nhanh')

    if not nqt_ho_ten or not nqt_sdt or not nqt_chi_nhanh:
        return nqt_loi('Thiếu họ tên, số điện thoại hoặc chi nhánh')
    if G6HoiVien.query.filter_by(g6_so_dien_thoai=nqt_sdt).first():
        return nqt_loi('Số điện thoại đã được đăng ký')

    nqt_row = G6HoiVien(
        g6_ho_ten=nqt_ho_ten,
        g6_so_dien_thoai=nqt_sdt,
        g6_ma_chi_nhanh=nqt_chi_nhanh,
        g6_ngay_dang_ky=date.today(),
        g6_ma_qr=str(uuid.uuid4()),
        g6_email=nqt_data.get('g6_email'),
        g6_ngay_sinh=nqt_data.get('g6_ngay_sinh'),
        g6_gioi_tinh=nqt_data.get('g6_gioi_tinh'),
        g6_dia_chi=nqt_data.get('g6_dia_chi'),
        g6_nguon_gioi_thieu=nqt_data.get('g6_nguon_gioi_thieu'),
        g6_ma_gioi_thieu=nqt_data.get('g6_ma_gioi_thieu'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo hội viên thành công', 201)


@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_sua_hoi_vien')
def nqt_cap_nhat_hoi_vien(nqt_id):
    nqt_row = G6HoiVien.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['g6_ho_ten', 'g6_email', 'g6_dia_chi', 'g6_la_hoat_dong', 'g6_ghi_chu']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_xoa_hoi_vien')
def nqt_xoa_hoi_vien(nqt_id):
    nqt_row = G6HoiVien.query.get_or_404(nqt_id)
    db.session.delete(nqt_row)
    db.session.commit()
    return nqt_ok(None, 'Xóa hội viên thành công')


# ---- GÓI TẬP ----

@nqt_hoi_vien_bp.route('/nqt-goi-tap', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_goi_tap():
    nqt_list = G6GoiTap.query.filter_by(g6_la_hoat_dong=True).order_by(G6GoiTap.g6_thu_tu_hien_thi).all()
    return nqt_ok([g.g6_to_dict() for g in nqt_list])


@nqt_hoi_vien_bp.route('/nqt-goi-tap', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_goi_tap():
    nqt_data = request.get_json() or {}
    nqt_row = G6GoiTap(
        g6_ten_goi=nqt_data.get('g6_ten_goi', ''),
        g6_mo_ta=nqt_data.get('g6_mo_ta'),
        g6_so_ngay=nqt_data.get('g6_so_ngay', 30),
        g6_gia=nqt_data.get('g6_gia', 0),
        g6_gia_khuyen_mai=nqt_data.get('g6_gia_khuyen_mai'),
        g6_co_pt=nqt_data.get('g6_co_pt', False),
        g6_so_buoi_pt=nqt_data.get('g6_so_buoi_pt', 0),
        g6_co_sauna=nqt_data.get('g6_co_sauna', False),
        g6_la_noi_bat=nqt_data.get('g6_la_noi_bat', False),
        g6_ma_chi_nhanh=nqt_data.get('g6_ma_chi_nhanh'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Tạo gói tập thành công', 201)


@nqt_hoi_vien_bp.route('/nqt-goi-tap/<int:nqt_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_cap_nhat_goi_tap(nqt_id):
    nqt_row = G6GoiTap.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    for nqt_f in ['g6_ten_goi', 'g6_gia', 'g6_gia_khuyen_mai', 'g6_la_hoat_dong', 'g6_la_noi_bat']:
        if nqt_f in nqt_data:
            setattr(nqt_row, nqt_f, nqt_data[nqt_f])
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict())


@nqt_hoi_vien_bp.route('/nqt-goi-tap/<int:nqt_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nqt_xoa_goi_tap(nqt_id):
    nqt_row = G6GoiTap.query.get_or_404(nqt_id)
    nqt_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn gói tập thành công')


# ---- ĐĂNG KÝ GÓI TẬP ----

@nqt_hoi_vien_bp.route('/nqt-dang-ky-goi-tap', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_tao_hoi_vien')
def nqt_dang_ky_goi_tap():
    from datetime import timedelta
    nqt_data = request.get_json() or {}
    nqt_hv_id = nqt_data.get('g6_ma_hoi_vien')
    nqt_gt_id = nqt_data.get('g6_ma_goi_tap')
    if not nqt_hv_id or not nqt_gt_id:
        return nqt_loi('Thiếu mã hội viên hoặc gói tập')
    nqt_hv = G6HoiVien.query.get_or_404(nqt_hv_id)
    nqt_gt = G6GoiTap.query.get_or_404(nqt_gt_id)
    nqt_ngay_bd = date.today()
    nqt_ngay_hh = nqt_ngay_bd + date.resolution.__class__(days=nqt_gt.g6_so_ngay)
    from datetime import timedelta
    nqt_ngay_hh = nqt_ngay_bd + timedelta(days=nqt_gt.g6_so_ngay)
    nqt_gia = float(nqt_gt.g6_gia_khuyen_mai or nqt_gt.g6_gia)
    nqt_row = G6DangKyGoiTap(
        g6_ma_hoi_vien=nqt_hv_id,
        g6_ma_goi_tap=nqt_gt_id,
        g6_ma_chi_nhanh=nqt_hv.g6_ma_chi_nhanh,
        g6_ngay_bat_dau=nqt_ngay_bd,
        g6_ngay_het_han=nqt_ngay_hh,
        g6_gia_thuc_te=nqt_gia,
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Đăng ký gói tập thành công', 201)


@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>/nqt-dang-ky', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_dang_ky(nqt_id):
    G6HoiVien.query.get_or_404(nqt_id)
    nqt_list = G6DangKyGoiTap.query.filter_by(g6_ma_hoi_vien=nqt_id).all()
    return nqt_ok([d.g6_to_dict() for d in nqt_list])


# ---- CHECK-IN ----

@nqt_hoi_vien_bp.route('/nqt-diem-danh/qr', methods=['POST'])
@nqt_yeu_cau_dang_nhap
@nqt_yeu_cau_quyen('g6_checkin_hoi_vien')
def nqt_checkin_qr():
    nqt_data = request.get_json() or {}
    nqt_qr = nqt_data.get('g6_ma_qr', '').strip()
    nqt_chi_nhanh = nqt_data.get('g6_ma_chi_nhanh')
    if not nqt_qr or not nqt_chi_nhanh:
        return nqt_loi('Thiếu mã QR hoặc chi nhánh')
    nqt_hv = G6HoiVien.query.filter_by(g6_ma_qr=nqt_qr, g6_la_hoat_dong=True).first()
    if not nqt_hv:
        return nqt_loi('Mã QR không hợp lệ', nqt_ma_trang=404)
    nqt_dang_ky = G6DangKyGoiTap.query.filter_by(
        g6_ma_hoi_vien=nqt_hv.g6_ma_hoi_vien,
        g6_trang_thai='dang_hoat_dong'
    ).filter(G6DangKyGoiTap.g6_ngay_het_han >= date.today()).first()
    if not nqt_dang_ky:
        return nqt_loi('Hội viên không có gói tập đang hoạt động', nqt_ma_trang=403)
    nqt_dd = G6DiemDanh(
        g6_ma_dang_ky=nqt_dang_ky.g6_ma_dang_ky,
        g6_ma_hoi_vien=nqt_hv.g6_ma_hoi_vien,
        g6_ma_chi_nhanh=nqt_chi_nhanh,
        g6_phuong_thuc='qr',
    )
    db.session.add(nqt_dd)
    db.session.commit()
    return nqt_ok({'g6_diem_danh': nqt_dd.g6_to_dict(), 'g6_hoi_vien': nqt_hv.g6_to_dict()},
                  f'Chào mừng {nqt_hv.g6_ho_ten}!')


# ---- CHỈ SỐ CƠ THỂ ----

@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>/nqt-chi-so', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_chi_so(nqt_id):
    G6HoiVien.query.get_or_404(nqt_id)
    nqt_list = G6ChiSoCoThe.query.filter_by(g6_ma_hoi_vien=nqt_id).order_by(
        G6ChiSoCoThe.g6_ngay_do.desc()
    ).all()
    return nqt_ok([c.g6_to_dict() for c in nqt_list])


@nqt_hoi_vien_bp.route('/nqt-hoi-vien/<int:nqt_id>/nqt-chi-so', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_them_chi_so(nqt_id):
    G6HoiVien.query.get_or_404(nqt_id)
    nqt_data = request.get_json() or {}
    nqt_can = nqt_data.get('g6_can_nang')
    nqt_cao = nqt_data.get('g6_chieu_cao')
    nqt_bmi = None
    if nqt_can and nqt_cao:
        nqt_bmi = round(float(nqt_can) / ((float(nqt_cao) / 100) ** 2), 2)
    nqt_row = G6ChiSoCoThe(
        g6_ma_hoi_vien=nqt_id,
        g6_ngay_do=nqt_data.get('g6_ngay_do', str(date.today())),
        g6_can_nang=nqt_can,
        g6_chieu_cao=nqt_cao,
        g6_chi_so_bmi=nqt_bmi,
        g6_ti_le_mo=nqt_data.get('g6_ti_le_mo'),
        g6_ti_le_co=nqt_data.get('g6_ti_le_co'),
        g6_vong_eo=nqt_data.get('g6_vong_eo'),
        g6_ghi_chu=nqt_data.get('g6_ghi_chu'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.g6_to_dict(), 'Đã lưu chỉ số', 201)


# ---- THỐNG KÊ DASHBOARD ----

@nqt_hoi_vien_bp.route('/nqt-thong-ke-dashboard', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_thong_ke_dashboard():
    nqt_hom_nay = date.today()
    nqt_dau_thang = nqt_hom_nay.replace(day=1)
    nqt_7_ngay_toi = nqt_hom_nay + timedelta(days=7)

    # Tổng hội viên
    nqt_tong_hv = G6HoiVien.query.filter_by(g6_la_hoat_dong=True).count()

    # Check-in hôm nay (tất cả lượt vào, kể cả đã ra)
    nqt_checkin_hom_nay = G6DiemDanh.query.filter(
        func.cast(G6DiemDanh.g6_thoi_gian_vao, db.Date) == nqt_hom_nay
    ).count()

    # Đang tập luyện (check-in vào hôm nay, chưa ra)
    nqt_dang_tap = G6DiemDanh.query.filter(
        func.cast(G6DiemDanh.g6_thoi_gian_vao, db.Date) == nqt_hom_nay,
        G6DiemDanh.g6_thoi_gian_ra.is_(None)
    ).count()

    # Sức chứa tối đa (lấy từ chi nhánh đầu tiên hoặc tổng)
    from backend.app.models.g6_chi_nhanh import G6ChiNhanh
    nqt_suc_chua = db.session.query(func.sum(G6ChiNhanh.g6_suc_chua_toi_da)).scalar() or 100

    # Gói tập sắp hết hạn trong 7 ngày
    nqt_sap_het_han = G6DangKyGoiTap.query.filter(
        G6DangKyGoiTap.g6_trang_thai == 'dang_hoat_dong',
        G6DangKyGoiTap.g6_ngay_het_han >= nqt_hom_nay,
        G6DangKyGoiTap.g6_ngay_het_han <= nqt_7_ngay_toi,
    ).count()

    # Doanh thu tháng hiện tại (trạng thái thanh_cong hoặc hoan_thanh)
    nqt_doanh_thu = db.session.query(func.sum(G6ThanhToan.g6_so_tien)).filter(
        G6ThanhToan.g6_trang_thai.in_(['thanh_cong', 'hoan_thanh']),
        func.cast(G6ThanhToan.g6_ngay_thanh_toan, db.Date) >= nqt_dau_thang,
    ).scalar() or 0

    # Hội viên mới đăng ký tháng này
    nqt_hv_moi = G6HoiVien.query.filter(
        G6HoiVien.g6_ngay_dang_ky >= nqt_dau_thang
    ).count()

    return nqt_ok({
        'g6_tong_hoi_vien': nqt_tong_hv,
        'g6_checkin_hom_nay': nqt_checkin_hom_nay,
        'g6_dang_tap_luyen': nqt_dang_tap,
        'g6_suc_chua': int(nqt_suc_chua),
        'g6_sap_het_han': nqt_sap_het_han,
        'g6_doanh_thu_thang': float(nqt_doanh_thu),
        'g6_hoi_vien_moi_thang': nqt_hv_moi,
    })


# ---- BIỂU ĐỒ TĂNG TRƯỞNG HỘI VIÊN ----

@nqt_hoi_vien_bp.route('/nqt-thong-ke-bieu-do', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_thong_ke_bieu_do():
    nqt_so_ngay = request.args.get('g6_so_ngay', 7, type=int)
    nqt_so_ngay = min(max(nqt_so_ngay, 7), 90)

    nqt_hom_nay = date.today()
    nqt_ngay_bat_dau = nqt_hom_nay - timedelta(days=nqt_so_ngay - 1)

    # Query số hội viên đăng ký theo ngày
    nqt_rows = db.session.query(
        cast(G6HoiVien.g6_ngay_dang_ky, Date).label('nqt_ngay'),
        func.count(G6HoiVien.g6_ma_hoi_vien).label('nqt_so_luong')
    ).filter(
        G6HoiVien.g6_ngay_dang_ky >= nqt_ngay_bat_dau
    ).group_by(
        cast(G6HoiVien.g6_ngay_dang_ky, Date)
    ).order_by(
        cast(G6HoiVien.g6_ngay_dang_ky, Date)
    ).all()

    # Tạo map ngày → số lượng
    nqt_map = {str(r.nqt_ngay): r.nqt_so_luong for r in nqt_rows}

    nqt_nhan = []
    nqt_gia_tri = []

    nqt_thu_vn = {0:'T2', 1:'T3', 2:'T4', 3:'T5', 4:'T6', 5:'T7', 6:'CN'}

    if nqt_so_ngay <= 30:
        # Từng ngày
        for nqt_i in range(nqt_so_ngay):
            nqt_ngay = nqt_ngay_bat_dau + timedelta(days=nqt_i)
            nqt_key = str(nqt_ngay)
            nqt_label = nqt_thu_vn[nqt_ngay.weekday()] if nqt_so_ngay <= 7 else f"{nqt_ngay.day}/{nqt_ngay.month}"
            nqt_nhan.append(nqt_label)
            nqt_gia_tri.append(nqt_map.get(nqt_key, 0))
    else:
        # Gộp theo tuần (90 ngày → ~13 tuần)
        nqt_tuan = 0
        nqt_ngay_hien_tai = nqt_ngay_bat_dau
        while nqt_ngay_hien_tai <= nqt_hom_nay:
            nqt_tuan += 1
            nqt_cuoi_tuan = min(nqt_ngay_hien_tai + timedelta(days=6), nqt_hom_nay)
            nqt_tong = sum(
                nqt_map.get(str(nqt_ngay_hien_tai + timedelta(days=nqt_d)), 0)
                for nqt_d in range((nqt_cuoi_tuan - nqt_ngay_hien_tai).days + 1)
            )
            nqt_nhan.append(f"T{nqt_tuan}")
            nqt_gia_tri.append(nqt_tong)
            nqt_ngay_hien_tai = nqt_cuoi_tuan + timedelta(days=1)

    return nqt_ok({
        'g6_nhan': nqt_nhan,
        'g6_gia_tri': nqt_gia_tri,
        'g6_so_ngay': nqt_so_ngay,
    })
