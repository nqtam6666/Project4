from datetime import date, datetime
from flask import Blueprint, request
from backend.app import db
from backend.app.models.g6_lop_hoc import G6LopHoc, G6LichLopHoc, G6DatChoLopHoc
from backend.app.utils.g6_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.g6_xac_thuc import nqt_yeu_cau_dang_nhap

nxv_lop_hoc_bp = Blueprint('nxv_lop_hoc', __name__, url_prefix='/api')


# ============================================================
# LỚP HỌC
# ============================================================

@nxv_lop_hoc_bp.route('/nxv-lop-hoc', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_lop_hoc():
    nxv_chi_nhanh = request.args.get('g6_ma_chi_nhanh', type=int)
    nxv_loai = request.args.get('g6_loai_lop', '').strip()

    nxv_q = G6LopHoc.query.filter_by(g6_la_hoat_dong=True)
    if nxv_chi_nhanh:
        nxv_q = nxv_q.filter_by(g6_ma_chi_nhanh=nxv_chi_nhanh)
    if nxv_loai:
        nxv_q = nxv_q.filter_by(g6_loai_lop=nxv_loai)

    return nqt_ok([l.g6_to_dict() for l in nxv_q.all()])


@nxv_lop_hoc_bp.route('/nxv-lop-hoc/<int:nxv_id>', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_chi_tiet_lop(nxv_id):
    nxv_row = G6LopHoc.query.get_or_404(nxv_id)
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_lop_hoc_bp.route('/nxv-lop-hoc', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_lop_hoc():
    nxv_data = request.get_json() or {}
    nxv_ten = nxv_data.get('g6_ten_lop', '').strip()
    nxv_loai = nxv_data.get('g6_loai_lop', '').strip()
    nxv_cn = nxv_data.get('g6_ma_chi_nhanh')
    if not nxv_ten or not nxv_loai or not nxv_cn:
        return nqt_loi('Thiếu tên lớp, loại lớp hoặc chi nhánh')

    nxv_row = G6LopHoc(
        g6_ma_chi_nhanh=nxv_cn,
        g6_ten_lop=nxv_ten,
        g6_loai_lop=nxv_loai,
        g6_mo_ta=nxv_data.get('g6_mo_ta'),
        g6_hinh_anh=nxv_data.get('g6_hinh_anh'),
        g6_do_kho=nxv_data.get('g6_do_kho', 'co_ban'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo lớp học thành công', 201)


@nxv_lop_hoc_bp.route('/nxv-lop-hoc/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_lop(nxv_id):
    nxv_row = G6LopHoc.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['g6_ten_lop', 'g6_loai_lop', 'g6_mo_ta', 'g6_hinh_anh', 'g6_do_kho', 'g6_la_hoat_dong']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_lop_hoc_bp.route('/nxv-lop-hoc/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_lop(nxv_id):
    nxv_row = G6LopHoc.query.get_or_404(nxv_id)
    nxv_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn lớp học')


# ============================================================
# LỊCH LỚP HỌC
# ============================================================

@nxv_lop_hoc_bp.route('/nxv-lich-lop-hoc', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_lich_lop():
    nxv_lop_id = request.args.get('g6_ma_lop_hoc', type=int)
    nxv_hlv_id = request.args.get('g6_ma_hlv', type=int)
    nxv_thu = request.args.get('g6_thu_trong_tuan', type=int)

    nxv_q = G6LichLopHoc.query.filter_by(g6_la_hoat_dong=True)
    if nxv_lop_id:
        nxv_q = nxv_q.filter_by(g6_ma_lop_hoc=nxv_lop_id)
    if nxv_hlv_id:
        nxv_q = nxv_q.filter_by(g6_ma_hlv=nxv_hlv_id)
    if nxv_thu:
        nxv_q = nxv_q.filter_by(g6_thu_trong_tuan=nxv_thu)

    return nqt_ok([l.g6_to_dict() for l in nxv_q.all()])


@nxv_lop_hoc_bp.route('/nxv-lich-lop-hoc', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_lich_lop():
    nxv_data = request.get_json() or {}
    nxv_lop_id = nxv_data.get('g6_ma_lop_hoc')
    nxv_hlv_id = nxv_data.get('g6_ma_hlv')
    nxv_thu = nxv_data.get('g6_thu_trong_tuan')
    nxv_gio = nxv_data.get('g6_gio_bat_dau')
    nxv_tluong = nxv_data.get('g6_thoi_luong')
    nxv_ngay_tu = nxv_data.get('g6_ngay_ap_dung_tu')

    if not all([nxv_lop_id, nxv_hlv_id, nxv_thu, nxv_gio, nxv_tluong, nxv_ngay_tu]):
        return nqt_loi('Thiếu thông tin lịch lớp học')

    nxv_row = G6LichLopHoc(
        g6_ma_lop_hoc=nxv_lop_id,
        g6_ma_hlv=nxv_hlv_id,
        g6_thu_trong_tuan=nxv_thu,
        g6_gio_bat_dau=nxv_gio,
        g6_thoi_luong=nxv_tluong,
        g6_suc_chua_toi_da=nxv_data.get('g6_suc_chua_toi_da', 20),
        g6_phong_tap=nxv_data.get('g6_phong_tap'),
        g6_ngay_ap_dung_tu=nxv_ngay_tu,
        g6_ngay_ap_dung_den=nxv_data.get('g6_ngay_ap_dung_den'),
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Tạo lịch lớp thành công', 201)


@nxv_lop_hoc_bp.route('/nxv-lich-lop-hoc/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_lich_lop(nxv_id):
    nxv_row = G6LichLopHoc.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    for nxv_f in ['g6_thu_trong_tuan', 'g6_gio_bat_dau', 'g6_thoi_luong',
                  'g6_suc_chua_toi_da', 'g6_phong_tap', 'g6_ngay_ap_dung_den', 'g6_la_hoat_dong']:
        if nxv_f in nxv_data:
            setattr(nxv_row, nxv_f, nxv_data[nxv_f])
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())


@nxv_lop_hoc_bp.route('/nxv-lich-lop-hoc/<int:nxv_id>', methods=['DELETE'])
@nqt_yeu_cau_dang_nhap
def nxv_xoa_lich_lop(nxv_id):
    nxv_row = G6LichLopHoc.query.get_or_404(nxv_id)
    nxv_row.g6_la_hoat_dong = False
    db.session.commit()
    return nqt_ok(None, 'Đã ẩn lịch lớp')


# ============================================================
# ĐẶT CHỖ LỚP HỌC
# ============================================================

@nxv_lop_hoc_bp.route('/nxv-dat-cho', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nxv_lay_dat_cho():
    nxv_lich_id = request.args.get('g6_ma_lich_lop', type=int)
    nxv_hv_id = request.args.get('g6_ma_hoi_vien', type=int)
    nxv_ngay = request.args.get('g6_ngay_tap', '').strip()

    nxv_q = G6DatChoLopHoc.query
    if nxv_lich_id:
        nxv_q = nxv_q.filter_by(g6_ma_lich_lop=nxv_lich_id)
    if nxv_hv_id:
        nxv_q = nxv_q.filter_by(g6_ma_hoi_vien=nxv_hv_id)
    if nxv_ngay:
        nxv_q = nxv_q.filter_by(g6_ngay_tap=nxv_ngay)

    return nqt_ok([d.g6_to_dict() for d in nxv_q.all()])


@nxv_lop_hoc_bp.route('/nxv-dat-cho', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nxv_tao_dat_cho():
    nxv_data = request.get_json() or {}
    nxv_lich_id = nxv_data.get('g6_ma_lich_lop')
    nxv_hv_id = nxv_data.get('g6_ma_hoi_vien')
    nxv_ngay = nxv_data.get('g6_ngay_tap')
    if not nxv_lich_id or not nxv_hv_id or not nxv_ngay:
        return nqt_loi('Thiếu mã lịch, hội viên hoặc ngày tập')

    # Kiểm tra trùng lịch
    nxv_trung = G6DatChoLopHoc.query.filter_by(
        g6_ma_lich_lop=nxv_lich_id,
        g6_ma_hoi_vien=nxv_hv_id,
        g6_ngay_tap=nxv_ngay,
    ).filter(G6DatChoLopHoc.g6_trang_thai != 'da_huy').first()
    if nxv_trung:
        return nqt_loi('Hội viên đã đặt chỗ cho lịch này')

    # Kiểm tra sức chứa
    nxv_lich = G6LichLopHoc.query.get_or_404(nxv_lich_id)
    nxv_so_dat = G6DatChoLopHoc.query.filter_by(
        g6_ma_lich_lop=nxv_lich_id,
        g6_ngay_tap=nxv_ngay,
    ).filter(G6DatChoLopHoc.g6_trang_thai.in_(['dat_cho', 'da_den'])).count()
    if nxv_so_dat >= nxv_lich.g6_suc_chua_toi_da:
        return nqt_loi('Lớp học đã đầy chỗ')

    nxv_row = G6DatChoLopHoc(
        g6_ma_lich_lop=nxv_lich_id,
        g6_ma_hoi_vien=nxv_hv_id,
        g6_ngay_tap=nxv_ngay,
    )
    db.session.add(nxv_row)
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict(), 'Đặt chỗ thành công', 201)


@nxv_lop_hoc_bp.route('/nxv-dat-cho/<int:nxv_id>', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nxv_cap_nhat_dat_cho(nxv_id):
    nxv_row = G6DatChoLopHoc.query.get_or_404(nxv_id)
    nxv_data = request.get_json() or {}
    nxv_tt_moi = nxv_data.get('g6_trang_thai')
    if nxv_tt_moi:
        nxv_row.g6_trang_thai = nxv_tt_moi
        if nxv_tt_moi == 'da_huy':
            nxv_row.g6_thoi_gian_huy = datetime.utcnow()
            nxv_row.g6_ly_do_huy = nxv_data.get('g6_ly_do_huy')
    db.session.commit()
    return nqt_ok(nxv_row.g6_to_dict())
